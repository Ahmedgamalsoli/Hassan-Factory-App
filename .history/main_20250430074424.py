import tkinter as tk
from tkinter import filedialog, ttk, messagebox,Tk, Label, PhotoImage,simpledialog
from PIL import Image, ImageTk, ImageDraw  # Import Pillow classes
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from fpdf import FPDF
import sqlite3
import csv
import os
from tkcalendar import DateEntry  # Import DateEntry
import sys
from io import BytesIO
from playsound import playsound
import threading  # To play sound without freezing the GUI

from pymongo import MongoClient
import cloudinary
import cloudinary.uploader
from cloudinary.uploader import upload
from urllib.parse import quote_plus
from bson.objectid import ObjectId

######################################################### Access Data Base ##############################################################################

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
        self.old = None
        self.root.title("مصنع حسن سليم للمنتجات البلاستيكية")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="white")
        
        self.Connect_DB()
                    
        self.stop_event = threading.Event()

        self.language = "Arabic"  # default language
        self.translations = {
            "Add New Product": {"Arabic": "امر انتاج", "English": "Production order"},
            # "Place Orders": {"Arabic": "تنفيذ الطلبات", "English": "Place Orders"},
            # "Expenses": {"Arabic": "المصاريف", "English": "Expenses"},
            # "Returns": {"Arabic": "المرتجعات", "English": "Returns"},
            # "Employees Appointments": {"Arabic": "مواعيد الموظفين", "English": "Employees Appointments"},
            # "Daily Shifts": {"Arabic": "الورديات اليومية", "English": "Daily Shifts"},
            # "View Product": {"Arabic": "عرض المنتجات", "English": "View Product"},
            # "View Orders": {"Arabic": "عرض الطلبات", "English": "View Orders"},
            # "View Customers": {"Arabic": "عرض العملاء", "English": "View Customers"},
            # "Edit Product": {"Arabic": "تعديل المنتج", "English": "Edit Product"},
            # "Accounting": {"Arabic": "الحسابات", "English": "Accounting"},
            "Reports": {"Arabic": "التقارير", "English": "Reports"},
            "Production Order": {"Arabic": "أمر انتاج", "English": "Production Order"},
            "Database": {"Arabic": "قاعدة البيانات", "English": "Database"},
            "Change Language": {"Arabic": "تغيير اللغة", "English": "Change Language"},
            "New Sales Invoice": {"Arabic": "فاتورة مبيعات جديدة", "English": "New Sales Invoice"},
            "New Purchase Invoice": {"Arabic": "فاتورة مشتريات جديدة", "English": "New Purchase Invoice"},
            "Receive Payment": {"Arabic": "استلام دفعة", "English": "Receive Payment"},
            "Make Payment": {"Arabic": "دفع دفعة", "English": "Make Payment"},
            "Customers": {"Arabic": "العملاء", "English": "Customers"},
            "Suppliers": {"Arabic": "الموردين", "English": "Suppliers"},
            "Products": {"Arabic": "المنتجات", "English": "Products"},
            "Materials": {"Arabic": "الخامات", "English": "Materials"},
            # "Reports": {"Arabic": "التقارير", "English": "Reports"},
            "Employees": {"Arabic": "الموظفين", "English": "Employees"},
        }
        self.db = None
        self.db_name = tk.StringVar()
        self.table_name = tk.StringVar()
        self.search_query = tk.StringVar()
        self.user_photo_path = ""  # Initialize with None or a default image path
        self.user_photo = ""
        self.user_name = ""  # Placeholder for dynamic user name
        self.user_role = ""  # Placeholder for user role
        self.all_customers = None  # Will be loaded on first search
        self._after_id = None
        self.logout_icon_path = os.path.join(BASE_DIR, "Static", "images", "Logout.png")  # Path to logout icon
        self.exit_icon_path   = os.path.join(BASE_DIR, "Static", "images", "Exit.png")  # Path to exit icon
        self.back_icon_path   = os.path.join(BASE_DIR, "Static", "images", "Back.png")  # Path to back icon
        
        # Get the correct path for the icon
        # if hasattr(sys, "_MEIPASS"):
        #     icon_path = os.path.abspath(os.path.join(sys._MEIPASS, "app_icon.ico"))
        # else:
        #     icon_path = os.path.abspath("app_icon.ico")  # For running as a script
        
        # Set the icon
        # self.root.iconbitmap(icon_path)
        # List to track selected products
        self.selected_products = []   

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
        try:
            client.admin.command('ping')
            print("✅ Connected to MongoDB")
        except Exception as e:
            print("❌ MongoDB connection failed:", e)

        db = client["Hassan"]   

        self.customers_collection             = db['Customers']
        self.employees_collection             = db['Employees']
        self.products_collection              = db['Products']
        self.sales_collection                 = db['Sales']
        self.suppliers_collection             = db['Suppliers']
        self.shipping_collection              = db['Shipping']
        self.orders_collection                = db['Orders']
        self.expenses_collection              = db['Expenses']
        self.employee_appointments_collection = db['Employee_appointments']
        self.daily_shifts_collection          = db['Daily_shifts']
        self.accounts_collection              = db['Accounts']
        self.transactions_collection          = db['Transactions']
        self.big_deals_collection             = db['Big_deals']
        self.TEX_Calculations_collection      = db['TEX_Calculations']

