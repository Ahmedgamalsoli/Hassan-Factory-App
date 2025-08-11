# ======================
# Used imports
# ======================

import tkinter as tk
import io
import re
import os
from annotated_types import doc
import pytz
import threading  # To play sound without freezing the GUI
import sys
import cloudinary
import cloudinary.uploader
import urllib.request
import matplotlib
import matplotlib.pyplot as plt
import random
import arabic_reshaper
import openpyxl

from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk  # Import Pillow classes
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
from reportlab.lib.pagesizes import letter,A7,A6,A5,A4,A3,A2,A1
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
matplotlib.use('TkAgg')  # Set the backend before importing pyplot

# ======================
# Files Imports
# ======================
import config
from Login import LoginWindow
from groupchat import GroupChat
from chatbot import chatbot
from topbar import topbar
from reports import reports
from sales_invoice import SalesInvoice
from purchases_invoice import PurchaseInvoice
from DB_operations import DBOperations
from production_order import ProductionOrder
from employee_window import EmployeeWindow
from treasury_window import TreasuryWindow
from general_exp_rev import GeneralExpRev
from visualization import Visualization
# ======================
# Unused imports
# ======================

# import sqlite3
# import csv
# import pandas as pd
# from tkinter import Tk, Label, PhotoImage,simpledialog
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# from babel.dates import format_time
# from fpdf import FPDF
# from io import BytesIO
# from cloudinary.uploader import upload
# from bidi.algorithm import get_display
# from matplotlib import rcParams
# from bson.objectid import ObjectId

# ======================
# Global Variables
# ======================

######################################################### Access Data Base ##############################################################################
dialog_width = 300  # Same width as AlwaysOnTopInputDialog
dialog_height = 150 # Same height as AlwaysOnTopInputDialog

ARRAY_FIELDS = ['Units', 'Items'] #Must be lower case


# Determine the base directory
if getattr(sys, "frozen", False):
    # Running as an executable
    BASE_DIR = sys._MEIPASS
else:
    # Running as a script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class SalesSystemApp:
    fields = {
        "Employees": [],  # array of strings
        "Products": [],    # array of strings
        "Customers": [],    # array of strings
        "Sales": [],    # array of strings
        "Suppliers": [],    # array of strings
        "Shipping": [],    # array of strings
        "Orders": [],    # array of strings
        "Expenses": [],    # array of strings
        "Employee_appointments": [],    # array of strings
        "Daily_shifts": [],    # array of strings
        "Accounts": [],    # array of strings
        "Transactions": [],    # array of strings
        "Big_deals": [],    # array of strings
        "TEX_Calculations": [],    # array of strings
    }

############################ Init ########################################################

    def __init__(self, root):
        self.root = root
        # ...existing code...
        self.root.title("مصنع حسن سليم للمنتجات البلاستيكية")
        self.root.attributes('-fullscreen', True)
        self.root.state("zoomed")
        self.root.configure(bg=config.COLORS["background"])
        self.current_window = None
        self.last_number_of_msgs = 0
        self.is_group_chat_read = False

        # Set main application icon (Logo.ico)
        logo_icon_path = os.path.join(BASE_DIR, "Static", "images", "Logo.ico")
        if os.path.exists(logo_icon_path):
            self.root.iconbitmap(logo_icon_path)
        # ...rest of your __init__ code...
        

        style = ttk.Style()
        style.theme_use("clam")  # Looks cleaner than default
        style.configure("Treeview", 
                        background="#f0f0f0",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#f0f0f0",
                        font=("Arial", 10))
        
        self.custom_font = ("Segoe UI", 12)
        self.title_font = ("Segoe UI", 16, "bold")
        
        style.map('Treeview', background=[('selected', '#2196F3')], foreground=[('selected', 'white')])
        
        # style.theme_use("modern")

        self.Connect_DB()
                    
        self.stop_event = threading.Event()
        
        self.image_refs = []
        self.filtered_transactions = []
        self.filtered_transactions_table = []
        self.production_entries = []
        self.language = "Arabic"  # default language       
        
        self.keys = [
        
            "Name", "Password", "Role", "Join_Date", "National_id_pic", "Phone_number", "Address", "Salary",
            "product_name", "category", "stock_quantity", "Specs", "Unit_Price", "product_code", "Units", "prod_pic",
            "Product_code", "unit", "numbering", "QTY", "Discount_Type", "Discount Value", "Total_QTY", "Total_Price",
            "Material_code", "Material_name", "material_name", "specs", "material_code", "material_pic",
            "Phone_number1", "Phone_number2", "Code", "Last_purchase_date", "Purchase_mgr_number", "Financial_mgr_number",
            "Purchase_mgr_name", "Financial_mgr_name", "Email", "Company_address", "Extra_address", "Maps_link",
            "Bank_account", "Instapay", "E_wallet", "Accountant_name", "Accountant_number", "Sales_grade", "Growth_grade",
            "Frequency_grade", "Credit", "Debit", "Balance", "Sales",
            "amount", "date", "description",
            "employee_code", "employee_name", "check_in", "check_out", "duration",
            "Receipt_Number", "Date", "customer_code", "customer_name", "customer_phone1", "customer_phone2",
            "customer_address", "Unit", "Unit_price", "Discount_Value", "Final_Price", "Net_total",
            "Previous_balance", "Total_balance", "Payed_cash", "Remaining_balance", "Payment_method", "PDF_Path",
            "supplier_code", "supplier_name", "supplier_phone1", "supplier_phone2", "supplier_address",
            "Operation_Number", "Time",
            "material_qty", "product_qty", "timestamp", "waste",
            "month_year", "base_salary", "total_withdrawls", "delay_penalty", "overtime_bonus", "net_salary",
            "payment_method", "previous_withdrawls", "amount_withdrawls",
            "code", "type"
        ]

        self.reverse_translations = {self.AuxiliaryClass.t(k): k for k in self.keys}
        
        self.db = None
        self.db_name = tk.StringVar()
        self.table_name = tk.StringVar()
        self.search_query = tk.StringVar()
        self.user_photo_path = ""  # Initialize with None or a default image path
        self.user_photo = ""
        self.user_name = ""  # Placeholder for dynamic user name
        self.user_role = ""  # Placeholder for user role
        self.user_id = None  # Placeholder for user ID
        self.all_customers = None  # Will be loaded on first search
        self._after_id = None
        self.logout_icon_path   = os.path.join(BASE_DIR, "Static", "images", "logout-dark.png")  # Path to logout icon
        self.exit_icon_path     = os.path.join(BASE_DIR, "Static", "images", "exit-dark.png")  # Path to exit icon
        self.calc_icon_path     = os.path.join(BASE_DIR, "Static", "images", "calculator-dark.png")  # Path to exit icon
        self.minimize_icon_path = os.path.join(BASE_DIR, "Static", "images", "minus-dark.png")  # Path to exit icon
        self.back_icon_path     = os.path.join(BASE_DIR, "Static", "images", "left-arrow-dark.png")  # Path to back icon
        self.dark_mode_img      = os.path.join(BASE_DIR, "Static", "images", "dark-mode.png")  # <- your image path
        self.light_mode_img     = os.path.join(BASE_DIR, "Static", "images", "light-mode.png")  # <- your image path
     
        # List to track selected products
        self.selected_products = []  
        self.raw_tree_data = [] 
        self.report_customer_name = ""
        self.update =False
        self.light = True  # Default to light mode
        self.update_purchase =False
        self.groupchat = GroupChat(self.root, self)
        self.db_operations = DBOperations(self.root, self)
        self.chatbot = chatbot(self.root, self)
        self.topbar = topbar(self.root, self)
        self.reports = reports(self.root, self)
        self.SalesInvoice = SalesInvoice(self.root, self)
        self.PurchaseInvoice = PurchaseInvoice(self.root, self)
        self.ProductionOrder = ProductionOrder(self.root, self)
        self.EmployeeWindow = EmployeeWindow(self.root, self)
        self.TreasuryWindow = TreasuryWindow(self.root, self)
        self.GeneralExpRev = GeneralExpRev(self.root, self)
        self.Visualization = Visualization(self.root, self)
        self.AuxiliaryClass = config.AuxiliaryClass(self.root, self)
        self.AuxiliaryClass.clean_materials_collection()
        self.AuxiliaryClass.clean_products_collection()
        self.AuxiliaryClass.clean_customers_collection()
        self.AuxiliaryClass.clean_employees_collection()
        self.AuxiliaryClass.clean_suppliers_collection()
    
    def start_with_login(self):
        self.login_window = LoginWindow(self.root, self)
        self.login_window.open_login_window()
        
    def start_without_login(self):
        self.login_window = LoginWindow(self.root, self)
        app.user_role="developer"
        self.topbar.toggle_theme()
        app.main_menu()
