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
class ProductionOrder:
    def __init__(self, root, app):
        self.root = root
        self.app = app  # save reference to SalesSystemApp

    def new_production_order(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Initialize mappings
        self.app.material_code_map = {}  # code -> {name, stock}
        self.app.material_name_map = {}  # name -> {code, stock}
        self.app.product_code_map = {}   # code -> {name, stock}
        self.app.product_name_map = {}   # name -> {code, stock}

        # Create top bar
        self.app.topbar.topbar(show_back_button=True)

        # Database collections
        materials_col = self.app.get_collection_by_name("Materials")
        products_col = self.app.get_collection_by_name("Products")
        production_col = self.app.get_collection_by_name("Production")

        # Load material data
        for mat in materials_col.find():
            code = mat.get('material_code', '')
            name = mat.get('material_name', '')
            stock = mat.get('stock_quantity', 0)
            self.app.material_code_map[code] = {'name': name, 'stock_quantity': stock}
            self.app.material_name_map[name] = {'code': code, 'stock_quantity': stock}

        # Load product data
        for prod in products_col.find():
            code = prod.get('product_code', '')
            name = prod.get('product_name', '')
            stock = prod.get('stock_quantity', 0)
            self.app.product_code_map[code] = {'name': name, 'stock_quantity': stock}
            self.app.product_name_map[name] = {'code': code, 'stock_quantity': stock}

        # Main form frame with responsive sizing
        form_frame = tk.Frame(self.root, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure columns - 9 columns with equal weight
        for i in range(9):
            form_frame.columnconfigure(i, weight=1)
        form_frame.grid_rowconfigure(1, weight=1)  # Make items grid expandable

        # Define columns
        columns = [
            "Material Code", "Material Name", "Material Available Qty",
            "Material Qty", "Product Code", "Product Name",
            "Product Available Qty", "Product Qty", "Waste"
        ]
        num_columns = len(columns)

        # Create header frame with uniform columns
        header_frame = tk.Frame(form_frame, bg='#f0f0f0')
        header_frame.grid(row=0, column=0, columnspan=num_columns, sticky='ew', pady=(10, 0))
        
        # Configure header columns with uniform weights
        for col_idx in range(num_columns):
            header_frame.columnconfigure(col_idx, weight=1, uniform='cols')
            tk.Label(header_frame, 
                    text=self.app.t(columns[col_idx]),
                    bg='#f0f0f0',
                    relief='ridge',
                    anchor='center',
                    padx=5).grid(row=0, column=col_idx, sticky='ew')

        # Scrollable Canvas with responsive sizing
        canvas_container = tk.Frame(form_frame)
        canvas_container.grid(row=1, column=0, columnspan=num_columns, sticky='nsew')
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

        self.app.production_entries = []

        # Create initial rows
        for _ in range(1):
            self.add_production_row()

        # Control buttons
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=num_columns, pady=10, sticky='ew')
        
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        tk.Button(button_frame, text=self.app.t("➕ Add Row"),
                command=self.add_production_row,
                bg='#4CAF50', fg='white').grid(row=0, column=0, padx=5, sticky='w')
        tk.Button(button_frame, text=self.app.t("💾 Save Order"),
                command=self.save_production_order,
                bg='#2196F3', fg='white').grid(row=0, column=1, padx=5, sticky='e')
        
        self.update_combobox_values()

    def add_production_row(self):
        row_idx = len(self.app.production_entries)
        row_frame = tk.Frame(self.app.rows_frame, bg='white' if row_idx % 2 == 0 else '#f0f0f0')
        row_frame.pack(fill=tk.X)  # Use pack with fill to ensure full width
        
        # Configure columns with uniform weights
        for col_idx in range(9):
            row_frame.columnconfigure(col_idx, weight=1, uniform='cols')
        
        entries = []
        for col_idx in range(9):
            if col_idx in [0, 1]:  # Material Code/Name comboboxes
                cb = ttk.Combobox(row_frame)
                cb.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                if col_idx == 0:
                    cb.bind('<<ComboboxSelected>>', lambda e, idx=row_idx: self.update_material_code(idx))
                else:
                    cb.bind('<<ComboboxSelected>>', lambda e, idx=row_idx: self.update_material_name(idx))
                entries.append(cb)
            
            elif col_idx in [4, 5]:  # Product Code/Name comboboxes
                cb = ttk.Combobox(row_frame)
                cb.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                if col_idx == 4:
                    cb.bind('<<ComboboxSelected>>', lambda e, idx=row_idx: self.update_product_code(idx))
                else:
                    cb.bind('<<ComboboxSelected>>', lambda e, idx=row_idx: self.update_product_name(idx))
                entries.append(cb)
            
            elif col_idx in [2, 6]:  # Available quantities (readonly)
                entry = tk.Entry(row_frame, state='readonly')
                entry.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                entries.append(entry)
            
            else:
                entry = tk.Entry(row_frame)
                entry.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                entries.append(entry)
        
        self.app.production_entries.append(entries)
        self.update_combobox_values()

    def update_combobox_values(self):
        material_codes = list(self.app.material_code_map.keys())
        material_names = list(self.app.material_name_map.keys())
        product_codes = list(self.app.product_code_map.keys())
        product_names = list(self.app.product_name_map.keys())
        
        for row in self.app.production_entries:
            row[0]['values'] = material_codes
            row[1]['values'] = material_names
            row[4]['values'] = product_codes
            row[5]['values'] = product_names

    def update_material_code(self, row_idx):
        code = self.app.production_entries[row_idx][0].get()
        if code in self.app.material_code_map:
            material = self.app.material_code_map[code]
            self.app.production_entries[row_idx][1].set(material['name'])
            self.app.production_entries[row_idx][2].config(state='normal')
            self.app.production_entries[row_idx][2].delete(0, tk.END)
            self.app.production_entries[row_idx][2].insert(0, str(material['stock_quantity']))
            self.app.production_entries[row_idx][2].config(state='readonly')

    def update_material_name(self, row_idx):
        name = self.app.production_entries[row_idx][1].get()
        if name in self.app.material_name_map:
            material = self.app.material_name_map[name]
            self.app.production_entries[row_idx][0].set(material['code'])
            self.app.production_entries[row_idx][2].config(state='normal')
            self.app.production_entries[row_idx][2].delete(0, tk.END)
            self.app.production_entries[row_idx][2].insert(0, str(material['stock_quantity']))
            self.app.production_entries[row_idx][2].config(state='readonly')

    def update_product_code(self, row_idx):
        code = self.app.production_entries[row_idx][4].get()
        if code in self.app.product_code_map:
            product = self.app.product_code_map[code]
            self.app.production_entries[row_idx][5].set(product['name'])
            self.app.production_entries[row_idx][6].config(state='normal')
            self.app.production_entries[row_idx][6].delete(0, tk.END)
            self.app.production_entries[row_idx][6].insert(0, str(product['stock_quantity']))
            self.app.production_entries[row_idx][6].config(state='readonly')

    def update_product_name(self, row_idx):
        name = self.app.production_entries[row_idx][5].get()
        if name in self.app.product_name_map:
            product = self.app.product_name_map[name]
            self.app.production_entries[row_idx][4].set(product['code'])
            self.app.production_entries[row_idx][6].config(state='normal')
            self.app.production_entries[row_idx][6].delete(0, tk.END)
            self.app.production_entries[row_idx][6].insert(0, str(product['stock_quantity']))
            self.app.production_entries[row_idx][6].config(state='readonly')

    def save_production_order(self):
        production_col = self.app.get_collection_by_name("Production")
        materials_col = self.app.get_collection_by_name("Materials")
        products_col = self.app.get_collection_by_name("Products")
        
        try:
            orders = []
            for idx, row in enumerate(self.app.production_entries):
                # Validate data
                try:
                    material_code = row[0].get()
                    material_qty = float(row[3].get())
                    product_code = row[4].get()
                    product_qty = float(row[7].get())
                    waste = float(row[8].get())
                except ValueError:
                    messagebox.showerror(self.app.t("Error"), f"{self.app.t("Invalid values in row")} {idx+1}")
                    return

                # Update material stock
                materials_col.update_one(
                    {'material_code': material_code},
                    {'$inc': {'stock_quantity': -material_qty}}
                )

                # Update product stock
                products_col.update_one(
                    {'product_code': product_code},
                    {'$inc': {'stock_quantity': product_qty}}
                )

                # Create production record
                orders.append({
                    'material_code': material_code,
                    'material_qty': material_qty,
                    'product_code': product_code,
                    'product_qty': product_qty,
                    'waste': waste,
                    'timestamp': datetime.now()
                })

            # Insert production records
            if orders:
                production_col.insert_many(orders)
                for order in orders:
                    config.report_log(self.app.logs_collection, self.app.user_name, production_col, f"{self.app.t("Added new record in")}", order)

            messagebox.showinfo(self.app.t("Success"), self.app.t("Production order saved successfully"))
            self.new_production_order(None)  # Refresh form

        except PyMongoError as e:
            messagebox.showerror(self.app.t("Database Error"), f"{self.app.t("Operation failed:")} {str(e)}")

    def update_inventory(self):
        # Update material and product stocks
        try:
            for row in self.app.production_entries:
                material_code = row[0].get()
                material_qty = float(row[3].get() or 0)
                
                product_code = row[4].get()
                product_qty = float(row[7].get() or 0)
                
                # Update material stock
                if material_code:
                    self.app.db.materials.update_one(
                        {'code': material_code},
                        {'$inc': {'stock_quantity': -material_qty}}
                    )

                # Update product stock
                if product_code:
                    self.app.db.products.update_one(
                        {'code': product_code},
                        {'$inc': {'stock_quantity': product_qty}}
                    )
                    
        except PyMongoError as e:
            messagebox.showerror(self.app.t("Inventory Error"), 
                f"{self.app.t("Failed to update inventory:")} {str(e)}")