############################################ Windows ########################################### 
    
    def open_login_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Load and set the background image
        image_path = os.path.join(BASE_DIR, "Static", "images", "Login.png")  # Path to your JPG image
        bg_image = Image.open(image_path)
        self.bg_photo = ImageTk.PhotoImage(bg_image)  # Convert to a format Tkinter can use
        bg_label = tk.Label(self.root, image=self.bg_photo)
        bg_label.place(relwidth=1, relheight=1)  # Cover the entire window
        
        # Login Frame
        login_frame = tk.Frame(self.root, bg="white", bd=2, relief="ridge")
        login_frame.place(relx=0.515, rely=0.5, anchor="center", width=400, height=350)

        # Load Circular Logo
        logo_path = os.path.join(BASE_DIR, "Static", "images", "Logo.jpg")  # Change this to your logo path
        self.logo_image = self.create_circular_image(logo_path)
        if self.logo_image:
            logo_label = tk.Label(login_frame, image=self.logo_image, bg="white")
            logo_label.place(x=150, y=10)

        # Title
        title = tk.Label(login_frame, text="Login", font=("Arial", 18, "bold"), bg="white")
        title.place(x=150, y=120)

        # Username
        username_label = tk.Label(login_frame, text="Username:", font=("Arial", 12), bg="white")
        username_label.place(x=50, y=160)
        username_entry = tk.Entry(login_frame, font=("Arial", 12), bg="#f0f0f0")
        username_entry.place(x=150, y=160, width=200)

        # Password
        password_label = tk.Label(login_frame, text="Password:", font=("Arial", 12), bg="white")
        password_label.place(x=50, y=190)
        password_entry = tk.Entry(login_frame, font=("Arial", 12), bg="#f0f0f0", show="*")
        password_entry.place(x=150, y=190, width=200)

        username_entry.bind("<Return>", lambda event: validate_login()) # Bind Enter key to trigger add_todo from name_entry
        password_entry.bind("<Return>", lambda event: validate_login()) # Bind Enter key to trigger add_todo from name_entry
        
        # Login Button
        def validate_login():
            username = username_entry.get()  # Assuming `username_entry` is the input field for the username
            password = password_entry.get()  # Assuming `password_entry` is the input field for the password
            self.user_name = username
            # Validate input
            if not username or not password:
                self.silent_popup("Error", f"Both fields are required.",self.play_Error)
                return

            try:
                user = self.employees_collection.find_one({"Name": username, "Password": password})
                # print(user)
                if user:
                    self.user_role = user.get("Role", "Unknown")
                    # messagebox.showinfo("Success", f"Login successful! Role: {self.user_role}")
                    self.silent_popup("Success", f"Login successful! Role: {self.user_role}",self.play_success)
                    open_main_menu(self.user_role)
                else:
                    self.silent_popup("Error", "Invalid username or password.", self.play_Error)

            except Exception as e:
                self.silent_popup("Database Error", f"An error occurred: {e}", self.play_Error)


        login_button = tk.Button(login_frame, text="Login", font=("Arial", 12), bg="lightblue", command=validate_login)
        login_button.place(x=150, y=270, width=100)

        # Exit Button
        exit_button = tk.Button(login_frame, text="Exit", font=("Arial", 12), bg="lightgray", command=self.root.quit)
        exit_button.place(x=270, y=270, width=80)
        def open_main_menu(role):
            if role:
                self.main_menu()
            else:
                self.silent_popup("Unknown role", "Access denied.", self.play_Error)

    def main_menu(self):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create the top bar
        self.topbar(show_back_button=False)

        # Main button frame
        button_frame = tk.Frame(self.root, bg="white")
        button_frame.pack(pady=30)

        # Define buttons with images, text, and commands
        buttons = [
            {"text": self.t("New Sales Invoice"), "image": "Sales.png", 
            "command": lambda: self.new_sales_invoice(self.user_role)},
            {"text": self.t("New Purchase Invoice"), "image": "Purchase.png", 
            "command": lambda: self.trash(self.user_role)},
            {"text": self.t("Receive Payment"), "image": "Recieve.png", 
            "command": lambda: self.trash(self.user_role)},
            {"text": self.t("Make Payment"), "image": "payment.png", 
            "command": lambda: self.trash(self.user_role)},
            {"text": self.t("Production Order"), "image": "Production Order.png", 
            "command": lambda: self.trash(self.user_role)},
            {"text": self.t("Customers"), "image": "customers.png", 
            "command": lambda: self.trash(self.user_role)},
            {"text": self.t("Suppliers"), "image": "suppliers.png", 
            "command": lambda: self.trash(self.user_role)},
            {"text": self.t("Employees"), "image": "Employees.png", 
            "command": lambda: self.trash(self.user_role)},
            {"text": self.t("Products"), "image": "Products.png", 
            "command": lambda: self.trash(self.user_role)},
            {"text": self.t("Materials"), "image": "Materials.png", 
            "command": lambda: self.trash(self.user_role)},
            {"text": self.t("Reports"), "image": "Reports.png", 
            "command": lambda: self.trash(self.user_role)},
        ]

        # if self.user_role == "employee":
        #     buttons.extend([
        #         {"text": self.t("View Product"), "image": "Exit.png", 
        #         "command": lambda: self.trash(self.user_role)},
        #         {"text": self.t("View Orders"), "image": "Exit.png", 
        #         "command": lambda: self.trash(self.user_role)},
        #         {"text": self.t("View Customers"), "image": "Exit.png", 
        #         "command": lambda: self.trash(self.user_role)}
        #     ])

        if self.user_role == "admin":
            # buttons.insert(1, {"text": self.t("Edit Product"), "image": "Exit.png", 
            #                 "command": lambda: self.trash(self.user_role)})
            buttons.extend([
            #     {"text": self.t("Accounting"), "image": "Exit.png", 
            #     "command": lambda: self.Accounting_Window()},
            #     {"text": self.t("Reports"), "image": "Exit.png", 
            #     "command": lambda: self.trash(self.user_role)},
            #     {"text": self.t("Big Deals"), "image": "Exit.png", 
            #     "command": lambda: self.trash(self.user_role)},
                {"text": self.t("Database"), "image": "database.png", 
                "command": lambda: self.check_access_and_open(self.user_role, 
                                                            db_name="clothes_sales.db", 
                                                            table_name="Employees")}
            ])

        # Load images and create buttons
        images = []  # Keep references to prevent garbage collection
        columns_per_row = 4  # Number of buttons per row

        try:
            for index, btn_info in enumerate(buttons):
                # Load and resize image
                img_path = os.path.join(BASE_DIR, "Static", "images", btn_info["image"])
                img = Image.open(img_path).resize((70, 70), Image.LANCZOS)
                photo_img = ImageTk.PhotoImage(img)
                images.append(photo_img)

                # Calculate grid position
                row = index // columns_per_row
                column = index % columns_per_row

                # Create sub-frame for each button
                sub_frame = tk.Frame(button_frame, bg="white")
                sub_frame.grid(row=row, column=column, padx=20, pady=20)

                # Image button
                btn = tk.Button(sub_frame, image=photo_img, bd=0, 
                            command=btn_info["command"])
                btn.image = photo_img  # Keep reference
                btn.pack()

                # Text label
                lbl = tk.Label(sub_frame, text=btn_info["text"], 
                            font=("Arial", 15, "bold"), bg="white", fg="#003366")
                lbl.pack(pady=5)

        except Exception as e:
            print(f"Error loading images: {e}")
            # Fallback to text buttons if images fail
            fallback_frame = tk.Frame(self.root, bg="white")
            fallback_frame.pack(pady=20)
            for btn_info in buttons:
                tk.Button(fallback_frame, text=btn_info["text"], 
                        command=btn_info["command"]).pack(side="left", padx=10)

    def manage_database_window(self, db_name=None, table_name=None):
        # self.db_name.set(db_name if db_name else "")
        self.table_name.set(table_name if table_name else "")

        for widget in self.root.winfo_children():
            widget.destroy()

        # تحميل صورة الخلفية
        self.topbar(show_back_button=True)

        tk.Label(self.root, text="Select Table:", bg="#4a90e2", fg="white", font=("Arial", 12)).place(x=130, y=110)
        table_dropdown = ttk.Combobox(self.root, textvariable=self.table_name, values=["Employees", "Products", "Sales", "Customers","Suppliers","Shipping","Orders","Expenses","Employee_appointments","Daily_shifts","Accounts","Transactions","Big_deals","TEX_Calculations"])
        table_dropdown.place(x=250, y=110)
        table_dropdown.bind("<<ComboboxSelected>>", lambda e: self.display_table())

        tk.Label(self.root, text="Search:", bg="#4a90e2", fg="white", font=("Arial", 12)).place(x=140, y=150)
        search_entry = tk.Entry(self.root, textvariable=self.search_query)
        search_entry.place(x=250, y=150)
        tk.Button(self.root, text="Search", command=self.display_table).place(x=410, y=145)

        self.tree = ttk.Treeview(self.root, show="headings")
        self.tree.place(x=0, y=190)

        # # Create scrollbars inside frame
        # self.tree_xscroll = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        # self.tree_yscroll = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)

        # # Attach scrollbars to tree
        # self.tree.configure(xscrollcommand=self.tree_xscroll.set, yscrollcommand=self.tree_yscroll.set)

        # # Place them manually
        # self.tree.place(x=0, y=0, width=780, height=230)  # little smaller so scrollbars fit
        # self.tree_xscroll.place(x=0, y=230, width=780, height=20)
        # self.tree_yscroll.place(x=780, y=0, width=20, height=230)


        tk.Button(self.root, text="Add Record", command=self.add_entry).place(width=120, height=40, x=100, y=450)
        tk.Button(self.root, text="Edit Record", command=self.edit_entry).place(width=120, height=40, x=250, y=450)
        tk.Button(self.root, text="Delete Record", command=self.delete_entry).place(width=120, height=40, x=400, y=450)

        self.display_table()

    def new_sales_invoice(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Initialize product mappings
        self.product_map = {}
        self.name_to_code = {}
        
        # Create top bar
        self.topbar(show_back_button=True)

        # MongoDB collections
        customers_col = self.get_collection_by_name("Customers")
        sales_col = self.get_collection_by_name("Sales")
        products_col = self.get_collection_by_name("Products")

        # Main form frame
        form_frame = tk.Frame(self.root, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Customer Selection Frame
        customer_frame = tk.Frame(form_frame, bd=1, relief=tk.SOLID, padx=5, pady=5)
        customer_frame.grid(row=0, column=0, columnspan=2, sticky='w', pady=5)

        # إضافة حقل المبلغ المدفوع
        tk.Label(customer_frame, text="المبلغ المدفوع:", font=("Arial", 12, "bold")).grid(row=0, column=2, sticky='e', padx=(20, 0))
        self.payed_cash_var = tk.DoubleVar()
        self.payed_cash_entry = tk.Entry(customer_frame, textvariable=self.payed_cash_var, width=15)
        self.payed_cash_entry.grid(row=0, column=3, sticky='e')

        # Customer Combobox with search
        tk.Label(customer_frame, text="Customer:", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky='w')
        self.customer_var = tk.StringVar()
        self.customer_cb = ttk.Combobox(customer_frame, textvariable=self.customer_var)
        self.customer_cb.grid(row=0, column=1, sticky='ew', padx=(5, 0))
        # تعديل توزيع الأعمدة
        customer_frame.columnconfigure(1, weight=1)
        customer_frame.columnconfigure(3, weight=0)
        
        # Populate and configure customers
        all_customers = [cust['Name'] for cust in customers_col.find()]
        self.customer_cb['values'] = all_customers
        self.customer_cb.bind('<KeyRelease>', 
                            lambda e: self.filter_combobox(e, all_customers, self.customer_cb))

        # Load product data with improved unit handling
        try:
            products = list(products_col.find())
            all_units = set()
            product_names = []
            product_codes = []

            for p in products:
                code = str(p.get('product_code', '')).strip().lower()
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

                # Handle price conversion with error checking
                try:
                    # Remove non-numeric characters from price
                    price_str = str(p.get('Unit_Price', '0')).strip('kgm ')
                    price = float(price_str) if price_str else 0.0
                except ValueError:
                    price = 0.0

                # Update mappings
                self.product_map[code] = {
                    'name': name,
                    'units': unit_names,
                    'price': price
                }
                self.name_to_code[name] = code
                product_names.append(name)
                product_codes.append(code)

            # Create unique sorted lists
            self.product_codes = sorted(list(set(product_codes)))  # Store as instance variable
            self.product_names = sorted(list(set(product_names)))  # Store as instance variable
            all_units = sorted(list(all_units))
                # Populate customers with code mapping
            self.customer_code_map = {}  # Add this as a class member
            all_customers = []
            for cust in customers_col.find():
                self.customer_code_map[cust['Name']] = cust.get('Customer_code', '')
                all_customers.append(cust['Name'])
            
            self.customer_cb['values'] = sorted(all_customers)

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load products: {str(e)}")
            return

        # Invoice Items Grid
        columns = self.get_fields_by_name("Sales_Header")
        col_width = 29

        # Header Row
        header_row = tk.Frame(form_frame, bg='#f0f0f0')
        header_row.grid(row=2, column=0, columnspan=len(columns), sticky='nsew', pady=(20, 0))
        for col_idx, col in enumerate(columns):
            tk.Label(header_row, text=col, width=col_width, relief='ridge',
                    bg='#f0f0f0', anchor='w').grid(row=0, column=col_idx, sticky='ew')
            header_row.columnconfigure(col_idx, weight=1)

        # Scrollable Canvas
        canvas = tk.Canvas(form_frame, highlightthickness=0)
        scrollbar = tk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        self.rows_frame = tk.Frame(canvas)
        
        # Canvas configuration
        self.rows_frame.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.rows_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=3, column=0, columnspan=len(columns), sticky="nsew")
        scrollbar.grid(row=3, column=len(columns), sticky="ns")
        
        # Configure grid weights
        form_frame.grid_rowconfigure(3, weight=1)
        for i in range(len(columns)):
            form_frame.columnconfigure(i, weight=1)

        self.entries = []

        # Modified create_row function with enhanced clearing
        def create_row(parent, row_number, bg_color):
            row_frame = tk.Frame(parent, bg=bg_color)
            row_frame.grid(row=row_number, column=0, sticky='ew')
            
            row_entries = []
            for col_idx, col in enumerate(columns):
                if col == "Product_code":
                    var = tk.StringVar()
                    cb = ttk.Combobox(row_frame, textvariable=var, values=product_codes, width=col_width-2)
                    cb.bind('<<ComboboxSelected>>', lambda e, r=row_number: self.update_product_info(r, "code"))
                    cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_combobox_change(e, r, "code"))
                    cb.grid(row=0, column=col_idx, sticky='ew')
                    row_entries.append(cb)
                elif col == "product_name":
                    var = tk.StringVar()
                    cb = ttk.Combobox(row_frame, textvariable=var, values=product_names, width=col_width-2)
                    cb.bind('<<ComboboxSelected>>', lambda e, r=row_number: self.update_product_info(r, "name"))
                    cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_combobox_change(e, r, "name"))
                    cb.grid(row=0, column=col_idx, sticky='ew')
                    row_entries.append(cb)
                elif col == "unit":
                    var = tk.StringVar()
                    cb = ttk.Combobox(row_frame, textvariable=var, values=[], width=col_width-2)
                    cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_unit_change(e, r))
                    cb.grid(row=0, column=col_idx, sticky='ew')
                    row_entries.append(cb)
                elif col in ["Unit_Price", "Total_QTY", "Total_Price"]:
                    entry = tk.Entry(row_frame, width=col_width+1, relief='flat', state='readonly')
                    entry.grid(row=0, column=col_idx, sticky='ew')
                    row_entries.append(entry)
                else:
                    entry = tk.Entry(row_frame, width=col_width+1, relief='sunken')
                    entry.bind('<KeyRelease>', lambda e, r=row_number: self.calculate_totals(r))
                    entry.grid(row=0, column=col_idx, sticky='ew')
                    row_entries.append(entry)
                
                row_frame.columnconfigure(col_idx, weight=1)
            
            return row_entries

        def add_three_rows():
            current_row_count = len(self.entries)
            for i in range(3):
                bg_color = 'white' if (current_row_count + i) % 2 == 0 else '#f0f0f0'
                row_entries = create_row(self.rows_frame, current_row_count + i, bg_color)
                self.entries.append(row_entries)

        # Initial rows
        add_three_rows()
        

        # Buttons Frame
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=len(columns), pady=10, sticky='ew')
        
        tk.Button(button_frame, text="➕ Add 3 More Rows", command=add_three_rows,
                bg='#4CAF50', fg='white').grid(row=0, column=0, padx=5, sticky='w')
        tk.Button(button_frame, text="💾 Save Invoice", 
                command=lambda: self.save_invoice(sales_col, customers_col,products_col),
                bg='#2196F3', fg='white').grid(row=0, column=1, padx=5, sticky='e')
        
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

    def handle_combobox_change(self, event, row_idx, field_type):
        """Handle changes in product code/name comboboxes"""
        value = event.widget.get().strip()
        
        # Clear dependent fields if value is empty
        if not value:
            self.clear_row_fields(row_idx)
            return
            
        # Filter combobox values
        if field_type == "code":
            full_list = self.product_codes  # Access instance variable
        else:
            full_list = self.product_names  # Access instance variable
            
        filtered = [item for item in full_list if value.lower() in str(item).lower()]
        event.widget['values'] = filtered
        
        # Auto-update if exact match found
        if value in full_list:
            self.update_product_info(row_idx, field_type)

    def handle_unit_change(self, event, row_idx):
        """Handle unit changes and clear price if unit changes"""
        unit = event.widget.get().strip()
        if not unit:
            self.entries[row_idx][6].config(state='normal')
            self.entries[row_idx][6].delete(0, tk.END)
            self.entries[row_idx][6].config(state='readonly')
            self.calculate_totals(row_idx)

    def clear_row_fields(self, row_idx):
        """Clear all dependent fields in a row"""
        # Clear product name
        self.entries[row_idx][1].set('')
        # Clear unit combobox
        self.entries[row_idx][2].set('')
        self.entries[row_idx][2]['values'] = []
        # Clear price fields
        self.entries[row_idx][6].config(state='normal')
        self.entries[row_idx][6].delete(0, tk.END)
        self.entries[row_idx][6].config(state='readonly')
        # Clear quantity fields
        self.entries[row_idx][3].delete(0, tk.END)
        self.entries[row_idx][4].delete(0, tk.END)
        # Clear calculated fields
        self.entries[row_idx][5].config(state='normal')
        self.entries[row_idx][5].delete(0, tk.END)
        self.entries[row_idx][5].config(state='readonly')
        self.entries[row_idx][7].config(state='normal')
        self.entries[row_idx][7].delete(0, tk.END)
        self.entries[row_idx][7].config(state='readonly')
    # Modified update_product_info
    def update_product_info(self, row_idx, source):
        """Update fields based on code or name selection"""
        try:
            if source == "code":
                product_code = self.entries[row_idx][0].get().strip().lower()
                product_info = self.product_map.get(product_code, {})
                product_name = product_info.get('name', '')
            else:
                product_name = self.entries[row_idx][1].get().strip()
                product_code = self.name_to_code.get(product_name, '')
                product_info = self.product_map.get(product_code, {})

            # Clear fields if no product found
            if not product_code:
                self.clear_row_fields(row_idx)
                return

            # Update both dropdowns
            self.entries[row_idx][0].set(product_code)
            self.entries[row_idx][1].set(product_name)
            
            # Update unit combobox values
            unit_combobox = self.entries[row_idx][2]
            unit_combobox['values'] = product_info.get('units', [])
            if product_info.get('units'):
                unit_combobox.current(0)
            
            # Update Unit Price
            self.entries[row_idx][6].config(state='normal')
            self.entries[row_idx][6].delete(0, tk.END)
            self.entries[row_idx][6].insert(0, f"{product_info.get('price', 0):.2f}")
            self.entries[row_idx][6].config(state='readonly')
            
            self.calculate_totals(row_idx)
        except Exception as e:
            print(f"Error updating product info: {str(e)}")

    def calculate_totals(self, row_idx):
        try:
            # Get quantity values with default to 0 if empty
            qty = float(self.entries[row_idx][3].get() or 0)
            numbering = float(self.entries[row_idx][4].get() or 0)
            unit_price = float(self.entries[row_idx][6].get() or 0)
            
            total_qty = qty * numbering
            total_price = unit_price * total_qty
            
            # Update Total QTY
            self.entries[row_idx][5].config(state='normal')
            self.entries[row_idx][5].delete(0, tk.END)
            self.entries[row_idx][5].insert(0, f"{total_qty:.2f}")
            self.entries[row_idx][5].config(state='readonly')
            
            # Update Total Price
            self.entries[row_idx][7].config(state='normal')
            self.entries[row_idx][7].delete(0, tk.END)
            self.entries[row_idx][7].insert(0, f"{total_price:.2f}")
            self.entries[row_idx][7].config(state='readonly')
        except ValueError:
            # Clear fields if invalid input
            self.entries[row_idx][5].config(state='normal')
            self.entries[row_idx][5].delete(0, tk.END)
            self.entries[row_idx][5].config(state='readonly')
            
            self.entries[row_idx][7].config(state='normal')
            self.entries[row_idx][7].delete(0, tk.END)
            self.entries[row_idx][7].config(state='readonly')