########################################## Tables on Data Base ########################################
    def Connect_DB(self):
        raw_password = "HassanFactory@1@6@6"
        encoded_password = quote_plus(raw_password)
        uri = f"mongodb+srv://hassanfactory116:{encoded_password}@hassan.fkplsys.mongodb.net/"
        cloudinary.config(
            cloud_name = 'dv5dpzmhm', 
            api_key = "229798327524238",
            api_secret = "CVbnCea6qpqIG2VhOOJoP_tQKuI"
        )

        client = MongoClient(uri,serverSelectionTimeoutMS=5000)
        print(client.server_info()["version"])
        try:
            client.admin.command('ping')
            print("✅ Connected to MongoDB")
        except Exception as e:
            messagebox.showerror(self.AuxiliaryClass.t("No Internet Connection"), str(e))

        db = client["Hassan"]   

        self.customers_collection             = db['Customers']
        self.employees_collection             = db['Employees']
        self.employees_appointments_collection= db['Employee_appointimets']
        self.employee_withdrawls_collection   = db['Employee_withdrawls']
        self.employee_salary_collection       = db['Employee_Salary']
        self.products_collection              = db['Products']
        self.sales_collection                 = db['Sales']
        self.suppliers_collection             = db['Suppliers']
        self.materials_collection             = db['Materials']
        self.purchases_collection             = db['Purchases']
        self.shipping_collection              = db['Shipping']
        self.orders_collection                = db['Orders']
        self.expenses_collection              = db['Expenses']
        self.daily_shifts_collection          = db['Daily_shifts']
        self.accounts_collection              = db['Accounts']
        self.transactions_collection          = db['Transactions']
        self.big_deals_collection             = db['Big_deals']
        self.TEX_Calculations_collection      = db['TEX_Calculations']
        self.production_collection            = db['Production']
        self.customer_payments                = db["Customer_Payments"]
        self.supplier_payments                = db["Supplier_Payments"]
        self.general_exp_rev_collection       = db["general_exp_rev"]
        self.messages_collection              = db["Messages"]
        self.logs_collection                  = db["Logs"]

