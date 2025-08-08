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
class SalesInvoice:
    def __init__(self, root, app):
        self.root = root
        self.app = app  # save reference to SalesSystemApp

    def manage_sales_invoices_window(self):
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
                {"text": self.app.t("New Sales Invoice"), "image": "new_invoice-dark.png",
                "command": lambda: self.sales_invoice(self.app.user_role,"add")},
                {"text": self.app.t("Update Sales Invoice"), "image": "update_invoice-dark.png",
                "command": lambda: self.sales_invoice(self.app.user_role,"update")}
            ]
        elif not self.app.light:
            buttons = [
                {"text": self.app.t("New Sales Invoice"), "image": "new_invoice-light.png",
                "command": lambda: self.sales_invoice(self.app.user_role,"add")},
                {"text": self.app.t("Update Sales Invoice"), "image": "update_invoice-light.png",
                "command": lambda: self.sales_invoice(self.app.user_role,"update")}
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
                btn.pack(expand=True, fill=tk.BOTH)  # Make button expand to fill frame
                
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=config.COLORS["primary"]))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=config.COLORS["background"]))

                # # Text label
                # lbl = tk.Label(sub_frame, text=btn_info["text"], 
                #             font=("Arial", 15, "bold"), bg=config.COLORS["background"], fg=config.COLORS["text"])
                # lbl.pack(pady=5)

        except Exception as e:
            print(f"Error loading images: {e}")
            # Fallback to text buttons if images fail
            fallback_frame = tk.Frame(self.root, bg=config.COLORS["background"])
            fallback_frame.pack(pady=20)
            for btn_info in buttons:
                tk.Button(fallback_frame, text=btn_info["text"], 
                        command=btn_info["command"]).pack(side="left", padx=10)
                
    def sales_invoice(self, user_role, add_or_update):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Initialize product mappings
        self.app.update = False
        self.app.product_map = {}
        self.app.name_to_code = {}
        
        # Create top bar
        self.app.topbar.topbar(show_back_button=True, Back_to_Sales_Window=True)

        # MongoDB collections
        customers_col = self.app.get_collection_by_name("Customers")
        sales_col = self.app.get_collection_by_name("Sales")
        products_col = self.app.get_collection_by_name("Products")

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
            invoice_numbers = [str(doc["Receipt_Number"]) for doc in sales_col.find({}, {"Receipt_Number": 1})]
            
            # Invoice selection
            tk.Label(invoice_frame, text=self.app.t("Select Invoice"), 
                    font=("Arial", 10, "bold")).grid(row=0, column=0, sticky='w')
            self.app.invoice_var = tk.StringVar()
            invoice_cb = ttk.Combobox(invoice_frame, textvariable=self.app.invoice_var, values=invoice_numbers)
            invoice_cb.grid(row=0, column=1, padx=5, sticky='ew', columnspan=3)
            
            # Load button
            load_btn = tk.Button(invoice_frame, text=self.app.t("Load Invoice"), 
                                command=lambda: self.load_invoice_data(sales_col),
                                bg='#2196F3', fg='white')
            load_btn.grid(row=0, column=4, padx=5, sticky='ew')
            
            # Delete button
            delete_btn = tk.Button(invoice_frame, text=self.app.t("Delete Invoice"), 
                                command=lambda: self.delete_invoice(products_col,sales_col, customers_col,"sales"),
                                bg='red', fg='white')
            delete_btn.grid(row=0, column=5, padx=5, sticky='ew')

        # ===== CUSTOMER SECTION =====
        # Create customer frame
        customer_frame = tk.Frame(form_frame, bd=1, relief=tk.SOLID, padx=5, pady=5)
        customer_frame.grid(row=current_row, column=0, columnspan=12, sticky='ew', pady=5)
        current_row += 1
        
        # Configure customer frame columns
        for i in range(12):
            customer_frame.columnconfigure(i, weight=1 if i % 2 == 1 else 0)
        
        # Create bidirectional customer mappings
        self.app.customer_code_map = {}  # name -> code
        self.app.code_name_map = {}      # code -> name
        self.app.customer_balance_map = {}  # name -> balance

        # Populate customer data
        all_customers = []
        all_codes = []
        for cust in customers_col.find():
            name = cust.get('Name', '')
            code = str(cust.get('Code', ''))
            balance = cust.get('Balance', 0)
            
            self.app.customer_code_map[name] = code
            self.app.code_name_map[code] = name
            self.app.customer_balance_map[name] = balance
            all_customers.append(name)
            all_codes.append(code)

        # Customer Name Combobox
        tk.Label(customer_frame, text=self.app.t("Customer Name"), 
                font=("Arial", 10, "bold")).grid(row=0, column=0, sticky='w')
        self.app.customer_name_var = tk.StringVar()
        self.app.customer_name_cb = ttk.Combobox(customer_frame, 
                                            textvariable=self.app.customer_name_var, 
                                            values=sorted(all_customers))
        self.app.customer_name_cb.grid(row=0, column=1, padx=5, sticky='ew')

        # Customer Code Combobox
        tk.Label(customer_frame, text=self.app.t("Customer Code"), 
                font=("Arial", 10, "bold")).grid(row=0, column=2, sticky='w')
        self.app.customer_code_var = tk.StringVar()
        self.app.customer_code_cb = ttk.Combobox(customer_frame, 
                                            textvariable=self.app.customer_code_var, 
                                            values=sorted(all_codes))
        self.app.customer_code_cb.grid(row=0, column=3, padx=5, sticky='ew')

        # Previous Balance Field
        tk.Label(customer_frame, text=self.app.t("Balance"), 
                font=("Arial", 10, "bold")).grid(row=0, column=4, sticky='e')
        self.app.previous_balance_var = tk.StringVar()
        self.app.previous_balance_entry = tk.Entry(customer_frame, 
                                            textvariable=self.app.previous_balance_var, 
                                            state='readonly', width=10)
        self.app.previous_balance_entry.grid(row=0, column=5, sticky='ew', padx=5)

        # Paid Money Field
        tk.Label(customer_frame, text=self.app.t("Paid Money"), 
                font=("Arial", 10, "bold")).grid(row=0, column=6, sticky='e')
        self.app.payed_cash_var = tk.DoubleVar()
        self.app.payed_cash_entry = tk.Entry(customer_frame, 
                                        textvariable=self.app.payed_cash_var,
                                        width=10)
        self.app.payed_cash_entry.grid(row=0, column=7, sticky='ew', padx=5)

        # Transportation Fees Field
        tk.Label(customer_frame, text=self.app.t("Transport"), 
                font=("Arial", 10, "bold")).grid(row=0, column=10, sticky='e')
        self.app.transport_fees_var = tk.DoubleVar(value=0.0)
        self.app.transport_fees_entry = tk.Entry(customer_frame, 
                                        textvariable=self.app.transport_fees_var,
                                        width=8)
        self.app.transport_fees_entry.grid(row=0, column=11, sticky='ew', padx=5)

        # Payment Method Dropdown
        tk.Label(customer_frame, text=self.app.t("Payment Method"), 
                font=("Arial", 10, "bold")).grid(row=0, column=8, sticky='e')
        self.app.payment_method_var = tk.StringVar()
        payment_methods = ['Cash', 'E_Wallet', 'bank_account', 'Instapay']
        payment_cb = ttk.Combobox(customer_frame, 
                                textvariable=self.app.payment_method_var, 
                                values=payment_methods, 
                                state='readonly',
                                width=8)
        payment_cb.grid(row=0, column=9, sticky='ew', padx=5)
        payment_cb.current(0)  # Set default to Cash
        
        # Synchronization functions
        def sync_from_name(event=None):
            name = self.app.customer_name_var.get()
            code = self.app.customer_code_map.get(name, '')
            self.app.customer_code_var.set(code)
            self.app.previous_balance_var.set(str(self.app.customer_balance_map.get(name, 0)))

        def sync_from_code(event=None):
            code = self.app.customer_code_var.get()
            name = self.app.code_name_map.get(code, '')
            self.app.customer_name_var.set(name)
            self.app.previous_balance_var.set(str(self.app.customer_balance_map.get(name, 0)))

        # Event bindings
        self.app.customer_name_cb.bind('<<ComboboxSelected>>', sync_from_name)
        self.app.customer_code_cb.bind('<<ComboboxSelected>>', sync_from_code)
        
        self.app.customer_name_cb.bind('<KeyRelease>', lambda e: [
            self.app.filter_combobox(e, all_customers, self.app.customer_name_cb),
            sync_from_name()
        ])
        
        self.app.customer_code_cb.bind('<KeyRelease>', lambda e: [
            self.app.filter_combobox(e, all_codes, self.app.customer_code_cb),
            sync_from_code()
        ])

        # ===== PRODUCTS SECTION =====
        # Load product data
        try:
            products = list(products_col.find())
            all_units = set()
            product_names = []
            product_codes = []

            for p in products:
                code = str(p.get('product_code', '')).strip()
                name = p.get('product_name', '').strip()
                units_list = p.get('Units', [])

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
                    price_str = str(p.get('Unit_Price', '0')).strip('kgm ')
                    price = float(price_str) if price_str else 0.0
                except ValueError:
                    price = 0.0

                # Update mappings
                self.app.product_map[code] = {
                    'name': name,
                    'units': unit_names,
                    'price': price
                }
                self.app.name_to_code[name] = code
                product_names.append(name)
                product_codes.append(code)

            self.app.product_codes = sorted(list(set(product_codes)))
            self.app.product_names = sorted(list(set(product_names)))
            all_units = sorted(list(all_units))

        except Exception as e:
            messagebox.showerror(self.app.t("Database Error"), f"{self.app.t("Failed to load products:")} {str(e)}")
            return

        # ===== ITEMS GRID SECTION =====
        # Make items grid expandable
        form_frame.grid_rowconfigure(current_row + 1, weight=1)
        
        # Invoice Items Grid
        columns = self.app.get_fields_by_name("Sales_Header")
        num_columns = len(columns)
        
        # Create header frame
        header_frame = tk.Frame(form_frame, bg='#f0f0f0')
        header_frame.grid(row=current_row, column=0, columnspan=10, sticky='ew', pady=(20, 0))
        current_row += 1
        
        # Configure header columns
        for col_idx in range(num_columns):
            header_frame.columnconfigure(col_idx, weight=1, uniform='cols')
            tk.Label(header_frame, text=self.app.t(columns[col_idx]), relief='ridge', 
                    bg='#f0f0f0', anchor='w', padx=5).grid(row=0, column=col_idx, sticky='ew')

        # Scrollable Canvas
        canvas_container = tk.Frame(form_frame)
        canvas_container.grid(row=current_row, column=0, columnspan=10, sticky='nsew')
        canvas_container.grid_rowconfigure(0, weight=1)
        canvas_container.grid_columnconfigure(0, weight=1)
        current_row += 1
        
        canvas = tk.Canvas(canvas_container, highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
        self.app.rows_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.app.rows_frame, anchor="nw", tags="inner_frame")
        
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def configure_canvas(event):
            canvas_width = event.width
            canvas.itemconfig("inner_frame", width=canvas_width)
        
        self.app.rows_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_canvas)

        self.app.entries = []

        # Add initial rows
        self.add_three_rows()

        # ===== BUTTONS SECTION =====
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=current_row, column=0, columnspan=10, pady=10, sticky='ew')
        
        # Configure button frame columns
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        add_btn = tk.Button(button_frame, text=self.app.t("➕ Add 3 More Rows"), 
                        command=self.add_three_rows, bg='#4CAF50', fg='white')
        add_btn.grid(row=0, column=0, padx=5, sticky='w')
        
        if add_or_update == "add":
            save_btn = tk.Button(button_frame, text=self.app.t("💾 Save Invoice"), 
                                command=lambda: self.save_invoice(sales_col, customers_col, products_col),
                                bg='#2196F3', fg='white')
            save_btn.grid(row=0, column=1, padx=5, sticky='e')
        else:
            self.app.update = True
            update_btn = tk.Button(button_frame, text=self.app.t("🔄 Update Invoice"), 
                                command=lambda: self.save_invoice(sales_col, customers_col, products_col),
                                bg='#FF9800', fg='white')
            update_btn.grid(row=0, column=1, padx=5, sticky='e')
        # Modified create_row function to accept initial values

    def load_invoice_data(self, sales_col):
        """Load selected invoice data into the form"""
        invoice_number = self.app.invoice_var.get()
        if not invoice_number:
            messagebox.showwarning(self.app.t("Selection Needed"), self.app.t("Please select an invoice first"))
            return
        
        # Fetch invoice data from MongoDB
        invoice_data = sales_col.find_one({"Receipt_Number": invoice_number})
        if not invoice_data:
            messagebox.showerror(self.app.t("Not Found"), self.app.t("Invoice not found in database"))
            return
        
        # Store invoice ID for later reference
        self.app.selected_invoice_id = str(invoice_data["_id"])
        
        # Extract nested dictionaries
        self.app.customer_info = invoice_data.get("Customer_info", {})
        self.app.financials = invoice_data.get("Financials", {})
        self.app.items = invoice_data.get("Items", [])

        # Populate customer information
        self.app.customer_name_var.set(self.app.customer_info.get("name", ""))
        self.app.customer_code_var.set(self.app.customer_info.get("code", ""))
        self.app.previous_balance_var.set(str(self.app.financials.get("Previous_balance", 0)))
        
        # Populate financial fields
        self.app.payed_cash_var.set(str(self.app.financials.get("Payed_cash", 0)))  # Ensure string conversion
        self.app.transport_fees_var.set(str(self.app.financials.get("transport_fees", 0)))  # Ensure string conversion
        
        # Set payment method
        payment_method = self.app.financials.get("payment_method", "Cash")
        if payment_method in ["Cash", "E_Wallet", "bank_account", "Instapay"]:
            self.app.payment_method_var.set(payment_method)
        
        # Clear existing items 
        self.app.entries.clear()
        for widget in self.app.rows_frame.winfo_children():
            widget.destroy()
        
        # Add rows with invoice items
        # Calculate the number of sets needed (each set contains 3 rows)
        num_sets = (len(self.app.items) + 2) // 3  # Round up to nearest multiple of 3
        # Process each set of items
        for set_index in range(num_sets):
            start_index = set_index * 3
            end_index = start_index + 3
            item_set = self.app.items[start_index:end_index]  # Get next 3 items (or remaining)
            self.add_three_rows(initial_data=item_set)  # Pass items to populate

    def delete_invoice(self,products_col, sales_col, customers_col,source):
        """Delete selected invoice from the database"""
        invoice_number = self.app.invoice_var.get()
        if not invoice_number:
            messagebox.showwarning(self.app.t("Selection Needed"), self.app.t("Please select an invoice first"))
            return
        
        # Confirm deletion
        if not messagebox.askyesno(self.app.t("Confirm Delete"), f"{self.app.t("Delete invoice")} {invoice_number} {self.app.t("permanently?")}"):
            return
        
        # Fetch invoice to get customer and amount details
        invoice_data = sales_col.find_one({"Receipt_Number": invoice_number})
        self.app.financials = invoice_data.get("Financials", {})

        # product_qty_map = {}

        if source == "sales":
            Customer_info = invoice_data.get("Customer_info", {})
            customer_name = Customer_info.get("name",{})
            customer = customers_col.find_one({"Name": customer_name})
            self.app.pending_customer_id = customer["_id"]
            for item in invoice_data.get("Items",[]):
                product_code = item.get("Product_code")
                total_qty = item.get("Total_QTY", 0)
                if product_code:
                    # product_qty_map[product_code] = total_qty
                    # Decrement the value in MongoDB
                    products_col.update_one(
                        {"product_code": product_code},
                        {"$inc": {"stock_quantity": total_qty}}
                    )

        else:
            supplier_info = invoice_data.get("supplier_info", {})
            supplier_name = supplier_info.get("name",{})
            supplier = customers_col.find_one({"Name": supplier_name})
            self.app.pending_customer_id = supplier["_id"]   
            for item in invoice_data.get("Items",[]):
                material_code = item.get("material_code")
                total_qty = item.get("Total_QTY", 0)
                if material_code:
                    products_col.update_one(
                        {"material_code": material_code},
                        {"$inc": {"stock_quantity": -total_qty}}
                    )
        prev_total_amount = self.app.financials.get("Net_total")
        prev_payed_cash = self.app.financials.get("Payed_cash")
        prev_added_balance = prev_total_amount - prev_payed_cash
        if source == "sales":
            customers_col.update_one(
                {"_id": self.app.pending_customer_id},
                {
                    "$set": {
                        "Last_purchase_date": datetime.now()
                    },
                    "$inc": {
                        "Sales": -1,
                        "Debit": -prev_total_amount,
                        "Credit": -prev_payed_cash,
                        "Balance": -prev_added_balance
                    }
                }
            )  
        else:
            customers_col.update_one(
                {"_id": self.app.pending_customer_id},
                {
                    "$set": {
                        "Last_purchase_date": datetime.now()
                    },
                    "$inc": {
                        "Sales": -1,
                        "Debit": -prev_payed_cash,
                        "Credit": -prev_total_amount,
                        "Balance": -prev_added_balance
                    }
                }
            )  
        if not invoice_data:
            messagebox.showerror(self.app.t("Not Found"), self.app.t("Invoice not found"))
            return
        
        # Delete from MongoDB
        sales_col.delete_one({"Receipt_Number": invoice_number})
        
        messagebox.showinfo(self.app.t("Success"), self.app.t("Invoice deleted successfully"))
        config.report_log(self.app.logs_collection, self.app.user_name, sales_col, f"Deleted {capitalize_first_letter(source)} Invoice in", invoice_data)
        # Clear the form or reset UI as needed
        self.app.invoice_var.set("")
        self.app.selected_invoice_id = None

        if source == "sales":
            self.sales_invoice(self.app.user_role,"update")
        else:
            self.app.PurchaseInvoice.new_Purchase_invoice(self.app.user_role,"update")

    def add_three_rows(self, initial_data=None):
        current_row_count = len(self.app.entries)
        for i in range(3):
            bg_color = 'white' if (current_row_count + i) % 2 == 0 else '#f0f0f0'
            row_data = initial_data[i] if initial_data and i < len(initial_data) else None
            row_entries = self.create_row(self.app.rows_frame, current_row_count + i, bg_color, row_data)
            self.app.entries.append(row_entries)
            
            # If we have initial data, update product info
            if row_data: #Seif: row_data is always empty
                # Calculate totals for this row
                self.calculate_totals(current_row_count + i)
    


    def save_invoice(self, sales_col, customers_col, products_col):
        """Prepare invoice data and show preview without saving"""
        try:
            # التحقق من وجود بيانات العميل
            customer_name = self.app.customer_name_var.get().strip()
            customer_code = self.app.customer_code_var.get().strip()
            if not customer_name:
                messagebox.showerror("خطأ", "يرجى اختيار عميل")
                return

            # البحث عن العميل في قاعدة البيانات
            # customer_code = customers_col.find_one({"": c})
            customer = customers_col.find_one({"Name": customer_name})
            if not customer:
                messagebox.showerror("خطأ", "العميل غير مسجل!")
                return

            # التحقق من المبلغ المدفوع
            payed_cash = float(self.app.payed_cash_var.get() or 0)
            transportation_fees = float(self.app.transport_fees_var.get() or 0)

            # جمع بيانات العناصر والتحقق من المخزون
            items = []
            total_amount = transportation_fees
            stock_updates = {}
            
            for row_idx, row in enumerate(self.app.entries):
                product_code = row[0].get().strip()
                if not product_code:
                    continue

                product = products_col.find_one({"product_code": product_code})
                if not product:
                    messagebox.showerror("خطأ", f"المنتج {product_code} غير موجود!")
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
                    stock = product.get("stock_quantity", 0)
                    stock = float(stock)
                    if self.app.update:
                        for item in self.app.items:
                            product_Code = item.get("Product_code")
                            Product = products_col.find_one({"product_code": product_Code})
                            total_Qty = item.get("Total_QTY")
                        if total_qty > (stock + total_Qty):
                            messagebox.showerror("نقص في المخزون", 
                                f"الكمية المطلوبة ({total_qty}) تتجاوز المخزون ({stock + total_Qty}) للمنتج {product_code}")
                            return
                        
                    else:
                        if total_qty > stock:
                            messagebox.showerror("نقص في المخزون", 
                                f"الكمية المطلوبة ({total_qty}) تتجاوز المخزون ({stock}) للمنتج {product_code}")
                            return
                    if self.app.update:

                            if product_Code is not None and total_Qty is not None:    
                                Stock = Product.get("stock_quantity", 0)
                                stock_updates[product_Code] = Stock + total_Qty 
                                if product_Code == product_code:
                                    stock_updates[product_Code] -= total_qty
                                else:
                                    stock_updates[product_code] = stock - total_qty
                    else:
                        stock_updates[product_code] = stock - total_qty
                    
                    total_amount += final_price

                    # إضافة العنصر
                    items.append({
                        "Product_code": product_code,
                        "product_name": row[1].get().strip(),
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
            if self.app.update:
                invoice_number = self.app.invoice_var.get()
            else:
                invoice_number = self.generate_invoice_number()
            if not invoice_number:
                return

            if self.app.update:
                Prev_customer_name = self.app.customer_info.get("name", "")
                Previous_Net_total= self.app.financials.get("Net_total", 0) # the old financials
                if Prev_customer_name == customer_name:
                    Previous_balance = (customer.get("Balance", 0)) - Previous_Net_total
                else:
                    Previous_balance = customer.get("Balance", 0)

            else:
                Previous_balance = customer.get("Balance", 0)

            print("\n###############################################################################################\n")
            # إنشاء بيانات الفاتورة الكاملة
            invoice_data = {
                "Receipt_Number": invoice_number,
                "Date": datetime.now(),
                "Customer_info": {
                    "code": customer.get("Code", "CUST-001"),
                    "name": customer.get("Name", "غير معروف"),
                    "phone1": customer.get("Phone_number1", ""),
                    "phone2": customer.get("Phone_number2", ""),
                    "address": customer.get("Company_address", "")
                },
                "Items": items,
                "Financials": {
                    "transport_fees":transportation_fees,
                    "Net_total": total_amount,
                    "Previous_balance": Previous_balance,
                    "Total_balance": total_amount + Previous_balance,
                    "Payed_cash": payed_cash,
                    "transportation_fees": transportation_fees,
                    "Remaining_balance": (total_amount + Previous_balance) - payed_cash,
                    "Payment_method": self.app.payment_method_var.get()
                },
                "PDF_Path": "",
            }

            # Store prepared invoice data for preview/final save
            self.app.pending_invoice_data = invoice_data
            self.app.pending_stock_updates = stock_updates
            self.app.pending_customer_id = customer["_id"]
            self.app.pending_collections = (sales_col, customers_col, products_col)
            
            # Show preview instead of saving immediately
            self.show_invoice_preview(invoice_data)
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في العملية: {str(e)}")

    def show_invoice_preview(self, invoice_data):
        """Display invoice preview window"""
        preview_win = tk.Toplevel(self.root)
        preview_win.title("معاينة الفاتورة")
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
            text=f"فاتورة مبيعات رقم: {invoice_data['Receipt_Number']}", 
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        ).pack(side=tk.TOP, anchor=tk.CENTER)
        
        tk.Label(
            header_frame, 
            text=f"التاريخ: {invoice_data['Date']}", 
            font=("Arial", 12)
        ).pack(side=tk.TOP, anchor=tk.CENTER, pady=5)
        
        # Customer info section
        cust_frame = ttk.LabelFrame(main_frame, text="معلومات العميل")
        cust_frame.pack(fill=tk.X, pady=10, padx=20)
        
        cust_grid = tk.Frame(cust_frame)
        cust_grid.pack(fill=tk.X, padx=10, pady=10)
        
        labels = [
            ("اسم العميل:", invoice_data['Customer_info']['name']),
            ("كود العميل:", invoice_data['Customer_info']['code']),
            ("التليفون:", invoice_data['Customer_info']['phone1']),
            ("العنوان:", invoice_data['Customer_info']['address'])
        ]
        
        for i, (label, value) in enumerate(labels):
            tk.Label(cust_grid, text=label, font=("Arial", 11, "bold"), 
                    anchor="e", width=10).grid(row=i//2, column=(i%2)*2, sticky="e", padx=5, pady=2)
            tk.Label(cust_grid, text=value, font=("Arial", 11), 
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
            tree.heading(col, text=self.app.t(col))
            tree.column(col, width=col_widths[idx], anchor="center")
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add items to tree
        for i, item in enumerate(invoice_data["Items"], 1):
            discount = f"{item['Discount_Value']}{'%' if item['Discount_Type'] == 'Percentage' else ' ج.م'}"
            tree.insert("", "end", values=(
                i,
                item["product_name"],
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
            ("مصاريف النقل :", f"{invoice_data['Financials']['transportation_fees']:,.2f}  ج.م"),
            ("المدفوع:", f"{invoice_data['Financials']['Payed_cash']:,.2f} ج.م"),
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
        
        tk.Button(
            btn_frame, 
            text="حفظ الفاتورة", 
            command=lambda: self.finalize_invoice_save(preview_win),
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

    def finalize_invoice_save(self, preview_window):
        """Finalize invoice saving process and generate PDF"""
        
        flag = 0

        if not hasattr(self.app, 'pending_invoice_data') or not self.app.pending_invoice_data:
            messagebox.showerror("خطأ", "لا توجد بيانات فاتورة معلقة!")
            preview_window.destroy()
            return
        
        try:
            sales_col, customers_col, products_col = self.app.pending_collections
            invoice_data = self.app.pending_invoice_data
            total_amount = invoice_data['Financials']['Net_total']
            payed_cash = invoice_data['Financials']['Payed_cash']
            # transportation_fees = invoice_data['Financials']['transportation_fees']
            
            # 1. Update stock
            for code, new_stock in self.app.pending_stock_updates.items():
                products_col.update_one(
                    {"product_code": code},
                    {"$set": {"stock_quantity": new_stock}}
                )
            # 2. Update customer
            # Fetch the customer document
            customer = customers_col.find_one({"_id": self.app.pending_customer_id})
            new_balance = total_amount - payed_cash
            # Prepare conversion updates if needed
            update_fields = {}

            # Fields to check and convert
            fields = ["Sales", "Balance", "Debit", "Credit"]

            for field in fields:
                value = customer.get(field)
                if isinstance(value, str):
                    try:
                        if field == "Sales":
                            update_fields[field] = int(float(value))  # Sales to int
                        else:
                            update_fields[field] = float(value)       # Others to double
                    except ValueError:
                        update_fields[field] = 0  # fallback to 0 if conversion fails

            # If any field needed conversion, apply the type fix fir
            if update_fields:
                customers_col.update_one(
                    {"_id": self.app.pending_customer_id},
                    {"$set": update_fields}
                )
            if self.app.update:
                Prev_customer_name = self.app.customer_info.get("name", "")
                prev_total_amount = self.app.financials.get("Net_total") # the old financials
                prev_payed_cash = self.app.financials.get("Payed_cash") # the old financials
                prev_added_balance = prev_total_amount - prev_payed_cash
                # Now perform the main update
                customers_col.update_one(
                    {"Name": Prev_customer_name},
                    {
                        "$inc": {
                            "Sales": -1,
                            "Balance": - prev_added_balance,
                            "Debit": - prev_total_amount,
                            "Credit": - prev_payed_cash
                        }
                    }
                )                               
            # Now perform the main update
            customers_col.update_one(
                {"_id": self.app.pending_customer_id},
                {
                    "$set": {
                        "Last_purchase_date": datetime.now()
                    },
                    "$inc": {
                        "Sales": 1,
                        "Balance": new_balance,
                        "Debit": total_amount,
                        "Credit": payed_cash
                    }
                }
            )
            
            # 3. Generate PDF
            pdf_path = self.generate_pdf(invoice_data)
            if not pdf_path:
                preview_window.destroy()
                return

            # 4. Save invoice with PDF path
            invoice_data["PDF_Path"] = pdf_path
            if self.app.update:
                sales_col.delete_one({"Receipt_Number":self.app.invoice_var.get()})
                config.report_log(self.app.logs_collection, self.app.user_name, sales_col, "Updated invoice to", invoice_data)
                flag=1
            sales_col.insert_one(invoice_data)
            
            
            # 5. Show success and clean up
            messagebox.showinfo("نجاح", f"تم حفظ فاتورة البيع رقم {invoice_data['Receipt_Number']}")
            self.clear_invoice_form()
            
            if not flag:
                config.report_log(self.app.logs_collection, self.app.user_name, sales_col, "Added new invoice to", invoice_data)
            

            # 6. Clear pending data
            del self.app.pending_invoice_data
            del self.app.pending_stock_updates
            del self.app.pending_customer_id
            del self.app.pending_collections
            
            preview_window.destroy()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ الفاتورة: {str(e)}")
            preview_window.destroy()

    def create_row(self, parent, row_number, bg_color, initial_values=None):
        columns = self.app.get_fields_by_name("Sales_Header")
        num_columns = len(columns)
        row_frame = tk.Frame(parent, bg=bg_color)
        row_frame.pack(fill=tk.X)
        
        for col_idx in range(num_columns):
            row_frame.columnconfigure(col_idx, weight=1, uniform='cols')

        # Standardize key names to match MongoDB
        key_map = {
            "Product_code": "Product_code",
            "product_name": "product_name",
            "unit": "Unit",
            "Unit_Price": "Unit_price",
            "QTY": "QTY",
            "Discount_Type": "Discount_Type",
            "Discount Value": "Discount_Value",
            "Total_QTY": "Total_QTY",
            "Numbering": "numbering",
            "Total_Price": "Final_Price"
        }
        row_entries = []
        row_entry_vars = []
        
        for col_idx, col in enumerate(columns):
            # Get value from initial data if available
            value = ""
            if initial_values:
                # Get the standardized key name
                db_key = key_map.get(col, col)
                value = initial_values.get(db_key, "")

                if col == "Product_code" and (value not in self.app.product_codes):
                    print(f"[WARN] '{value}' not in dropdown list!")
                # Handle special cases
                if col == "Discount_Type" and not value:
                    value = "Percentage"
                elif col == "Discount Value" and not value:
                    value = 0
                
            if col == "Product_code":
                vars = tk.StringVar(value=value)
                # print(vars)
                row_entry_vars.append(vars)
                cb = ttk.Combobox(row_frame, textvariable=vars, values=self.app.product_codes)
                cb.bind('<<ComboboxSelected>>', lambda e, r=row_number: self.update_product_info(r, "code"))
                cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_combobox_change(e, r, "code"))
                cb.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                value = value.strip()
                cb.set(value)
                row_entries.append(vars)
            elif col == "product_name":
                var = tk.StringVar(value=value)
                row_entry_vars.append(var)
                cb = ttk.Combobox(row_frame, textvariable=var, values=self.app.product_names)
                cb.bind('<<ComboboxSelected>>', lambda e, r=row_number: self.update_product_info(r, "name"))
                cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_combobox_change(e, r, "name"))
                cb.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                value = value.strip()
                cb.set(value)
                row_entries.append(var)
            elif col == "unit":
                var = tk.StringVar(value=value)
                cb = ttk.Combobox(row_frame, textvariable=var, values=[])
                var = tk.StringVar(value=value)
                cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_unit_change(e, r))
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
                cb.set(value)
                row_entries.append(cb)

            elif col == "Discount Value":
                var = tk.StringVar(value=value)
                entry = tk.Entry(row_frame, textvariable=var)
                entry.bind('<KeyRelease>', lambda e, r=row_number: self.calculate_totals(r))
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
                # Recalculate totals when unit price changes
                entry.bind('<KeyRelease>', lambda e, r=row_number: self.calculate_totals(r))
                row_entries.append(entry)
            else:
                var = tk.StringVar(value=value)
                entry = tk.Entry(row_frame, textvariable=var)
                entry.bind('<KeyRelease>', lambda e, r=row_number: self.calculate_totals(r))
                entry.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                row_entries.append(entry)

        return row_entries
    

    def generate_invoice_number(self):
        """توليد رقم فاتورة تسلسلي"""
        try:
            print(0)
            sales_col = self.app.get_collection_by_name('Sales')
            print(10)
            last_invoice = sales_col.find_one(sort=[("Receipt_Number", -1)])
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
        

    def generate_pdf(self, invoice_data):
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
            from reportlab.lib import colors

            # Load Arabic font
            try:
                arabic_font_path = self.resource_path(os.path.join("Static", "Fonts", "Amiri-Regular.ttf"))
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
            invoice_folder = os.path.join(desktop, "sale_invoice")

            # Create folder if it doesn't exist
            if not os.path.exists(invoice_folder):
                os.makedirs(invoice_folder)

            # Generate file name
            invoice_number = str(invoice_data['Receipt_Number']).replace("INV-", "").strip()
            file_name = f"فاتورة بيع_{invoice_number}.pdf"

            # Full PDF path
            pdf_path = os.path.join(invoice_folder, file_name)

            # إعداد مستند PDF
            c = canvas.Canvas(pdf_path, pagesize=A5)
            width, height = A5
            c.setFont("Arabic", 12)

            # إضافة الشعار
            logo_path = os.path.join(BASE_DIR, "Static", "images", "Logo.jpg")
            if os.path.exists(logo_path):
                logo = ImageReader(logo_path)
                c.drawImage(logo, 0.5*cm, height-3.5*cm, width=4*cm, height=2.5*cm, preserveAspectRatio=True)

            # ========== العنوان المركزي ==========
            invoice_number = str(invoice_data['Receipt_Number']).replace("INV-", "").strip()
            invoice_title = f"فاتورة بيع رقم {invoice_number}"
            
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
                f"اسم العميل:    {invoice_data['Customer_info']['name']}",
                f"الكود:         {invoice_data['Customer_info']['code']}",
                f"العنوان:       {invoice_data['Customer_info']['address']}",
                f"التليفون:      {invoice_data['Customer_info']['phone1']}"
            ]
            
            for line in customer_fields:
                c.drawRightString(width - 0.4*cm, customer_y, format_arabic(line))
                customer_y -= 0.8*cm

            # ========== جدول العناصر ==========
            headers = ["كود الصنف", "     الصنف", "العدد", "الوحدة", "سعر الوحدة", "الكمية", "الإجمالي"]
            col_positions = [
                width - 0.4*cm,    # كود الصنف
                width - 2*cm,       # الصنف
                width - 6*cm,     # العدد
                width - 7.5*cm,     # الوحدة
                width - 9.5*cm,     # السعر
                width - 11.5*cm,    # الكمية
                width - 13*cm       # الإجمالي
            ]
            
            # رأس الجدول مع لون خلفية
            table_y = customer_y - 0.25*cm
            
            # رسم خلفية ملونة للرأس
            header_height = 0.65*cm
            c.setFillColor(colors.lightblue)  # لون خلفية الرأس
            c.rect(
                col_positions[-1] - 2.0*cm,  # أقصى يسار
                table_y - header_height + 0.2*cm,  # أسفل
                col_positions[0] - col_positions[-1] + 5.0*cm,  # العرض
                header_height,  # الارتفاع
                fill=1,
                stroke=0
            )
            
            c.setFont("Arabic-Bold", 10)
            c.setFillColor(colors.black)  # لون النص الأسود
            for i, header in enumerate(headers):
                c.drawRightString(col_positions[i], table_y - 0.3*cm, format_arabic(header))

            # بيانات الجدول مع دعم الأسطر المتعددة
            c.setFont("Arabic", 8)
            row_height = 0.7*cm
            max_product_width = 3.5*cm  # أقصى عرض لعمود "الصنف"
            
            # تحديد موضع الصف الأول للبيانات
            table_y -= row_height
            
            for item in invoice_data["Items"]:
                # التحقق مما إذا كان اسم المنتج يتجاوز المساحة المتاحة
                product_name = item.get("product_name", "")
                product_code = item.get("Product_code", "")
                
                # تقسيم اسم المنتج إلى أسطر متعددة إذا كان طويلاً
                product_lines = []
                current_line = ""
                
                # دالة لتقسيم النص إلى أسطر بناءً على المساحة المتاحة
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
                
                # تقسيم اسم المنتج إذا كان طويلاً
                product_width = c.stringWidth(format_arabic(product_name), "Arabic", 8)
                if product_width > max_product_width:
                    product_lines = split_text(product_name, max_product_width)
                else:
                    product_lines = [product_name]
                
                # حساب ارتفاع الصف بناءً على عدد الأسطر
                item_height = row_height * len(product_lines)
                
                # رسم خلفية بيضاء للصف (اختياري)
                c.setFillColor(colors.white)
                c.rect(
                    col_positions[-1] - 0.5*cm,
                    table_y - item_height + 0.1*cm,
                    col_positions[0] - col_positions[-1] + 1.0*cm,
                    item_height - 0.2*cm,
                    fill=1,
                    stroke=0
                )
                c.setFillColor(colors.black)  # إعادة لون النص إلى الأسود
                
                # رسم كل سطر من أسطر المنتج
                for i, line in enumerate(product_lines):
                    line_y = table_y - (i * row_height)
                    
                    # رسم محتويات الصف
                    columns = [
                        product_code if i == 0 else "",  # عرض الكود في السطر الأول فقط
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
                ("الباقي:", invoice_data['Financials']['Remaining_balance']),
                # ("طريقة الدفع:", invoice_data['Financials']['Payment_method']),
                ("مصاريف النقل:", invoice_data['Financials']['transportation_fees'])
            ]
            
            c.setFont("Arabic-Bold", 12)
            for label, value in totals:
                text = f"{format_arabic(f'{value:,.2f}')} {format_arabic(label)}"
                c.drawRightString(width - 0.3*cm, totals_y, text)
                totals_y -= 0.8*cm

            # ========== التوقيعات ==========
            c.setFont("Arabic", 10)
            c.drawRightString(width - 2.2*cm, totals_y - 0.25*cm, format_arabic("____________________"))
            c.drawString(1.5*cm, totals_y - 0.25*cm, format_arabic("____________________"))

            c.save()
            config.report_log(self.app.logs_collection, self.app.user_name, None, f"Generated Pdf Sales Invoice with Id {invoice_data['Receipt_Number']} for Customer {invoice_data['Customer_info']['code']}", None)
            try:
                os.startfile(pdf_path, "print")
            except OSError as e:
                messagebox.showerror(self.app.t("Print Error"), f"{self.app.t("Failed to print PDF:")}\n{e}")

            pdf_path = self.app.upload_pdf_to_cloudinary(pdf_path)
            return pdf_path

        except Exception as e:
            messagebox.showerror("خطأ PDF", f"فشل في توليد الملف: {str(e)}")
            return None
        

    def clear_invoice_form(self):
            """تنظيف جميع حقول الفاتورة"""
            try:
                # تنظيف Combobox العميل
                self.app.customer_name_var.set('')
                
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
                if self.app.update:
                    self.sales_invoice(self.app.user_role,"update")
                else:
                    self.sales_invoice(self.app.user_role,"add")
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل في تنظيف الحقول: {str(e)}")

    def update_product_info(self, row_idx, source):
        """Update fields based on code or name selection"""
        try:
            if source == "code":
              
                product_code = self.app.entries[row_idx][0]
                print("\n")
                print(product_code)
                print("\n")
                product_code = product_code.get().strip()
                product_info = self.app.product_map.get(product_code, {})
                product_name = product_info.get('name', '')
            else:
                print(2)
                product_name = self.app.entries[row_idx][1].get().strip()
                product_code = self.app.name_to_code.get(product_name, '')
                product_info = self.app.product_map.get(product_code, {})

            # Clear fields if no product found
            if not product_code:
                self.clear_row_fields(row_idx)
                print(3)
                return

            # Update both dropdowns
            self.app.entries[row_idx][0].set(product_code)
            self.app.entries[row_idx][1].set(product_name)
            
            # Update unit combobox values (index 2)
            unit_combobox = self.app.entries[row_idx][2]
            unit_combobox['values'] = product_info.get('units', [])
            if product_info.get('units'):
                unit_combobox.current(0)
            
            # Update Unit Price (index 8)
            self.app.entries[row_idx][8].config(state='normal')
            self.app.entries[row_idx][8].delete(0, tk.END)
            self.app.entries[row_idx][8].insert(0, f"{product_info.get('price', 0):.2f}")
            # self.entries[row_idx][8].config(state='readonly')
            
            self.calculate_totals(row_idx)
        except Exception as e:
            messagebox.showerror(self.app.t("Update Error"), f"{self.app.t("Failed to update product info:")} {str(e)}")
            self.clear_row_fields(row_idx)

    def handle_combobox_change(self, event, row_idx, field_type):
        """Handle changes in product code/name comboboxes"""
        value = event.widget.get().strip()
        
        # Clear dependent fields if value is empty
        if not value:
            self.clear_row_fields(row_idx)
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
            self.update_material_info(row_idx, field_type)

    def handle_unit_change(self, event, row_idx):
        """Handle unit changes and clear price if unit changes"""
        unit = event.widget.get().strip()
        if not unit:
            # Clear Unit Price (index 8) if unit is cleared
            self.app.entries[row_idx][8].config(state='normal')
            self.app.entries[row_idx][8].delete(0, tk.END)
            self.app.entries[row_idx][8].config(state='readonly')
            self.calculate_totals(row_idx)

    def calculate_totals(self, row_idx):
        try:
            # Get values using correct column indices
            numbering = float(self.app.entries[row_idx][3].get() or 0)  # index 3
            qty = float(self.app.entries[row_idx][4].get() or 0)        # index 4
            x = self.app.entries[row_idx][4]
            y= float(self.app.entries[row_idx][4].get())
            unit_price = float(self.app.entries[row_idx][8].get() or 0)  # index 8
            discount_type = self.app.entries[row_idx][5].get()           # index 5
            discount_value = float(self.app.entries[row_idx][6].get() or 0)  # index 6

            # Calculate initial totals
            total_qty = qty * numbering
            total_price = unit_price * total_qty

            # Apply discounts
            if discount_type == "Percentage":
                if discount_value < 0 or discount_value > 100:
                    raise ValueError("Percentage must be between 0-100")
                discount = total_price * (discount_value / 100)
            else:  # Value discount
                discount = min(discount_value, total_price)
                
            final_price = max(total_price - discount, 0)

            # Update Total_QTY (index 7)
            self.app.entries[row_idx][7].config(state='normal')
            self.app.entries[row_idx][7].delete(0, tk.END)
            self.app.entries[row_idx][7].insert(0, f"{total_qty:.2f}")
            self.app.entries[row_idx][7].config(state='readonly')
            
            # Update Total_Price (index 9)
            self.app.entries[row_idx][9].config(state='normal')
            self.app.entries[row_idx][9].delete(0, tk.END)
            self.app.entries[row_idx][9].insert(0, f"{final_price:.2f}")
            self.app.entries[row_idx][9].config(state='readonly')

        except ValueError as e:
            if "Percentage" in str(e):
                messagebox.showerror(self.app.t("Discount Error"), str(e))
                self.app.entries[row_idx][6].delete(0, tk.END)
                self.app.entries[row_idx][6].insert(0, "0")
                
            # Reset calculated fields
            self.app.entries[row_idx][7].config(state='normal')
            self.app.entries[row_idx][7].delete(0, tk.END)
            self.app.entries[row_idx][7].config(state='readonly')
            
            self.app.entries[row_idx][9].config(state='normal')
            self.app.entries[row_idx][9].delete(0, tk.END)
            self.app.entries[row_idx][9].config(state='readonly')


    def resource_path(self,relative_path):
        """ Get absolute path to resource, works for dev and PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    
    def clear_row_fields(self, row_idx):
        """Clear all dependent fields in a row"""
        # Clear product name (index 1)
        self.app.entries[row_idx][1].set('')
        # Clear unit combobox (index 2)
        self.app.entries[row_idx][2].set('')
        self.app.entries[row_idx][2]['values'] = []
        # Clear Unit Price (index 8)
        self.app.entries[row_idx][8].config(state='normal')
        self.app.entries[row_idx][8].delete(0, tk.END)
        self.app.entries[row_idx][8].config(state='readonly')
        # Clear quantity fields (index 3: numbering, 4: QTY)
        self.app.entries[row_idx][3].delete(0, tk.END)
        self.app.entries[row_idx][4].delete(0, tk.END)
        # Clear calculated fields (index 7: Total_QTY, 9: Total_Price)
        self.app.entries[row_idx][7].config(state='normal')
        self.app.entries[row_idx][7].delete(0, tk.END)
        self.app.entries[row_idx][7].config(state='readonly')
        self.app.entries[row_idx][9].config(state='normal')
        self.app.entries[row_idx][9].delete(0, tk.END)
        self.app.entries[row_idx][9].config(state='readonly')
        # Reset discount fields (index 5: Type, 6: Value)
        self.app.entries[row_idx][5].set('Percentage')
        self.app.entries[row_idx][6].delete(0, tk.END)
        self.app.entries[row_idx][6].insert(0, '0')


    def update_material_info(self, row_idx, source):
        """Update fields based on code or name selection"""
        try:
            material_code = self.app.entries[row_idx][0]
            print("1")
            if source == "code":
                ########### Print the type:
                print("\n")
                print("material_code entry:", material_code)
                print("type:", type(material_code))
                print("\n")
                
                ######## Check for index error:
                if row_idx >= len(self.app.entries):
                    print("Invalid row index:", row_idx)
                    return
                ######### Ensure it's a valid widget:
                if not hasattr(material_code, 'get'):
                    print("Not a widget with .get() method!")
                    return

                
                print("\n")
                print(material_code)
                print("\n")
                material_code = material_code.get().strip()
                material_info = self.app.material_map.get(material_code, {})
                material_name = material_info.get('name', '')
                print("2")
            else:
                material_name = self.app.entries[row_idx][1].get().strip()
                material_code = self.app.name_to_code.get(material_name, '')
                material_info = self.app.material_map.get(material_code, {})
                print("3")

            # Clear fields if no product found
            if not material_code:
                self.clear_row_fields(row_idx)
                return

            # Update both dropdowns
            self.app.entries[row_idx][0].set(material_code)
            self.app.entries[row_idx][1].delete(0, tk.END)
            self.app.entries[row_idx][1].insert(0, material_name)

            
            # Update unit combobox values (index 2)
            unit_combobox = self.app.entries[row_idx][2]
            unit_combobox['values'] = material_info.get('units', [])
            if material_info.get('units'):
                unit_combobox.current(0)
            
            # Update Unit Price (index 8)
            self.app.entries[row_idx][8].config(state='normal')
            self.app.entries[row_idx][8].delete(0, tk.END)
            self.app.entries[row_idx][8].insert(0, f"{material_info.get('price', 0):.2f}")
            # self.entries[row_idx][8].config(state='readonly')
            
            self.calculate_totals(row_idx)
        except Exception as e:
            messagebox.showerror(self.app.t("Update Error"), f"{self.app.t("Failed to update Material info:")} {str(e)}")
            self.clear_row_fields(row_idx)



def capitalize_first_letter(text):
    if not text:
        return text
    return text[0].upper() + text[1:]