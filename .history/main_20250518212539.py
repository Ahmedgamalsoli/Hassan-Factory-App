import tkinter as tk
from tkinter import filedialog, ttk, messagebox,Tk, Label, PhotoImage,simpledialog
from PIL import Image, ImageTk, ImageDraw  # Import Pillow classes
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime,time , time
from fpdf import FPDF
import sqlite3
import csv
import io
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
import urllib.request
# Add these imports at the top of your file
import matplotlib
matplotlib.use('TkAgg')  # Set the backend before importing pyplot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

######################################################### Access Data Base ##############################################################################
dialog_width = 300  # Same width as AlwaysOnTopInputDialog
dialog_height = 150 # Same height as AlwaysOnTopInputDialog

ARRAY_FIELDS = ['Units'] #Must be lower case
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
        style = ttk.Style()
        style.theme_use("clam")  # Looks cleaner than default
        style.configure("Treeview", 
                        background="#f0f0f0",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="#f0f0f0",
                        font=("Arial", 10))
        style.map('Treeview', background=[('selected', '#2196F3')], foreground=[('selected', 'white')])

        self.Connect_DB()
                    
        self.stop_event = threading.Event()
        
        self.image_refs = []
        #         elif collection_name == "Sales_Header":
        #     return [self.t("Product_code"), self.t("product_name"), self.t("unit"),self.t("numbering"),self.t("QTY"),self.t("Discount Type"),self.t("Discount Value"),self.t("Total_QTY"),self.t("Unit_Price"),self.t("Total_Price")]
       
        # elif collection_name == "Materials_Header":
        #     return [self.t("Material_code"), self.t("Material_name"), self.t("unit"),self.t("numbering"),self.t("QTY"),self.t("Discount Type"),self.t("Discount Value"),self.t("Total_QTY"),self.t("Unit_Price"),self.t("Total_Price")]
        self.language = "Arabic"  # default language
        self.translations = {
            "Add New Product": {"Arabic": "امر انتاج", "English": "Production order"},
            "Reports": {"Arabic": "التقارير", "English": "Reports"},
            "Production Order": {"Arabic": "أمر انتاج", "English": "Production Order"},
            "Employee interactions": {"Arabic": "تعاملات الموظفين", "English": "Employee Interactions"},
            "Database": {"Arabic": "قاعدة البيانات", "English": "Database"},
            "Change Language": {"Arabic": "تغيير اللغة", "English": "Change Language"},
            "New Sales Invoice": {"Arabic": "فاتورة مبيعات جديدة", "English": "New Sales Invoice"},
            "New Purchase Invoice": {"Arabic": "فاتورة مشتريات جديدة", "English": "New Purchase Invoice"},
            "Receive Payment": {"Arabic": "حسابات وتوريدات العملاء", "English": "Customer Supply Hub"},
            "Treasury": {"Arabic": "الخزينة", "English": "Treasury"},
            "Make Payment": {"Arabic": "حسابات وتوريدات الموردين", "English": "Supplier Supply Hub"},
            "Customers": {"Arabic": "العملاء", "English": "Customers"},
            "Suppliers": {"Arabic": "الموردين", "English": "Suppliers"},
            "Products": {"Arabic": "المنتجات", "English": "Products"},
            "Materials": {"Arabic": "الخامات", "English": "Materials"},
            "Employees": {"Arabic": "الموظفين", "English": "Employees"},
            "Customer Name":{"Arabic": "العميل:", "English": "Customer:"},
            "Supplier Name":{"Arabic": "المورد:", "English": "Supplier:"},
            "Previous Balance":{"Arabic": "الحساب السابق:", "English": "Previous Balance:"},
            "Paid Money":{"Arabic": "المبلغ المدفوع:", "English": "Paid Money:"},
            "Customer Code":{"Arabic": "كود العميل:", "English": "Customer Code:"},
            "Supplier Code":{"Arabic": "كود المورد:", "English": "Supplier Code:"},
            "Payment Method":{"Arabic": "طريقة الدفع:", "English": "Payment Method:"},
            "Product_code":{"Arabic": "كود المنتج", "English": "Product Code"},
            "product_name":{"Arabic": "اسم المنتج", "English": "Product Name"},
            "unit":{"Arabic": "الوحدة", "English": "Unit:"},
            "numbering":{"Arabic": "العدد", "English": "Numbering"},
            "QTY":{"Arabic": "الكمية", "English": "Quantity"},
            "Discount Type":{"Arabic": "نوع الخصم", "English": "Discount Type"},
            "Discount Value":{"Arabic": "قيمة الخصم", "English": "Discount Value"},
            "Total_QTY":{"Arabic": "إجمالي الكمية", "English": "Total Quantity"},
            "Unit_Price":{"Arabic": "سعر الوحدة", "English": "Unit Price"},
            "Total_Price":{"Arabic": "إجمالي السعر", "English": "Total Price"},
            "Material_code":{"Arabic": "كود الخام", "English": "Material Code"},
            "Material_name":{"Arabic": "اسم الخام", "English": "Material Name"},
            "➕ Add 3 More Rows":{"Arabic": "➕ أضف 3 صفوف أخرى", "English": "➕ Add 3 More Rows"},
            "💾 Save Invoice":{"Arabic": "💾 حفظ الفاتورة", "English": "💾 Save Invoice"},
            "Search":{"Arabic": "ابحث", "English": "Search"},
            "Name":{"Arabic": "الاسم", "English": "Name"},
            "Phone_number1":{"Arabic": "رقم التليفون 1", "English": "Phone Number 1"},
            "Phone_number2":{"Arabic": "رقم التليفون 2", "English": "Phone Number 2"},
            "Code":{"Arabic": "كوود", "English": "Code"},
            "Purchase_mgr_number":{"Arabic": "رقم مدير المشتريات", "English": "Purchase Manager Number"},
            "Financial_mgr_number":{"Arabic": "رقم مدير المالية", "English": "Financial Manager Number"},
            "Purchase_mgr_name":{"Arabic": "اسم مديرالمشتريات", "English": "Purchase Manager Name"},
            "Financial_mgr_name":{"Arabic": "اسم مدير المالية", "English": "Financial Manager Name"},
            "Email":{"Arabic": "الايميل", "English": "Email"},
            "Company_address":{"Arabic": "عنوان الشركة", "English": "Company Address"},
            "Extra_address":{"Arabic": "عنوان اضافي", "English": "Extra Address"},
            "Maps_link":{"Arabic": "رابط العنوان", "English": "Maps Link"},
            "Bank_account":{"Arabic": "حساب بنكي", "English": "Bank Account"},
            "Instapay":{"Arabic": "انستاباي", "English": "Instapay"},
            "E_wallet":{"Arabic": "محفظه الكترونية", "English": "E_wallet"},
            "Accountant_name":{"Arabic": "اسم المحاسب", "English": "Accountant Name"},
            "Accountant_number":{"Arabic": "رقم المحاسب", "English": "Accountant Number"},
            "Sales_grade":{"Arabic": "تصنيف قيمة المبيعات", "English": "Sales Grade"},
            "Growth_grade":{"Arabic": "تصنيف معدل الزيادة", "English": "Growth Grade"},
            "Frequency_grade":{"Arabic": "تصنيف معدل الشراء", "English": "Frequency Grade"},
            "Credit":{"Arabic": "دائن", "English": "Credit"},
            "Debit":{"Arabic": "مدين", "English": "Debit"},
            "Balance":{"Arabic": "صافي الحساب", "English": "Balance"},
            "Last_purchase_date":{"Arabic": "تاريخ اخر فاتورة", "English": "Last Purchase"},
            "Sales":{"Arabic": "عدد المبيعات", "English": "Sales"},
            "Password":{"Arabic": "الباسورد", "English": "Password"},
            "Role":{"Arabic": "الوظيفة", "English": "Role"},
            "Join_Date":{"Arabic": "تاريخ الالتحاق", "English": "Join Date"},
            "National_id_pic":{"Arabic": "", "English": "National ID Picture"},
            "Phone_number":{"Arabic": "رقم التليفون", "English": "Phone Number"},
            "Address":{"Arabic": "العنوان", "English": "Address"},
            "Salary":{"Arabic": "المرتب", "English": "Salary"},
            "category":{"Arabic": "التصنيف", "English": "category"},
            "stock_quantity":{"Arabic": "كمية المخزون", "English": "stock Quantity"},
            "Specs":{"Arabic": "المواصفات", "English": "Specs"},
            "product_code":{"Arabic": "كود المنتج", "English": "product Code"},
            "Units":{"Arabic": "الوحدات", "English": "Units"},
            "prod_pic":{"Arabic": "صورة المنتج", "English": "product Picture"},
            "sales":{"Arabic": "المبيعات", "English": "Sales"},
            "purchases":{"Arabic": "المشتريات", "English": "Purchases"},
            "Employee Statistics":{"Arabic": "احصائيات الموظفين", "English": "Employees Statistics"},
            "Employee hours":{"Arabic": "مواعيد الموظفين", "English": "Employees hours"},
            "Employee Withdrawals":{"Arabic": "مسحوبات الموظفين", "English": "Employees Withdrawals"},
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
        # self.customer_name_var = None
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
        self.materials_collection             = db['Materials']
        self.purchases_collection             = db['Purchases']
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
            "command": lambda: self.new_Purchase_invoice(self.user_role)},
            {"text": self.t("Receive Payment"), "image": "Recieve.png", 
            "command": lambda: self.trash(self.user_role)},
            {"text": self.t("Make Payment"), "image": "payment.png", 
            "command": lambda: self.trash(self.user_role)},
            {"text": self.t("Production Order"), "image": "Production Order.png", 
            "command": lambda: self.trash(self.user_role)},
            {"text": self.t("Employee interactions"), "image": "Employees.png", 
            "command": lambda: self.manage_Employees_window(self.user_role)},
            # {"text": self.t("Customers"), "image": "customers.png", 
            # "command": lambda: self.new_customer(self.user_role)},
            # {"text": self.t("Suppliers"), "image": "suppliers.png", 
            # "command": lambda: self.new_supplier(self.user_role)},
            # {"text": self.t("Employees"), "image": "Employees.png", 
            # "command": lambda: self.new_employee(self.user_role)},
            # {"text": self.t("Products"), "image": "Products.png", 
            # "command": lambda: self.new_products(self.user_role)},
            # {"text": self.t("Materials"), "image": "Materials.png", 
            # "command": lambda: self.new_material(self.user_role)},
            {"text": self.t("Treasury"), "image": "Treasury.png", 
            "command": lambda: self.trash(self.user_role)},
            {"text": self.t("Reports"), "image": "Reports.png", 
            "command": lambda: self.show_visualizations},
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
                "command": lambda: self.check_access_and_open(self.user_role)}
            ])

        # Load images and create buttons
        images = []  # Keep references to prevent garbage collection
        columns_per_row = 3  # Number of buttons per row

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
    # Modify your show_visualizations method:
    def show_visualizations(self):
        try:
            # Create new window
            vis_window = tk.Toplevel(self.root)
            vis_window.title("Business Analytics")
            vis_window.state("zoomed")  # Maximized window
            
            # Create main container
            main_frame = tk.Frame(vis_window, bg="white")
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            # Get data from database
            data = {
                'customers': self.get_customer_count(),
                'suppliers': self.get_supplier_count(),
                'sales': self.get_sales_count(),
                'purchases': self.get_purchase_count(),
                'top_client': self.get_top_client()
            }

            # Create figure
            fig = plt.Figure(figsize=(16, 10), dpi=100)
            fig.suptitle("Business Performance Dashboard", fontsize=16, y=0.95)
            
            # Create subplots
            ax1 = fig.add_subplot(221)
            ax2 = fig.add_subplot(222)
            ax3 = fig.add_subplot(223)
            ax4 = fig.add_subplot(224)

            # Chart 1: Customers vs Suppliers
            ax1.bar(['Customers', 'Suppliers'], 
                    [data['customers'], data['suppliers']], 
                    color=['#1f77b4', '#ff7f0e'])
            ax1.set_title("Customer & Supplier Count", pad=15)
            ax1.set_ylabel("Count")

            # Chart 2: Sales/Purchases Ratio
            ax2.pie([data['sales'], data['purchases']],
                    labels=['Sales', 'Purchases'],
                    autopct='%1.1f%%',
                    colors=['#2ca02c', '#d62728'],
                    startangle=90)
            ax2.set_title("Sales vs Purchases Ratio", pad=15)

            # Chart 3: Top Client
            if data['top_client']:
                ax3.bar(data['top_client'][0], data['top_client'][1],
                        color='#9467bd')
                ax3.set_title("Top Performing Client", pad=15)
                ax3.set_ylabel("Sales Amount")

            # Chart 4: Summary Table
            table_data = [
                ['Metric', 'Value'],
                ['Total Customers', data['customers']],
                ['Total Suppliers', data['suppliers']],
                ['Total Sales', data['sales']],
                ['Total Purchases', data['purchases']]
            ]
            ax4.axis('off')
            table = ax4.table(cellText=table_data, 
                            loc='center', 
                            cellLoc='center',
                            colWidths=[0.4, 0.4])
            table.auto_set_font_size(False)
            table.set_fontsize(12)

            # Embed in Tkinter
            canvas = FigureCanvasTkAgg(fig, master=main_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            # Add close button
            close_btn = tk.Button(vis_window, 
                                text="Back to Main Menu",
                                command=vis_window.destroy,
                                bg="#003366",
                                fg="white",
                                font=("Arial", 12, "bold"))
            close_btn.pack(pady=10)

        except Exception as e:
            print(f"Error generating visualizations: {e}")
            tk.messagebox.showerror("Error", f"Failed to load reports: {str(e)}")

    # Add database query methods (implement with your actual DB connection)
    def get_customer_count(self):
        # Example: return self.db.execute("SELECT COUNT(*) FROM Customers").fetchone()[0]
        return 42

    def get_supplier_count(self):
        return 15

    def get_sales_count(self):
        return 175

    def get_purchase_count(self):
        return 89

    def get_top_client(self):
        return ("Maggie Corp", 175000)             
    def manage_database_window(self):
                # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create the top bar
        self.topbar(show_back_button=True)

        # Main button frame
        button_frame = tk.Frame(self.root, bg="white")
        button_frame.pack(pady=30)

        # Define buttons with images, text, and commands
        buttons = [
            {"text": self.t("Customers"), "image": "customers.png", 
            "command": lambda: self.new_customer(self.user_role)},
            {"text": self.t("Suppliers"), "image": "suppliers.png", 
            "command": lambda: self.new_supplier(self.user_role)},
            {"text": self.t("Employees"), "image": "Employees.png", 
            "command": lambda: self.new_employee(self.user_role)},
            {"text": self.t("Products"), "image": "Products.png", 
            "command": lambda: self.new_products(self.user_role)},
            {"text": self.t("Materials"), "image": "Materials.png", 
            "command": lambda: self.new_material(self.user_role)},
            {"text": self.t("purchases"), "image": "Purchases_DB.png", 
            "command": lambda: self.trash(self.user_role)},
            {"text": self.t("sales"), "image": "Sales_DB.png", 
            "command": lambda: self.trash(self.user_role)},
        ]
        images = []  # Keep references to prevent garbage collection
        columns_per_row = 3  # Number of buttons per row

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
    def manage_Employees_window(self,user_role):
                # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create the top bar
        self.topbar(show_back_button=True)

        # Main button frame
        button_frame = tk.Frame(self.root, bg="white")
        button_frame.pack(pady=30)

        # Define buttons with images, text, and commands
        buttons = [
            {"text": self.t("Employee hours"), "image": "Emp_hours.png", 
            "command": lambda: self.trash(self.user_role)},
            {"text": self.t("Employee Withdrawals"), "image": "Emp_Withdraw.png", 
            "command": lambda: self.trash(self.user_role)},
            {"text": self.t("Employee Statistics"), "image": "employee time statistics.png", 
            "command": lambda: self.trash(self.user_role)},
        ]
        images = []  # Keep references to prevent garbage collection
        columns_per_row = 3  # Number of buttons per row

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
                
    def manage_old_database_window(self, db_name=None, table_name=None):
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
        self.tree.place(x=50, y=190)

        # # Create scrollbars inside frame
        # self.tree_xscroll = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        # self.tree_yscroll = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)

        # # Attach scrollbars to tree
        # self.tree.configure(xscrollcommand=self.tree_xscroll.set, yscrollcommand=self.tree_yscroll.set)

        # # Place them manually
        # self.tree.place(x=0, y=0, width=780, height=230)  # little smaller so scrollbars fit
        # self.tree_xscroll.place(x=0, y=230, width=780, height=20)
        # self.tree_yscroll.place(x=780, y=0, width=20, height=230)


        tk.Button(self.root, text="Add Record", command=self.add_entry).place(width=120, height=40, x=100, y=550)
        tk.Button(self.root, text="Edit Record", command=self.edit_entry).place(width=120, height=40, x=250, y=550)
        tk.Button(self.root, text="Delete Record", command=self.delete_entry).place(width=120, height=40, x=400, y=550)

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

        # Create bidirectional customer mappings
        self.customer_code_map = {}  # name -> code
        self.code_name_map = {}      # code -> name
        self.customer_balance_map = {}  # name -> balance

        # Populate customer data
        all_customers = []
        all_codes = []
        for cust in customers_col.find():
            name = cust.get('Name', '')
            code = str(cust.get('Code', ''))
            balance = cust.get('Balance', 0)
            
            self.customer_code_map[name] = code
            self.code_name_map[code] = name
            self.customer_balance_map[name] = balance
            all_customers.append(name)
            all_codes.append(code)

        # Customer Name Combobox
        tk.Label(customer_frame, text=self.t("Customer Name"), font=("Arial", 12, "bold")).grid(row=0, column=0, sticky='w')
        self.customer_name_var = tk.StringVar()
        self.customer_name_cb = ttk.Combobox(customer_frame, textvariable=self.customer_name_var, values=sorted(all_customers))
        self.customer_name_cb.grid(row=0, column=1, padx=5, sticky='ew')

        # Customer Code Combobox
        tk.Label(customer_frame, text=self.t("Customer Code"), font=("Arial", 12, "bold")).grid(row=0, column=2, sticky='w')
        self.customer_code_var = tk.StringVar()
        self.customer_code_cb = ttk.Combobox(customer_frame, textvariable=self.customer_code_var, values=sorted(all_codes))
        self.customer_code_cb.grid(row=0, column=3, padx=5, sticky='ew')

        # Balance and Payment Fields
        tk.Label(customer_frame, text=self.t("Previous Balance"), font=("Arial", 12, "bold")).grid(row=0, column=4, sticky='e', padx=(20, 0))
        self.previous_balance_var = tk.StringVar()
        self.previous_balance_entry = tk.Entry(customer_frame, textvariable=self.previous_balance_var, 
                                            width=15, state='readonly')
        self.previous_balance_entry.grid(row=0, column=5, sticky='e')

        tk.Label(customer_frame, text=self.t("Paid Money"), font=("Arial", 12, "bold")).grid(row=0, column=6, sticky='e', padx=(20, 0))
        self.payed_cash_var = tk.DoubleVar()
        self.payed_cash_entry = tk.Entry(customer_frame, textvariable=self.payed_cash_var, width=15)
        self.payed_cash_entry.grid(row=0, column=7, sticky='e')

        # Payment Method Dropdown
        tk.Label(customer_frame, text=self.t("Payment Method"), font=("Arial", 12, "bold")).grid(row=0, column=8, sticky='e', padx=(20, 0))
        self.payment_method_var = tk.StringVar()
        payment_methods = ['Cash', 'E_Wallet', 'Bank_account', 'Instapay']
        payment_cb = ttk.Combobox(customer_frame, textvariable=self.payment_method_var, 
                                values=payment_methods, state='readonly', width=12)
        payment_cb.grid(row=0, column=9, sticky='ew', padx=(5, 10))
        payment_cb.current(0)  # Set default to Cash

        # Configure column weights
        customer_frame.columnconfigure(1, weight=1)
        customer_frame.columnconfigure(3, weight=1)
        customer_frame.columnconfigure(5, weight=0)
        customer_frame.columnconfigure(7, weight=0)
        customer_frame.columnconfigure(9, weight=0)

        # Synchronization functions
        def sync_from_name(event=None):
            name = self.customer_name_var.get()
            code = self.customer_code_map.get(name, '')
            self.customer_code_var.set(code)
            self.previous_balance_var.set(str(self.customer_balance_map.get(name, 0)))

        def sync_from_code(event=None):
            code = self.customer_code_var.get()
            name = self.code_name_map.get(code, '')
            self.customer_name_var.set(name)
            self.previous_balance_var.set(str(self.customer_balance_map.get(name, 0)))

        # Event bindings
        self.customer_name_cb.bind('<<ComboboxSelected>>', sync_from_name)
        self.customer_code_cb.bind('<<ComboboxSelected>>', sync_from_code)
        
        self.customer_name_cb.bind('<KeyRelease>', lambda e: [
            self.filter_combobox(e, all_customers, self.customer_name_cb),
            sync_from_name()
        ])
        
        self.customer_code_cb.bind('<KeyRelease>', lambda e: [
            self.filter_combobox(e, all_codes, self.customer_code_cb),
            sync_from_code()
        ])

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
                self.product_map[code] = {
                    'name': name,
                    'units': unit_names,
                    'price': price
                }
                self.name_to_code[name] = code
                product_names.append(name)
                product_codes.append(code)

            self.product_codes = sorted(list(set(product_codes)))
            self.product_names = sorted(list(set(product_names)))
            all_units = sorted(list(all_units))

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load products: {str(e)}")
            return

        # Invoice Items Grid
        columns = self.get_fields_by_name("Sales_Header")
        col_width = 23

        header_row = tk.Frame(form_frame, bg='#f0f0f0')
        header_row.grid(row=2, column=0, columnspan=len(columns), sticky='nsew', pady=(20, 0))
        for col_idx, col in enumerate(columns):
            tk.Label(header_row, text=self.t(col), width=col_width, relief='ridge',
                    bg='#f0f0f0', anchor='w').grid(row=0, column=col_idx, sticky='ew')
            header_row.columnconfigure(col_idx, weight=1)

        # Scrollable Canvas
        canvas = tk.Canvas(form_frame, highlightthickness=0)
        scrollbar = tk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        self.rows_frame = tk.Frame(canvas)
        
        self.rows_frame.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.rows_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=3, column=0, columnspan=len(columns), sticky="nsew")
        scrollbar.grid(row=3, column=len(columns), sticky="ns")
        
        form_frame.grid_rowconfigure(3, weight=1)
        for i in range(len(columns)):
            form_frame.columnconfigure(i, weight=1)

        self.entries = []

        # Modified create_row function with discount fields
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
                elif col == "Discount Type":
                    var = tk.StringVar()
                    cb = ttk.Combobox(row_frame, textvariable=var, 
                                    values=["Percentage", "Value"], 
                                    state="readonly",
                                    width=col_width-2)
                    cb.current(0)  # Default to Percentage
                    cb.grid(row=0, column=col_idx, sticky='ew')
                    row_entries.append(cb)
                elif col == "Discount Value":
                    var = tk.StringVar()
                    entry = tk.Entry(row_frame, textvariable=var, width=col_width+1)
                    entry.bind('<KeyRelease>', lambda e, r=row_number: self.calculate_totals(r))
                    entry.grid(row=0, column=col_idx, sticky='ew')
                    row_entries.append(entry)
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

        add_three_rows()

        # Buttons Frame
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=len(columns), pady=10, sticky='ew')
        
        tk.Button(button_frame, text=self.t("➕ Add 3 More Rows"), command=add_three_rows,
                bg='#4CAF50', fg='white').grid(row=0, column=0, padx=5, sticky='w')
        tk.Button(button_frame, text=self.t("💾 Save Invoice"), 
                command=lambda: self.save_invoice(sales_col, customers_col,products_col),
                bg='#2196F3', fg='white').grid(row=0, column=1, padx=5, sticky='e')
        
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
    # def Receive_payment_window(self, user_role):
    #     # Clear current window
    #     for widget in self.root.winfo_children():
    #         widget.destroy()

    #     # Initialize product mappings
    #     self.product_map = {}
    #     self.name_to_code = {}
        
    #     # Create top bar
    #     self.topbar(show_back_button=True)

    #     # MongoDB collections
    #     customers_col = self.get_collection_by_name("Customers")
    #     # sales_col = self.get_collection_by_name("Sales")
    #     # products_col = self.get_collection_by_name("Products")

    #     # Main form frame
    #     form_frame = tk.Frame(self.root, padx=20, pady=20)
    #     form_frame.pack(fill=tk.BOTH, expand=True)

    #     # Customer Selection Frame
    #     customer_frame = tk.Frame(form_frame, bd=1, relief=tk.SOLID, padx=5, pady=5)
    #     customer_frame.grid(row=0, column=0, columnspan=2, sticky='w', pady=5)

    #     # Create bidirectional customer mappings
    #     self.customer_code_map = {}  # name -> code
    #     self.code_name_map = {}      # code -> name
    #     self.customer_balance_map = {}  # name -> balance

    #     # Populate customer data
    #     all_customers = []
    #     all_codes = []
    #     for cust in customers_col.find():
    #         name = cust.get('Name', '')
    #         code = str(cust.get('Code', ''))
    #         balance = cust.get('Balance', 0)
            
    #         self.customer_code_map[name] = code
    #         self.code_name_map[code] = name
    #         self.customer_balance_map[name] = balance
    #         all_customers.append(name)
    #         all_codes.append(code)

    #     # Customer Name Combobox
    #     tk.Label(customer_frame, text=self.t("Customer Name"), font=("Arial", 12, "bold")).grid(row=0, column=0, sticky='w')
    #     self.customer_name_var = tk.StringVar()
    #     self.customer_name_cb = ttk.Combobox(customer_frame, textvariable=self.customer_name_var, values=sorted(all_customers))
    #     self.customer_name_cb.grid(row=0, column=1, padx=5, sticky='ew')

    #     # Customer Code Combobox
    #     tk.Label(customer_frame, text=self.t("Customer Code"), font=("Arial", 12, "bold")).grid(row=0, column=2, sticky='w')
    #     self.customer_code_var = tk.StringVar()
    #     self.customer_code_cb = ttk.Combobox(customer_frame, textvariable=self.customer_code_var, values=sorted(all_codes))
    #     self.customer_code_cb.grid(row=0, column=3, padx=5, sticky='ew')

    #     # Balance and Payment Fields
    #     tk.Label(customer_frame, text=self.t("Previous Balance"), font=("Arial", 12, "bold")).grid(row=0, column=4, sticky='e', padx=(20, 0))
    #     self.previous_balance_var = tk.StringVar()
    #     self.previous_balance_entry = tk.Entry(customer_frame, textvariable=self.previous_balance_var, 
    #                                         width=15, state='readonly')
    #     self.previous_balance_entry.grid(row=0, column=5, sticky='e')

    #     tk.Label(customer_frame, text=self.t("Paid Money"), font=("Arial", 12, "bold")).grid(row=0, column=6, sticky='e', padx=(20, 0))
    #     self.payed_cash_var = tk.DoubleVar()
    #     self.payed_cash_entry = tk.Entry(customer_frame, textvariable=self.payed_cash_var, width=15)
    #     self.payed_cash_entry.grid(row=0, column=7, sticky='e')

    #     # Payment Method Dropdown
    #     tk.Label(customer_frame, text=self.t("Payment Method"), font=("Arial", 12, "bold")).grid(row=0, column=8, sticky='e', padx=(20, 0))
    #     self.payment_method_var = tk.StringVar()
    #     payment_methods = ['Cash', 'E_Wallet', 'Bank_account', 'Instapay']
    #     payment_cb = ttk.Combobox(customer_frame, textvariable=self.payment_method_var, 
    #                             values=payment_methods, state='readonly', width=12)
    #     payment_cb.grid(row=0, column=9, sticky='ew', padx=(5, 10))
    #     payment_cb.current(0)  # Set default to Cash

    #     # Configure column weights
    #     customer_frame.columnconfigure(1, weight=1)
    #     customer_frame.columnconfigure(3, weight=1)
    #     customer_frame.columnconfigure(5, weight=0)
    #     customer_frame.columnconfigure(7, weight=0)
    #     customer_frame.columnconfigure(9, weight=0)

    #     # Synchronization functions
    #     def sync_from_name(event=None):
    #         name = self.customer_name_var.get()
    #         code = self.customer_code_map.get(name, '')
    #         self.customer_code_var.set(code)
    #         self.previous_balance_var.set(str(self.customer_balance_map.get(name, 0)))

    #     def sync_from_code(event=None):
    #         code = self.customer_code_var.get()
    #         name = self.code_name_map.get(code, '')
    #         self.customer_name_var.set(name)
    #         self.previous_balance_var.set(str(self.customer_balance_map.get(name, 0)))

    #     # Event bindings
    #     self.customer_name_cb.bind('<<ComboboxSelected>>', sync_from_name)
    #     self.customer_code_cb.bind('<<ComboboxSelected>>', sync_from_code)
        
    #     self.customer_name_cb.bind('<KeyRelease>', lambda e: [
    #         self.filter_combobox(e, all_customers, self.customer_name_cb),
    #         sync_from_name()
    #     ])
        
    #     self.customer_code_cb.bind('<KeyRelease>', lambda e: [
    #         self.filter_combobox(e, all_codes, self.customer_code_cb),
    #         sync_from_code()
    #     ])

    #     # # Load product data
    #     # try:
    #     #     products = list(products_col.find())
    #     #     all_units = set()
    #     #     product_names = []
    #     #     product_codes = []

    #     #     for p in products:
    #     #         code = str(p.get('product_code', '')).strip()
    #     #         name = p.get('product_name', '').strip()
    #     #         units_list = p.get('Units', [])

    #     #         # Process units
    #     #         unit_names = []
    #     #         for unit in units_list:
    #     #             if isinstance(unit, dict):
    #     #                 unit_name = str(unit.get('unit_name', '')).strip()
    #     #             elif isinstance(unit, str):
    #     #                 unit_name = unit.strip()
    #     #             else:
    #     #                 continue
                    
    #     #             if unit_name:
    #     #                 unit_names.append(unit_name)
    #     #                 all_units.add(unit_name)

    #     #         # Handle price conversion
    #     #         try:
    #     #             price_str = str(p.get('Unit_Price', '0')).strip('kgm ')
    #     #             price = float(price_str) if price_str else 0.0
    #     #         except ValueError:
    #     #             price = 0.0

    #     #         # Update mappings
    #     #         self.product_map[code] = {
    #     #             'name': name,
    #     #             'units': unit_names,
    #     #             'price': price
    #     #         }
    #     #         self.name_to_code[name] = code
    #     #         product_names.append(name)
    #     #         product_codes.append(code)

    #     #     self.product_codes = sorted(list(set(product_codes)))
    #     #     self.product_names = sorted(list(set(product_names)))
    #     #     all_units = sorted(list(all_units))

    #     # except Exception as e:
    #     #     messagebox.showerror("Database Error", f"Failed to load products: {str(e)}")
    #     #     return

    #     # # Invoice Items Grid
    #     # columns = self.get_fields_by_name("Sales_Header")
    #     # col_width = 23

    #     # header_row = tk.Frame(form_frame, bg='#f0f0f0')
    #     # header_row.grid(row=2, column=0, columnspan=len(columns), sticky='nsew', pady=(20, 0))
    #     # for col_idx, col in enumerate(columns):
    #     #     tk.Label(header_row, text=self.t(col), width=col_width, relief='ridge',
    #     #             bg='#f0f0f0', anchor='w').grid(row=0, column=col_idx, sticky='ew')
    #     #     header_row.columnconfigure(col_idx, weight=1)

    #     # # Scrollable Canvas
    #     # canvas = tk.Canvas(form_frame, highlightthickness=0)
    #     # scrollbar = tk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
    #     # self.rows_frame = tk.Frame(canvas)
        
    #     # self.rows_frame.bind("<Configure>", lambda e: canvas.configure(
    #     #     scrollregion=canvas.bbox("all")))
    #     # canvas.create_window((0, 0), window=self.rows_frame, anchor="nw")
    #     # canvas.configure(yscrollcommand=scrollbar.set)

    #     # canvas.grid(row=3, column=0, columnspan=len(columns), sticky="nsew")
    #     # scrollbar.grid(row=3, column=len(columns), sticky="ns")
        
    #     # form_frame.grid_rowconfigure(3, weight=1)
    #     # for i in range(len(columns)):
    #     #     form_frame.columnconfigure(i, weight=1)

    #     # self.entries = []

    #     # # Modified create_row function with discount fields
    #     # def create_row(parent, row_number, bg_color):
    #     #     row_frame = tk.Frame(parent, bg=bg_color)
    #     #     row_frame.grid(row=row_number, column=0, sticky='ew')
            
    #     #     row_entries = []
    #     #     for col_idx, col in enumerate(columns):
    #     #         if col == "Product_code":
    #     #             var = tk.StringVar()
    #     #             cb = ttk.Combobox(row_frame, textvariable=var, values=product_codes, width=col_width-2)
    #     #             cb.bind('<<ComboboxSelected>>', lambda e, r=row_number: self.update_product_info(r, "code"))
    #     #             cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_combobox_change(e, r, "code"))
    #     #             cb.grid(row=0, column=col_idx, sticky='ew')
    #     #             row_entries.append(cb)
    #     #         elif col == "product_name":
    #     #             var = tk.StringVar()
    #     #             cb = ttk.Combobox(row_frame, textvariable=var, values=product_names, width=col_width-2)
    #     #             cb.bind('<<ComboboxSelected>>', lambda e, r=row_number: self.update_product_info(r, "name"))
    #     #             cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_combobox_change(e, r, "name"))
    #     #             cb.grid(row=0, column=col_idx, sticky='ew')
    #     #             row_entries.append(cb)
    #     #         elif col == "unit":
    #     #             var = tk.StringVar()
    #     #             cb = ttk.Combobox(row_frame, textvariable=var, values=[], width=col_width-2)
    #     #             cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_unit_change(e, r))
    #     #             cb.grid(row=0, column=col_idx, sticky='ew')
    #     #             row_entries.append(cb)
    #     #         elif col == "Discount Type":
    #     #             var = tk.StringVar()
    #     #             cb = ttk.Combobox(row_frame, textvariable=var, 
    #     #                             values=["Percentage", "Value"], 
    #     #                             state="readonly",
    #     #                             width=col_width-2)
    #     #             cb.current(0)  # Default to Percentage
    #     #             cb.grid(row=0, column=col_idx, sticky='ew')
    #     #             row_entries.append(cb)
    #     #         elif col == "Discount Value":
    #     #             var = tk.StringVar()
    #     #             entry = tk.Entry(row_frame, textvariable=var, width=col_width+1)
    #     #             entry.bind('<KeyRelease>', lambda e, r=row_number: self.calculate_totals(r))
    #     #             entry.grid(row=0, column=col_idx, sticky='ew')
    #     #             row_entries.append(entry)
    #     #         elif col in ["Unit_Price", "Total_QTY", "Total_Price"]:
    #     #             entry = tk.Entry(row_frame, width=col_width+1, relief='flat', state='readonly')
    #     #             entry.grid(row=0, column=col_idx, sticky='ew')
    #     #             row_entries.append(entry)
    #     #         else:
    #     #             entry = tk.Entry(row_frame, width=col_width+1, relief='sunken')
    #     #             entry.bind('<KeyRelease>', lambda e, r=row_number: self.calculate_totals(r))
    #     #             entry.grid(row=0, column=col_idx, sticky='ew')
    #     #             row_entries.append(entry)
                
    #     #         row_frame.columnconfigure(col_idx, weight=1)
            
    #     #     return row_entries

    #     # def add_three_rows():
    #     #     current_row_count = len(self.entries)
    #     #     for i in range(3):
    #     #         bg_color = 'white' if (current_row_count + i) % 2 == 0 else '#f0f0f0'
    #     #         row_entries = create_row(self.rows_frame, current_row_count + i, bg_color)
    #     #         self.entries.append(row_entries)

    #     # add_three_rows()

    #     # # Buttons Frame
    #     button_frame = tk.Frame(form_frame)
    #     # button_frame.grid(row=4, column=0, columnspan=len(columns), pady=10, sticky='ew')
    #     button_frame.grid(row=4, column=0, pady=10, sticky='ew')
        
    #     # tk.Button(button_frame, text=self.t("➕ Add 3 More Rows"), command=add_three_rows,
    #     #         bg='#4CAF50', fg='white').grid(row=0, column=0, padx=5, sticky='w')
    #     # tk.Button(button_frame, text=self.t("💾 Save Invoice"), 
    #     #         command=lambda: self.save_invoice(sales_col, customers_col,products_col),
    #     #         bg='#2196F3', fg='white').grid(row=0, column=1, padx=5, sticky='e')
        
    #     button_frame.columnconfigure(0, weight=1)
    #     button_frame.columnconfigure(1, weight=1)

    def new_Purchase_invoice(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Initialize product mappings
        self.material_map = {}
        self.name_to_code = {}
        
        # Create top bar
        self.topbar(show_back_button=True)

        # MongoDB collections
        suppliers_col = self.get_collection_by_name("Suppliers")
        purchases_col = self.get_collection_by_name("Purchases")
        materials_col = self.get_collection_by_name("Materials")

        # Main form frame
        form_frame = tk.Frame(self.root, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Supplier Selection Frame
        Supplier_frame = tk.Frame(form_frame, bd=1, relief=tk.SOLID, padx=5, pady=5)
        Supplier_frame.grid(row=0, column=0, columnspan=2, sticky='w', pady=5)

        # Create bidirectional Supplier mappings
        self.supplier_code_map = {}  # name -> code
        self.code_name_map = {}      # code -> name
        self.supplier_balance_map = {}  # name -> balance

        # Populate Supplier data
        all_suppliers = []
        all_codes = []
        for supp in suppliers_col.find():
            name = supp.get('Name', '')
            code = str(supp.get('Code', ''))
            balance = supp.get('Balance', 0)
            
            self.supplier_code_map[name] = code
            self.code_name_map[code] = name
            self.supplier_balance_map[name] = balance
            all_suppliers.append(name)
            all_codes.append(code)

        # Supplier Name Combobox
        tk.Label(Supplier_frame, text=self.t("Supplier Name"), font=("Arial", 12, "bold")).grid(row=0, column=0, sticky='w')
        self.supplier_name_var = tk.StringVar()
        self.supplier_name_cb = ttk.Combobox(Supplier_frame, textvariable=self.supplier_name_var, values=sorted(all_suppliers))
        self.supplier_name_cb.grid(row=0, column=1, padx=5, sticky='ew')

        # Supplier Code Combobox
        tk.Label(Supplier_frame, text=self.t("Supplier Code"), font=("Arial", 12, "bold")).grid(row=0, column=2, sticky='w')
        self.supplier_code_var = tk.StringVar()
        self.supplier_code_cb = ttk.Combobox(Supplier_frame, textvariable=self.supplier_code_var, values=sorted(all_codes))
        self.supplier_code_cb.grid(row=0, column=3, padx=5, sticky='ew')

        # Balance and Payment Fields
        tk.Label(Supplier_frame, text=self.t("Previous Balance"), font=("Arial", 12, "bold")).grid(row=0, column=4, sticky='e', padx=(20, 0))
        self.previous_balance_var = tk.StringVar()
        self.previous_balance_entry = tk.Entry(Supplier_frame, textvariable=self.previous_balance_var, 
                                            width=15, state='readonly')
        self.previous_balance_entry.grid(row=0, column=5, sticky='e')

        tk.Label(Supplier_frame, text=self.t("Paid Money"), font=("Arial", 12, "bold")).grid(row=0, column=6, sticky='e', padx=(20, 0))
        self.payed_cash_var = tk.DoubleVar()
        self.payed_cash_entry = tk.Entry(Supplier_frame, textvariable=self.payed_cash_var, width=15)
        self.payed_cash_entry.grid(row=0, column=7, sticky='e')

        # Payment Method Dropdown
        tk.Label(Supplier_frame, text=self.t("Payment Method"), font=("Arial", 12, "bold")).grid(row=0, column=8, sticky='e', padx=(20, 0))
        self.payment_method_var = tk.StringVar()
        payment_methods = ['Cash', 'E_Wallet', 'Bank_account', 'Instapay']
        payment_cb = ttk.Combobox(Supplier_frame, textvariable=self.payment_method_var, 
                                values=payment_methods, state='readonly', width=12)
        payment_cb.grid(row=0, column=9, sticky='ew', padx=(5, 10))
        payment_cb.current(0)  # Set default to Cash

        # Configure column weights
        Supplier_frame.columnconfigure(1, weight=1)
        Supplier_frame.columnconfigure(3, weight=1)
        Supplier_frame.columnconfigure(5, weight=0)
        Supplier_frame.columnconfigure(7, weight=0)
        Supplier_frame.columnconfigure(9, weight=0)

        # Synchronization functions
        def sync_from_name(event=None):
            name = self.supplier_name_var.get()
            code = self.supplier_code_map.get(name, '')
            self.supplier_code_var.set(code)
            self.previous_balance_var.set(str(self.supplier_balance_map.get(name, 0)))

        def sync_from_code(event=None):
            code = self.supplier_code_var.get()
            name = self.code_name_map.get(code, '')
            self.supplier_name_var.set(name)
            self.previous_balance_var.set(str(self.supplier_balance_map.get(name, 0)))

        # Event bindings
        self.supplier_name_cb.bind('<<ComboboxSelected>>', sync_from_name)
        self.supplier_code_cb.bind('<<ComboboxSelected>>', sync_from_code)
        
        self.supplier_name_cb.bind('<KeyRelease>', lambda e: [
            self.filter_combobox(e, all_suppliers, self.supplier_name_cb),
            sync_from_name()
        ])
        
        self.supplier_code_cb.bind('<KeyRelease>', lambda e: [
            self.filter_combobox(e, all_codes, self.supplier_code_cb),
            sync_from_code()
        ])

        # Load product data
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
                self.material_map[code] = {
                    'name': name,
                    'units': unit_names,
                    'price': price
                }
                self.name_to_code[name] = code
                material_names.append(name)
                material_codes.append(code)

            self.product_codes = sorted(list(set(material_codes)))
            self.product_names = sorted(list(set(material_names)))
            all_units = sorted(list(all_units))

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load products: {str(e)}")
            return

        # Invoice Items Grid
        columns = self.get_fields_by_name("Materials_Header")
        col_width = 23

        header_row = tk.Frame(form_frame, bg='#f0f0f0')
        header_row.grid(row=2, column=0, columnspan=len(columns), sticky='nsew', pady=(20, 0))
        for col_idx, col in enumerate(columns):
            tk.Label(header_row, text=self.t(col), width=col_width, relief='ridge',
                    bg='#f0f0f0', anchor='w').grid(row=0, column=col_idx, sticky='ew')
            header_row.columnconfigure(col_idx, weight=1)

        # Scrollable Canvas
        canvas = tk.Canvas(form_frame, highlightthickness=0)
        scrollbar = tk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        self.rows_frame = tk.Frame(canvas)
        
        self.rows_frame.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.rows_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=3, column=0, columnspan=len(columns), sticky="nsew")
        scrollbar.grid(row=3, column=len(columns), sticky="ns")
        
        form_frame.grid_rowconfigure(3, weight=1)
        for i in range(len(columns)):
            form_frame.columnconfigure(i, weight=1)

        self.entries = []

        # Modified create_row function with discount fields
        def create_row(parent, row_number, bg_color):
            row_frame = tk.Frame(parent, bg=bg_color)
            row_frame.grid(row=row_number, column=0, sticky='ew')
            
            row_entries = []
            for col_idx, col in enumerate(columns):
                if col == "Material_code":
                    var = tk.StringVar()
                    cb = ttk.Combobox(row_frame, textvariable=var, values=material_codes, width=col_width-2)
                    cb.bind('<<ComboboxSelected>>', lambda e, r=row_number: self.update_material_info(r, "code"))
                    cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_combobox_change_purchase(e, r, "code"))
                    cb.grid(row=0, column=col_idx, sticky='ew')
                    row_entries.append(cb)
                elif col == "Material_name":
                    var = tk.StringVar()
                    cb = ttk.Combobox(row_frame, textvariable=var, values=material_names, width=col_width-2)
                    cb.bind('<<ComboboxSelected>>', lambda e, r=row_number: self.update_material_info(r, "name"))
                    cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_combobox_change_purchase(e, r, "name"))
                    cb.grid(row=0, column=col_idx, sticky='ew')
                    row_entries.append(cb)
                elif col == "unit":
                    var = tk.StringVar()
                    cb = ttk.Combobox(row_frame, textvariable=var, values=[], width=col_width-2)
                    cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_unit_change(e, r))
                    cb.grid(row=0, column=col_idx, sticky='ew')
                    row_entries.append(cb)
                elif col == "Discount Type":
                    var = tk.StringVar()
                    cb = ttk.Combobox(row_frame, textvariable=var, 
                                    values=["Percentage", "Value"], 
                                    state="readonly",
                                    width=col_width-2)
                    cb.current(0)  # Default to Percentage
                    cb.grid(row=0, column=col_idx, sticky='ew')
                    row_entries.append(cb)
                elif col == "Discount Value":
                    var = tk.StringVar()
                    entry = tk.Entry(row_frame, textvariable=var, width=col_width+1)
                    entry.bind('<KeyRelease>', lambda e, r=row_number: self.calculate_totals(r))
                    entry.grid(row=0, column=col_idx, sticky='ew')
                    row_entries.append(entry)
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

        add_three_rows()

        # Buttons Frame
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=len(columns), pady=10, sticky='ew')
        
        tk.Button(button_frame, text=self.t("➕ Add 3 More Rows"), command=add_three_rows,
                bg='#4CAF50', fg='white').grid(row=0, column=0, padx=5, sticky='w')
        tk.Button(button_frame, text=self.t("💾 Save Invoice"), 
                command=lambda: self.save_invoice_purchase(purchases_col, suppliers_col,materials_col),
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
            full_list = self.product_codes
        else:
            full_list = self.product_names
            
        filtered = [item for item in full_list if value.lower() in str(item).lower()]
        event.widget['values'] = filtered
        
        # Auto-update if exact match found
        if value in full_list:
            self.update_material_info(row_idx, field_type)

    def handle_combobox_change_purchase(self, event, row_idx, field_type):
        """Handle changes in product code/name comboboxes"""
        value = event.widget.get().strip()
        
        # Clear dependent fields if value is empty
        if not value:
            self.clear_row_fields(row_idx)
            return
            
        # Filter combobox values
        if field_type == "code":
            full_list = self.product_codes
        else:
            full_list = self.product_names
            
        filtered = [item for item in full_list if value.lower() in str(item).lower()]
        event.widget['values'] = filtered
        
        # Auto-update if exact match found
        if value in full_list:
            self.update_product_info(row_idx, field_type)

    def handle_unit_change(self, event, row_idx):
        """Handle unit changes and clear price if unit changes"""
        unit = event.widget.get().strip()
        if not unit:
            # Clear Unit Price (index 8) if unit is cleared
            self.entries[row_idx][8].config(state='normal')
            self.entries[row_idx][8].delete(0, tk.END)
            self.entries[row_idx][8].config(state='readonly')
            self.calculate_totals(row_idx)

    def clear_row_fields(self, row_idx):
        """Clear all dependent fields in a row"""
        # Clear product name (index 1)
        self.entries[row_idx][1].set('')
        # Clear unit combobox (index 2)
        self.entries[row_idx][2].set('')
        self.entries[row_idx][2]['values'] = []
        # Clear Unit Price (index 8)
        self.entries[row_idx][8].config(state='normal')
        self.entries[row_idx][8].delete(0, tk.END)
        self.entries[row_idx][8].config(state='readonly')
        # Clear quantity fields (index 3: numbering, 4: QTY)
        self.entries[row_idx][3].delete(0, tk.END)
        self.entries[row_idx][4].delete(0, tk.END)
        # Clear calculated fields (index 7: Total_QTY, 9: Total_Price)
        self.entries[row_idx][7].config(state='normal')
        self.entries[row_idx][7].delete(0, tk.END)
        self.entries[row_idx][7].config(state='readonly')
        self.entries[row_idx][9].config(state='normal')
        self.entries[row_idx][9].delete(0, tk.END)
        self.entries[row_idx][9].config(state='readonly')
        # Reset discount fields (index 5: Type, 6: Value)
        self.entries[row_idx][5].set('Percentage')
        self.entries[row_idx][6].delete(0, tk.END)
        self.entries[row_idx][6].insert(0, '0')

    def update_product_info(self, row_idx, source):
        """Update fields based on code or name selection"""
        try:
            if source == "code":
                product_code = self.entries[row_idx][0].get().strip()
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
            
            # Update unit combobox values (index 2)
            unit_combobox = self.entries[row_idx][2]
            unit_combobox['values'] = product_info.get('units', [])
            if product_info.get('units'):
                unit_combobox.current(0)
            
            # Update Unit Price (index 8)
            self.entries[row_idx][8].config(state='normal')
            self.entries[row_idx][8].delete(0, tk.END)
            self.entries[row_idx][8].insert(0, f"{product_info.get('price', 0):.2f}")
            self.entries[row_idx][8].config(state='readonly')
            
            self.calculate_totals(row_idx)
        except Exception as e:
            messagebox.showerror("Update Error", f"Failed to update product info: {str(e)}")
            self.clear_row_fields(row_idx)
    def update_material_info(self, row_idx, source):
        """Update fields based on code or name selection"""
        try:
            print("1")
            if source == "code":
                material_code = self.entries[row_idx][0].get().strip()
                material_info = self.material_map.get(material_code, {})
                material_name = material_info.get('name', '')
                print("2")
            else:
                material_name = self.entries[row_idx][1].get().strip()
                material_code = self.name_to_code.get(material_name, '')
                material_info = self.material_map.get(material_code, {})
                print("3")

            # Clear fields if no product found
            if not material_code:
                self.clear_row_fields(row_idx)
                return

            # Update both dropdowns
            self.entries[row_idx][0].set(material_code)
            self.entries[row_idx][1].set(material_name)
            
            # Update unit combobox values (index 2)
            unit_combobox = self.entries[row_idx][2]
            unit_combobox['values'] = material_info.get('units', [])
            if material_info.get('units'):
                unit_combobox.current(0)
            
            # Update Unit Price (index 8)
            self.entries[row_idx][8].config(state='normal')
            self.entries[row_idx][8].delete(0, tk.END)
            self.entries[row_idx][8].insert(0, f"{material_info.get('price', 0):.2f}")
            self.entries[row_idx][8].config(state='readonly')
            
            self.calculate_totals(row_idx)
        except Exception as e:
            messagebox.showerror("Update Error", f"Failed to update product info: {str(e)}")
            self.clear_row_fields(row_idx)

    def calculate_totals(self, row_idx):
        try:
            # Get values using correct column indices
            numbering = float(self.entries[row_idx][3].get() or 0)  # index 3
            qty = float(self.entries[row_idx][4].get() or 0)        # index 4
            unit_price = float(self.entries[row_idx][8].get() or 0)  # index 8
            discount_type = self.entries[row_idx][5].get()           # index 5
            discount_value = float(self.entries[row_idx][6].get() or 0)  # index 6

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
            self.entries[row_idx][7].config(state='normal')
            self.entries[row_idx][7].delete(0, tk.END)
            self.entries[row_idx][7].insert(0, f"{total_qty:.2f}")
            self.entries[row_idx][7].config(state='readonly')
            
            # Update Total_Price (index 9)
            self.entries[row_idx][9].config(state='normal')
            self.entries[row_idx][9].delete(0, tk.END)
            self.entries[row_idx][9].insert(0, f"{final_price:.2f}")
            self.entries[row_idx][9].config(state='readonly')

        except ValueError as e:
            if "Percentage" in str(e):
                messagebox.showerror("Discount Error", str(e))
                self.entries[row_idx][6].delete(0, tk.END)
                self.entries[row_idx][6].insert(0, "0")
                
            # Reset calculated fields
            self.entries[row_idx][7].config(state='normal')
            self.entries[row_idx][7].delete(0, tk.END)
            self.entries[row_idx][7].config(state='readonly')
            
            self.entries[row_idx][9].config(state='normal')
            self.entries[row_idx][9].delete(0, tk.END)
            self.entries[row_idx][9].config(state='readonly')

############################ Main Functions ########################################
    def new_employee(self, user_role):
        self.table_name.set("Employees")
        for widget in self.root.winfo_children():
            widget.destroy()
        # تحميل صورة الخلفية
        self.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.display_general_table(self.employees_collection, "Employees")
    
    def new_supplier(self, user_role):
        self.table_name.set("Suppliers")
        for widget in self.root.winfo_children():
            widget.destroy()
        self.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.display_general_table(self.suppliers_collection, "Suppliers")
    
    def new_customer(self, user_role):
        self.table_name.set("Customers")
        for widget in self.root.winfo_children():
            widget.destroy()

        self.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.display_general_table(self.customers_collection, "Customers")

    def new_products(self, user_role):
        self.table_name.set("Products")
        for widget in self.root.winfo_children():
            widget.destroy()
    
        self.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.display_general_table(self.products_collection, "Products")
    
    def new_material(self, user_role):
        self.table_name.set("Materials")
        for widget in self.root.winfo_children():
            widget.destroy()
    
        self.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.display_general_table(self.materials_collection, "Materials")

############################ Main Functions ########################################
    def display_table(self):
        self.image_refs.clear()
        collection_name = self.table_name.get()
        search_query = self.search_query.get()
        
        current_collection = self.get_collection_by_name(collection_name)

        for row in self.tree.get_children():
            self.tree.delete(row)
        
        try:
            # Fetch all documents
            if search_query:
                # Create a dynamic query based on the search term
                first_document = current_collection.find_one()
                if first_document:
                    search_fields = self.get_fields_by_name(collection_name)
                    or_conditions = [{"$expr": {"$regexMatch": {"input": {"$toString": f"${field}"}, "regex": search_query, "options": "i"}}} for field in search_fields]
                    data = list(current_collection.find({"$or": or_conditions}).sort("Id", 1))
                else:
                    data = [] # No documents to search in
            else:
                data = list(current_collection.find().sort("Id", 1))

            if data:
                columns = self.get_fields_by_name(collection_name)
                self.tree["columns"] = columns

                for col in columns:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=152, anchor="center", stretch=False)

                self.tree.column("#0", width=152, anchor="center")
                self.tree.heading("#0", text="Image")

                for row_data in data:
                    values = []
                    for col in columns:
                        val = row_data.get(col, '')
                        if 'pic' in col.lower():
                            if isinstance(val, str) and val.startswith("http"):
                                print(val)  # Optional: print the URL
                            
                        if 'date' in col.lower() and isinstance(val, datetime):
                            val = val.strftime("%d-%m-%Y")
                        values.append(val)
                            
                    self.tree.insert("", "end", values=values)
            else:
                # Show placeholder column and row
                self.tree["columns"] = ("No Data",)
                self.tree.heading("No Data", text="No Data Available")
                self.tree.column("No Data", width=300, anchor="center", stretch=True)
                self.tree.insert("", "end", values=("This collection has no documents.",))
                return

        except Exception as e:
            messagebox.showerror("Error", f"Error displaying data:\n{e}")

    #TODO fix search feature ... start fixing add,edit and delete
    def display_general_table(self, current_collection, collection_name):
        img_label= None
        columns = self.get_fields_by_name(collection_name)
        
        normal_fields = [label for label in columns if label != "Id" and "pic" not in label.lower()]
        pic_fields = [label for label in columns if "pic" in label.lower()]
        ordered_fields = normal_fields + pic_fields

        main_frame = tk.Frame(root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=50)


        # ==== 1. Create scrollable form frame ====
        form_container = tk.Frame(main_frame)
        form_container.pack(side="left", fill="y", padx=10, pady=10)

        canvas = tk.Canvas(form_container, width=350)   # Set width for form
        scrollbar = tk.Scrollbar(form_container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.pack(side="left", fill="y", expand=False)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame inside canvas (holds labels + entries)
        form_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=form_frame, anchor='nw')

        # Ensure scrollregion resizes automatically
        def on_frame_config(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        form_frame.bind("<Configure>", on_frame_config)

        # Optional — enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # Enable scrolling when mouse hovers inside form_frame
        def enable_scrolling(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
                
        def disable_scrolling(event):
            canvas.unbind_all("<MouseWheel>")

        # Bind mouse hovering for scroll enable/disable
        form_container.bind("<Enter>", enable_scrolling)
        form_container.bind("<Leave>", disable_scrolling)

        self.entries = {}
        for i, label in enumerate(ordered_fields):
            if label == "Id":
                continue
            
            tk.Label(form_frame, text=self.t(label), font=("Arial", 12), anchor="w").grid(row=i, column=0, sticky="w", pady=5)

            if "date" in label.lower():
                entry = DateEntry(form_frame, font=("Arial", 12), date_pattern='dd-MM-yyyy', width=18)
                entry.grid(row=i, column=1, pady=5)
                self.entries[label] = entry
            elif "pic" in label.lower():
                frame = tk.Frame(form_frame)
                frame.grid(row=i, column=1, pady=5)
                
                # Image Label in a *new row* below the current field
                img_label = tk.Label(form_frame)
                img_label.grid(row=i + 1, column=0, columnspan=3, pady=5)

                def browse_file(e=entry, img_lbl=img_label):  # Pass the current entry as argument
                    filepath = filedialog.askopenfilename(
                        title="Select a file",
                        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All files", "*.*")]
                    )
                    if filepath:
                        load_image_preview(filepath, img_lbl)

                browse_btn = tk.Button(frame, text="Browse",width=10, command=lambda e=entry: browse_file(e))
                browse_btn.pack(side="left", padx=5)
                self.entries[label] = img_label
            else:
                entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
                entry.grid(row=i, column=1, pady=5)
                self.entries[label] = entry


        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True)

        search_frame = tk.Frame(right_frame)
        search_frame.pack(fill="x", pady=(0, 10))

        self.selected_field = tk.StringVar()
        self.selected_field.set(ordered_fields[0])
        field_dropdown = ttk.Combobox(search_frame, textvariable=self.selected_field, values=columns, width=14)
        field_dropdown.pack(side="left", padx=(0, 5))

        local_search_query = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=local_search_query)
        search_entry.pack(side="left", padx=(0, 5))

        table_frame = tk.Frame(right_frame)
        table_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(table_frame, columns=ordered_fields, show="headings")
        for col in ordered_fields:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", stretch=True)
        tree.pack(fill="both", expand=True)
        tree.bind("<<TreeviewSelect>>", lambda event: self.on_tree_selection(event, tree, columns, collection_name, img_label)) #Bind tree selection to an event handler

        horizontal_scrollbar = ttk.Scrollbar(tree, orient="horizontal", command=tree.xview)
        horizontal_scrollbar.pack(side="bottom", fill="x")
        tree.configure(xscrollcommand=horizontal_scrollbar.set)

        vertical_scrollbar = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
        vertical_scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=vertical_scrollbar.set)

        # Search button now refreshes table, doesn't rebuild everything!
        tk.Button(
            search_frame,
            text=self.t("Search"),
            command=lambda: self.refresh_generic_table(tree, current_collection, collection_name, local_search_query.get())
        ).pack(side="left")
        
        # Bottom buttons
        button_frame = tk.LabelFrame(root, text="Actions", padx=10, pady=10, font=("Arial", 12, 'bold'))
        button_frame.pack(pady=10)

        btn_add = tk.Button(button_frame, text="Add Entry", font=("Arial", 12), width=15, command=lambda: self.add_generic_entry(tree, current_collection,collection_name))
        btn_edit = tk.Button(button_frame, text="Update Entry", font=("Arial", 12), width=15, command=lambda: self.edit_generic_entry(tree, current_collection,collection_name))
        btn_delete = tk.Button(button_frame, text="Delete Entry", font=("Arial", 12), width=15, command=lambda: self.delete_generic_entry(tree, current_collection))
        btn_deselect = tk.Button(button_frame, text="Deselect Entry", font=("Arial", 12), width=15, command=lambda:self.deselect_entry(tree))

        btn_add.grid(row=0, column=0, padx=10)
        btn_edit.grid(row=0, column=1, padx=10)
        btn_delete.grid(row=0, column=2, padx=10)
        btn_deselect.grid(row=0, column=3, padx=10)

        # Load initial table content
        self.refresh_generic_table(tree, current_collection, collection_name, search_text="")

    def on_tree_selection(self, event, tree, columns, collection_name, img_label):
        first_document = None
        current_collection = None
        id_index = 0
        selected_item = tree.selection()
        if not selected_item:
            for entry in self.entries.values():
                entry.delete(0, tk.END)
            # Also clear image preview(s)
            if(img_label):
                img_label.config(image="")
                img_label.image = None
            return
        try:
            lower_columns = [col.lower() for col in columns]
            if "id" in lower_columns:
                id_index = columns.index("Id")  # Dynamically get the index of "Id" #TODO need something different to loop on
            elif any('code' in col for col in lower_columns):
                for idx, col in enumerate(lower_columns):
                    if 'code' in col:
                        id_index = idx
                        break
            unique_id = tree.item(selected_item)['values'][id_index]
            print(f"unique_id type: {get_type(unique_id)}")
            current_collection = self.get_collection_by_name(collection_name)
            first_document = current_collection.find_one({columns[id_index]: unique_id})

            if not first_document and isinstance(unique_id, str):
                try:
                    first_document = current_collection.find_one({columns[id_index]: int(unique_id)})
                except ValueError:
                    pass

            # If not found, and type is int, try converting to str
            elif not first_document and isinstance(unique_id, int):
                first_document = current_collection.find_one({columns[id_index]: str(unique_id)})

        except IndexError:
            return


        for field, entry in self.entries.items():
            value = first_document.get(field, "")
            if isinstance(value, datetime):
                value = value.strftime('%d-%m-%Y')
                entry.delete(0, tk.END)
                entry.insert(0, value)
            elif field == "Units" and isinstance(value, list):
                value_str = ','.join(map(str, value))
                entry.delete(0, tk.END)
                entry.insert(0, value_str)
            # If it's a pic field, load preview
            elif "pic" in field.lower():
                if img_label and value:
                    load_image_preview_from_url(value, img_label)
            else:
                entry.delete(0, tk.END)
                entry.insert(0, value)

    def refresh_generic_table(self, tree, current_collection, collection_name, search_text):
        try:
            # Clear existing rows
            for row in tree.get_children():
                tree.delete(row)

            if search_text:
                selected_field = self.selected_field.get()
                first_document = current_collection.find_one()
                if first_document:
                    search_fields = self.get_fields_by_name(collection_name)
                    or_conditions = [{"$expr": {"$regexMatch": {"input": {"$toString": f"${selected_field}"}, "regex": search_text, "options": "i"}}} for field in search_fields]
                    data = list(current_collection.find({"$or": or_conditions}).sort("Id", 1))
                else:
                    data = []
            else:
                data = list(current_collection.find().sort("Id", 1))

            if data:
                columns = self.get_fields_by_name(collection_name)
                if '_id' in columns:
                    columns.remove('_id')

                tree["columns"] = columns
                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=152, anchor="center", stretch=False)

                for row_data in data:
                    units = row_data.get('Units', [])
                    
                    # If Units is a non-empty list
                    if isinstance(units, list) and len(units) > 0:
                        for unit_value in units:
                            values = []
                            for col in columns:
                                value = row_data.get(col, '')
                                
                                if col == 'Units':
                                    value = unit_value  # Set current unit value
                                
                                elif isinstance(value, datetime):
                                    value = value.strftime('%d-%m-%Y')
                                
                                values.append(value)
                            
                            tree.insert("", "end", values=values)
                    
                    else:
                        # Fallback to insert normally if Units is not a list or is empty
                        values = []
                        for col in columns:
                            value = row_data.get(col, '')
                            if isinstance(value, datetime):
                                value = value.strftime('%d-%m-%Y')
                            values.append(value)
                        
                        tree.insert("", "end", values=values)
            else:
                tree["columns"] = ("No Data",)
                tree.heading("No Data", text="No Data Available")
                tree.column("No Data", width=300, anchor="center", stretch=True)
                tree.insert("", "end", values=("This collection has no documents.",))

        except Exception as e:
            messagebox.showerror("Error", f"Error displaying data: {e}")

    def add_generic_entry(self, tree, current_collection, collection_name):
        # collection_name = self.table_name.get()
        fields = self.get_fields_by_name(collection_name)

        new_entry = {}
        for field, widget in self.entries.items():
            if field == "Id":
                continue  # Skip Id

            if "date" in field.lower():
                value = widget.get()
                if value:
                    try:
                        value_date = datetime.strptime(value, '%d-%m-%Y').date()
                        value = datetime.combine(value_date, time.min)
                    except Exception as e:
                        messagebox.showerror("Error", f"Invalid date format for {field}: {e}")
                        return
                else:
                    messagebox.showwarning("Warning", f"Please enter a value for {field}")
                    return
            elif "pic" in field.lower():
                local_image_path = getattr(widget, 'image_path', None)
                if not local_image_path:
                    return  # User cancelled
                try:
                    value = upload_file_to_cloudinary(local_image_path)
                except Exception as e:
                    messagebox.showerror("Upload Error", f"Failed to upload image: {e}")
                    return
            elif any(word in field.lower() for word in ["stock_quantity","instapay","bank_account","e-wallet"]):
                value = widget.get()
                try: 
                    value = int(value)
                except Exception as e:
                    messagebox.showerror("Error", f"{field} should be a number")
                    return
            elif any(word in field.lower() for word in ["salary", "credit", "debit", "balance", "stock_quantity"]):
                value = widget.get()
                if not value:
                    messagebox.showwarning("Warning", f"Please enter a value for {field}")
                    return
                try: 
                    value = float(value)
                except Exception as e:
                    messagebox.showerror("Error", f"{field} should be a floating number")
                    return
            else:
                value = widget.get()
                if not value:
                    messagebox.showwarning("Warning", f"Please enter a value for {field}")
                    return
                if any(word in field.lower() for word in ["units"]):
                    # Parse comma-separated input to list
                    value = [item.strip() for item in value.split(',') if item.strip()]

            new_entry[field] = value

        try:
            # Generate unique Id
            if "Id" in fields:
                existing_ids = [doc["Id"] for doc in current_collection.find({}, {"Id": 1})]
                print(f"existing_ids{existing_ids}")
                new_id = max(existing_ids, default=0) + 1
                new_entry["Id"] = new_id

            current_collection.insert_one(new_entry)
            self.refresh_generic_table(tree, current_collection, collection_name, search_text="")
            messagebox.showinfo("Success", "Record added successfully")

            # Clear form fields after successful addition
            for field, widget in self.entries.items():
                if "date" in field.lower():
                    widget.set_date(datetime.now())
                elif "pic" in field.lower():
                    widget.config(image='')
                    widget.image = None
                else:
                    widget.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"Error adding record: {e}")
  
    def edit_generic_entry(self, tree, current_collection, collection_name):
        selected_item = tree.selection()
        unique_id = 0
        first_document = None
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to edit")
            return

        selected_data = tree.item(selected_item)["values"]
        if not selected_data:
            messagebox.showwarning("Warning", "No data found for selected record")
            return

        columns = tree["columns"]  # This returns a tuple/list of column names
        try:
            lower_columns = [col.lower() for col in columns]
            if "id" in lower_columns:
                id_index = columns.index("Id")  # Dynamically get the index of "Id" #TODO need something different to loop on
            elif any('code' in col for col in lower_columns):
                for idx, col in enumerate(lower_columns):
                    if 'code' in col:
                        id_index = idx
                        break
        except ValueError:
            messagebox.showerror("Error", "'Id' field not found in table columns")
            return

        record_id = selected_data[id_index]
        existing_record = current_collection.find_one({columns[id_index]: record_id})

        if not existing_record:
            try:
                record_id = str(record_id)
                existing_record = current_collection.find_one({columns[id_index]: record_id})
            except ValueError:
                pass

        if not existing_record:
            messagebox.showerror("Error", "Could not find record in database")
            return

        updated_entry = {}
        for field, widget in self.entries.items():
            if field == "Id":
                continue  # Skip Id

            existing_value = existing_record.get(field, None)

            if "date" in field.lower():
                value = widget.get()
                if value:
                    try:
                        value_date = datetime.strptime(value, '%d-%m-%Y').date()
                        value = datetime.combine(value_date, time.min)
                    except Exception as e:
                        messagebox.showerror("Error", f"Invalid date format for {field}: {e}")
                        return
                else:
                    value = existing_value  # Keep old date if no new input

            elif "pic" in field.lower():
                local_image_path = getattr(widget, 'image_path', None)

                if local_image_path:
                    try:
                        value = upload_file_to_cloudinary(local_image_path)
                    except Exception as e:
                        messagebox.showerror("Upload Error", f"Failed to upload image: {e}")
                        return
                else:
                    value = existing_value  # Keep old image URL if no new selection

            else:
                try:
                    value = widget.get()
                except Exception:
                    value = None  # For non-entry widgets (just in case)

                if not value:
                    value = existing_value  # Keep old text if no new input
                else:
                    if "units" in field.lower():
                        value = [item.strip() for item in value.split(',') if item.strip()]

            updated_entry[field] = value

        try:
            identifier_field = columns[id_index]
            result = current_collection.update_one({identifier_field: record_id}, {"$set": updated_entry})
            
            if result.modified_count > 0:
                messagebox.showinfo("Success", "Record updated successfully")
            else:
                messagebox.showinfo("Info", "No changes were made (record was identical)")

            # Refresh table
            # collection_name = self.table_name.get()
            self.refresh_generic_table(tree, current_collection, collection_name, search_text="")

            # Clear form fields after update
            for field, widget in self.entries.items():
                if "date" in field.lower():
                    widget.set_date(datetime.now())
                elif "pic" in field.lower():
                    widget.config(image='')
                    widget.image = None
                    widget.image_path = None
                else:
                    widget.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Error", f"Error updating record: {e}")

    def delete_generic_entry(self, tree, current_collection):
        selected_item = tree.selection()
        id_index = None
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to delete")
            return

        columns = tree["columns"]  # Tuple/list of column names
        try:
            lower_columns = [col.lower() for col in columns]

            # Find which column is used as identifier (id / code)

            if "id" in lower_columns:
                id_index = columns.index("Id")
            elif any('code' in col for col in lower_columns):
                for idx, col in enumerate(lower_columns):
                    if 'code' in col:
                        id_index = idx
                        break

            if id_index is None:
                messagebox.showerror("Error", "Unable to determine identifier column.")
                return

            field_name = columns[id_index]
            unique_id = tree.item(selected_item)["values"][id_index]

        except (IndexError, ValueError):
            messagebox.showerror("Error", "Unable to read selected row data.")
            return

        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            return

        try:
            # ARRAY_FIELDS = ['units']  # Fields you want to treat as arrays (custom handling)

            # Step 1: Find the document based on the selected field (id/code)
            query = {field_name: unique_id}
            document = current_collection.find_one(query)
            
            if not document:
                try:
                    query = {field_name: str(unique_id)}
                    document = current_collection.find_one(query)
                except ValueError:
                    pass

            if not document:
                messagebox.showwarning("Not Found", "No matching record found to delete.")
                return

            # Step 2: Check if document contains any ARRAY_FIELDS (like 'units')
            handled = False
            values = tree.item(selected_item)["values"]
            
            if("Units" in columns):
                index = columns.index('Units')
                unit_value = values[index]

            for array_field in ARRAY_FIELDS:
                units_list = document.get(array_field, None)
                print(f"units_list: {isinstance(units_list, list)} , unique_id {unique_id}")
                if isinstance(units_list, list):
                    # Found Units array and unique_id is inside → handle it
                    handled = True
                    if len(units_list) > 1:
                        update_result = current_collection.update_one(
                            {"_id": document["_id"]},
                            {"$pull": {array_field: unit_value}}
                        )
                        if update_result.modified_count > 0:
                            self.deselect_entry(tree)
                            self.refresh_generic_table(tree, current_collection, self.table_name.get(), search_text="")
                            messagebox.showinfo("Success", f"Unit '{unique_id}' removed from record.")
                        else:
                            messagebox.showwarning("Warning", "No changes were made to the document.")
                    else:
                        delete_result = current_collection.delete_one({"_id": document["_id"]})
                        if delete_result.deleted_count > 0:
                            self.deselect_entry(tree)
                            self.refresh_generic_table(tree, current_collection, self.table_name.get(), search_text="")
                            messagebox.showinfo("Success", "Record deleted successfully.")
                        else:
                            messagebox.showwarning("Warning", "No matching record found to delete.")
                    return  # After handling Units logic, exit

            # Step 3: If no ARRAY_FIELDS handling triggered → do standard delete
            if not handled:
                delete_result = current_collection.delete_one(query)
                if delete_result.deleted_count > 0:
                    self.deselect_entry(tree)
                    self.refresh_generic_table(tree, current_collection, self.table_name.get(), search_text="")
                    messagebox.showinfo("Success", "Record deleted successfully.")
                else:
                    messagebox.showwarning("Warning", "No matching record found to delete.")

        except Exception as e:
            messagebox.showerror("Error", f"Error deleting record: {e}")         

    def add_entry(self):
        collection_name = self.table_name.get()
        current_collection = self.get_collection_by_name(collection_name)

        new_entry = {}
        fields = self.get_fields_by_name(collection_name)
    
        try:
            latest_entry = current_collection.find_one(sort=[("Id", -1)])  # Sort by Id descending
            new_id = (latest_entry["Id"] + 1) if latest_entry else 1
        except Exception:
            new_id = 1

        new_entry["Id"] = new_id

        for field in fields:
            if field == "Id":
                continue
            if "date" in field.lower():
                dialog = tk.Toplevel(self.root)  # Create a Toplevel for date input
                dialog.transient(self.root)
                dialog.grab_set()
                dialog.title(f"Enter value for {field}")

                date_label = tk.Label(dialog, text=f"Enter {field}:")
                date_label.pack(padx=10, pady=5)

                date_entry = DateEntry(dialog, font=("Arial", 12), date_pattern='dd-MM-yyyy')
                date_entry.pack(padx=10, pady=5)

                selected_date = tk.StringVar()

                def on_ok():
                    selected_date_obj = date_entry.get_date()
                    selected_date_str = selected_date_obj.strftime('%d-%m-%Y')
                    selected_date.set(selected_date_str)
                    dialog.destroy()

                ok_button = tk.Button(dialog, text="OK", command=on_ok)
                ok_button.pack(pady=5)
                ok_button.bind("<Return>", lambda event: ok_button.invoke())

                # Center the date selection dialog
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                x_position = (screen_width // 2) - (dialog_width // 2)
                y_position = (screen_height // 2) - (dialog_height // 2)
                dialog.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")
                self.root.wait_window(dialog)

                value = selected_date.get()
                if value:
                    try:
                        value = datetime.strptime(value, '%d-%m-%Y').date()
                        value = datetime.combine(value, time.min) #Must do this to be comaptible with mongodb's Date type 
                    except Exception as e:
                        print(f"ValueError: {e}")
                        messagebox.showerror("Error", f"Invalid date format for {field}")
                        return
                else:
                    return  # User cancelled
            elif "pic" in field.lower():
                file_path = filedialog.askopenfilename(title=f"Select image for {field}",
                                                    filetypes=[("Image files", "*.jpg *.jpeg *.png")])
                if not file_path:
                    return  # User cancelled
                try:
                    value = upload_file_to_cloudinary(file_path)
                except Exception as e:
                    messagebox.showerror("Upload Error", f"Failed to upload image: {e}")
                    return
            else:
                dialog = AlwaysOnTopInputDialog(self.root, f"Enter value for {field}:")
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

        #TODO fix this ID no longer available in tree
        try:
            unique_id = self.tree.item(selected_item)['values'][2]  # Assuming this holds the custom unique ID
        except IndexError:
            messagebox.showerror("Error", "Unable to read selected row data.")
            return
        
        # Get the fields to edit (excluding _id)
        first_document = current_collection.find_one({"Id": unique_id})
        if not first_document:
            messagebox.showerror("Error", "Could not retrieve record for editing.")
            return

        fields = self.get_fields_by_name(collection_name)
        updated_values = {}

        for field in fields:
            if field == "Id":
                continue
            if "date" in field.lower():
                dialog = tk.Toplevel(self.root)  # Create a Toplevel for date input
                dialog.transient(self.root)
                dialog.grab_set()
                dialog.title(f"Enter value for {field}")

                date_label = tk.Label(dialog, text=f"Enter {field}:")
                date_label.pack(padx=10, pady=5)

                date_entry = DateEntry(dialog, font=("Arial", 12), date_pattern='dd-MM-yyyy')
                date_entry.pack(padx=10, pady=5)

                selected_date = tk.StringVar()

                def on_ok():
                    selected_date_obj = date_entry.get_date()
                    selected_date_str = selected_date_obj.strftime('%d-%m-%Y')
                    selected_date.set(selected_date_str)
                    dialog.destroy()

                ok_button = tk.Button(dialog, text="OK", command=on_ok)
                ok_button.pack(pady=5)
                ok_button.bind("<Return>", lambda event: ok_button.invoke())

                # Center the date selection dialog
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                x_position = (screen_width // 2) - (dialog_width // 2)
                y_position = (screen_height // 2) - (dialog_height // 2)
                dialog.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")
                self.root.wait_window(dialog)

                value = selected_date.get()
                if value:
                    try:
                        value = datetime.strptime(value, '%d-%m-%Y').date()
                        value = datetime.combine(value, time.min) #Must do this to be comaptible with mongodb's Date type 

                    except Exception as e:
                        print(f"ValueError: {e}")
                        messagebox.showerror("Error", f"Invalid date format for {field}")
                        return
                else:
                    return  # User cancelled

            else:
                dialog = AlwaysOnTopInputDialog(self.root, f"Enter value for {field}:")
                value = dialog.get_result()
                if value is None:
                    return

            updated_values[field] = value

        try:
            current_collection.update_one({"Id": unique_id}, {"$set": updated_values})
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

        try:
            unique_id = self.tree.item(selected_item)['values'][2]  # Assuming this holds the custom unique ID
        except IndexError:
            messagebox.showerror("Error", "Unable to read selected row data.")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this record?"):
            try:
                delete_result = current_collection.delete_one({"Id": unique_id})
                if delete_result.deleted_count == 0:
                    messagebox.showwarning("Not Found", "No matching record found to delete.")
                else:
                    self.display_table()
                    messagebox.showinfo("Success", "Record deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting record: {e}")

############################ Utility Functions ########################################
    def check_access_and_open(self, role):
        allowed_roles = ["admin"]  # Define roles that can access this
        if role in allowed_roles:
            # self.manage_old_database_window(db_name, table_name)
            self.manage_database_window()
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
        elif collection_name =="Materials":
            return self.materials_collection
        elif collection_name =="Purchases":
            return self.purchases_collection
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
            return ["product_name", "category", "stock_quantity", "Specs", "Unit_Price", "product_code", "Units", "prod_pic"]
        
        elif collection_name == "Sales":
            return ["product_code", "Product_name", "unit", "QTY", "numbering","Total_QTY","Unit_Price","Total Price","Date","Reciept_Number","Customer_name","Customer_code"]

        # elif collection_name == "Sales_Header":
        #     return [self.t("Product_code"), self.t("product_name"), self.t("unit"),self.t("numbering"),self.t("QTY"),self.t("Discount Type"),self.t("Discount Value"),self.t("Total_QTY"),self.t("Unit_Price"),self.t("Total_Price")]
       
        # elif collection_name == "Materials_Header":
        #     return [self.t("Material_code"), self.t("Material_name"), self.t("unit"),self.t("numbering"),self.t("QTY"),self.t("Discount Type"),self.t("Discount Value"),self.t("Total_QTY"),self.t("Unit_Price"),self.t("Total_Price")]
      
        elif collection_name == "Sales_Header":
            return ["Product_code", "product_name", "unit","numbering","QTY","Discount Type","Discount Value","Total_QTY","Unit_Price","Total_Price"]
       
        elif collection_name == "Materials":
            return ["material_name", "category","stock_quantity","specs","material_code","Units","material_pic","Unit_Price"]

        elif collection_name == "Materials_Header":
            return ["Material_code", "Material_name", "unit","numbering","QTY","Discount Type","Discount Value","Total_QTY","Unit_Price","Total_Price"]
       
        elif collection_name == "Customers":
            return ["Name", "Phone_number1", "Phone_number2", "Code", "Last_purchase_date" , "Purchase_mgr_number", "Financial_mgr_number", "Purchase_mgr_name", 
                    "Financial_mgr_name", "Email", "Company_address", "Extra_address", "Maps_link", "Bank_account",
                    "Instapay", "E_wallet", "Accountant_name", "Accountant_number", "Sales_grade", "Growth_grade", "Frequency_grade", "Credit",
                    "Debit", "Balance", "Sales"]
        
        elif collection_name == "Suppliers":
            return ["Name", "Phone_number1", "Phone_number2", "Code", "Last_purchase_date" , "Purchase_mgr_number", "Financial_mgr_number", "Purchase_mgr_name", 
                    "Financial_mgr_name", "Email", "Company_address", "Extra_address", "Maps_link", "Bank_account",
                    "Instapay", "E_wallet", "Accountant_name", "Accountant_number", "Sales_grade", "Growth_grade", "Frequency_grade", "Credit",
                    "Debit", "Balance", "Sales"]
        
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

    def update_search_purchase(self, event, collection):
        # Cancel any previous scheduled search **only if valid**
        if hasattr(self, '_after_id') and self._after_id is not None:
            try:
                self.root.after_cancel(self._after_id)
            except ValueError:
                pass  # Ignore if it was already canceled
        
        # Mark that user is typing
        self.is_typing = True
        
        # Schedule the search with the current text
        self._after_id = self.root.after(300, self.perform_search_purchase, collection)

    def perform_search(self, collection):
        # Mark that user is not typing anymore
        self.is_typing = False

        search_term = self.customer_name_var.get()

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
    def perform_search_purchase(self, collection):
        # Mark that user is not typing anymore
        self.is_typing = False

        search_term = self.supplier_name_var.get()

        # If search term is empty, you can clear the combobox
        if search_term == "":
            self.supplier_cb['values'] = []
            return

        # Perform search
        filtered_suppliers = [supp['Name'] for supp in collection.find(
            {"Name": {"$regex": f"^{search_term}", "$options": "i"}}
        )]
        
        # Update combobox values only if user is not typing
        if not self.is_typing:
            self.supplier_cb['values'] = filtered_suppliers
            
            if filtered_suppliers:
                self.supplier_cb.event_generate('<Down>')
            else:
                self.supplier_cb.event_generate('<Up>')  # Close dropdown
    
    def generate_invoice_number(self):
        """توليد رقم فاتورة تسلسلي"""
        try:
            print(0)
            sales_col = self.get_collection_by_name('Sales')
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
                        print(2)
                    except (ValueError, IndexError):
                        last_number = 0
                        print(3)
            
            new_number = last_number + 1
            # print(4)
            return f"INV-{new_number:04d}"
        
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل توليد الرقم التسلسلي: {str(e)}")
            return None
    def generate_invoice_number_purchase(self):
        """توليد رقم فاتورة تسلسلي"""
        try:
            print(0)
            purchaes_col = self.get_collection_by_name('Purchases')
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
                        print(2)
                    except (ValueError, IndexError):
                        last_number = 0
                        print(3)
            
            new_number = last_number + 1
            # print(4)
            return f"INV-{new_number:04d}"
        
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل توليد الرقم التسلسلي: {str(e)}")
            return None

    def save_invoice(self, sales_col, customers_col, products_col):
        """حفظ الفاتورة مع التحقق من المخزون وتحديثه"""
        try:
            # التحقق من وجود بيانات العميل
            customer_name = self.customer_name_var.get().strip()
            if not customer_name:
                messagebox.showerror("خطأ", "يرجى اختيار عميل")
                return

            # البحث عن العميل في قاعدة البيانات
            customer = customers_col.find_one({"Name": customer_name})
            if not customer:
                messagebox.showerror("خطأ", "العميل غير مسجل!")
                return

            # التحقق من المبلغ المدفوع
            payed_cash = float(self.payed_cash_var.get() or 0)
            # if payed_cash < 0:
            #     messagebox.showerror("خطأ", "المبلغ المدفوع لا يمكن أن يكون سالبًا!")
            #     return

            # جمع بيانات العناصر والتحقق من المخزون
            items = []
            total_amount = 0.0
            stock_updates = {}
            
            for row_idx, row in enumerate(self.entries):
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
                    if total_qty > stock:
                        messagebox.showerror("نقص في المخزون", 
                            f"الكمية المطلوبة ({total_qty}) تتجاوز المخزون ({stock}) للمنتج {product_code}")
                        return

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
            invoice_number = self.generate_invoice_number()
            if not invoice_number:
                return
            # إنشاء بيانات الفاتورة الكاملة
            invoice_data = {
                "Receipt_Number": invoice_number,
                "Date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "Customer_info": {
                    "code": customer.get("Code", "CUST-001"),
                    "name": customer.get("Name", "غير معروف"),
                    "phone1": customer.get("Phone_number1", ""),
                    "phone2": customer.get("Phone_number2", ""),
                    "address": customer.get("Company_address", "")
                },
                "Items": items,
                "Financials": {
                    "Net_total": total_amount,
                    "Previous_balance": customer.get("Balance", 0),
                    "Total_balance": total_amount + customer.get("Balance", 0),
                    "Payed_cash": payed_cash,
                    "Remaining_balance": (total_amount + customer.get("Balance", 0)) - payed_cash,
                    "Payment_method": self.payment_method_var.get()
                },
                "PDF_Path": "",
                
            }

            # تحديث المخزون
            for code, new_stock in stock_updates.items():
                products_col.update_one(
                    {"product_code": code},
                    {"$set": {"stock_quantity": new_stock}}
                )

            # تحديث بيانات العميل
            new_balance = (customer.get("Balance", 0) + total_amount) - payed_cash
            customers_col.update_one(
                {"_id": customer["_id"]},
                {
                    "$set": {
                        "Last_purchase_date": datetime.now(),
                        "Balance": new_balance
                    },
                    "$inc": {
                        "Sales": 1,
                        "Debit": total_amount,
                        "Credit": payed_cash
                    }
                }
            )

            # توليد ملف PDF
            pdf_path = self.generate_pdf(invoice_data)
            if not pdf_path:
                return
            # إضافة مسار PDF للبيانات
            invoice_data["PDF_Path"] = pdf_path
            
            # حفظ الفاتورة في قاعدة البيانات
            sales_col.insert_one(invoice_data)

            messagebox.showinfo("نجاح", f"تم حفظ فاتورة البيع رقم {invoice_data['Receipt_Number']}")
            self.clear_invoice_form()

        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في العملية: {str(e)}")
            # logging.error(f"Invoice Error: {str(e)}")
    def save_invoice_purchase(self, purchase_col, suppliers_col, materials_col):
        """حفظ الفاتورة مع التحقق من المخزون وتحديثه"""
        try:
            # التحقق من وجود بيانات العميل
            supplier_name = self.supplier_name_var.get().strip()
            if not supplier_name:
                messagebox.showerror("خطأ", "يرجى اختيار عميل")
                return

            # البحث عن العميل في قاعدة البيانات
            supplier = suppliers_col.find_one({"Name": supplier_name})
            if not supplier:
                messagebox.showerror("خطأ", "العميل غير مسجل!")
                return

            # التحقق من المبلغ المدفوع
            payed_cash = float(self.payed_cash_var.get() or 0)
            # if payed_cash < 0:
            #     messagebox.showerror("خطأ", "المبلغ المدفوع لا يمكن أن يكون سالبًا!")
            #     return

            # جمع بيانات العناصر والتحقق من المخزون
            items = []
            total_amount = 0.0
            stock_updates = {}
            
            for row_idx, row in enumerate(self.entries):
                material_code = row[0].get().strip()
                if not material_code:
                    continue

                material = materials_col.find_one({"material_code": material_code})
                if not material:
                    messagebox.showerror("خطأ", f"المنتج {material_code} غير موجود!")
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
                    if total_qty > stock:
                        messagebox.showerror("نقص في المخزون", 
                            f"الكمية المطلوبة ({total_qty}) تتجاوز المخزون ({stock}) للمنتج {material_code}")
                        return

                    stock_updates[material_code] = stock - total_qty
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
            invoice_number = self.generate_invoice_number_purchase()
            if not invoice_number:
                return
            # إنشاء بيانات الفاتورة الكاملة
            invoice_data = {
                "Receipt_Number": invoice_number,
                "Date": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "supplier_info": {
                    "code": supplier.get("Code", "CUST-001"),
                    "name": supplier.get("Name", "غير معروف"),
                    "phone1": supplier.get("Phone_number1", ""),
                    "phone2": supplier.get("Phone_number2", ""),
                    "address": supplier.get("Company_address", "")
                },
                "Items": items,
                "Financials": {
                    "Net_total": total_amount,
                    "Previous_balance": supplier.get("Balance", 0),
                    "Total_balance": total_amount + supplier.get("Balance", 0),
                    "Payed_cash": payed_cash,
                    "Remaining_balance": (total_amount + supplier.get("Balance", 0)) - payed_cash,
                    "Payment_method": self.payment_method_var.get()
                },
                "PDF_Path": "",
                
            }

            # تحديث المخزون
            for code, new_stock in stock_updates.items():
                materials_col.update_one(
                    {"product_code": code},
                    {"$set": {"stock_quantity": new_stock}}
                )

            # تحديث بيانات العميل
            new_balance = (supplier.get("Balance", 0) + total_amount) - payed_cash
            suppliers_col.update_one(
                {"_id": supplier["_id"]},
                {
                    "$set": {
                        "Last_purchase": datetime.now(),
                        "Balance": new_balance
                    },
                    "$inc": {
                        "Sales": 1,
                        "Debit": total_amount,
                        "Credit": payed_cash
                    }
                }
            )

            # توليد ملف PDF
            pdf_path = self.generate_pdf_purchase(invoice_data)
            if not pdf_path:
                return
            # إضافة مسار PDF للبيانات
            invoice_data["PDF_Path"] = pdf_path
            
            # حفظ الفاتورة في قاعدة البيانات
            purchase_col.insert_one(invoice_data)

            messagebox.showinfo("نجاح", f"تم حفظ فاتورة الشراء رقم {invoice_data['Receipt_Number']}")
            print(3)
            self.clear_invoice_form_purchase()
            print(4)
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في العملية: {str(e)}")
            # logging.error(f"Invoice Error: {str(e)}")

    def clear_invoice_form(self):
            """تنظيف جميع حقول الفاتورة"""
            try:
                # تنظيف Combobox العميل
                self.customer_name_var.set('')
                
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
    def clear_invoice_form_purchase(self):
            """تنظيف جميع حقول الفاتورة"""
            try:
                # تنظيف Combobox العميل
                self.supplier_name_var.set('')
                
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
                self.new_Purchase_invoice(self.user_role)
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل في تنظيف الحقول: {str(e)}")
                
    def generate_pdf(self, invoice_data):
        """توليد ملف PDF بحجم A5 بتنسيق عربي مطابق للنموذج"""
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
            file_name = f"فاتورة بيع_{str(invoice_data['Receipt_Number']).replace("INV-", "").strip()}.pdf"
            pdf_path = os.path.join(desktop, file_name)

            # إعداد مستند PDF
            c = canvas.Canvas(pdf_path, pagesize=A5)
            width, height = A5
            c.setFont("Arabic", 12)

            # إضافة الشعار
            logo_path = os.path.join("Static", "images", "Logo.jpg")
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
            c.rect(frame_x, frame_y, frame_width, frame_height)
            
            # كتابة العنوان المركزي
            c.setFont("Arabic", 12)  # تأكد من وجود خط عريض
            title_x = width / 2
            title_y = height - 2.2*cm
            c.drawCentredString(title_x, title_y, format_arabic(invoice_title))

            # ========== معلومات الشركة ==========
            company_info = [
                "      حسن سليم",
                "للمنتجات البلاستيكية"
            ]
            
            y_position = height - 2*cm
            c.setFont("Arabic", 12)
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
                # text = f"{format_arabic(field)} {format_arabic(value)}"
                c.drawRightString(width - 0.4*cm, customer_y, format_arabic(line))
                customer_y -= 0.8*cm

            # ========== جدول العناصر ==========
            headers = ["كود الصنف","     الصنف", "العدد", "الوحدة", "سعر الوحدة", "الكمية", "الإجمالي"]
            col_positions = [
                width - 0.4*cm,    # كود الصنف
                width - 2*cm,    # الصنف
                width - 5.5*cm,    # العدد
                width - 7.5*cm,    # الوحدة
                width - 9.5*cm,    # السعر
                width - 11.5*cm,     # الكمية
                width - 13*cm      # الإجمالي
            ]
            
            # رأس الجدول
            table_y = customer_y - 0.25*cm
            c.setFont("Arabic", 10)
            for i, header in enumerate(headers):
                c.drawRightString(col_positions[i], table_y, format_arabic(header))

            # بيانات الجدول
            c.setFont("Arabic", 8)
            row_height = 0.7*cm
            for item in invoice_data["Items"]:
                table_y -= row_height
                columns = [
                    item.get("Product_code", ""),
                    item.get("product_name",""),
                    str(item.get("numbering", "")),
                    item.get("Unit", ""),
                    f"{item.get('Unit_price', 0):.2f}",
                    str(item.get('QTY', 0)),
                    f"{item.get('Final_Price', 0):.2f}"
                ]
                for i, value in enumerate(columns):
                    c.drawRightString(col_positions[i], table_y, format_arabic(value))

            # ========== الإجماليات ==========
            totals_y = table_y - 1*cm
            totals = [
                ("صافي الفاتورة:", invoice_data['Financials']['Net_total']),
                ("حساب سابق:", invoice_data['Financials']['Previous_balance']),
                ("إجمالي الفاتورة:", invoice_data['Financials']['Total_balance']),
                ("المدفوع:", invoice_data['Financials']['Payed_cash']),
                ("الباقي:", invoice_data['Financials']['Remaining_balance'])
            ]
            
            c.setFont("Arabic", 12)
            for label, value in totals:
                text = f"{format_arabic(f'{value:,.2f}')} {format_arabic(label)}"
                c.drawRightString(width - 0.3*cm, totals_y, text)
                totals_y -= 0.8*cm

            # ========== التوقيعات ==========
            c.setFont("Arabic", 10)
            c.drawRightString(width - 2.2*cm, totals_y - 0.25*cm, format_arabic("____________________"))
            c.drawString(1.5*cm, totals_y - 0.25*cm, format_arabic("____________________"))
            
            c.save()
            pdf_path = self.upload_pdf_to_cloudinary(pdf_path)
            return pdf_path

        except Exception as e:
            messagebox.showerror("خطأ PDF", f"فشل في توليد الملف: {str(e)}")
            return None
    def generate_pdf_purchase(self, invoice_data):
        """توليد ملف PDF بحجم A5 بتنسيق عربي مطابق للنموذج"""
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
            file_name = f"فاتورة شراء_{invoice_data['Receipt_Number']}.pdf"
            pdf_path = os.path.join(desktop, file_name)

            # إعداد مستند PDF
            c = canvas.Canvas(pdf_path, pagesize=A5)
            width, height = A5
            c.setFont("Arabic", 12)

            # إضافة الشعار
            logo_path = os.path.join("Static", "images", "Logo.jpg")
            if os.path.exists(logo_path):
                logo = ImageReader(logo_path)
                c.drawImage(logo, 0.5*cm, height-3.5*cm, width=4*cm, height=2.5*cm, preserveAspectRatio=True)

            # ========== العنوان المركزي ==========
            invoice_number = str(invoice_data['Receipt_Number']).replace("INV-", "").strip()
            invoice_title = f"فاتورة شراء رقم {invoice_number}"
            
            # رسم الإطار حول العنوان
            frame_width = 4*cm
            frame_height = 1*cm
            frame_x = (width - frame_width) / 2  # مركز أفقي
            frame_y = height - 2.5*cm
            c.setLineWidth(1)
            c.rect(frame_x, frame_y, frame_width, frame_height)
            
            # كتابة العنوان المركزي
            c.setFont("Arabic", 12)  # تأكد من وجود خط عريض
            title_x = width / 2
            title_y = height - 2.2*cm
            c.drawCentredString(title_x, title_y, format_arabic(invoice_title))

            # ========== معلومات الشركة ==========
            company_info = [
                "      حسن سليم",
                "للمنتجات البلاستيكية"
            ]
            
            y_position = height - 2*cm
            c.setFont("Arabic", 12)
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
                # text = f"{format_arabic(field)} {format_arabic(value)}"
                c.drawRightString(width - 0.4*cm, customer_y, format_arabic(line))
                customer_y -= 0.8*cm

            # ========== جدول العناصر ==========
            headers = ["كود الصنف","     الصنف", "العدد", "الوحدة", "سعر الوحدة", "الكمية", "الإجمالي"]
            col_positions = [
                width - 0.4*cm,    # كود الصنف
                width - 2*cm,    # الصنف
                width - 5.5*cm,    # العدد
                width - 7.5*cm,    # الوحدة
                width - 9.5*cm,    # السعر
                width - 11.5*cm,     # الكمية
                width - 13*cm      # الإجمالي
            ]
            
            # رأس الجدول
            table_y = customer_y - 0.25*cm
            c.setFont("Arabic", 10)
            for i, header in enumerate(headers):
                c.drawRightString(col_positions[i], table_y, format_arabic(header))

            # بيانات الجدول
            c.setFont("Arabic", 8)
            row_height = 0.7*cm
            for item in invoice_data["Items"]:
                table_y -= row_height
                columns = [
                    item.get("material_code", ""),
                    item.get("material_name",""),
                    str(item.get("numbering", "")),
                    item.get("Unit", ""),
                    f"{item.get('Unit_price', 0):.2f}",
                    str(item.get('QTY', 0)),
                    f"{item.get('Final_Price', 0):.2f}"
                ]
                for i, value in enumerate(columns):
                    c.drawRightString(col_positions[i], table_y, format_arabic(value))

            # ========== الإجماليات ==========
            totals_y = table_y - 1*cm
            totals = [
                ("صافي الفاتورة:", invoice_data['Financials']['Net_total']),
                ("حساب سابق:", invoice_data['Financials']['Previous_balance']),
                ("إجمالي الفاتورة:", invoice_data['Financials']['Total_balance']),
                ("المدفوع:", invoice_data['Financials']['Payed_cash']),
                ("الباقي:", invoice_data['Financials']['Remaining_balance'])
            ]
            
            c.setFont("Arabic", 12)
            for label, value in totals:
                text = f"{format_arabic(f'{value:,.2f}')} {format_arabic(label)}"
                c.drawRightString(width - 0.3*cm, totals_y, text)
                totals_y -= 0.8*cm

            # ========== التوقيعات ==========
            c.setFont("Arabic", 10)
            c.drawRightString(width - 2.2*cm, totals_y - 0.25*cm, format_arabic("____________________"))
            c.drawString(1.5*cm, totals_y - 0.25*cm, format_arabic("____________________"))
            
            c.save()
            pdf_path = self.upload_pdf_to_cloudinary(pdf_path)
            return pdf_path

        except Exception as e:
            messagebox.showerror("خطأ PDF", f"فشل في توليد الملف: {str(e)}")
            return None
        

    def upload_pdf_to_cloudinary(self,file_path_param):
        # import cloudinary.uploader
        try:
            response = cloudinary.uploader.upload(file_path_param, resource_type="raw")
            return response['secure_url']
        except Exception as e:
            print(f"[Cloudinary Upload Error]: {e}")
            return None

    def deselect_entry(self,tree):
        tree.selection_remove(tree.selection())
        # Clear form fields
        for field, widget in self.entries.items():
            if "date" in field.lower():
                widget.set_date(datetime.now())
            elif "pic" in field.lower():
                widget.config(image='')
                widget.image = None
            else:
                widget.delete(0, tk.END)

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
    def topbar(self, show_back_button=False, Back_to_Database_Window = False):
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
                if Back_to_Database_Window:
                    back_icon = tk.Button(top_bar, image=self.back_photo, bg="#dbb40f", bd=0, command=self.manage_database_window)
                else:
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
        # popup.geometry("300x120")
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

def upload_file_to_cloudinary(file_path_param):
    # import cloudinary.uploader
    try:
        response = cloudinary.uploader.upload(file_path_param, resource_type="image")
        return response['secure_url']
    except Exception as e:
        print(f"[Cloudinary Upload Error]: {e}")
        return None
def load_image_preview(filepath, img_label):
    try:
        img = Image.open(filepath)
        img.thumbnail((300, 300))  # Make it bigger (adjust size as you wish)
        img_tk = ImageTk.PhotoImage(img)
        
        img_label.config(image=img_tk)
        img_label.image = img_tk
        img_label.image_path = filepath   # <== DID YOU ADD THIS LINE? 👈👈👈
    except Exception as e:
        print(f"Error loading image preview: {e}")

def load_image_preview_from_url(image_url, label, max_size=(300, 300)):
    """Load image from a URL and display it in a Tkinter Label.
    Args:image_url (str): The image URL to load.
         label (tk.Label): The Tkinter Label to display the image in.
         image_refs (list): A list to store image references (to avoid garbage collection).
         max_size (tuple): Max size of the image (width, height)"""
    try:
        with urllib.request.urlopen(image_url) as response:
            image_data = Image.open(io.BytesIO(response.read()))
            image_data.thumbnail(max_size)  # Resize image
            image_obj = ImageTk.PhotoImage(image_data)

            label.config(image=image_obj)
            label.image = image_obj  # Also attach to label itself (extra safety)
    except Exception as e:
        print(f"Error loading image from URL: {e}")
        label.config(image="")
        label.image = None

def get_type(var):
    return type(var).__name__

######################### Auxiliary classes #########################################################
class AlwaysOnTopInputDialog(tk.Toplevel):
    def __init__(self, parent, prompt):
        super().__init__(parent)
        self.transient(parent)
        self.grab_set()

        self.title("Input")

        self.prompt_label = tk.Label(self, text=prompt)
        self.prompt_label.pack(padx=10, pady=10)

        self.input_widget = tk.Entry(self)
        self.input_widget.pack(padx=10, pady=10)
        self.input_widget.focus_set()

        self.result = None

        self.ok_button = tk.Button(self, text="OK", command=self.on_ok)
        self.ok_button.pack(pady=5)
        self.ok_button.bind("<Return>", lambda event: self.ok_button.invoke())

        self.after(1, self.adjust_geometry)
        self.center_dialog(parent)

    def adjust_geometry(self):
        self.geometry("300x150")

    def center_dialog(self, parent):
        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        dialog_width = self.winfo_reqwidth()
        dialog_height = self.winfo_reqheight()
        x_position = (screen_width // 2) - (dialog_width // 2)
        y_position = (screen_height // 2) - (dialog_height // 2)
        self.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")

    def on_ok(self):
        if isinstance(self.input_widget, DateEntry):
            self.result = self.input_widget.get_date()
        else:
            self.result = self.input_widget.get()
        self.destroy()

    def get_result(self):
        self.wait_window(self)
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