############################################ Windows ########################################### 


    # To use: add a button in your main menu or topbar.topbar to call self.open_chatbot()
    def main_menu(self):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create the top bar
        self.topbar.topbar(show_back_button=False)
        
        main_container = tk.Frame(self.root, bg=config.COLORS["background"])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Visualization frames
        left_viz_frame = self.Visualization.create_card_frame(main_container)
        left_viz_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Button frame
        button_frame = self.Visualization.create_card_frame(main_container, padding=20)
        button_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)
        
        right_viz_frame = self.Visualization.create_card_frame(main_container)    
        right_viz_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        
        # Configure grid weights
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=2)
        main_container.grid_columnconfigure(2, weight=1)
        main_container.grid_rowconfigure(0, weight=1)

        # Create visualizations
        self.Visualization.create_left_visualization(left_viz_frame)
        self.Visualization.create_right_visualization(right_viz_frame)
        if self.light:
            # Define buttons with images, text, and commands
            buttons = [
                {"text": self.AuxiliaryClass.t("Sales Invoice"), "image": "sales_invoice-dark.png",
                "command": lambda: self.SalesInvoice.manage_sales_invoices_window()},
                {"text": self.AuxiliaryClass.t("Purchase Invoice"), "image": "purchases_invoice-dark.png", 
                "command": lambda: self.PurchaseInvoice.manage_purchases_invoices_window()},
                {"text": self.AuxiliaryClass.t("Receive Payment"), "image": "customer_payment-dark.png", 
                "command": lambda: self.customer_interactions(self.user_role)},
                {"text": self.AuxiliaryClass.t("Make Payment"), "image": "supplier_payment-dark.png", 
                "command": lambda: self.supplier_interactions(self.user_role)},
                {"text": self.AuxiliaryClass.t("Production Order"), "image": "production-dark.png", 
                "command": lambda: self.ProductionOrder.new_production_order(self.user_role)},
                {"text": self.AuxiliaryClass.t("Employee interactions"), "image": "employee-dark.png", 
                "command": lambda: self.EmployeeWindow.manage_Employees_window()},
                {"text": self.AuxiliaryClass.t("Treasury"), "image": "treasury-dark.png", 
                "command": lambda: self.TreasuryWindow.Treasury_window(self.user_role)},
                {"text": self.AuxiliaryClass.t("General_Exp_And_Rev"), "image": "financial-dark.png", 
                "command": lambda: self.GeneralExpRev.general_exp_rev(self.user_role)},
                {"text": self.AuxiliaryClass.t("Reports"), "image": "report-dark.png", 
                "command": lambda: self.reports.manage_Reports_window()},
                {"text": self.AuxiliaryClass.t("Logs"), "image": "logs-dark.png", 
                "command": lambda: self.Logs_window()},
            ]
            
            if self.user_role == "admin" or self.user_role == "developer":
                buttons.extend([
                    {"text": self.AuxiliaryClass.t("Database"), "image": "database-dark.png", 
                    "command": lambda: self.manage_database_window()}
                ])
        elif not self.light:
            # Define buttons with images, text, and commands
            buttons = [
                {"text": self.AuxiliaryClass.t("Sales Invoice"), "image": "sales_invoice-light.png",
                "command": lambda: self.SalesInvoice.manage_sales_invoices_window()},
                {"text": self.AuxiliaryClass.t("Purchase Invoice"), "image": "purchases_invoice-light.png", 
                "command": lambda: self.PurchaseInvoice.manage_purchases_invoices_window()},
                {"text": self.AuxiliaryClass.t("Receive Payment"), "image": "customer_payment-light.png", 
                "command": lambda: self.customer_interactions(self.user_role)},
                {"text": self.AuxiliaryClass.t("Make Payment"), "image": "supplier_payment-light.png", 
                "command": lambda: self.supplier_interactions(self.user_role)},
                {"text": self.AuxiliaryClass.t("Production Order"), "image": "production-light.png", 
                "command": lambda: self.ProductionOrder.new_production_order(self.user_role)},
                {"text": self.AuxiliaryClass.t("Employee interactions"), "image": "employee-light.png", 
                "command": lambda: self.EmployeeWindow.manage_Employees_window()},
                {"text": self.AuxiliaryClass.t("Treasury"), "image": "treasury-light.png", 
                "command": lambda: self.TreasuryWindow.Treasury_window(self.user_role)},
                {"text": self.AuxiliaryClass.t("General_Exp_And_Rev"), "image": "financial-light.png", 
                "command": lambda: self.GeneralExpRev.general_exp_rev(self.user_role)},
                {"text": self.AuxiliaryClass.t("Reports"), "image": "report-light.png", 
                "command": lambda: self.reports.manage_Reports_window()},
                {"text": self.AuxiliaryClass.t("Logs"), "image": "logs-light.png", 
                "command": lambda: self.Logs_window()},
            ]

            if self.user_role == "admin" or self.user_role == "developer":
                buttons.extend([
                    {"text": self.AuxiliaryClass.t("Database"), "image": "database-light.png", 
                    "command": lambda: self.manage_database_window()}
                ])
        
        # Create button container with centered alignment
        button_container = tk.Frame(button_frame, bg=config.COLORS["card"])
        button_container.pack(fill=tk.BOTH, expand=True)  # Expand to fill available space
        
        # Create frame for the button grid (centered horizontally, aligned to top)
        grid_container = tk.Frame(button_container, bg=config.COLORS["card"])
        grid_container.pack(side="top", pady=20)  # Align to top with padding
        
        # Center the grid horizontally
        grid_container.grid_columnconfigure(0, weight=1)  # Left spacer
        grid_container.grid_columnconfigure(2, weight=1)  # Right spacer
        
        # Create a centered frame inside grid_container
        centered_frame = tk.Frame(grid_container, bg=config.COLORS["card"])
        centered_frame.grid(row=0, column=1)  # Center column
        
        # Load images and create buttons
        images = []  # Keep references to prevent garbage collection
        columns_per_row = 3  # Number of buttons per row
        button_size = 100
        
        try:
            for index, btn_info in enumerate(buttons):
                row = index // columns_per_row
                column = index % columns_per_row
                
                # Create frame for each button
                btn_frame = tk.Frame(centered_frame, bg=config.COLORS["card"])
                btn_frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
                
                # Load and process image
                img_path = os.path.join(BASE_DIR, "Static", "images", btn_info["image"])
                # ...existing code...
                img = Image.open(img_path).resize((button_size, button_size), Image.LANCZOS)
                
                # Change opacity (e.g., 0.5 for 50% opacity)
                opacity = 1
                if img.mode != "RGBA":
                    img = img.convert("RGBA")
                alpha = img.split()[3]
                alpha = alpha.point(lambda p: int(p * opacity))
                img.putalpha(alpha)
                
                photo_img = ImageTk.PhotoImage(img)
                # ...existing code...
                images.append(photo_img)  # Keep reference to prevent garbage collection
                
                # Create modern button
                btn = tk.Button(btn_frame,
                            image=photo_img,
                            text=btn_info["text"],
                            compound=tk.TOP,
                            bg=config.COLORS["card"],
                            fg=config.COLORS["text"],
                            activebackground=config.COLORS["highlight"],
                            font=("Arial", 15, "bold"),
                            borderwidth=0,
                            command=btn_info["command"])
                btn.image = photo_img  # Keep reference
                btn.pack(expand=True, fill=tk.BOTH)  # Make button expand to fill frame
                
                # Hover effect
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=config.COLORS["primary"]))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=config.COLORS["card"]))
                
        except Exception as e:
            print(f"Error loading images: {e}")
            # Fallback to text buttons if images fail
            text_frame = tk.Frame(centered_frame, bg=config.COLORS["card"])
            text_frame.grid(row=0, column=0, sticky="nsew")
            
            for i, btn_info in enumerate(buttons):
                row = i // columns_per_row
                column = i % columns_per_row
                
                btn = tk.Button(text_frame, 
                            text=btn_info["text"], 
                            command=btn_info["command"],
                            padx=10, pady=5,
                            bg=config.COLORS["card"],
                            fg=config.COLORS["text"],
                            activebackground=config.COLORS["highlight"],
                            font=("Segoe UI", 10))
                btn.grid(row=row, column=column, padx=5, pady=5)


        def start_drag(event):
            widget = event.widget
            # Store initial cursor position (window-relative)
            widget._drag_start_x = event.x_root - widget.winfo_rootx()
            widget._drag_start_y = event.y_root - widget.winfo_rooty()

        def do_drag(event):
            widget = event.widget
            if hasattr(widget, '_drag_start_x'):
                # Calculate new position in window coordinates
                new_x = event.x_root - widget._drag_start_x
                new_y = event.y_root - widget._drag_start_y
                
                # Convert to relative (0.0-1.0) coordinates
                relx = new_x / widget.winfo_toplevel().winfo_width()
                rely = new_y / widget.winfo_toplevel().winfo_height()
                
                # Constrain to window bounds
                relx = max(0.0, min(relx, 0.99))  # 1% margin
                rely = max(0.0, min(rely, 0.99))
                
                # Update position
                widget.place(relx=relx, rely=rely, anchor='nw')  # Anchor NW for smooth dragging

        def on_drag_end(event):
            self.groupchat.open_group_chat_window()


        # Remove previous chatbot icon if exists
        if hasattr(self, 'chatbot_main_btn') and self.chatbot_main_btn.winfo_exists():
            self.chatbot_main_btn.destroy()

        try:
            self.chatbot.create_chatbot_button()  # Add this where you build your menu


        except Exception as e:
            print(f"Error loading chatbot icon for main window: {e}")

        if hasattr(self, 'groupchat_main_btn') and self.groupchat_main_btn.winfo_exists():
            self.groupchat_main_btn.destroy()
        try:
            groupchat_icon_path = os.path.join(BASE_DIR, "Static", "images", "groupchat.ico")
            groupchat_img = Image.open(groupchat_icon_path).resize((60, 60), Image.LANCZOS)
            self.groupchat_main_photo = ImageTk.PhotoImage(groupchat_img)
            self.groupchat_main_btn = tk.Label(self.root, image=self.groupchat_main_photo, bg=config.COLORS["card"], cursor="hand2")
            self.groupchat_main_btn.place(relx=0.05, rely=0.97, anchor='sw')

            self.groupchat_main_btn.bind("<Button-1>", start_drag)
            self.groupchat_main_btn.bind("<B1-Motion>", do_drag)
            self.groupchat_main_btn.bind("<ButtonRelease-1>", on_drag_end)
            self.groupchat.update_groupchat_icon()

        except Exception as e:
            print(f"Error loading groupchat icon for main window: {e}")
        
     
        

    def manage_database_window(self):
                # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg=config.COLORS["background"])
        # Create the top bar
        self.topbar.topbar(show_back_button=True)

        # Main button frame
        button_frame = tk.Frame(self.root, bg=config.COLORS["background"])
        button_frame.pack(pady=30)

        # Define buttons with images, text, and commands
        if self.light:
            buttons = [
                {"text": self.AuxiliaryClass.t("Customers"), "image": "cus_db-dark.png", 
                "command": lambda: self.new_customer(self.user_role)},
                {"text": self.AuxiliaryClass.t("Suppliers"), "image": "supp_db-dark.png", 
                "command": lambda: self.new_supplier(self.user_role)},
                {"text": self.AuxiliaryClass.t("Employees"), "image": "emp_db-dark.png", 
                "command": lambda: self.new_employee(self.user_role)},
                {"text": self.AuxiliaryClass.t("Products"), "image": "prod_db-dark.png", 
                "command": lambda: self.new_products(self.user_role)},
                {"text": self.AuxiliaryClass.t("Materials"), "image": "mat_db-dark.png", 
                "command": lambda: self.new_material(self.user_role)},
                {"text": self.AuxiliaryClass.t("Employee Salary"), "image": "emp_salary_db-dark.png", 
                "command": lambda: self.new_emp_salary(self.user_role)},
                {"text": self.AuxiliaryClass.t("Employee Appointments"), "image": "emp_hour-dark.png", 
                "command": lambda: self.new_emp_appointment(self.user_role)},
                {"text": self.AuxiliaryClass.t("Employee Withdrawals"), "image": "emp_with-dark.png", 
                "command": lambda: self.new_emp_withdrawal(self.user_role)},
                {"text": self.AuxiliaryClass.t("General_Exp_And_Rev"), "image": "financial-dark.png", 
                "command": lambda: self.new_general_exp(self.user_role)}
            ]
        elif not self.light:
            buttons = [
                {"text": self.AuxiliaryClass.t("Customers"), "image": "cus_db-light.png", 
                "command": lambda: self.new_customer(self.user_role)},
                {"text": self.AuxiliaryClass.t("Suppliers"), "image": "supp_db-light.png", 
                "command": lambda: self.new_supplier(self.user_role)},
                {"text": self.AuxiliaryClass.t("Employees"), "image": "emp_db-light.png", 
                "command": lambda: self.new_employee(self.user_role)},
                {"text": self.AuxiliaryClass.t("Products"), "image": "prod_db-light.png", 
                "command": lambda: self.new_products(self.user_role)},
                {"text": self.AuxiliaryClass.t("Materials"), "image": "mat_db-light.png", 
                "command": lambda: self.new_material(self.user_role)},
                {"text": self.AuxiliaryClass.t("Employee Salary"), "image": "emp_salary_db-light.png", 
                "command": lambda: self.new_emp_salary(self.user_role)},
                {"text": self.AuxiliaryClass.t("Employee Appointments"), "image": "emp_hour-light.png", 
                "command": lambda: self.new_emp_appointment(self.user_role)},
                {"text": self.AuxiliaryClass.t("Employee Withdrawals"), "image": "emp_with-light.png", 
                "command": lambda: self.new_emp_withdrawal(self.user_role)},
                {"text": self.AuxiliaryClass.t("General_Exp_And_Rev"), "image": "financial-light.png", 
                "command": lambda: self.new_general_exp(self.user_role)}
            ]
        if self.user_role == "developer":
            if self.light:
                buttons.extend([
                    {"text": self.AuxiliaryClass.t("purchases"), "image": "purchases_invoice-dark.png", 
                    "command": lambda: self.new_purchases(self.user_role)},
                    {"text": self.AuxiliaryClass.t("sales"), "image": "sales_invoice-dark.png", 
                    "command": lambda: self.new_sales(self.user_role)},
                    {"text": self.AuxiliaryClass.t("Customer Payments"), "image": "customer_payment-dark.png", 
                    "command": lambda: self.new_customer_payment(self.user_role)},
                    {"text": self.AuxiliaryClass.t("Supplier Payments"), "image": "supplier_payment-dark.png", 
                    "command": lambda: self.new_supplier_payment(self.user_role)},
                    {"text": self.AuxiliaryClass.t("Produnction"), "image": "production-dark.png", 
                    "command": lambda: self.new_production(self.user_role)},

                ])
            elif not self.light:
                buttons.extend([
                    {"text": self.AuxiliaryClass.t("purchases"), "image": "purchases_invoice-light.png", 
                    "command": lambda: self.new_purchases(self.user_role)},
                    {"text": self.AuxiliaryClass.t("sales"), "image": "sales_invoice-light.png", 
                    "command": lambda: self.new_sales(self.user_role)},
                    {"text": self.AuxiliaryClass.t("Customer Payments"), "image": "customer_payment-light.png", 
                    "command": lambda: self.new_customer_payment(self.user_role)},
                    {"text": self.AuxiliaryClass.t("Supplier Payments"), "image": "supplier_payment-light.png", 
                    "command": lambda: self.new_supplier_payment(self.user_role)},
                    {"text": self.AuxiliaryClass.t("Produnction"), "image": "production-light.png", 
                    "command": lambda: self.new_production(self.user_role)},

                ])
        images = []  # Keep references to prevent garbage collection
        columns_per_row = 5  # Number of buttons per row
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

                # Text label
                # lbl = tk.Label(sub_frame, text=btn_info["text"], 
                #             font=("Arial", 15, "bold"), bg=config.COLORS["background"], fg="#003366")
                # lbl.pack(pady=5)

        except Exception as e:
            print(f"Error loading images: {e}")
            # Fallback to text buttons if images fail
            fallback_frame = tk.Frame(self.root, bg=config.COLORS["background"])
            fallback_frame.pack(pady=20)
            for btn_info in buttons:
                tk.Button(fallback_frame, text=btn_info["text"], 
                        command=btn_info["command"]).pack(side="left", padx=10)

    
    def Logs_window(self):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        self.topbar.topbar(show_back_button=True)

        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Filters section
        filter_frame = tk.Frame(main_frame)
        filter_frame.pack(fill=tk.X, pady=10)

        tk.Label(filter_frame, text=self.AuxiliaryClass.t("From Date:")).pack(side=tk.LEFT)
        from_date = DateEntry(filter_frame, date_pattern="dd/mm/yyyy")
        from_date.pack(side=tk.LEFT, padx=5)
        
        # self.end_date_entry = DateEntry(right_frame, font=("Arial", 12), date_pattern='dd-MM-yyyy', width=14)
        
        tk.Label(filter_frame, text=self.AuxiliaryClass.t("To Date:")).pack(side=tk.LEFT)
        to_date = DateEntry(filter_frame, date_pattern="dd/mm/yyyy")
        to_date.pack(side=tk.LEFT, padx=5)

        employees_names = self.employees_collection.find({}, {"Name": 1})
        names = [doc.get("Name", "") for doc in employees_names]
        
        tk.Label(filter_frame, text=self.AuxiliaryClass.t("Employee:")).pack(side=tk.LEFT)
        employee_var = tk.StringVar()
        employee_cb = ttk.Combobox(filter_frame, textvariable=employee_var, values= names)
        employee_cb.pack(side=tk.LEFT, padx=5)

        search_btn = tk.Button(filter_frame, text=self.AuxiliaryClass.t("Search"), command=lambda: self.load_logs(tree, from_date.get_date(), to_date.get_date(), employee_var.get()))
        search_btn.pack(side=tk.LEFT, padx=10)

        # Logs Table
        columns = ("date", "employee_name", "action")
        tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=self.AuxiliaryClass.t(col.replace("_", " ").title()))
            if col in ["date","employee_name"]:
                tree.column(col, width=100, anchor="center")
            else:
                tree.column(col, width=400, anchor="center")

        tree.pack(fill=tk.BOTH, expand=True, pady=10)
        self.load_logs(tree, from_date.get_date(), to_date.get_date(), None)
    
    def load_logs(self, tree, from_date, to_date, employee_name):
        query = {}
        
        if isinstance(from_date, date) and not isinstance(from_date, datetime):
            from_date = datetime.combine(from_date, datetime.min.time())
        if isinstance(to_date, date) and not isinstance(to_date, datetime):
            to_date = datetime.combine(to_date, datetime.max.time())

        if from_date and to_date:
            query["date"] = {"$gte": from_date, "$lte": to_date}
        if employee_name:
            query["employee_name"] = employee_name
        logs = self.logs_collection.find(query).sort("date", -1)
        tree.delete(*tree.get_children())
        for log in logs:
            tree.insert("", "end", values=(
                log.get("date", "").strftime("%Y-%m-%d %H:%M") if log.get("date") else "",
                log.get("employee_name", ""),
                log.get("action", "")
            ))
    