############################ Main Functions ########################################
    def display_table(self):
        collection_name = self.table_name.get()
        search_query = self.search_query.get()
        
        current_collection = self.get_collection_by_name(collection_name)
        
        # self.tree = ttk.Treeview(root)
        # scrollbar = ttk.Scrollbar(root, orient="horizontal", command=self.tree.xview)
        # self.tree.configure(yscrollcommand=scrollbar.set)

        for row in self.tree.get_children():
            self.tree.delete(row)
        
        try:
            # Fetch all documents
            if search_query:
                # Create a dynamic query based on the search term
                first_document = current_collection.find_one()
                if first_document:
                    search_fields = list(first_document.keys())
                    # Remove '_id' as we usually don't search by it directly
                    if '_id' in search_fields:
                        search_fields.remove('_id')
                    or_conditions = [{"$expr": {"$regexMatch": {"input": {"$toString": f"${field}"}, "regex": search_query, "options": "i"}}} for field in search_fields]
                    data = list(current_collection.find({"$or": or_conditions}))
                else:
                    data = [] # No documents to search in
            else:
                data = list(current_collection.find())

            if data:
                columns = self.get_fields_by_name(collection_name)
                if '_id' in columns:
                    columns.remove('_id')
                    columns.insert(0, self.t("ID")) # ROW ID

                self.tree["columns"] = columns
                for col in columns:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=152, anchor="center", stretch=False)

                for row_data in data:
                    values = []
                    record_id = row_data.get('_id', '')
                    values.append(str(record_id)) # Display ObjectId as string
                    for col in columns[1:]: # Start from the second column as the first is 'ID'
                        values.append(row_data.get(col, ''))
                    self.tree.insert("", "end", values=values)
            else:
                # Show placeholder column and row
                self.tree["columns"] = ("No Data",)
                self.tree.heading("No Data", text="No Data Available")
                self.tree.column("No Data", width=300, anchor="center", stretch=True)
                self.tree.insert("", "end", values=("This collection has no documents.",))
                return

        except Exception as e:
            messagebox.showerror("Error", f"Error displaying data: {e}")

    def add_entry(self):
        collection_name = self.table_name.get()

        current_collection = self.get_collection_by_name(collection_name)

        new_entry = {}
        fields = self.get_fields_by_name(collection_name)

        for field in fields:
            dialog = AlwaysOnTopInputDialog(root, f"Enter value for {field}:")
            value = dialog.get_result()
            if value is None:
                return            
            new_entry[field] = value


        try:
            current_collection.insert_one(new_entry)
            self.display_table()
            messagebox.showinfo("Success", "Record added successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding record: {e}")

    def edit_entry(self):
        collection_name = self.table_name.get()

        current_collection = self.get_collection_by_name(collection_name)

        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to edit")
            return

        record_id_str  = self.tree.item(selected_item)['values'][0]
        try:
            record_id = ObjectId(record_id_str)
        except Exception:
            messagebox.showerror("Error", "Invalid ID format.")
            return
        
        # Get the fields to edit (excluding _id)
        first_document = current_collection.find_one({"_id": record_id})
        if not first_document:
            messagebox.showerror("Error", "Could not retrieve record for editing.")
            return

        fields = self.get_fields_by_name(collection_name)
        updated_values = {}

        for field in fields:
            dialog = AlwaysOnTopInputDialog(root, f"Enter value for {field}:")
            value = dialog.get_result()
            if value is None:
                return            
            updated_values[field] = value

        try:
            current_collection.update_one({"_id": record_id}, {"$set": updated_values})
            self.display_table()
            messagebox.showinfo("Success", "Record updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating record: {e}")

    def delete_entry(self):
        collection_name = self.table_name.get()

        current_collection = self.get_collection_by_name(collection_name)

        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to delete")
            return

        record_id_str = self.tree.item(selected_item)['values'][0]
        try:
            record_id = ObjectId(record_id_str)
        except Exception:
            messagebox.showerror("Error", "Invalid ID format.")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            try:
                current_collection.delete_one({"_id": record_id})
                self.display_table()
                messagebox.showinfo("Success", "Record deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting record: {e}")

