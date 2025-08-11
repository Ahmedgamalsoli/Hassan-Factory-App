# ======================
# Used imports
# ======================

import tkinter as tk
import config
import os
import sys
import matplotlib
import matplotlib.pyplot as plt


from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk, ImageDraw  # Import Pillow classes
from datetime import datetime,time , time, timedelta, date
from tkcalendar import DateEntry  # Import DateEntry
from playsound import playsound
from pymongo import MongoClient
from urllib.parse import quote_plus
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from collections import defaultdict
from bidi.algorithm import get_display
from matplotlib.figure import Figure    
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter,A5
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
matplotlib.use('TkAgg')  # Set the backend before importing pyplot


# Determine the base directory
if getattr(sys, "frozen", False):
    # Running as an executable
    BASE_DIR = sys._MEIPASS
else:
    # Running as a script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class PurchaseInvoice:
    def __init__(self, root, app):
        self.root = root
        self.app = app  # save reference to SalesSystemApp
        # self.AuxiliaryClass.t = self.app.AuxiliaryClass.t

    def manage_purchases_invoices_window(self):
                # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg=config.COLORS["background"])
        # Create the top bar
        self.app.topbar.topbar(show_back_button=True)

        # Main button frame
        button_frame = tk.Frame(self.root, bg=config.COLORS["background"])
        button_frame.pack(pady=30)

        # Define buttons with images, text, and commands
        if self.app.light:
            buttons = [
                {"text": self.app.AuxiliaryClass.t("New Purchase Invoice"), "image": "new_invoice-dark.png", 
                "command": lambda: self.new_Purchase_invoice(self.app.user_role,"add")},
                {"text": self.app.AuxiliaryClass.t("Update Purchase Invoice"), "image": "update_invoice-dark.png",
                "command": lambda: self.new_Purchase_invoice(self.app.user_role,"update")}
            ]
        elif not self.app.light:
            buttons = [
                {"text": self.app.AuxiliaryClass.t("New Purchase Invoice"), "image": "new_invoice-light.png", 
                "command": lambda: self.new_Purchase_invoice(self.app.user_role,"add")},
                {"text": self.app.AuxiliaryClass.t("Update Purchase Invoice"), "image": "update_invoice-light.png",
                "command": lambda: self.new_Purchase_invoice(self.app.user_role,"update")}
            ]            
        
        images = []  # Keep references to prevent garbage collection
        columns_per_row = 3  # Number of buttons per row
        button_size = 120
        try:
            for index, btn_info in enumerate(buttons):
                # Load and resize image
                img_path = os.path.join(BASE_DIR, "Static", "images", btn_info["image"])
                img = Image.open(img_path).resize((button_size, button_size), Image.LANCZOS)
                photo_img = ImageTk.PhotoImage(img)
                images.append(photo_img)

                # Calculate grid position
                row = index // columns_per_row
                column = index % columns_per_row

                # Create sub-frame for each button
                sub_frame = tk.Frame(button_frame, bg=config.COLORS["background"])
                sub_frame.grid(row=row, column=column, padx=20, pady=20)

                # Image button
                btn = tk.Button(sub_frame, image=photo_img, bd=0,
                                text=btn_info["text"], 
                                font=("Arial", 15, "bold"),
                                compound=tk.TOP,
                                bg=config.COLORS["background"],
                                fg=config.COLORS["text"],
                                activebackground=config.COLORS["highlight"],
                                command=btn_info["command"])
                btn.image = photo_img  # Keep reference
                btn.pack()
                
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=config.COLORS["primary"]))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=config.COLORS["background"]))

        except Exception as e:
            print(f"Error loading images: {e}")
            # Fallback to text buttons if images fail
            fallback_frame = tk.Frame(self.root, bg=config.COLORS["background"])
            fallback_frame.pack(pady=20)
            for btn_info in buttons:
                tk.Button(fallback_frame, text=btn_info["text"], 
                        command=btn_info["command"]).pack(side="left", padx=10)
                
    def new_Purchase_invoice(self, user_role, add_or_update):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Initialize product mappings
        self.app.update_purchase = False
        self.app.material_map = {}
        self.app.name_to_code = {}
        
        # Create top bar
        self.app.topbar.topbar(show_back_button=True,Back_to_Purchases_Window=True)

        # MongoDB collections
        suppliers_col = self.app.AuxiliaryClass.get_collection_by_name("Suppliers")
        purchases_col = self.app.AuxiliaryClass.get_collection_by_name("Purchases")
        materials_col = self.app.AuxiliaryClass.get_collection_by_name("Materials")

        # Main form frame with responsive sizing
        form_frame = tk.Frame(self.root, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure columns - 10 columns with equal weight
        for i in range(10):
            form_frame.columnconfigure(i, weight=1)

        # ===== INVOICE SELECTION FOR UPDATE MODE =====
        current_row = 0
        self.app.selected_invoice_id = None
        
        if add_or_update == "update":
            # Create invoice selection frame
            invoice_frame = tk.Frame(form_frame, bd=1, relief=tk.SOLID, padx=5, pady=5)
            invoice_frame.grid(row=current_row, column=0, columnspan=12, sticky='ew', pady=5)
            current_row += 1
            
            # Configure invoice frame columns
            for i in range(12):
                invoice_frame.columnconfigure(i, weight=1 if i % 2 == 1 else 0)
            
            # Fetch invoice numbers
            invoice_numbers = [str(doc["Receipt_Number"]) for doc in purchases_col.find({}, {"Receipt_Number": 1})]
            
            # Invoice selection
            tk.Label(invoice_frame, text=self.app.AuxiliaryClass.t("Select Invoice"), 
                    font=("Arial", 10, "bold")).grid(row=0, column=0, sticky='w')
            self.app.invoice_var = tk.StringVar()
            invoice_cb = ttk.Combobox(invoice_frame, textvariable=self.app.invoice_var, values=invoice_numbers)
            invoice_cb.grid(row=0, column=1, padx=5, sticky='ew', columnspan=3)
            
            # Load button
            load_btn = tk.Button(invoice_frame, text=self.app.AuxiliaryClass.t("Load Invoice"), 
                                command=lambda: self.load_invoice_data_purchase(purchases_col),
                                bg='#2196F3', fg='white')
            load_btn.grid(row=0, column=4, padx=5, sticky='ew')
            
            # Delete button
            delete_btn = tk.Button(invoice_frame, text=self.app.AuxiliaryClass.t("Delete Invoice"), 
                                command=lambda: self.app.SalesInvoice.delete_invoice(materials_col,purchases_col, suppliers_col,"purchase"),
                                bg='red', fg='white')
            delete_btn.grid(row=0, column=5, padx=5, sticky='ew')

        # ===== Supplier SECTION =====
        # Create Supplier frame
        supplier_frame = tk.Frame(form_frame, bd=1, relief=tk.SOLID, padx=5, pady=5)
        supplier_frame.grid(row=current_row, column=0, columnspan=12, sticky='ew', pady=5)
        current_row += 1
        
        # Configure Supplier frame columns
        for i in range(12):
            supplier_frame.columnconfigure(i, weight=1 if i % 2 == 1 else 0)        

        # Create bidirectional supplier mappings
        self.app.supplier_code_map = {}  # name -> code
        self.app.code_name_map = {}      # code -> name
        self.app.supplier_balance_map = {}  # name -> balance

        # Populate supplier data
        all_suppliers = []
        all_codes = []
        for supp in suppliers_col.find():
            name = supp.get('Name', '')
            code = str(supp.get('Code', ''))
            balance = supp.get('Balance', 0)
            
            self.app.supplier_code_map[name] = code
            self.app.code_name_map[code] = name
            self.app.supplier_balance_map[name] = balance
            all_suppliers.append(name)
            all_codes.append(code)

        # Supplier Name Combobox
        tk.Label(supplier_frame, text=self.app.AuxiliaryClass.t("Supplier Name"), 
                font=("Arial", 10, "bold")).grid(row=0, column=0, sticky='w')
        self.app.supplier_name_var = tk.StringVar()
        self.app.supplier_name_cb = ttk.Combobox(supplier_frame, 
                                            textvariable=self.app.supplier_name_var, 
                                            values=sorted(all_suppliers))
        self.app.supplier_name_cb.grid(row=0, column=1, padx=5, sticky='ew')

        # Supplier Code Combobox
        tk.Label(supplier_frame, text=self.app.AuxiliaryClass.t("Supplier Code"), 
                font=("Arial", 10, "bold")).grid(row=0, column=2, sticky='w')
        self.app.supplier_code_var = tk.StringVar()
        self.app.supplier_code_cb = ttk.Combobox(supplier_frame, 
                                            textvariable=self.app.supplier_code_var, 
                                            values=sorted(all_codes))
        self.app.supplier_code_cb.grid(row=0, column=3, padx=5, sticky='ew')

        # Balance and Payment Fields
        tk.Label(supplier_frame, text=self.app.AuxiliaryClass.t("Previous Balance"), 
                font=("Arial", 10, "bold")).grid(row=0, column=4, sticky='e')
        self.app.previous_balance_var = tk.StringVar()
        self.app.previous_balance_entry = tk.Entry(supplier_frame, 
                                            textvariable=self.app.previous_balance_var, 
                                            state='readonly')
        self.app.previous_balance_entry.grid(row=0, column=5, sticky='ew', padx=5)

        tk.Label(supplier_frame, text=self.app.AuxiliaryClass.t("Paid Money"), 
                font=("Arial", 10, "bold")).grid(row=0, column=6, sticky='e')
        self.app.payed_cash_var = tk.DoubleVar()
        self.app.payed_cash_entry = tk.Entry(supplier_frame, 
                                        textvariable=self.app.payed_cash_var)
        self.app.payed_cash_entry.grid(row=0, column=7, sticky='ew', padx=5)

        # Payment Method Dropdown
        tk.Label(supplier_frame, text=self.app.AuxiliaryClass.t("Payment Method"), 
                font=("Arial", 10, "bold")).grid(row=0, column=8, sticky='e')
        self.app.payment_method_var = tk.StringVar()
        payment_methods = ['Cash', 'E_Wallet', 'Bank_account', 'Instapay']
        payment_cb = ttk.Combobox(supplier_frame, 
                                textvariable=self.app.payment_method_var, 
                                values=payment_methods, 
                                state='readonly')
        payment_cb.grid(row=0, column=9, sticky='ew', padx=5)
        payment_cb.current(0)  # Set default to Cash

        # Synchronization functions
        def sync_from_name(event=None):
            name = self.app.supplier_name_var.get()
            code = self.app.supplier_code_map.get(name, '')
            self.app.supplier_code_var.set(code)
            self.app.previous_balance_var.set(str(self.app.supplier_balance_map.get(name, 0)))

        def sync_from_code(event=None):
            code = self.app.supplier_code_var.get()
            name = self.app.code_name_map.get(code, '')
            self.app.supplier_name_var.set(name)
            self.app.previous_balance_var.set(str(self.app.supplier_balance_map.get(name, 0)))

        # Event bindings
        self.app.supplier_name_cb.bind('<<ComboboxSelected>>', sync_from_name)
        self.app.supplier_code_cb.bind('<<ComboboxSelected>>', sync_from_code)
        
        self.app.supplier_name_cb.bind('<KeyRelease>', lambda e: [
            self.app.filter_combobox(e, all_suppliers, self.app.supplier_name_cb),
            sync_from_name()
        ])
        
        self.app.supplier_code_cb.bind('<KeyRelease>', lambda e: [
            self.app.filter_combobox(e, all_codes, self.app.supplier_code_cb),
            sync_from_code()
        ])

        # Load material data
        try:
            materials = list(materials_col.find())
            all_units = set()
            material_names = []
            material_codes = []

            for m in materials:
                code = str(m.get('material_code', '')).strip()
                name = m.get('material_name', '').strip()
                units_list = m.get('Units', [])

                # Process units
                unit_names = []
                for unit in units_list:
                    if isinstance(unit, dict):
                        unit_name = str(unit.get('unit_name', '')).strip()
                    elif isinstance(unit, str):
                        unit_name = unit.strip()
                    else:
                        continue
                    
                    if unit_name:
                        unit_names.append(unit_name)
                        all_units.add(unit_name)

                # Handle price conversion
                try:
                    price_str = str(m.get('Unit_Price', '0')).strip('kgm ')
                    price = float(price_str) if price_str else 0.0
                except ValueError:
                    price = 0.0

                # Update mappings
                self.app.material_map[code] = {
                    'name': name,
                    'units': unit_names,
                    'price': price
                }
                self.app.name_to_code[name] = code
                material_names.append(name)
                material_codes.append(code)

            self.app.product_codes = sorted(list(set(material_codes)))
            self.app.product_names = sorted(list(set(material_names)))
            all_units = sorted(list(all_units))

        except Exception as e:
            messagebox.showerror(self.app.AuxiliaryClass.t("Database Error"), f"{self.app.AuxiliaryClass.t("Failed to load materials:")} {str(e)}")
            return

        # ===== ITEMS GRID SECTION =====
        # Make items grid expandable
        form_frame.grid_rowconfigure(current_row + 1, weight=1)
        
        # Invoice Items Grid - Responsive Configuration
        columns = config.get_fields_by_name("Materials_Header")
        num_columns = len(columns)
        
        # Create header frame with uniform columns
        header_frame = tk.Frame(form_frame, bg='#f0f0f0')
        header_frame.grid(row=current_row, column=0, columnspan=10, sticky='ew', pady=(20, 0))
        current_row += 1

        # Configure header columns with uniform weights
        for col_idx in range(num_columns):
            header_frame.columnconfigure(col_idx, weight=1, uniform='cols')
            tk.Label(header_frame, text=self.app.AuxiliaryClass.t(columns[col_idx]), relief='ridge', 
                    bg='#f0f0f0', anchor='w', padx=5).grid(row=0, column=col_idx, sticky='ew')

        # Scrollable Canvas with responsive sizing
        canvas_container = tk.Frame(form_frame)
        canvas_container.grid(row=current_row, column=0, columnspan=10, sticky='nsew')
        canvas_container.grid_rowconfigure(0, weight=1)
        canvas_container.grid_columnconfigure(0, weight=1)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(canvas_container, highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
        
        # Create a frame inside the canvas for the rows
        self.app.rows_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.app.rows_frame, anchor="nw", tags="inner_frame")
        
        # Grid layout for canvas and scrollbar
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure scroll region
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        # Configure canvas width
        def configure_canvas(event):
            canvas_width = event.width
            canvas.itemconfig("inner_frame", width=canvas_width)
        
        # Bind events
        self.app.rows_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_canvas)

        # Set initial width
        canvas.update_idletasks()
        canvas_width = canvas.winfo_width()
        if canvas_width > 1:
            canvas.itemconfig("inner_frame", width=canvas_width)

        self.app.entries = []


        self.add_three_rows_purchase()

        # Buttons Frame
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=10, pady=10, sticky='ew')
        
        # Configure button frame columns
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        add_btn = tk.Button(button_frame, text=self.app.AuxiliaryClass.t("➕ Add 3 More Rows"), 
                        command=self.add_three_rows_purchase, bg='#4CAF50', fg='white')
        add_btn.grid(row=0, column=0, padx=5, sticky='w')
        if add_or_update == "add":
            save_btn = tk.Button(button_frame, text=self.app.AuxiliaryClass.t("💾 Save Invoice"), 
                                command=lambda: self.save_invoice_purchase(purchases_col, suppliers_col, materials_col),
                                bg='#2196F3', fg='white')
            save_btn.grid(row=0, column=1, padx=5, sticky='e')
        else:
            self.app.update_purchase = True
            update_btn = tk.Button(button_frame, text=self.app.AuxiliaryClass.t("🔄 Update Invoice"), 
                                command=lambda: self.save_invoice_purchase(purchases_col, suppliers_col, materials_col),
                                bg='#FF9800', fg='white')
            update_btn.grid(row=0, column=1, padx=5, sticky='e')        
      

    def create_row_purchase(self,parent, row_number, bg_color, initial_values=None):

        # Invoice Items Grid - Responsive Configuration
        columns = config.get_fields_by_name("Materials_Header")
        num_columns = len(columns)       
        row_frame = tk.Frame(parent, bg=bg_color)
        row_frame.pack(fill=tk.X)  # Use pack with fill to ensure full width
        
        # Configure columns with uniform weights (same as header)
        for col_idx in range(num_columns):
            row_frame.columnconfigure(col_idx, weight=1, uniform='cols')
        
        row_entries = []
        row_entry_vars = []
        key_map = {
            "Material_code": "material_code",
            "Material_name": "material_name",
            "unit": "Unit",
            "Unit_Price": "Unit_price",
            "QTY": "QTY",
            "Discount_Type": "Discount_Type",
            "Discount Value": "Discount_Value",
            "Total_QTY": "Total_QTY",
            "Numbering": "numbering",
            "Total_Price": "Final_Price"
        }
        for col_idx, col in enumerate(columns):
            value = ""
            if initial_values:
                db_key = key_map.get(col, col)
                value = initial_values.get(db_key, "")
                if col == "Material_code" and (value not in self.app.product_codes):
                    print(f"[WARN] '{value}' not in dropdown list!")
                # Handle special cases
                if col == "Discount_Type" and not value:
                    value = "Percentage"
                elif col == "Discount Value" and not value:
                    value = 0
            if col == "Material_code":
                value = value.strip()
                var = tk.StringVar(value=value)
                # row_entry_vars.append(var)
                cb = ttk.Combobox(row_frame, textvariable=var, values=self.app.product_codes)
                cb.bind('<<ComboboxSelected>>', lambda e, r=row_number: self.app.SalesInvoice.update_material_info(r, "code"))
                cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_combobox_change_purchase(e, r, "code"))
                cb.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                value = value.strip()
                cb.set(value)
                row_entries.append(var)
            elif col == "Material_name":
                value = value.strip()
                var = tk.StringVar(value=value)
                # row_entry_vars.append(var)
                cb = ttk.Combobox(row_frame, textvariable=var, values=self.app.product_names)
                var = tk.StringVar(value=value)
                cb.bind('<<ComboboxSelected>>', lambda e, r=row_number: self.app.SalesInvoice.update_material_info(r, "name"))
                var = tk.StringVar(value=value)
                cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_combobox_change_purchase(e, r, "name"))
                var = tk.StringVar(value=value)
                cb.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                value = value.strip()
                cb.set(value)
                row_entries.append(cb)
                # row_entries.append(var)
                # row_entries.append(value)
            elif col == "unit":
                var = tk.StringVar(value=value)
                cb = ttk.Combobox(row_frame, textvariable=var, values=[])
                var = tk.StringVar(value=value)
                cb.bind('<KeyRelease>', lambda e, r=row_number: self.app.SalesInvoice.handle_unit_change(e, r))
                cb.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                cb.set(value)
                row_entries.append(cb)
            elif col == "Discount_Type":
                var = tk.StringVar(value=value)
                cb = ttk.Combobox(row_frame, textvariable=var, 
                                  values=["Percentage", "Value"], 
                                  state="readonly")
                
                var = tk.StringVar(value=value)
                cb.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                # cb.set(var)
                if value == "":
                    value = "Percentage"
                cb.set(value)
                row_entries.append(cb)
                # row_entries.append(value)
                # row_entries.append(var)
            elif col == "Discount Value":
                var = tk.StringVar(value=value)
                entry = tk.Entry(row_frame, textvariable=var)
                entry.bind('<KeyRelease>', lambda e, r=row_number: self.app.SalesInvoice.calculate_totals(r))
                entry.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                row_entries.append(entry)
            elif col in ["Total_QTY", "Total_Price"]:
                var = tk.StringVar(value=value)
                entry = tk.Entry(row_frame, textvariable=var, relief='flat', state='readonly')
                entry.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                row_entries.append(entry)
            elif col in ["Unit_Price"]:
                var = tk.StringVar(value=value)
                entry = tk.Entry(row_frame, textvariable=var, relief='flat')
                entry.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                entry.bind('<KeyRelease>', lambda e, r=row_number: self.app.SalesInvoice.calculate_totals(r))
                row_entries.append(entry)
            else:
                var = tk.StringVar(value=value)
                entry = tk.Entry(row_frame, textvariable=var)
                entry.bind('<KeyRelease>', lambda e, r=row_number: self.app.SalesInvoice.calculate_totals(r))
                entry.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                row_entries.append(entry)
        
        return row_entries
    
    def add_three_rows_purchase(self, initial_data=None):
        current_row_count = len(self.app.entries)
        for i in range(3):
            bg_color = 'white' if (current_row_count + i) % 2 == 0 else '#f0f0f0'
            row_data = initial_data[i] if initial_data and i < len(initial_data) else None
            row_entries = self.create_row_purchase(self.app.rows_frame, current_row_count + i, bg_color, row_data)
            self.app.entries.append(row_entries)
            
            # If we have initial data, update product info
            if row_data: #Seif: row_data is always empty
                
                # Calculate totals for this row
                self.app.SalesInvoice.calculate_totals(current_row_count + i)



    def load_invoice_data_purchase(self, sales_col):
        """Load selected invoice data into the form"""
        invoice_number = self.app.invoice_var.get()
        if not invoice_number:
            messagebox.showwarning(self.app.AuxiliaryClass.t("Selection Needed"), self.app.AuxiliaryClass.t("Please select an invoice first"))
            return
        
        # Fetch invoice data from MongoDB
        invoice_data = sales_col.find_one({"Receipt_Number": invoice_number})
        if not invoice_data:
            messagebox.showerror(self.app.AuxiliaryClass.t("Not Found"), self.app.AuxiliaryClass.t("Invoice not found in database")   )
            return
        
        # Store invoice ID for later reference
        self.app.selected_invoice_id = str(invoice_data["_id"])
        
        # Extract nested dictionaries
        self.app.supplier_info = invoice_data.get("supplier_info", {})
        self.app.financials_purchases = invoice_data.get("Financials", {})
        self.app.items_purchase = invoice_data.get("Items", [])

        # Populate customer information
        self.app.supplier_name_var.set(self.app.supplier_info.get("name", ""))
        self.app.supplier_code_var.set(self.app.supplier_info.get("code", ""))
        self.app.previous_balance_var.set(str(self.app.financials_purchases.get("Previous_balance", 0)))
        
        # Populate financial fields
        self.app.payed_cash_var.set(str(self.app.financials_purchases.get("Payed_cash", 0)))  # Ensure string conversion
        # self.transport_fees_var.set(str(financials.get("transport_fees", 0)))  # Ensure string conversion
        
        # Set payment method
        payment_method = self.app.financials_purchases.get("Payment_method", "Cash")   
        if payment_method in ["Cash", "E_Wallet", "bank_account", "Instapay"]:
            self.app.payment_method_var.set(payment_method)
        
        # Clear existing items 
        self.app.entries.clear()
        for widget in self.app.rows_frame.winfo_children():
            widget.destroy()
        
        # Add rows with invoice items
        # Calculate the number of sets needed (each set contains 3 rows)
        num_sets = (len(self.app.items_purchase) + 2) // 3  # Round up to nearest multiple of 3
        # Process each set of items
        for set_index in range(num_sets):
            start_index = set_index * 3
            end_index = start_index + 3
            item_set = self.app.items_purchase[start_index:end_index]  # Get next 3 items (or remaining)
            self.add_three_rows_purchase(initial_data=item_set)  # Pass items to populate


    def save_invoice_purchase(self, purchase_col, suppliers_col, materials_col):
        """Prepare purchase invoice data and show preview without saving"""
        try:
            # التحقق من وجود بيانات المورد
            supplier_name = self.app.supplier_name_var.get().strip()
            if not supplier_name:
                messagebox.showerror("خطأ", "يرجى اختيار مورد")
                return

            # البحث عن المورد في قاعدة البيانات
            supplier = suppliers_col.find_one({"Name": supplier_name})
            if not supplier:
                messagebox.showerror("خطأ", "المورد غير مسجل!")
                return

            # التحقق من المبلغ المدفوع
            payed_cash = float(self.app.payed_cash_var.get() or 0)

            # جمع بيانات العناصر والتحقق من المخزون
            items = []
            total_amount = 0.0
            stock_updates = {}
            
            for row_idx, row in enumerate(self.app.entries):
                material_code = row[0].get().strip()
                if not material_code:
                    continue

                material = materials_col.find_one({"material_code": material_code})
                if not material:
                    messagebox.showerror("خطأ", f"الخامة {material_code} غير موجود!")
                    return

                try:
                    # استخراج القيم من الحقول
                    qty = float(row[4].get() or 0)
                    numbering = float(row[3].get() or 0)
                    unit_price = float(row[8].get() or 0)
                    discount_type = row[5].get()
                    discount_value = float(row[6].get() or 0)
                    
                    # حساب القيم
                    total_qty = qty * numbering
                    total_price = unit_price * total_qty
                    
                    # تطبيق الخصم
                    if discount_type == "Percentage":
                        discount = total_price * (discount_value / 100)
                    else:
                        discount = min(discount_value, total_price)
                    
                    final_price = max(total_price - discount, 0)

                    # التحقق من المخزون
                    stock = material.get("stock_quantity", 0)
                    stock = float(stock)
                    # if total_qty > stock:
                    #     messagebox.showerror("نقص في المخزون", 
                    #         f"الكمية المطلوبة ({total_qty}) تتجاوز المخزون ({stock}) للمنتج {material_code}")
                    #     return
                    if self.app.update_purchase:
                        for item in self.app.items_purchase:
                            Material_code =item.get("material_code")
                            Material = materials_col.find_one({"material_code": Material_code})
                            total_Qty = float(item.get("Total_QTY"))
                            if Material_code is not None and total_Qty is not None:    
                                Stock = Material.get("stock_quantity", 0)
                                stock_updates[Material_code] = Stock - total_Qty
                                if Material_code == material_code:
                                    stock_updates[Material_code] += total_qty
                                else:
                                    stock_updates[material_code] = stock + total_qty                        
                    else:
                        stock_updates[material_code] = stock + total_qty
                    total_amount += final_price

                    # إضافة العنصر
                    items.append({
                        "material_code": material_code,
                        "material_name": row[1].get().strip(),
                        "Unit": row[2].get().strip(),
                        "QTY": qty,
                        "numbering": numbering,
                        "Total_QTY": total_qty,
                        "Unit_price": unit_price,
                        "Discount_Type": discount_type,
                        "Discount_Value": discount_value,
                        "Final_Price": final_price
                    })
                    
                except ValueError as e:
                    messagebox.showerror("خطأ", f"قيم غير صالحة في الصف {row_idx+1}: {str(e)}")
                    return

            if not items:
                messagebox.showerror("خطأ", "لا توجد عناصر في الفاتورة!")
                return
                
            # توليد رقم الفاتورة
            if self.app.update_purchase:
                invoice_number = self.app.invoice_var.get()
            else:
                invoice_number = self.generate_invoice_number_purchase()
            if not invoice_number:
                return
            
            if self.app.update_purchase:
                Prev_supplier_name = self.app.supplier_info.get("name", "")
                Previous_Net_total= self.app.financials_purchases.get("Net_total", 0) # the old financials
                if Prev_supplier_name == supplier_name:
                    Previous_balance = (supplier.get("Balance", 0)) - Previous_Net_total
                else:
                    Previous_balance = supplier.get("Balance", 0)
            else:
                Previous_balance = supplier.get("Balance", 0)

            # إنشاء بيانات الفاتورة الكاملة
            invoice_data = {
                "Receipt_Number": invoice_number,
                "Date": datetime.now(),
                "supplier_info": {
                    "code": supplier.get("Code", "SUP-001"),
                    "name": supplier.get("Name", "غير معروف"),
                    "phone1": supplier.get("Phone_number1", ""),
                    "phone2": supplier.get("Phone_number2", ""),
                    "address": supplier.get("Company_address", "")
                },
                "Items": items,
                "Financials": {
                    "Net_total": total_amount,
                    "Previous_balance": Previous_balance,
                    "Total_balance": total_amount + Previous_balance,
                    "Payed_cash": payed_cash,
                    "Remaining_balance": (total_amount + Previous_balance) - payed_cash,
                    "Payment_method": self.app.payment_method_var.get()
                },
                "PDF_Path": "",
            }

            # Store prepared invoice data for preview/final save
            self.app.pending_invoice_data = invoice_data
            self.app.pending_stock_updates = stock_updates
            self.app.pending_supplier_id = supplier["_id"]
            self.app.pending_collections = (purchase_col, suppliers_col, materials_col)
            
            # Show preview instead of saving immediately
            self.show_invoice_preview_purchase(invoice_data)
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في العملية: {str(e)}")

    def show_invoice_preview_purchase(self, invoice_data):
        """Display purchase invoice preview window"""
        preview_win = tk.Toplevel(self.root)
        preview_win.title("معاينة فاتورة الشراء")
        preview_win.geometry("900x650")
        preview_win.resizable(True, True)
        
        # Create a container frame for canvas and scrollbar
        container = tk.Frame(preview_win)
        container.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient=tk.VERTICAL, command=canvas.yview)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure canvas scrolling
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Create scrollable frame inside canvas
        main_frame = tk.Frame(canvas)
        canvas_frame = canvas.create_window((0, 0), window=main_frame, anchor="nw")
        
        # Update the scroll region when main_frame size changes
        main_frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))
        
        # Header section
        header_frame = tk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            header_frame, 
            text=f"فاتورة شراء رقم: {invoice_data['Receipt_Number']}", 
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        ).pack(side=tk.TOP, anchor=tk.CENTER)
        
        tk.Label(
            header_frame, 
            text=f"التاريخ: {invoice_data['Date']}", 
            font=("Arial", 12)
        ).pack(side=tk.TOP, anchor=tk.CENTER, pady=5)
        
        # Supplier info section
        supp_frame = ttk.LabelFrame(main_frame, text="معلومات المورد")
        supp_frame.pack(fill=tk.X, pady=10, padx=20)
        
        supp_grid = tk.Frame(supp_frame)
        supp_grid.pack(fill=tk.X, padx=10, pady=10)
        
        labels = [
            ("اسم المورد:", invoice_data['supplier_info']['name']),
            ("كود المورد:", invoice_data['supplier_info']['code']),
            ("التليفون:", invoice_data['supplier_info']['phone1']),
            ("العنوان:", invoice_data['supplier_info']['address'])
        ]
        
        for i, (label, value) in enumerate(labels):
            tk.Label(supp_grid, text=label, font=("Arial", 11, "bold"), 
                    anchor="e", width=10).grid(row=i//2, column=(i%2)*2, sticky="e", padx=5, pady=2)
            tk.Label(supp_grid, text=value, font=("Arial", 11), 
                    anchor="w", width=25).grid(row=i//2, column=(i%2)*2+1, sticky="w", padx=5, pady=2)
        
        # Items table
        table_frame = ttk.LabelFrame(main_frame, text="تفاصيل الفاتورة")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10, padx=20)
        
        # Create Treeview with scrollbars
        tree_scroll = tk.Scrollbar(table_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("#", "الصنف", "الوحدة", "الكمية", "العدد", "السعر", "الخصم", "الإجمالي")
        tree = ttk.Treeview(
            table_frame, 
            columns=columns, 
            show="headings", 
            height=10,
            yscrollcommand=tree_scroll.set
        )
        tree_scroll.config(command=tree.yview)
        
        # Define columns
        col_widths = [40, 150, 70, 60, 60, 80, 80, 80]
        for idx, col in enumerate(columns):
            tree.heading(col, text=self.app.AuxiliaryClass.t(col))
            tree.column(col, width=col_widths[idx], anchor="center")
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add items to tree
        for i, item in enumerate(invoice_data["Items"], 1):
            discount = f"{item['Discount_Value']}{'%' if item['Discount_Type'] == 'Percentage' else ' ج.م'}"
            tree.insert("", "end", values=(
                i,
                item["material_name"],
                item["Unit"],
                f"{item['QTY']}",
                f"{item['numbering']}",
                f"{item['Unit_price']:.2f}",
                discount,
                f"{item['Final_Price']:.2f}"
            ))
        
        # Financial summary
        fin_frame = ttk.LabelFrame(main_frame, text="الملخص المالي")
        fin_frame.pack(fill=tk.X, pady=10, padx=20)
        
        fin_data = [
            ("صافي الفاتورة:", f"{invoice_data['Financials']['Net_total']:,.2f}  ج.م"),
            ("رصيد سابق:", f"{invoice_data['Financials']['Previous_balance']:,.2f}  ج.م"),
            ("إجمالي المستحق:", f"{invoice_data['Financials']['Total_balance']:,.2f}  ج.م"),
            ("المدفوع:", f"{invoice_data['Financials']['Payed_cash']:,.2f}  ج.م"),
            ("الباقي:", f"{invoice_data['Financials']['Remaining_balance']:,.2f}  ج.م"),
            ("طريقة الدفع:", invoice_data['Financials']['Payment_method'])
        ]
        
        for i, (label, value) in enumerate(fin_data):
            row = tk.Frame(fin_frame)
            row.pack(fill=tk.X, padx=10, pady=3)
            tk.Label(row, text=label, font=("Arial", 11, "bold"), 
                    width=15, anchor="e").pack(side=tk.LEFT)
            tk.Label(row, text=value, font=("Arial", 11), 
                    fg="#2980b9", anchor="w").pack(side=tk.LEFT)
        
        # Action buttons (outside scrollable area)
        btn_frame = tk.Frame(preview_win)
        btn_frame.pack(fill=tk.X, pady=20)
        
        tk.Button(
            btn_frame, 
            text="إلغاء الفاتورة", 
            command=preview_win.destroy,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=5
        ).pack(side=tk.LEFT, padx=10)
        # Create a variable to hold the selected page size
        self.page_size_var = tk.StringVar(value="A5")  # Default value

        # Create the OptionMenu (drop-down list)
        page_sizes = ["A1", "A2", "A3", "A4", "A5", "A6", "A7"]
        page_size_menu = tk.OptionMenu(btn_frame, self.page_size_var, *page_sizes)
        page_size_menu.pack(side=tk.RIGHT, padx=10)       
        tk.Button(
            btn_frame, 
            text="حفظ و طباعة الفاتورة", 
            command=lambda: self.finalize_purchase_invoice(preview_win,page_size=config.PAGE_SIZES[self.page_size_var.get()]),
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=5
        ).pack(side=tk.RIGHT, padx=10)
        
        # Center window
        preview_win.update_idletasks()
        width = preview_win.winfo_width()
        height = preview_win.winfo_height()
        x = (preview_win.winfo_screenwidth() // 2) - (width // 2)
        y = (preview_win.winfo_screenheight() // 2) - (height // 2)
        preview_win.geometry(f'+{x}+{y}')
        
        # Add mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def finalize_purchase_invoice(self, preview_window,page_size):
        """Finalize purchase invoice saving process and generate PDF"""
        flag = 0

        if not hasattr(self.app, 'pending_invoice_data') or not self.app.pending_invoice_data:
            messagebox.showerror("خطأ", "لا توجد بيانات فاتورة معلقة!")
            preview_window.destroy()
            return
        
        try:
            purchase_col, suppliers_col, materials_col = self.app.pending_collections
            invoice_data = self.app.pending_invoice_data
            total_amount = invoice_data['Financials']['Net_total']
            payed_cash = invoice_data['Financials']['Payed_cash']
            
            # 1. Update stock
            for code, new_stock in self.app.pending_stock_updates.items():
                materials_col.update_one(
                    {"material_code": code},
                    {"$set": {"stock_quantity": new_stock}}
                )
            
            # 2. Update supplier
            new_balance = total_amount - payed_cash

            # Fetch the customer document
            supplier = suppliers_col.find_one({"_id": self.app.pending_supplier_id})

            # Prepare conversion updates if needed
            update_fields = {}

            # Fields to check and convert
            fields = ["Sales", "Balance", "Debit", "Credit"]

            for field in fields:
                value = supplier.get(field)
                if isinstance(value, str):
                    try:
                        if field == "Sales":
                            update_fields[field] = int(float(value))  # Sales to int
                        else:
                            update_fields[field] = float(value)       # Others to double
                    except ValueError:
                        update_fields[field] = 0  # fallback to 0 if conversion fails
            if update_fields:
                suppliers_col.update_one(
                    {"_id": self.app.pending_supplier_id},
                    {"$set": update_fields}
                )
            if self.app.update_purchase:
                prev_supplier_name = self.app.supplier_info.get("name", "")
                prev_total_amount = self.app.financials_purchases.get("Net_total")
                prev_payed_cash = self.app.financials_purchases.get("Payed_cash")
                prev_added_balance = prev_total_amount - prev_payed_cash
                # Now perform the main update
                suppliers_col.update_one(
                    {"Name": prev_supplier_name},
                    {   
                        "$inc": {
                            "Sales": -1,
                            "Balance": - prev_added_balance,
                            "Debit": - prev_payed_cash,
                            "Credit": - prev_total_amount
                        }
                    }
                )

            suppliers_col.update_one(
                {"_id": self.app.pending_supplier_id},
                {
                    "$set": {
                        "Last_purchase": datetime.now(),
                    },
                    
                    "$inc": {
                        "Sales": 1,
                        "Balance": new_balance,
                        "Debit": payed_cash,
                        "Credit": total_amount
                    }
                }
            )
            
            # 3. Generate PDF
            pdf_path = self.generate_pdf_purchase(invoice_data,page_size=page_size)
            if not pdf_path:
                preview_window.destroy()
                return
                
            # 4. Save invoice with PDF path
            if self.app.update_purchase:
                purchase_col.delete_one({"Receipt_Number":self.app.invoice_var.get()})
                config.report_log(self.app.logs_collection, self.app.user_name, purchase_col, self.app.AuxiliaryClass.t("Updated new invoice to"), invoice_data, self.app.AuxiliaryClass.t)
                flag=1
            invoice_data["PDF_Path"] = pdf_path
            purchase_col.insert_one(invoice_data)
            
            # 5. Show success and clean up
            messagebox.showinfo("نجاح", f"تم حفظ فاتورة الشراء رقم {invoice_data['Receipt_Number']}")
            self.clear_invoice_form_purchase()
            
            if not flag:
                config.report_log(self.app.logs_collection, self.app.user_name, purchase_col, self.app.AuxiliaryClass.t("Added invoice to"), invoice_data, self.app.AuxiliaryClass.t)
            
            # 6. Clear pending data
            del self.app.pending_invoice_data
            del self.app.pending_stock_updates
            del self.app.pending_supplier_id
            del self.app.pending_collections
            
            preview_window.destroy()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ الفاتورة: {str(e)}")
            preview_window.destroy()

    def clear_invoice_form_purchase(self):
        """Clear the purchase invoice form"""
        try:
            # تنظيف Combobox المورد
            self.app.supplier_name_var.set('')
            
            # تنظيف حقول العناصر
            for row in self.app.entries:
                for entry in row:
                    if isinstance(entry, ttk.Combobox):
                        entry.set('')
                    elif isinstance(entry, tk.Entry):
                        entry.delete(0, tk.END)
            
            
            # إعادة تعيين القائمة
            self.app.entries = []
            # إعادة إنشاء الصفوف الأساسية
            # إذا كنت تستخدم دالة لإضافة الصفوف
            # self.new_Purchase_invoice(self.user_role)
            if self.app.update_purchase:
                self.new_Purchase_invoice(self.app.user_role,"update")
            else:
                self.new_Purchase_invoice(self.app.user_role,"add")
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تنظيف الحقول: {str(e)}")


    def generate_pdf_purchase(self, invoice_data,page_size):
        """توليد ملف PDF بحجم A5 بتنسيق عربي مطابق للنموذج"""
        try:
            from reportlab.lib.pagesizes import A5
            from reportlab.pdfgen import canvas
            from reportlab.lib.units import cm
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            import os
            from bidi.algorithm import get_display
            import arabic_reshaper
            from reportlab.lib.utils import ImageReader
            from reportlab.lib import colors  # Added for colors

            # Load Arabic font
            try:
                arabic_font_path = self.app.SalesInvoice.resource_path(os.path.join("Static", "Fonts", "Amiri-Regular.ttf"))
                if not os.path.exists(arabic_font_path):
                    raise FileNotFoundError(f"Font file not found: {arabic_font_path}")
                pdfmetrics.registerFont(TTFont('Arabic', arabic_font_path))
                pdfmetrics.registerFont(TTFont('Arabic-Bold', arabic_font_path))  # For bold text
            except Exception as e:
                print(f"Error loading Arabic font: {e}")
                # Fallback to a default font if Arabic font fails to load
                pdfmetrics.registerFont(TTFont('Arabic', 'Arial'))
                pdfmetrics.registerFont(TTFont('Arabic-Bold', 'Arial-Bold'))

            # دالة معالجة النصوص العربية
            def format_arabic(text):
                reshaped_text = arabic_reshaper.reshape(str(text))
                return get_display(reshaped_text)

            # Create save path
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            invoice_folder = os.path.join(desktop, "purchase_invoice")

            # Create folder if it doesn't exist
            if not os.path.exists(invoice_folder):
                os.makedirs(invoice_folder)

            # Generate file name
            invoice_number = str(invoice_data['Receipt_Number']).replace("INV-", "").strip()
            file_name = f"فاتورة شراء_{invoice_number}.pdf"

            # Full PDF path
            pdf_path = os.path.join(invoice_folder, file_name)

            # إعداد مستند PDF
            c = canvas.Canvas(pdf_path, pagesize=page_size)
            width, height = A5
            c.setFont("Arabic", 12)

            # إضافة الشعار
            logo_path = os.path.join("Static", "images", "Logo.jpg")
            if os.path.exists(logo_path):
                logo = ImageReader(logo_path)
                c.drawImage(logo, 0.5*cm, height-3.5*cm, width=4*cm, height=2.5*cm, preserveAspectRatio=True)

            # ========== العنوان المركزي ==========
            invoice_title = f"فاتورة شراء رقم {invoice_number}"
            
            # رسم الإطار حول العنوان
            frame_width = 4*cm
            frame_height = 1*cm
            frame_x = (width - frame_width) / 2  # مركز أفقي
            frame_y = height - 2.5*cm
            c.setLineWidth(1)
            c.rect(frame_x, frame_y, frame_width, frame_height, stroke=1)
            
            # كتابة العنوان المركزي
            c.setFont("Arabic-Bold", 12)
            title_x = width / 2
            title_y = height - 2.2*cm
            c.drawCentredString(title_x, title_y, format_arabic(invoice_title))

            # ========== معلومات الشركة ==========
            company_info = [
                "      حسن سليم",
                "للمنتجات البلاستيكية"
            ]
            
            y_position = height - 2*cm
            c.setFont("Arabic-Bold", 12)
            for line in company_info:
                c.drawRightString(width - 1.75*cm, y_position, format_arabic(line))
                y_position -= 0.8*cm

            # ========== معلومات العميل ==========
            customer_y = height - 3.8*cm
            c.setFont("Arabic", 12)
            customer_fields = [
                f"التاريخ:       {invoice_data['Date']}",            
                f"اسم المورد:    {invoice_data['supplier_info']['name']}",
                f"الكود:         {invoice_data['supplier_info']['code']}",
                f"العنوان:       {invoice_data['supplier_info']['address']}",
                f"التليفون:      {invoice_data['supplier_info']['phone1']}"
            ]
            
            for line in customer_fields:
                c.drawRightString(width - 0.4*cm, customer_y, format_arabic(line))
                customer_y -= 0.8*cm

            # ========== جدول العناصر ==========
            headers = ["كود الصنف", "     الصنف", "العدد", "الوحدة", "سعر الوحدة", "الكمية", "الإجمالي"]
            col_positions = [
                width - 0.4*cm,    # كود الصنف
                width - 2*cm,       # الصنف
                width - 6*cm,       # العدد
                width - 7.5*cm,     # الوحدة
                width - 9.5*cm,     # السعر
                width - 11.5*cm,    # الكمية
                width - 13*cm       # الإجمالي
            ]
            
            # رأس الجدول مع لون خلفية
            table_y = customer_y - 0.25*cm
            
            # رسم خلفية ملونة للرأس
            header_height = 0.65*cm
            c.setFillColor(colors.lightblue)
            c.rect(
                col_positions[-1] - 2.0*cm,
                table_y - header_height + 0.2*cm,
                col_positions[0] - col_positions[-1] + 5.0*cm,
                header_height,
                fill=1,
                stroke=0
            )
            
            c.setFont("Arabic-Bold", 10)
            c.setFillColor(colors.black)
            for i, header in enumerate(headers):
                c.drawRightString(col_positions[i], table_y - 0.3*cm, format_arabic(header))

            # بيانات الجدول مع دعم الأسطر المتعددة
            c.setFont("Arabic", 8)
            row_height = 0.7*cm
            max_product_width = 3.5*cm  # أقصى عرض لعمود "الصنف"
            
            # تحديد موضع الصف الأول للبيانات
            table_y -= row_height
            
            # دالة لتقسيم النص الطويل
            def split_text(text, max_width):
                lines = []
                current = ""
                for char in text:
                    test_line = current + char
                    if c.stringWidth(format_arabic(test_line), "Arabic", 8) < max_width:
                        current = test_line
                    else:
                        lines.append(current)
                        current = char
                if current:
                    lines.append(current)
                return lines
            
            for item in invoice_data["Items"]:
                material_name = item.get("material_name", "")
                material_code = item.get("material_code", "")
                
                # تقسيم اسم المادة إذا كان طويلاً
                product_width = c.stringWidth(format_arabic(material_name), "Arabic", 8)
                if product_width > max_product_width:
                    product_lines = split_text(material_name, max_product_width)
                else:
                    product_lines = [material_name]
                
                # حساب ارتفاع الصف بناءً على عدد الأسطر
                item_height = row_height * len(product_lines)
                
                # رسم خلفية بيضاء للصف
                c.setFillColor(colors.white)
                c.rect(
                    col_positions[-1] - 0.5*cm,
                    table_y - item_height + 0.1*cm,
                    col_positions[0] - col_positions[-1] + 1.0*cm,
                    item_height - 0.2*cm,
                    fill=1,
                    stroke=0
                )
                c.setFillColor(colors.black)
                
                # رسم كل سطر من أسطر المادة
                for i, line in enumerate(product_lines):
                    line_y = table_y - (i * row_height)
                    
                    # رسم محتويات الصف
                    columns = [
                        material_code if i == 0 else "",  # عرض الكود في السطر الأول فقط
                        line,
                        str(item.get("numbering", "")) if i == 0 else "",
                        item.get("Unit", "") if i == 0 else "",
                        f"{item.get('Unit_price', 0):.2f}" if i == 0 else "",
                        str(item.get('QTY', 0)) if i == 0 else "",
                        f"{item.get('Final_Price', 0):.2f}" if i == 0 else ""
                    ]
                    
                    for col_index, value in enumerate(columns):
                        c.drawRightString(col_positions[col_index], line_y, format_arabic(value))
                
                # تحديث موضع y للصف التالي
                table_y -= item_height

            # ========== الإجماليات ==========
            totals_y = table_y - 1*cm
            totals = [
                ("صافي الفاتورة:", invoice_data['Financials']['Net_total']),
                ("حساب سابق:", invoice_data['Financials']['Previous_balance']),
                ("إجمالي الفاتورة:", invoice_data['Financials']['Total_balance']),
                ("المدفوع:", invoice_data['Financials']['Payed_cash']),
                ("الباقي:", invoice_data['Financials']['Remaining_balance'])
            ]
            
            c.setFont("Arabic-Bold", 12)
            for label, value in totals:
                text = f"{format_arabic(f'{value:,.2f}')} {format_arabic(label)}"
                c.drawRightString(width - 0.3*cm, totals_y, text)
                totals_y -= 0.8*cm

            # ========== التوقيعات ==========
            c.setFont("Arabic", 10)
            c.drawRightString(width - 2.2*cm, totals_y - 0.5*cm, format_arabic("____________________"))
            c.drawString(1.5*cm, totals_y - 0.5*cm, format_arabic("____________________"))
            
            c.save()

            config.report_log(self.app.logs_collection, self.app.user_name, None, f"{self.app.AuxiliaryClass.t('Generated Pdf Purchase Invoice with Id')} {invoice_data['Receipt_Number']} {self.app.AuxiliaryClass.t('for supplier')} {invoice_data['supplier_info']['code']}", None,self.app.AuxiliaryClass.t)

            try:
                os.startfile(pdf_path, "print")
            except OSError as e:
                messagebox.showerror(self.app.AuxiliaryClass.t("Print Error"), f"{self.app.AuxiliaryClass.t("Failed to print PDF:")}\n{e}")

            pdf_path = config.upload_pdf_to_cloudinary(pdf_path)
            return pdf_path

        except Exception as e:
            messagebox.showerror("خطأ PDF", f"فشل في توليد الملف: {str(e)}")
            return None        
        
    def handle_combobox_change_purchase(self, event, row_idx, field_type):
        """Handle changes in product code/name comboboxes"""
        value = event.widget.get().strip()
        
        # Clear dependent fields if value is empty
        if not value:
            self.app.SalesInvoice.clear_row_fields(row_idx)
            return
            
        # Filter combobox values
        if field_type == "code":
            full_list = self.app.product_codes
        else:
            full_list = self.app.product_names
            
        filtered = [item for item in full_list if value.lower() in str(item).lower()]
        event.widget['values'] = filtered
        
        # Auto-update if exact match found
        if value in full_list:
            self.app.SalesInvoice.update_material_info(row_idx, field_type)


    def generate_invoice_number_purchase(self):
        """توليد رقم فاتورة تسلسلي"""
        try:
            print(0)
            purchaes_col = self.app.AuxiliaryClass.get_collection_by_name('Purchases')
            print(10)
            last_invoice = purchaes_col.find_one(sort=[("Receipt_Number", -1)])
            print(20)
            # التحقق من وجود الفاتورة وتنسيقها
            last_number = 0
            if last_invoice:
                print(1)
                reciept_number = last_invoice.get("Receipt_Number")
                if (
                    reciept_number 
                    and isinstance(reciept_number, str) 
                    and reciept_number.startswith("INV-")
                ):
                    try:
                        last_number = int(reciept_number.split("-")[-1])
                    except (ValueError, IndexError):
                        last_number = 0
            
            new_number = last_number + 1
            # print(4)
            return f"INV-{new_number:05d}"
        
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل توليد الرقم التسلسلي: {str(e)}")
            return None
    def update_search_purchase(self, event, collection):
        # Cancel any previous scheduled search **only if valid**
        if hasattr(self.app, '_after_id') and self.app._after_id is not None:
            try:
                self.root.after_cancel(self.app._after_id)
            except ValueError:
                pass  # Ignore if it was already canceled
        
        # Mark that user is typing
        self.app.is_typing = True
        
        # Schedule the search with the current text
        self.app._after_id = self.root.after(300, self.perform_search_purchase, collection)


    def perform_search_purchase(self, collection):
        # Mark that user is not typing anymore
        self.app.is_typing = False

        search_term = self.app.supplier_name_var.get()

        # If search term is empty, you can clear the combobox
        if search_term == "":
            self.app.supplier_cb['values'] = []
            return

        # Perform search
        filtered_suppliers = [supp['Name'] for supp in collection.find(
            {"Name": {"$regex": f"^{search_term}", "$options": "i"}}
        )]
        
        # Update combobox values only if user is not typing
        if not self.app.is_typing:
            self.app.supplier_cb['values'] = filtered_suppliers
            
            if filtered_suppliers:
                self.app.supplier_cb.event_generate('<Down>')
            else:
                self.app.supplier_cb.event_generate('<Up>')  # Close dropdown