############################ Main Functions ########################################
    def new_employee(self, user_role):
        self.table_name.set("Employees")
        for widget in self.root.winfo_children():
            widget.destroy()
        # تحميل صورة الخلفية
        self.topbar.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.db_operations.display_general_table(self.employees_collection, "Employees")
    
    def new_supplier(self, user_role):
        self.table_name.set("Suppliers")
        for widget in self.root.winfo_children():
            widget.destroy()
        self.topbar.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.db_operations.display_general_table(self.suppliers_collection, "Suppliers")
    
    def new_customer(self, user_role):
        self.table_name.set("Customers")
        for widget in self.root.winfo_children():
            widget.destroy()

        self.topbar.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.db_operations.display_general_table(self.customers_collection, "Customers")

    def new_products(self, user_role):
        self.table_name.set("Products")
        for widget in self.root.winfo_children():
            widget.destroy()
    
        self.topbar.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.db_operations.display_general_table(self.products_collection, "Products")
    
    def new_material(self, user_role):
        self.table_name.set("Materials")
        for widget in self.root.winfo_children():
            widget.destroy()
    
        self.topbar.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.db_operations.display_general_table(self.materials_collection, "Materials")
    
    def new_sales(self,user_role):
        self.table_name.set("Sales")
        for widget in self.root.winfo_children():
            widget.destroy()

        self.topbar.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.db_operations.display_general_table(self.sales_collection, "Sales")

    def new_purchases(self,user_role):
        self.table_name.set("Purchases")
        for widget in self.root.winfo_children():
            widget.destroy()

        self.topbar.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.db_operations.display_general_table(self.purchases_collection, "Purchases")
    
    def new_customer_payment(self,user_role):
        self.table_name.set("Customer_Payments")
        for widget in self.root.winfo_children():
            widget.destroy()
    
        self.topbar.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.db_operations.display_general_table(self.customer_payments, "Customer_Payments")
    
    def new_supplier_payment(self,user_role):
        self.table_name.set("Supplier_Payments")
        for widget in self.root.winfo_children():
            widget.destroy()
    
        self.topbar.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.db_operations.display_general_table(self.supplier_payments, "Supplier_Payments")
    
    def new_emp_salary(self,user_role):
        self.table_name.set("Employee_Salary")
        for widget in self.root.winfo_children():
            widget.destroy()

        self.topbar.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.db_operations.display_general_table(self.employee_salary_collection, "Employee_Salary")
    
    def new_emp_appointment(self,user_role):
        self.table_name.set("Employee_appointimets")
        for widget in self.root.winfo_children():
            widget.destroy()
    
        self.topbar.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.db_operations.display_general_table(self.employees_appointments_collection, "Employee_appointimets")
    
    def new_emp_withdrawal(self,user_role):
        self.table_name.set("Employee_withdrawls")
        for widget in self.root.winfo_children():
            widget.destroy()
    
        self.topbar.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.db_operations.display_general_table(self.employee_withdrawls_collection, "Employee_withdrawls")
    
    def new_production(self,user_role):
        self.table_name.set("Production")
        for widget in self.root.winfo_children():
            widget.destroy()

        self.topbar.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.db_operations.display_general_table(self.production_collection, "Production")

    def new_general_exp(self,user_role):
        self.table_name.set("general_exp_rev")
        for widget in self.root.winfo_children():
            widget.destroy()

        self.topbar.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.db_operations.display_general_table(self.general_exp_rev_collection, "general_exp_rev")

    def supplier_interactions(self, user_role):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.topbar.topbar(show_back_button=True, Back_to_Database_Window=False)
        
        self.supplier_collection = config.get_collection_by_name("Suppliers")
        self.supplier_payment_collection = config.get_collection_by_name("Supplier_Payments")
        self.purchases_collection = config.get_collection_by_name("Purchases")

        supplier_codes = []
        supplier_names = []

        for supplier in self.supplier_collection.find({}, {"Name": 1, "Code": 1, "_id": 0}):
            supplier_codes.append(supplier.get("Code"))
            supplier_names.append(supplier.get("Name"))
        
        main_frame = tk.Frame(root, padx=20, pady=50)
        main_frame.pack(fill="both", expand=True)
        
        left_frame = tk.Frame(main_frame, width=330)
        left_frame.pack(side="left", fill="y")
        left_frame.pack_propagate(False)  # Prevent auto-resizing

        # Left half
        tk.Label(left_frame, text=self.AuxiliaryClass.t("Cash"), font=("Arial", 12)).pack(pady=10, anchor="w", padx=10)
        self.cash_entry = tk.Entry(left_frame, font=("Arial", 12))
        self.cash_entry.pack(pady=5, padx=10, fill="x")

        tk.Label(left_frame, text=self.AuxiliaryClass.t("Payment Method"), font=("Arial", 12)).pack(pady=10, anchor="w", padx=10)
        selected_method = tk.StringVar()
        self.payment_entry = ttk.Combobox(left_frame, textvariable=selected_method, 
                                        values=['Cash', 'E_Wallet', 'Bank_account', 'Instapay'], 
                                        state="readonly", width=18)
        self.payment_entry.pack(pady=5, padx=10, fill="x")
        self.payment_entry.set("Cash")  

        add_btn = tk.Button(left_frame, text=self.AuxiliaryClass.t("Add Entry"), width=35, 
                           command=lambda: self.add_supplier_payment(tree))
        add_btn.pack(pady=20, padx=10)

        # Right part (table)
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="left", fill="both", expand=True)

        # ==== Drop-down Section ====
        tk.Label(right_frame, text=self.AuxiliaryClass.t("Supplier Code")).grid(row=0, column=4)
        self.supplier_code_cb = ttk.Combobox(right_frame, values=supplier_codes)
        self.supplier_code_cb.grid(padx=(10,20), row=1, column=4)

        tk.Label(right_frame, text=self.AuxiliaryClass.t("Supplier Name")).grid(padx=(10,20), row=0, column=5)
        self.supplier_name_cb = ttk.Combobox(right_frame, values=supplier_names)
        self.supplier_name_cb.grid(padx=(10,20), row=1, column=5)

        # Bind combobox events with tree parameter
        self.supplier_code_cb.bind("<<ComboboxSelected>>", lambda event: self.on_code_selected(
                                      event, self.supplier_code_cb, self.supplier_name_cb, 
                                      self.supplier_collection, self.purchases_collection, self.supplier_payment_collection, 
                                      "supplier_info.code", tree))
                                      
        self.supplier_name_cb.bind("<<ComboboxSelected>>", lambda event: self.on_name_selected(
                                      event, self.supplier_code_cb, self.supplier_name_cb, 
                                      self.supplier_collection, self.purchases_collection, self.supplier_payment_collection, 
                                      "supplier_info.code", tree))

        tk.Label(right_frame, text=self.AuxiliaryClass.t("Start Date")).grid(padx=(10,20), row=0, column=7)
        self.start_date_entry = DateEntry(right_frame, font=("Arial", 12), date_pattern='dd-MM-yyyy', width=14)
        self.start_date_entry.grid(padx=(10,20), row=1, column=7)
        self.start_date_entry.set_date(date(2022, 1, 1))

        tk.Label(right_frame, text=self.AuxiliaryClass.t("End Date")).grid(padx=(10,20), row=0, column=8)
        self.end_date_entry = DateEntry(right_frame, font=("Arial", 12), date_pattern='dd-MM-yyyy', width=14)
        self.end_date_entry.grid(padx=(10,20), row=1, column=8)
        # self.end_date_entry.set_date(date(2025, 7, 7))
        self.end_date_entry.set_date(date.today())

        search_btn = tk.Button(
            right_frame,
            text=self.AuxiliaryClass.t("Search"),
            font=("Arial", 11),
            width=12,
            command=lambda: self.on_code_selected(
                None,
                self.supplier_code_cb,
                self.supplier_name_cb,
                self.supplier_collection,
                self.purchases_collection,
                self.supplier_payment_collection,
                "supplier_info.code",
                tree
            )
        )
        search_btn.grid(row=1, column=10, padx=(5, 0), pady=5)

        # ==== Table Section ====
        columns = ("date", "invoice_no", "debit", "credit", "Payment_method")
        tree_container = ttk.Frame(right_frame)
        tree_container.grid(row=3, column=3, columnspan=7, padx=10, pady=10, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_container, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Treeview
        tree = ttk.Treeview(tree_container, columns=columns, show="headings", height=8, 
                           yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)

        # Configure scrollbar
        scrollbar.config(command=tree.yview)

        for col in columns:
            tree.heading(col, text=self.AuxiliaryClass.t(col))
            # tree.heading(col, text=col.capitalize())
            tree.column(col, width=150)
            tree.column(col, anchor="center")  # This centers the content

        # ==== Footer Totals ====
        tk.Label(right_frame, text=self.AuxiliaryClass.t("Total Debit")).grid(row=13, column=3, sticky="e")
        self.total_debit_entry = tk.Entry(right_frame)
        self.total_debit_entry.grid(row=13, column=4, sticky="w")

        tk.Label(right_frame, text=self.AuxiliaryClass.t("Total Credit")).grid(row=13, column=5, sticky="e")
        self.total_credit_entry = tk.Entry(right_frame)
        self.total_credit_entry.grid(row=13, column=6, sticky="w")

        tk.Label(right_frame, text=self.AuxiliaryClass.t("Balance")).grid(row=13, column=7, sticky="e")
        self.balance_entry = tk.Entry(right_frame)
        self.balance_entry.grid(row=13, column=8, sticky="w")
        if self.language == "Arabic":
            headers = ["التاريخ", "الوصف", 'المدين', 'الدائن',  "طريقة الدفع"]
        else:
            headers = ["date", "description", 'debit', 'credit',  "payment_method"]
        # 1. Get the selected customer name from the Combobox
    
        # 2. Clean the name for use in filenames (remove special characters)
        def clean_filename(text):
            # Replace spaces and special characters
            return (text.replace(" ", "_")
                        .replace("/", "-")
                        .replace("\\", "-")
                        .replace(":", "-")
                        .replace("*", "")
                        .replace("?", "")
                        .replace('"', "")
                        .replace("<", "")
                        .replace(">", "")
                        .replace("|", "")
                        .strip())

        report_folder = "حسابات مفصلة للموردين"
        # Initial update with empty query
        self.update_totals(self.purchases_collection, self.supplier_payment_collection, tree=tree)
        tk.Button(right_frame,
                            text=self.AuxiliaryClass.t("Export to Excel"), 
                            command=lambda: self.AuxiliaryClass.export_to_excel(self.raw_tree_data,headers=headers,filename= f"كشف_حساب_للعميل_{clean_filename(self.report_customer_name)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                                                report_folder=report_folder,title=report_folder,
                                                                startdate=self.start_date_entry.get() if hasattr(self.start_date_entry, 'get') else str(self.start_date_entry),
                                                                enddate=self.end_date_entry.get() if hasattr(self.end_date_entry, 'get') else str(self.end_date_entry),
                                                                footerline_out_of_table=[
                                                                    f"إجمالي دائن: {str(self.total_credit_entry.get())}",
                                                                    f"إجمالي مدين: {str(self.total_debit_entry.get())}",
                                                                    f"الرصيد: {str(self.balance_entry.get())}"
                                                                ], source="Supplier Interaction"
                                                                 ),bg="#21F35D", fg='white').grid(row=13, column=9, sticky="w")

        # Create a variable to hold the selected page size
        self.page_size_var = tk.StringVar(value="A4")  # Default value

        # Create the OptionMenu (drop-down list)
        page_sizes = ["A1", "A2", "A3", "A4", "A5", "A6", "A7"]
        page_size_menu = tk.OptionMenu(right_frame, self.page_size_var, *page_sizes)
        page_size_menu.grid(row=13, column=11, sticky="w", padx=5)  # Placed before the button
        tk.Button(right_frame, 
                            text=self.AuxiliaryClass.t("Export to PDF and Print"),
                            command=lambda: self.AuxiliaryClass.export_to_pdf(self.raw_tree_data,headers=headers,filename= f"كشف_حساب_للعميل_{clean_filename(self.report_customer_name)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                                                report_folder=report_folder,title=report_folder,
                                                                startdate=self.start_date_entry.get() if hasattr(self.start_date_entry, 'get') else str(self.start_date_entry),
                                                                enddate=self.end_date_entry.get() if hasattr(self.end_date_entry, 'get') else str(self.end_date_entry),
                                                                footerline_out_of_table=[
                                                                    f"إجمالي دائن: {str(self.total_credit_entry.get())}",
                                                                    f"إجمالي مدين: {str(self.total_debit_entry.get())}",
                                                                    f"الرصيد: {str(self.balance_entry.get())}"
                                                                ], source="Supplier Interaction",page_size=config.PAGE_SIZES[self.page_size_var.get()]
                                                                ),bg="#2144F3", fg='white').grid(row=13, column=10, sticky="w", padx=10)
    def add_supplier_payment(self, tree):
        debit = self.cash_entry.get().strip()
        payment_method = self.payment_entry.get().strip()
        supplier_code = self.supplier_code_cb.get().strip()
        supplier_name = self.supplier_name_cb.get().strip()
        supplier_payment_collection = config.get_collection_by_name("Supplier_Payments")
        purchases_collection = config.get_collection_by_name("Purchases")
        
        if not debit or not payment_method or not supplier_code or not supplier_name:
            messagebox.showerror(self.AuxiliaryClass.t("Error"), self.AuxiliaryClass.t("All fields must be filled!"))
            return

        try:
            debit_val = float(debit)
        except ValueError:
            messagebox.showerror(self.AuxiliaryClass.t("Error"), self.AuxiliaryClass.t("Cash must be a valid number."))
            return

        operation_number = config.get_next_operation_number(supplier_payment_collection)
        current_time = datetime.now()

        doc = {
            "Operation_Number": operation_number,
            "Time": current_time,
            "Credit": 0.0,
            "Debit": debit_val,
            "Payment_method": payment_method,
            "supplier_info": {
                "code": supplier_code,
                "name": supplier_name
            }
        }
    
        formatted = current_time.strftime("%Y-%m-%d %H:%M")
        
        supplier_payment_collection.insert_one(doc)
        tree.insert("", tk.END, values=(formatted, operation_number, debit_val, 0.0, payment_method))

        # self.supplier_collection = config.get_collection_by_name("Suppliers")
        self.supplier_collection.update_one(
            {"Code": supplier_code},
            {
                "$inc": {
                    "Debit": debit_val,
                    "Balance": -debit_val
                }
            }
        )

        self.on_code_selected(
            event=None,
            code_cb=self.supplier_code_cb,
            name_cb=self.supplier_name_cb,
            collection=config.get_collection_by_name("Suppliers"),
            invoices_collection=purchases_collection,
            payment_collection=supplier_payment_collection,
            field_path="supplier_info.code",
            tree=tree
        )
        config.report_log(self.logs_collection, self.user_name, supplier_payment_collection, f"{self.AuxiliaryClass.t("Added new record to")}", doc, self.AuxiliaryClass.t)
        messagebox.showinfo(self.AuxiliaryClass.t("Success"), f"{self.AuxiliaryClass.t("Entry")} {operation_number} {self.AuxiliaryClass.t("added.")}")

    def add_customer_payment(self, tree):
        credit = self.cash_entry.get().strip()
        payment_method = self.payment_entry.get().strip()
        customer_code = self.customer_code_cb.get().strip()
        customer_name = self.customer_name_cb.get().strip()
        customer_payment_collection = config.get_collection_by_name("Customer_Payments")
        sales_collection = config.get_collection_by_name("Sales")
        
        if not credit or not payment_method or not customer_code or not customer_name:
            messagebox.showerror(self.AuxiliaryClass.t("Error"), self.AuxiliaryClass.t("All fields must be filled!"))
            return

        try:
            credit_val = float(credit)
        except ValueError:
            messagebox.showerror(self.AuxiliaryClass.t("Error"), self.AuxiliaryClass.t("Cash must be a valid number."))
            return

        operation_number = config.get_next_operation_number(customer_payment_collection)
        # current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
        current_time = datetime.now()

        doc = {
            "Operation_Number": operation_number,
            "Time": current_time,
            "Credit": credit_val,
            "Debit": 0.0,
            "Payment_method": payment_method,
            "Customer_info": {
                "code": customer_code,
                "name": customer_name
            }
        }
        
        formatted = current_time.strftime("%Y-%m-%d %H:%M")
        
        customer_payment_collection.insert_one(doc)
        tree.insert("", tk.END, values=(formatted, operation_number, 0.0, credit_val,payment_method))

        self.customer_collection.update_one(
            {"Code": customer_code},
            {
                "$inc": {
                    "Credit": credit_val,
                    "Balance": -credit_val
                }
            }
        )

        self.on_code_selected(
            event=None,
            code_cb=self.customer_code_cb,
            name_cb=self.customer_name_cb,
            collection=config.get_collection_by_name("Customers"),
            invoices_collection=sales_collection,
            payment_collection=customer_payment_collection,
            field_path="Customer_info.code",
            tree=tree
        )
        config.report_log(self.logs_collection, self.user_name, customer_payment_collection, f"{self.AuxiliaryClass.t("Added new record to")}", doc, self.AuxiliaryClass.t)
        messagebox.showinfo(self.AuxiliaryClass.t("Success"), f"{self.AuxiliaryClass.t("Entry")} {operation_number} {self.AuxiliaryClass.t("added.")}")
        #TODO Block of code to preview invoice to be generated + generate invoice as pdf

    def on_code_selected(self, event, code_cb, name_cb, collection, invoices_collection, payment_collection, field_path, tree):
        selected_code = code_cb.get().strip()
        
        start_date_raw = self.start_date_entry.get_date()  # These should be instance variables
        end_date_raw = self.end_date_entry.get_date()
        start_date = datetime.combine(start_date_raw, time.min)          # 00:00:00
        end_date = datetime.combine(end_date_raw, time.max)              # 23:59:59.999999
        payment_query = {}
        invoice_query = {}
        
        if not selected_code:
            # returns
            #time_query (it also compares dates but from payment db)
            payment_query =  {"Time": { "$gte": start_date,"$lte": end_date } } 
            #date_query
            invoice_query = {"Date": { "$gte": start_date, "$lte": end_date} }  
                
        else:
            try:
                person = collection.find_one({"Code": selected_code}, {"Name": 1, "_id": 0})
                if not person:
                    try:
                        # selected_code_int = int(selected_code)
                        # person = collection.find_one({"Code": selected_code_int}, {"Name": 1, "_id": 0})
                        
                        selected_code = int(selected_code)
                        person = collection.find_one({"Code": selected_code}, {"Name": 1, "_id": 0})
                        
                        ## selected_code = selected_code_int  # update for consistency in update_totals
                    except ValueError:
                        pass 

                if person:
                    name_cb.set(person["Name"])
                    self.report_customer_name = name_cb.get().strip()  # Store the selected name for later use
                    payment_query = { #time_query (it also compares dates but from payment db)
                        "$and": [
                            {field_path: selected_code},
                            {"Time": { "$gte": start_date,"$lte": end_date } }
                        ]
                    }

                    invoice_query = { #date_query
                        "$and": [
                            {field_path: selected_code},
                            {"Date": { "$gte": start_date, "$lte": end_date} }
                        ]
                    }

            except Exception as e:
                messagebox.showerror(self.AuxiliaryClass.t("Database Error"), f"{self.AuxiliaryClass.t("Failed to process code:")} {selected_code}.\n{self.AuxiliaryClass.t("Error")}: {str(e)}")
        self.update_totals(invoices_collection, payment_collection, payment_query, invoice_query, tree, selected_code)

    def on_name_selected(self, event, code_cb, name_cb, collection, invoices_collection, payment_collection, field_path, tree):
        selected_name = name_cb.get().strip()
        self.report_customer_name = selected_name  # Store the selected name for later use
        if not selected_name:
            return
        
        start_date_raw = self.start_date_entry.get_date()  # These should be instance variables
        end_date_raw = self.end_date_entry.get_date()
        
        start_date = datetime.combine(start_date_raw, time.min)          # 00:00:00
        end_date = datetime.combine(end_date_raw, time.max)              # 23:59:59.999999

        try:
            person = collection.find_one({"Name": selected_name}, {"Code": 1, "_id": 0})
            if person:
                code = person["Code"]
                code_cb.set(code)
                payment_query = { #time_query (it also compares dates but from payment db)
                    "$and": [
                        {field_path: code},
                        {"Time": { "$gte": start_date,"$lte": end_date } }
                    ]
                }

                invoice_query = { #date_query
                    "$and": [
                        {field_path: code},
                        {"Date": { "$gte": start_date,"$lte": end_date } }
                    ]
                }

                self.update_totals(invoices_collection, payment_collection, payment_query, invoice_query, tree, code)
            else:
                messagebox.showwarning(self.AuxiliaryClass.t("Warning"), f"{self.AuxiliaryClass.t("No matching code found for name:")} {selected_name}")
        except Exception as e:
            messagebox.showerror(self.AuxiliaryClass.t("Database Error"), f"{self.AuxiliaryClass.t("Failed to fetch code for")} {selected_name}.\n{self.AuxiliaryClass.t("Error")}: {str(e)}")

    def update_totals(self, invoices_collection, payment_collection, payment_query=None, invoice_query=None, tree=None, person_code=None, cust_supp=None):
        # cust_supp = 0 -> customer
        # cust_supp = 1 -> supplier

        if payment_query is None:
            payment_query = {}
        
        if invoice_query is None:
            invoice_query = {}

        invoices = invoices_collection.find(invoice_query)
        payments = payment_collection.find(payment_query)

        # invoice_count = invoices_collection.count_documents({ "supplier_info.code": "A00" })
        # payment_count = payment_collection.count_documents({ "supplier_info.code": "A00" })

        total_debit = 0.0
        total_credit = 0.0
        balance = 0.0
        sample_data = []

        if invoices_collection.name == "Purchases":
            for inv in invoices:
                financials = inv.get("Financials", {})
                total_debit += float(financials.get("Payed_cash", 0))
                total_credit += float(financials.get("Net_total", 0))
                
                # Add to sample_data for tree
                date = inv.get("Date", "")
                formatted = date.strftime("%Y-%m-%d %H:%M")
                invoice_no = inv.get("Receipt_Number", "")
                payment_method = financials.get("Payment_method", "Cash") #if it doesn't exist then by default = "Cash"
                sample_data.append((formatted, invoice_no, str(financials.get("Payed_cash", 0.0)), str(financials.get("Net_total", 0.0)), payment_method))
                
        else:
            for inv in invoices:
                financials = inv.get("Financials", {})
                total_debit += float(financials.get("Net_total", 0))
                total_credit += float(financials.get("Payed_cash", 0))
                
                # Add to sample_data for tree
                date = inv.get("Date", "")
                formatted = date.strftime("%Y-%m-%d %H:%M")
                invoice_no = inv.get("Receipt_Number", "")
                payment_method = financials.get("Payment_method", "Cash")
                sample_data.append((formatted, invoice_no, str(financials.get("Net_total", 0.0)), str(financials.get("Payed_cash", 0.0)), payment_method))
                
        for payment in payments:
            total_debit += float(payment.get("Debit", 0.0))
            total_credit += float(payment.get("Credit", 0.0))
            
            # Add to sample_data for tree
            date = payment.get("Time", "")
            formatted = date.strftime("%Y-%m-%d %H:%M")
            payment_no = payment.get("Operation_Number", "")
            payment_method = payment.get("Payment_method", "Cash")
            sample_data.append((formatted, payment_no, str(payment.get("Debit", 0.0)), str(payment.get("Credit", 0.0)), payment_method))
        
        if invoices_collection.name == "Purchases": #Case of Supplier/Purchases
            balance += float(total_credit - total_debit)
        else: #Case of Customer/Sales
            balance += float(total_debit - total_credit)

        if not invoice_query:
            # Insert calculated totals into entries (clear first)
            self.total_debit_entry.delete(0, tk.END)
            self.total_debit_entry.insert(0, str(total_debit))

            self.total_credit_entry.delete(0, tk.END)
            self.total_credit_entry.insert(0, str(total_credit))

            self.balance_entry.delete(0, tk.END)
            self.balance_entry.insert(0, str(balance))

            if tree:
                tree.delete(*tree.get_children())
                for row in sample_data:
                    tree.insert("", tk.END, values=row)
        else:
            #load total_debit/credit of the user selected
            if (payment_collection.name == "Customer_Payments"):
                doc = self.customer_collection.find_one({"Code": person_code}, {"Debit": 1, "Credit": 1, "Balance": 1})
            else:
                doc = self.supplier_collection.find_one({"Code": person_code}, {"Debit": 1, "Credit": 1, "Balance": 1})

            tree.delete(*tree.get_children())
            
            if not doc:
                if tree:
                    for row in sample_data:
                        tree.insert("", tk.END, values=row)
            
            else:
                doc_debit = doc.get("Debit", 0)
                doc_credit = doc.get("Credit", 0)
                doc_balance = doc.get("Balance", 0)

                self.total_debit_entry.delete(0, tk.END)
                self.total_debit_entry.insert(0, str(doc_debit))

                self.total_credit_entry.delete(0, tk.END)
                self.total_credit_entry.insert(0, str(doc_credit))

                self.balance_entry.delete(0, tk.END)
                self.balance_entry.insert(0, str(doc_balance))

                formatted = datetime.now().strftime("%Y-%m-%d %H:%M")
                new_credit =  doc_credit - total_credit
                new_debit = doc_debit - total_debit
                if new_credit > 0 or new_debit > 0:
                    # tree.insert("", tk.END, values=(formatted, "Other", new_debit, new_credit, "Cash"))
                    sample_data.insert(0, (formatted, "Other", str(new_debit), str(new_credit), "Cash"))
                
                if tree:
                    # tree.delete(*tree.get_children())
                    for row in sample_data:
                        tree.insert("", tk.END, values=row)
                    # Also store raw values for PDF export
        self.raw_tree_data = sample_data

    def customer_interactions(self, user_role):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.topbar.topbar(show_back_button=True,Back_to_Database_Window=False)
        
        self.customer_collection         = config.get_collection_by_name("Customers")
        self.customer_payment_collection = config.get_collection_by_name("Customer_Payments")
        self.sales_collection            = config.get_collection_by_name("Sales")

        customer_codes = []
        customer_names = []

        for customer in self.customer_collection.find({}, {"Name": 1, "Code": 1, "_id": 0}):
            customer_codes.append(customer.get("Code"))
            customer_names.append(customer.get("Name"))
        
        main_frame = tk.Frame(root ,padx=20, pady=50)
        main_frame.pack(fill="both", expand=True)
        
        left_frame = tk.Frame(main_frame, width=330)
        left_frame.pack(side="left", fill="y")
        left_frame.pack_propagate(False)  # Prevent auto-resizing

        # Left half
        tk.Label(left_frame, text=self.AuxiliaryClass.t("Cash"), font=("Arial", 12)).pack(pady=10, anchor="w", padx=10)
        self.cash_entry = tk.Entry(left_frame, font=("Arial", 12))
        self.cash_entry.pack(pady=5, padx=10, fill="x")

        tk.Label(left_frame, text=self.AuxiliaryClass.t("Payment Method"), font=("Arial", 12)).pack(pady=10, anchor="w", padx=10)
        selected_method = tk.StringVar()
        self.payment_entry = ttk.Combobox(left_frame, textvariable=selected_method, values=['Cash', 'E_Wallet', 'Bank_account', 'Instapay'], state="readonly", width=18)
        self.payment_entry.pack(pady=5, padx=10, fill="x")
        self.payment_entry.set(self.AuxiliaryClass.t("Cash"))  

        add_btn = tk.Button(left_frame, text=self.AuxiliaryClass.t("Add Entry"), width=35, 
                            command=lambda: self.add_customer_payment(tree))
        add_btn.pack(pady=20 , padx=10)

        #Right part (table)
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="left", fill="both", expand=True)

        # ==== Drop-down Section ====
        tk.Label(right_frame, text=self.AuxiliaryClass.t("Customer Code")).grid(padx=(10,20), row=0, column=4)
        self.customer_code_cb = ttk.Combobox(right_frame, values=customer_codes)
        self.customer_code_cb.grid(padx=(10,20), row=1, column=4)

        tk.Label(right_frame, text=self.AuxiliaryClass.t("Customer Name")).grid(padx=(10,20), row=0, column=5)
        self.customer_name_cb = ttk.Combobox(right_frame, values=customer_names)
        self.customer_name_cb.grid(padx=(10,20), row=1, column=5)

        self.customer_code_cb.bind("<<ComboboxSelected>>", lambda event: self.on_code_selected(
                                        event, self.customer_code_cb, self.customer_name_cb, 
                                        self.customer_collection, self.sales_collection, self.customer_payment_collection, 
                                        "Customer_info.code", tree))
        self.customer_name_cb.bind("<<ComboboxSelected>>", lambda event: self.on_name_selected(
                                        event, self.customer_code_cb, self.customer_name_cb, 
                                        self.customer_collection, self.sales_collection, self.customer_payment_collection, 
                                        "Customer_info.code", tree))
        
        tk.Label(right_frame, text=self.AuxiliaryClass.t("Start Date")).grid(padx=(10,20), row=0, column=7)
        self.start_date_entry = DateEntry(right_frame, font=("Arial", 12), date_pattern='dd-MM-yyyy', width=14)
        self.start_date_entry.grid(padx=(10,20), row=1, column=7)
        self.start_date_entry.set_date(date(2022, 1, 1))

        tk.Label(right_frame, text=self.AuxiliaryClass.t("End Date")).grid(padx=(10,20), row=0, column=8)
        self.end_date_entry = DateEntry(right_frame, font=("Arial", 12), date_pattern='dd-MM-yyyy', width=14)
        self.end_date_entry.grid(padx=(10,20), row=1, column=8)
        # self.end_date_entry.set_date(date(2025, 7, 7))
        self.end_date_entry.set_date(date.today())
        
        search_btn = tk.Button(
            right_frame,
            text=self.AuxiliaryClass.t("Search"),
            font=("Arial", 11),
            width=12,
            command=lambda: self.on_code_selected(
                None,
                self.customer_code_cb,
                self.customer_name_cb,
                self.customer_collection,
                self.sales_collection,
                self.customer_payment_collection,
                "Customer_info.code",
                tree
            )
        )
        search_btn.grid(row=1, column=10, padx=(5, 0), pady=5)

        # ==== Table Section ====
        columns = ("date", "invoice_no", "debit", "credit", "Payment_method")
        tree_container = ttk.Frame(right_frame)
        tree_container.grid(row=3, column=3, columnspan=7, padx=10, pady=10, sticky="nsew")

        # Scrollbar (attached to the right side of the tree)
        scrollbar = ttk.Scrollbar(tree_container, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Treeview
        tree = ttk.Treeview(tree_container, columns=self.AuxiliaryClass.t(columns), show="headings", height=8, yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)

        # Configure scrollbar to control tree
        scrollbar.config(command=tree.yview)
        
        for col in columns:
            tree.heading(col, text=self.AuxiliaryClass.t(col))
            # tree.heading(col, text=col.capitalize())
            tree.column(col, width=150)
            tree.column(col, anchor="center")  # This centers the content

        # ==== Footer Totals ====
        tk.Label(right_frame, text=self.AuxiliaryClass.t("Total Debit")).grid(row=13, column=3, sticky="e")
        self.total_debit_entry = tk.Entry(right_frame)
        self.total_debit_entry.grid(row=13, column=4, sticky="w")

        tk.Label(right_frame, text=self.AuxiliaryClass.t("Total Credit")).grid(row=13, column=5, sticky="e")
        self.total_credit_entry = tk.Entry(right_frame)
        self.total_credit_entry.grid(row=13, column=6, sticky="w")

        tk.Label(right_frame, text=self.AuxiliaryClass.t("Balance")).grid(row=13, column=7, sticky="e")
        self.balance_entry = tk.Entry(right_frame)
        self.balance_entry.grid(row=13, column=8, sticky="w")

        if self.language == "Arabic":
            headers = ["التاريخ", "الوصف", 'المدين', 'الدائن',  "طريقة الدفع"]
        else:
            headers = ["date", "description", 'debit', 'credit',  "payment_method"]
        # 1. Get the selected customer name from the Combobox
    
        # 2. Clean the name for use in filenames (remove special characters)
        def clean_filename(text):
            # Replace spaces and special characters
            return (text.replace(" ", "_")
                        .replace("/", "-")
                        .replace("\\", "-")
                        .replace(":", "-")
                        .replace("*", "")
                        .replace("?", "")
                        .replace('"', "")
                        .replace("<", "")
                        .replace(">", "")
                        .replace("|", "")
                        .strip())

        report_folder = "حسابات مفصلة للعملاء"
        # Initial update with empty query
        self.update_totals(self.sales_collection, self.customer_payment_collection, tree=tree)
        tk.Button(right_frame,
                            text=self.AuxiliaryClass.t("Export to Excel"), 
                            command=lambda: self.AuxiliaryClass.export_to_excel(self.raw_tree_data,headers=headers,filename= f"كشف_حساب_للعميل_{clean_filename(self.report_customer_name)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                                                report_folder=report_folder,title=report_folder,
                                                                startdate=self.start_date_entry.get() if hasattr(self.start_date_entry, 'get') else str(self.start_date_entry),
                                                                enddate=self.end_date_entry.get() if hasattr(self.end_date_entry, 'get') else str(self.end_date_entry),
                                                                footerline_out_of_table=[
                                                                    f"إجمالي دائن: {str(self.total_credit_entry.get())}",
                                                                    f"إجمالي مدين: {str(self.total_debit_entry.get())}",
                                                                    f"الرصيد: {str(self.balance_entry.get())}"
                                                                ], source="Customer Interaction"
                                                                 ),bg="#21F35D", fg='white').grid(row=13, column=9, sticky="w")
        # Create a variable to hold the selected page size
        self.page_size_var = tk.StringVar(value="A4")  # Default value

        # Create the OptionMenu (drop-down list)
        page_sizes = ["A1", "A2", "A3", "A4", "A5", "A6", "A7"]
        page_size_menu = tk.OptionMenu(right_frame, self.page_size_var, *page_sizes)
        page_size_menu.grid(row=13, column=11, sticky="w", padx=5)  # Placed before the button
        tk.Button(right_frame, 
                            text=self.AuxiliaryClass.t("Export to PDF and Print"),
                            command=lambda: self.AuxiliaryClass.export_to_pdf(self.raw_tree_data,headers=headers,filename= f"كشف_حساب_للعميل_{clean_filename(self.report_customer_name)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                                                report_folder=report_folder,title=report_folder,
                                                                startdate=self.start_date_entry.get() if hasattr(self.start_date_entry, 'get') else str(self.start_date_entry),
                                                                enddate=self.end_date_entry.get() if hasattr(self.end_date_entry, 'get') else str(self.end_date_entry),
                                                                footerline_out_of_table=[
                                                                    f"إجمالي دائن: {str(self.total_credit_entry.get())}",
                                                                    f"إجمالي مدين: {str(self.total_debit_entry.get())}",
                                                                    f"الرصيد: {str(self.balance_entry.get())}"
                                                                ], source="Customer Interaction",page_size=config.PAGE_SIZES[self.page_size_var.get()]
                                                                ),bg="#2144F3", fg='white').grid(row=13, column=10, sticky="w", padx=10)


############################ Utility Functions ########################################





    def handle_logout(self):
        if self.user_id:
            self.employees_collection.update_one(
                {"_id": self.user_id},
                {"$set": {
                    "logged_in": False,
                    "last_number_of_msgs": self.last_number_of_msgs
                }})
        config.report_log(self.logs_collection, self.user_name, None, f"{self.user_name} {self.AuxiliaryClass.t("logout from the application")}", None)
        self.login_window.open_login_window()

    def on_app_exit(self):
        if self.user_id:
            self.employees_collection.update_one(
                {"_id": self.user_id},
                {"$set": {
                    "logged_in": False,
                    "last_number_of_msgs": self.last_number_of_msgs
                }})
        config.report_log(self.logs_collection, self.user_name, None, f"{self.user_name} {self.AuxiliaryClass.t("Exit the application")}", None)
        self.root.quit()


##################################################################### Main #########################################################

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesSystemApp(root)       # Create main app first
    app.start_without_login()
    app.start_with_login()     # Then launch the login screen through app
    try:
        root.mainloop()
    except Exception as e:
        print("Error during mainloop:", e)