############################ Utility Functions ########################################
    def check_access_and_open(self, role, db_name, table_name):
        allowed_roles = ["admin"]  # Define roles that can access this
        if role in allowed_roles:
            self.manage_database_window(db_name, table_name)
        else:
            messagebox.showwarning("Access Denied", "You do not have permission to access this page.")

    def get_collection_by_name(self, collection_name):
        """Returns the appropriate MongoDB collection object based on the provided name.
        Args: collection_name (str): The name of the collection to access (e.g., "Employees", "Products").
        Returns: pymongo.collection.Collection or None: The corresponding MongoDB collection object,
                                                   or None if the name is not recognized."""
        if collection_name == "Employees":
            return self.employees_collection
        elif collection_name == "Products":
            return self.products_collection
        elif collection_name == "Sales":
            return self.sales_collection
        elif collection_name == "Customers":
            return self.customers_collection
        elif collection_name == "Suppliers":
            return self.suppliers_collection
        elif collection_name == "Shipping":
            return self.shipping_collection
        elif collection_name == "Orders":
            return self.orders_collection
        elif collection_name == "Expenses":
            return self.expenses_collection
        elif collection_name == "Employee_appointments":
            return self.employee_appointments_collection
        elif collection_name == "Daily_shifts":
            return self.daily_shifts_collection
        elif collection_name == "Accounts":
            return self.accounts_collection
        elif collection_name == "Transactions":
            return self.transactions_collection
        elif collection_name == "Big_deals":
            return self.big_deals_collection
        elif collection_name == "TEX_Calculations":
            return self.TEX_Calculations_collection
        else:
            print(f"Warning: Collection name '{collection_name}' not recognized.")
            return None

    def get_fields_by_name(self, collection_name):
        """Returns the appropriate fields array based on the provided collection name.
        Args: collection_name (str): The name of the collection (e.g., "Employees", "Products").
        Returns: list: A list of field names for the corresponding collection, or an empty list if the name is not recognized.
        """
        if collection_name == "Employees":#DONE
            return ["Name", "Password", "Id", "Role", "Join_Date", "National_id_pic", "Phone_number", "Address", "Salary"]
        
        elif collection_name == "Products":
            return ["product_name", "category", "price", "stock_quantity", "supplier"]
        
        elif collection_name == "Sales":
            return ["product_code", "Product_name", "unit", "QTY", "numbering","Total_QTY","Unit_Price","Total Price","Date","Reciept_Number","Customer_name","Customer_code"]

        elif collection_name == "Sales_Header":
            return ["Product_code", "product_name", "unit", "QTY", "numbering","Total_QTY","Unit_Price","Total_Price"]
       
        elif collection_name == "Customers":
            return ["Name", "Phone_number1", "Phone_number2", "Code", "Purchase_mgr_number", "Financial_mgr_number", "Purchase_mgr_name", 
                    "Financial_mgr_name", "Email", "Company_address", "Extra_address", "Maps_link", "Bank_account",
                    "Instapay", "E_wallet", "Accountant_name", "Accountant_number", "Sales_grade", "Growth_grade", "Frequency_grade", "Credit",
                    "Debit"]
        
        elif collection_name == "Suppliers":
            return ["Name", "Phone_number1", "Phone_number2", "Code", "Purchase_mgr_number", "Financial_mgr_number", "Purchase_mgr_name", 
                    "Financial_mgr_name", "Email", "Company_address", "Extra_address", "Maps_link", "Bank_account",
                    "Instapay", "E_wallet", "Accountant_name", "Accountant_number", "Sales_grade", "Growth_grade", "Frequency_grade", "Credit",
                    "Debit" ]
        
        elif collection_name == "Shipping":
            return ["order_id", "shipping_date", "tracking_number", "shipping_address"]
        
        elif collection_name == "Orders":
            return ["order_id", "order_date", "customer_id", "total_amount", "status"]
        
        elif collection_name == "Expenses":
            return ["expense_id", "expense_type", "amount", "date", "description"]
        
        elif collection_name == "Employee_appointments":
            return ["appointment_id", "employee_id", "appointment_date", "appointment_type"]
        
        elif collection_name == "Daily_shifts":
            return ["shift_id", "employee_id", "shift_date", "start_time", "end_time"]
        
        elif collection_name == "Accounts":
            return ["account_id", "account_name", "balance", "account_type"]
        
        elif collection_name == "Transactions":
            return ["transaction_id", "account_id", "transaction_date", "amount", "transaction_type"]
        
        elif collection_name == "Big_deals":
            return ["deal_id", "deal_date", "customer_id", "product_id", "deal_value"]
        
        elif collection_name == "TEX_Calculations":
            return ["calculation_id", "product_id", "calculation_date", "value"]
        
        else:
            print(f"Warning: Collection name '{collection_name}' not recognized.")
            return []

    def update_search(self, event, collection):
        # Cancel any previous scheduled search **only if valid**
        if hasattr(self, '_after_id') and self._after_id is not None:
            try:
                self.root.after_cancel(self._after_id)
            except ValueError:
                pass  # Ignore if it was already canceled
        
        # Mark that user is typing
        self.is_typing = True
        
        # Schedule the search with the current text
        self._after_id = self.root.after(300, self.perform_search, collection)

    def perform_search(self, collection):
        # Mark that user is not typing anymore
        self.is_typing = False

        search_term = self.customer_var.get()

        # If search term is empty, you can clear the combobox
        if search_term == "":
            self.customer_cb['values'] = []
            return

        # Perform search
        filtered_customers = [cust['Name'] for cust in collection.find(
            {"Name": {"$regex": f"^{search_term}", "$options": "i"}}
        )]
        
        # Update combobox values only if user is not typing
        if not self.is_typing:
            self.customer_cb['values'] = filtered_customers
            
            if filtered_customers:
                self.customer_cb.event_generate('<Down>')
            else:
                self.customer_cb.event_generate('<Up>')  # Close dropdown
    
    def generate_invoice_number(self):
        """توليد رقم فاتورة تسلسلي (أرقام فقط)"""
        try:
            sales_col = self.get_collection_by_name('Sales')
            
            # 1. البحث عن آخر فاتورة مع فرز صحيح
            last_invoice = sales_col.find_one(
                {"Reciept_Number": {"$exists": True}},
                sort=[("Reciept_Number", -1)]
            )
            
            # 2. معالجة حالة عدم وجود فواتير سابقة
            last_number = 0
            if last_invoice:
                receipt_number = last_invoice.get("Reciept_Number", 0)
                
                # 3. تحويل التنسيقات القديمة (INV-xxxx)
                if isinstance(receipt_number, str) and receipt_number.startswith("INV-"):
                    try:
                        last_number = int(receipt_number.split("-")[-1])
                    except (ValueError, IndexError):
                        last_number = 0
                
                # 4. معالجة الأرقام كنصوص أو أعداد صحيحة
                elif isinstance(receipt_number, (int, str)):
                    try:
                        last_number = int(receipt_number)
                    except ValueError:
                        last_number = 0
            
            # 5. توليد الرقم الجديد
            new_number = last_number + 1
            return str(new_number)
    
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل توليد الرقم التسلسلي: {str(e)}")

    def save_invoice(self, sales_col, customers_col, products_col):
        """حفظ الفاتورة مع التحقق من المخزون وتحديثه"""
        try:
            # جمع بيانات العميل
            customer_name = self.customer_var.get().strip()
            if not customer_name:
                messagebox.showerror("خطأ", "يرجى اختيار عميل")
                return

            # البحث عن العميل مع التحقق من وجوده
            customer = customers_col.find_one({
                "Name": {"$regex": f"^{customer_name.strip()}$", "$options": "i"}
            })
            if not customer:
                messagebox.showerror("خطأ", "العميل غير مسجل!")
                return
            if "_id" not in customer:
                messagebox.showerror("خطأ", "بيانات العميل تالفة!")
                return
             # استخراج المبلغ المدفوع
            payed_cash = self.payed_cash_var.get() if self.payed_cash_var.get() else 0.0

            # التحقق من صحة القيمة
            if payed_cash < 0:
                messagebox.showerror("خطأ", "المبلغ المدفوع لا يمكن أن يكون سالبًا!")
                return
            # جمع بيانات العناصر والتحقق من المخزون
            items = []
            total_amount = 0.0
            stock_updates = {}  # لتخزين تحديثات المخزون
            
            for row_idx, row in enumerate(self.entries):
                product_code = row[0].get().strip()
                product_name = row[1].get().strip()
                unit = row[2].get().strip()
                
                if not (product_code or product_name or unit):
                    continue

                try:
                    # استخراج القيم الرقمية
                    qty = float(row[3].get() or 0)
                    numbering = float(row[4].get() or 0)
                    unit_price = float(row[6].get() or 0)
                    total_qty = qty * numbering
                    total_price = total_qty * unit_price
                    
                    # البحث عن المنتج في المخزون
                    product = products_col.find_one({"product_code": product_code})
                    if not product:
                        messagebox.showerror("خطأ", f"المنتج {product_code} غير موجود!")
                        return
                    
                    # التحقق من توفر الكمية
                    stock = product.get("stock_quantity", 0)
                    if total_qty > stock:
                        messagebox.showerror(
                            "نقص في المخزون", 
                            f"الكمية المطلوبة ({total_qty}) تتجاوز المخزون ({stock}) للمنتج {product_code}"
                        )
                        return
                    
                    # تخزين تحديثات المخزون
                    stock_updates[product_code] = stock - total_qty
                    
                    # إضافة العنصر للفاتورة
                    items.append({
                        "Product_code": product_code,
                        "product_name": product_name,
                        "Unit": unit,
                        "QTY": qty,
                        "numbering": numbering,
                        "Total_QTY": total_qty,
                        "Unit_price": unit_price,
                        "Total_price": total_price
                    })
                    total_amount += total_price
                    
                except ValueError as e:
                    messagebox.showerror("خطأ", f"قيم غير صالحة في الصف {row_idx+1}: {str(e)}")
                    return

            if not items:
                messagebox.showerror("خطأ", "لا توجد عناصر في الفاتورة!")
                return

            # توليد رقم الفاتورة
            invoice_number = self.generate_invoice_number()
            if not invoice_number:
                return

            # إنشاء وثيقة الفاتورة
            invoice_data = {
                "Reciept_Number": invoice_number,
                "Date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Customer_code": customer.get("Customer_code", "CUST-001"),
                "Customer_name": customer.get("Name", "غير معروف"),
                "Customer_phone1": customer.get("Phone_number1", ""),
                "Customer_phone2": customer.get("Phone_number2", ""),
                "Customer_address": customer.get("Company_address", ""),
                "Items": items,
                "Net_total": total_amount,
                "Balance":customer.get("Balance",""),
                "Payed_cash": self.payed_cash_var.get() if self.payed_cash_var.get() else 0.0,
                # "Grand_total": total_amount,
                # "Status": "معلقة",
                "PDF_Path": ""
            }

            # توليد PDF
            pdf_path = self.generate_pdf(invoice_data)
            if not pdf_path:
                return
            
            invoice_data["PDF_Path"] = pdf_path

            # تحديث المخزون
            for code, new_stock in stock_updates.items():
                products_col.update_one(
                    {"product_code": code},
                    {"$set": {"stock_quantity": new_stock}}
                )

            # حفظ الفاتورة
            sales_col.insert_one(invoice_data)
            customers_col.update_one(
                {"_id": customer["_id"]},
                {
                    "$set": {"Last_purchase": datetime.now()},
                    "$inc": {
                        "Sales": 1,
                        "Debit": total_amount,    # إضافة الدين
                        "Balance": (total_amount - payed_cash),   # إضافة الرصيد
                        "Credit": payed_cash
                    }
                }
            )

            messagebox.showinfo("نجاح", f"تم الحفظ بنجاح\nرقم الفاتورة: {invoice_number}")
            self.clear_invoice_form()

        except Exception as e:
            messagebox.showerror("خطأ فادح", f"فشل في العملية: {str(e)}")


    def clear_invoice_form(self):
            """تنظيف جميع حقول الفاتورة"""
            try:
                # تنظيف Combobox العميل
                self.customer_var.set('')
                
                # تنظيف حقول العناصر
                for row in self.entries:
                    for entry in row:
                        if isinstance(entry, ttk.Combobox):
                            entry.set('')
                        elif isinstance(entry, tk.Entry):
                            entry.delete(0, tk.END)
                
                # إعادة تعيين القائمة
                self.entries = []
                # إعادة إنشاء الصفوف الأساسية
                # إذا كنت تستخدم دالة لإضافة الصفوف
                self.new_sales_invoice(self.user_role)
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل في تنظيف الحقول: {str(e)}")
                
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

            # تسجيل الخط العربي
            arabic_font_path = os.path.join("Static", "Fonts", "Amiri-Regular.ttf")
            if not os.path.exists(arabic_font_path):
                raise FileNotFoundError(f"ملف الخط غير موجود: {arabic_font_path}")
            pdfmetrics.registerFont(TTFont('Arabic', arabic_font_path))

            # دالة معالجة النصوص العربية
            def format_arabic(text):
                reshaped_text = arabic_reshaper.reshape(str(text))
                return get_display(reshaped_text)

            # إنشاء مسار الحفظ
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            file_name = f"فاتورة_{invoice_data['Reciept_Number']}.pdf"
            pdf_path = os.path.join(desktop, file_name)

            # إعداد مستند PDF
            c = canvas.Canvas(pdf_path, pagesize=A5)
            width, height = A5
            print("width")
            print(width)
            c.setFont("Arabic", 14)

            # معلومات الشركة (الجزء العلوي)
            company_info = [
                f"فاتورة بيع رقم {invoice_data['Reciept_Number']}",
                "مصنع حسن سليم للمنتجات البلاستيكية",
                f"التاريخ: {invoice_data['Date']}",
                "رقم السجل: 6300"
            ]
            y_position = height - 2*cm
            for line in company_info:
                c.drawRightString(width - 2*cm, y_position, format_arabic(line))
                y_position -= 0.7*cm

            # معلومات العميل (الجزء الأوسط)
            customer_y = y_position - 1.5*cm
            c.setFont("Arabic", 12)
            customer_fields = [
                ("اسم العميل:", invoice_data['Customer_name']),
                ("الكود:", invoice_data['Customer_code']),
                ("العنوان:", invoice_data['Customer_address']),
                ("الهاتف:", invoice_data['Customer_phone1'])
            ]
            for field, value in customer_fields:
                text = f"{format_arabic(field)} {format_arabic(value)}"
                c.drawString(2*cm, customer_y, text)
                customer_y -= 0.7*cm

            # جدول العناصر
            headers = [
                "كود الصنف",
                "العدد",
                "الوحدة",
                "السعر",
                "الكمية",
                "الإجمالي"
            ]
            col_positions = [
                width - 2*cm,
                width - 4.5*cm,
                width - 7*cm,
                width - 9.5*cm,
                width - 12*cm,
                width - 15*cm
            ]
            
            # رسم رأس الجدول
            table_y = customer_y - 1.5*cm
            c.setFont("Arabic", 12)
            for i, header in enumerate(headers):
                c.drawRightString(col_positions[i], table_y, format_arabic(header))

            # بيانات الجدول
            c.setFont("Arabic", 10)
            row_height = 0.7*cm
            for item in invoice_data["Items"]:
                table_y -= row_height
                columns = [
                    item.get("Product_code", ""),
                    str(item.get("numbering", "")),
                    item.get("Unit", ""),
                    f"{item.get('Unit_price', 0):.2f}",
                    str(item.get('QTY', 0)),
                    f"{item.get('Total_price', 0):.2f}"
                ]
                for i, value in enumerate(columns):
                    c.drawRightString(col_positions[i], table_y, format_arabic(value))

            # الإجماليات
            totals_y = table_y - 2*cm
            totals = [
                ("صافي الفاتورة:", invoice_data['Net_total']),
                ("المبلغ المدفوع:", invoice_data.get('Payed_cash', 0)),
                ("الباقي:", invoice_data['Net_total'] - invoice_data.get('Payed_cash', 0))
            ]
            
            c.setFont("Arabic", 12)
            for label, value in totals:
                text = f"{format_arabic(label)} {format_arabic(f'{value:,.2f}')}"
                c.drawRightString(width - 2*cm, totals_y, text)
                totals_y -= 0.7*cm

            # التوقيعات
            c.setFont("Arabic", 10)
            c.drawRightString(width - 2*cm, 2*cm, format_arabic("ختم وتوقيع المدير: __________"))
            c.drawString(2*cm, 2*cm, format_arabic("الاستلام: __________"))

            c.save()
            return pdf_path

        except Exception as e:
            messagebox.showerror("خطأ PDF", f"فشل في توليد الملف: {str(e)}")
            return None
        
    def on_canvas_press(self, event):
        self.tree.scan_mark(event.x, event.y)

    def on_canvas_drag(self, event):
        self.tree.scan_dragto(event.x, event.y, gain=1)

    # Update scroll region dynamically
    def update_scroll_region(self, event=None):
        self.tree.configure(scrollregion=self.tree.bbox("all"))

    # Function to Create Circular Image
    def create_circular_image(self, image_path, size=(100, 100)):  
        """Creates a circular version of an image"""
        if not os.path.exists(image_path):
            return None  # Return None if the image doesn't exist

        img = Image.open(image_path).resize(size, Image.LANCZOS)  
        mask = Image.new("L", size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        
        circular_img = Image.new("RGBA", size)
        circular_img.paste(img, (0, 0), mask)
        return ImageTk.PhotoImage(circular_img)

    # To get the text button based on language
    def t(self, text):
        return self.translations.get(text, {}).get(self.language, text)
    
    # Function tot oggle from Arabic to English and Vicaverse
    def toggle_language(self):
        self.language = "English" if self.language == "Arabic" else "Arabic"
        self.main_menu()

    #Function to update the time 
    def update_time(self, time_label):
        time_label.config(text=datetime.now().strftime('%B %d, %Y %I:%M %p'))
        self.root.after(1000, self.update_time, time_label)


    # Function to make the top bar part
    def topbar(self, show_back_button=False):
        # Top Bar
        top_bar = tk.Frame(self.root, bg="#dbb40f", height=60)
        top_bar.pack(fill="x")
        # Exit icon
        try:
            exit_image = Image.open(self.exit_icon_path)
            exit_image = exit_image.resize((35, 35), Image.LANCZOS)
            self.exit_photo = ImageTk.PhotoImage(exit_image)
            exit_icon = tk.Label(top_bar, image=self.exit_photo, bg="#dbb40f")
            exit_icon.pack(side="right", padx=10)
            exit_icon.bind("<Button-1>", lambda e: self.root.quit())
        except Exception as e:
            self.silent_popup("Error", "Error loading exit icon: {e}", self.play_Error)

        # Logout icon
        try:
            logout_image = Image.open(self.logout_icon_path)
            logout_image = logout_image.resize((40, 40), Image.LANCZOS)
            self.logout_photo = ImageTk.PhotoImage(logout_image)
            logout_icon = tk.Button(top_bar, image=self.logout_photo, bg="#dbb40f", bd=0, command=self.open_login_window)
            logout_icon.pack(side="right", padx=10)
        except Exception as e:
            self.silent_popup("Error", "Error loading Logout icon: {e}", self.play_Error)

        # Left side: Language or Back button
        if show_back_button:
            try:
                back_image = Image.open(self.back_icon_path)
                back_image = back_image.resize((40, 40), Image.LANCZOS)
                self.back_photo = ImageTk.PhotoImage(back_image)
                back_icon = tk.Button(top_bar, image=self.back_photo, bg="#dbb40f", bd=0, command=self.main_menu)
                back_icon.pack(side="left", padx=10)
            except Exception as e:
                self.silent_popup("Error", "Error loading back icon: {e}", self.play_Error)
        else:
            lang_btn = tk.Button(top_bar, text=self.t("Change Language"), bg="#dbb40f", fg="black",
                                font=("Arial", 10, "bold"), bd=0, command=self.toggle_language)
            lang_btn.pack(side="left", padx=10)

        # Time label
        time_label = tk.Label(top_bar, text=datetime.now().strftime('%B %d, %Y %I:%M %p'),
                            font=("Arial", 20, "bold"), fg="black", bg="#dbb40f")

        time_label.place(relx=0.5, rely=0.5, anchor="center")
        self.update_time(time_label)
        #TODO
        # User info frame
        user_frame = tk.Frame(top_bar, bg="#dbb40f")
        user_frame.pack(side="right", padx=10)

        username_label = tk.Label(user_frame, text=self.user_name, font=("Arial", 14), fg="black", bg="#dbb40f")
        username_label.pack(side="left")
    
    def trash(self,user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # make the top bar with change language button
        self.topbar(show_back_button=True)


    def play_Error(self):
        sound_path = os.path.join(BASE_DIR, 'Static', 'sounds', 'Error.mp3')
        if os.path.exists(sound_path):
            threading.Thread(target=playsound, args=(sound_path,), daemon=True).start()
            print("done")
        else:
            print("Sound file not found:", sound_path)

    # def play_(self):
    #     sound_path = os.path.join(BASE_DIR, 'Static', 'sounds', 'Error.mp3')
    #     threading.Thread(target=playsound, args=(sound_path,), daemon=True).start()

    def play_success(self):
        sound_path = os.path.join(BASE_DIR, 'Static', 'sounds', 'Success.mp3')

        def play_sound():
            if os.path.exists(sound_path):
                while not self.stop_event.is_set():  # Check if stop_event is set
                    playsound(sound_path)
                    break  # In this case, we'll play the sound only once.
                print("done")
            else:
                print("Sound file not found:", sound_path)

        # Create and start the thread to play sound
        self.stop_event.clear()  # Clear the stop event before starting the thread
        threading.Thread(target=play_sound, daemon=True).start()

    def stop_sound(self):
        """Method to stop the sound playing."""
        self.stop_event.set()

    def silent_popup(self, title, message, callback):
        callback()

        popup = tk.Toplevel()
        popup.title(title)
        popup.geometry("300x120")
        popup.resizable(False, False)
        popup.grab_set()  # Makes it modal

        main_x = self.root.winfo_x()
        main_y = self.root.winfo_y()
        main_width = self.root.winfo_width()
        main_height = self.root.winfo_height()

        popup_width = 300
        popup_height = 120

        pos_x = main_x + (main_width // 2) - (popup_width // 2)
        pos_y = main_y + (main_height // 2) - (popup_height // 2)

        popup.geometry(f"{popup_width}x{popup_height}+{pos_x}+{pos_y}")

        tk.Label(popup, text=message, fg="#b58612", font=("Arial", 12)).pack(pady=10)
        tk.Button(popup, text="OK", width=10, command=popup.destroy).pack(pady=20)

        popup.wait_window()  # Blocks further execution until the popup is closed
        self.stop_sound()


######################### Auxiliary classes #########################################################
class AlwaysOnTopInputDialog(tk.Toplevel):
    def __init__(self, parent, prompt):
        super().__init__(parent)
        self.transient(parent)  # Make sure this dialog is always on top of the parent window
        self.grab_set()  # Lock interaction to this dialog until it is closed

        self.title("Input")
        
        # Create the widgets for the dialog
        self.prompt_label = tk.Label(self, text=prompt)
        self.prompt_label.pack(padx=10, pady=10)
        
        self.entry = tk.Entry(self)
        self.entry.pack(padx=10, pady=10)
        self.entry.focus_set()  # Set focus on the entry field

        self.result = None
        
        self.ok_button = tk.Button(self, text="OK", command=self.on_ok)
        self.ok_button.pack(pady=5)
        self.ok_button.bind("<Return>", lambda event: self.ok_button.invoke())

        self.after(1, self.adjust_geometry) 

        # Center the dialog on the screen
        self.center_dialog(parent)

    def adjust_geometry(self):
        # Set the fixed size of the dialog window after widget creation
        self.geometry("300x150")  # Width=400, Height=150 (Fixed Size)

    def center_dialog(self, parent):
        # Get the screen width and height
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()

        # Get the size of the dialog window
        dialog_width = self.winfo_reqwidth()
        dialog_height = self.winfo_reqheight()

        # Calculate the position to center the dialog
        x_position = (screen_width // 2) - (dialog_width // 2)
        y_position = (screen_height // 2) - (dialog_height // 2)

        # Set the geometry of the dialog window
        self.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")

    def on_ok(self):
        self.result = self.entry.get()
        self.destroy()  # Close the dialog when the user clicks OK

    def get_result(self):
        self.wait_window(self)  # Wait for this window to close and get the result
        return self.result

######################### Main #########################################################

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesSystemApp(root)
    app.open_login_window()  # Start with the login window
    try:
        root.mainloop()
    except Exception as e:
        print("Error during mainloop:", e)