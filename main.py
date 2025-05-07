import tkinter as tk
from tkinter import filedialog, ttk, messagebox,Tk, Label, PhotoImage,simpledialog
from PIL import Image, ImageTk, ImageDraw  # Import Pillow classes
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
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

######################################################### Access Data Base ##############################################################################
dialog_width = 300  # Same width as AlwaysOnTopInputDialog
dialog_height = 150 # Same height as AlwaysOnTopInputDialog

ARRAY_FIELDS = ['Units'] #Must be lower case

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

        username_entry.bind("<Return>", lambda event: validate_login()) 
        password_entry.bind("<Return>", lambda event: validate_login()) 
        
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
                user = self.employees_collection.find_one({"Name": username, "Password": password})
                # print(user)
                if user:
                    self.user_role = user.get("Role", "Unknown")
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
            "command": lambda: self.new_customer(self.user_role)},
            {"text": self.t("Suppliers"), "image": "suppliers.png", 
            "command": lambda: self.new_supplier(self.user_role)},
            {"text": self.t("Employees"), "image": "Employees.png", 
            "command": lambda: self.new_employee(self.user_role)},
            {"text": self.t("Products"), "image": "Products.png", 
            "command": lambda: self.new_products(self.user_role)},
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
        self.tree.place(x=50, y=190)

        tk.Button(self.root, text="Add Record", command=self.add_entry).place(width=120, height=40, x=100, y=550)
        tk.Button(self.root, text="Edit Record", command=self.edit_entry).place(width=120, height=40, x=250, y=550)
        tk.Button(self.root, text="Delete Record", command=self.delete_entry).place(width=120, height=40, x=400, y=550)

        self.display_table()

    def new_sales_invoice(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create top bar
        self.topbar(show_back_button=True)

        # MongoDB collections
        customers_col = self.get_collection_by_name("Customers")#done
        sales_col = self.get_collection_by_name("Sales")
        products_col = self.get_collection_by_name("Products")

        # Frame for invoice form
        form_frame = tk.Frame(self.root, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Customer Dropdown with Search
        tk.Label(form_frame, text="Customer:",font=("Arial", 15, "bold")).grid(row=0, column=1, sticky='w')
        self.customer_var = tk.StringVar()
        self.customer_cb = ttk.Combobox(form_frame, textvariable=self.customer_var)
        self.customer_cb.grid(row=0, column=1, padx=5, pady=5)
        
        # Fetch customers and set autocomplete
        all_customers = [cust['Name'] for cust in customers_col.find()]
        self.customer_cb['values'] = all_customers
        self.customer_cb.bind('<KeyRelease>', lambda event: self.update_search(event, customers_col))

        # Invoice Items Table
        columns = self.get_fields_by_name("Sales")
        self.tree = ttk.Treeview(form_frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.grid(row=2, column=0, columnspan=3, pady=10)

        # Add Product Button
        tk.Button(form_frame, text="Add Product", command=lambda: self.add_product(products_col)).grid(row=3, column=0)

        # Save Invoice Button
        tk.Button(form_frame, text="Save Invoice", 
                command=lambda: self.save_invoice(sales_col, customers_col)).grid(row=3, column=1)
    
    def new_employee(self, user_role):
        self.table_name.set("Employees")
        for widget in self.root.winfo_children():
            widget.destroy()
        # تحميل صورة الخلفية
        self.topbar(show_back_button=True)
        self.display_general_table(self.employees_collection, "Employees")
    
    def new_supplier(self, user_role):
        self.table_name.set("Suppliers")
        for widget in self.root.winfo_children():
            widget.destroy()
        self.topbar(show_back_button=True)
        self.display_general_table(self.suppliers_collection, "Suppliers")
    
    def new_customer(self, user_role):
        self.table_name.set("Customers")
        for widget in self.root.winfo_children():
            widget.destroy()

        self.topbar(show_back_button=True)
        self.display_general_table(self.customers_collection, "Customers")

    def new_products(self, user_role):
        self.table_name.set("Products")
        for widget in self.root.winfo_children():
            widget.destroy()
    
        self.topbar(show_back_button=True)
        self.display_general_table(self.products_collection, "Products")
        
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
                            
                        if 'date' in col.lower() and isinstance(val, datetime.datetime):
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

        canvas = tk.Canvas(form_container, width=300)   # Set width for form
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
            
            tk.Label(form_frame, text=label, font=("Arial", 12), anchor="w").grid(row=i, column=0, sticky="w", pady=5)

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
            text="Search",
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
            current_collection = self.get_collection_by_name(collection_name)
            first_document = current_collection.find_one({columns[id_index]: unique_id})

        except IndexError:
            return

        if not first_document:
            print(1)
            return

        for field, entry in self.entries.items():
            value = first_document.get(field, "")
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d-%m-%Y')
                entry.delete(0, tk.END)
                entry.insert(0, value)
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
                                
                                elif isinstance(value, datetime.datetime):
                                    value = value.strftime('%d-%m-%Y')
                                
                                values.append(value)
                            
                            tree.insert("", "end", values=values)
                    
                    else:
                        # Fallback to insert normally if Units is not a list or is empty
                        values = []
                        for col in columns:
                            value = row_data.get(col, '')
                            if isinstance(value, datetime.datetime):
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
                        value_date = datetime.datetime.strptime(value, '%d-%m-%Y').date()
                        value = datetime.datetime.combine(value_date, datetime.time.min)
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
            elif any(word in field.lower() for word in ["number, stock_quantity"]):
                value = widget.get()
                value = int(value)
                if not value:
                    messagebox.showwarning("Warning", f"Please enter a value for {field}")
                    return
            elif any(word in field.lower() for word in ["salary", "credit", "debit"]):
                value = widget.get()
                value = float(value)
                if not value:
                    messagebox.showwarning("Warning", f"Please enter a value for {field}")
                    return
            else:
                value = widget.get()
                if not value:
                    messagebox.showwarning("Warning", f"Please enter a value for {field}")
                    return

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
                    widget.set_date(datetime.datetime.now())
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
                        value_date = datetime.datetime.strptime(value, '%d-%m-%Y').date()
                        value = datetime.datetime.combine(value_date, datetime.time.min)
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

            updated_entry[field] = value

        try:
            result = current_collection.update_one({"Id": record_id}, {"$set": updated_entry})
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
                    widget.set_date(datetime.datetime.now())
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
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a record to delete")
            return

        try:
            columns = tree["columns"]  # Tuple/list of column names
            lower_columns = [col.lower() for col in columns]

            # Find which column is used as identifier (id / code)
            id_index = None
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
                messagebox.showwarning("Not Found", "No matching record found to delete.")
                return

            # Step 2: Check if document contains any ARRAY_FIELDS (like 'units')
            handled = False
            values = tree.item(selected_item)["values"]
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
                        value = datetime.datetime.strptime(value, '%d-%m-%Y').date()
                        value = datetime.datetime.combine(value, datetime.time.min) #Must do this to be comaptible with mongodb's Date type 
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
                        value = datetime.datetime.strptime(value, '%d-%m-%Y').date()
                        value = datetime.datetime.combine(value, datetime.time.min) #Must do this to be comaptible with mongodb's Date type 

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
        if collection_name == "Employees":
            return ["Name", "Password", "Id", "Role", "Join_Date", "National_id_pic", "Phone_number", "Address", "Salary"]
        
        elif collection_name == "Products":
            return ["product_name", "category", "stock_quantity", "Specs", "Unit_Price", "product_code", "Units", "prod_pic"]
        
        elif collection_name == "Sales":
            return ["sale_date", "product_id", "quantity", "total_price", "customer_id"]
        #TODO Id
        elif collection_name == "Customers":
            return ["Name", "Phone_number1", "Phone_number2", "Code" , "Purchase_mgr_number", "Financial_mgr_number", "Purchase_mgr_name", 
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

    def add_product(self, products_col):
        # New window for product selection
        product_win = tk.Toplevel()
        product_win.title("Select Product")
        
        # Product Search and Selection
        tk.Label(product_win, text="Search Product:").pack()
        product_var = tk.StringVar()
        product_cb = ttk.Combobox(product_win, textvariable=product_var)
        product_cb.pack()
        product_cb['values'] = [prod['product_name'] for prod in products_col.find()]
        
        # Add selected product to invoice
        tk.Button(product_win, text="Add", command=lambda: self.add_to_invoice(product_var.get(), products_col)).pack()

    def add_to_invoice(self, product_name, products_col):
        product = products_col.find_one({"product_name": product_name})
        if product:
            self.tree.insert('', 'end', values=(
                product['Code'],
                product['product_name'],
                1,  # Default quantity
                product['price'],
                product['price']  # Initial total
            ))
    def generate_invoice_number(self):
        # Use a counter collection for sequential numbering
        counter_col = self.db['counters']
        counter = counter_col.find_one_and_update(
            {'_id': 'invoice_number'},
            {'$inc': {'sequence_value': 1}},
            upsert=True,
            return_document=True
        )
        return f"INV-{counter['sequence_value']:04d}"

    def generate_sales_report(self, invoice_id):
        # Fetch invoice data
        sales_col = self.db['sales']
        invoice = sales_col.find_one({'_id': invoice_id})
        
        # Fetch customer data
        customers_col = self.db['customers']
        customer = customers_col.find_one({'_id': invoice['customer_id']})
        
        # Create report window
        report_win = tk.Toplevel()
        report_win.title(f"Sales Report - {invoice['invoice_number']}")
        
        # Arabic labels with right-to-left layout
        main_frame = tk.Frame(report_win)
        main_frame.pack(padx=20, pady=20)
        
        # Header Section
        tk.Label(main_frame, text="فاتورة بيع رقم", font=('Arial', 14, 'bold')).grid(row=0, column=4, sticky='e')
        tk.Label(main_frame, text=invoice['invoice_number'], font=('Arial', 14)).grid(row=0, column=5, sticky='w')
        
        # Customer Information
        tk.Label(main_frame, text="الاسم:", anchor='e').grid(row=1, column=4, sticky='e')
        tk.Label(main_frame, text=customer['Name']).grid(row=1, column=5, sticky='w')
        
        # Date Information
        tk.Label(main_frame, text="التاريخ:").grid(row=2, column=4, sticky='e')
        tk.Label(main_frame, text=invoice['date'].strftime('%d/%m/%Y')).grid(row=2, column=5, sticky='w')
        
        # Items Table
        columns = ('كود الصنف', 'الصنف', 'الكمية', 'سعر الوحدة', 'الإجمالي')
        tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=4)
        
        # Right-to-left column alignment
        for col in columns:
            tree.heading(col, text=col, anchor='e')
            tree.column(col, anchor='e')
        
        tree.grid(row=3, column=0, columnspan=6, pady=10)
        
        # Add invoice items
        products_col = self.db['products']
        for item in invoice['items']:
            product = products_col.find_one({'Code': item['product_code']})
            tree.insert('', 'end', values=(
                item['product_code'],
                product['product_name'] if product else 'N/A',
                item['quantity'],
                f"{float(item['unit_price']):,.2f}",
                f"{float(item['total']):,.2f}"
            ))
        
        # Totals Section
        totals_frame = tk.Frame(main_frame)
        totals_frame.grid(row=4, column=0, columnspan=6, pady=10)
        
        totals_data = [
            ("صافي الفاتورة", invoice['total']),
            ("حساب سابق", invoice.get('previous_balance', 0)),
            ("إجمالي الفاتورة", invoice['total'] + invoice.get('previous_balance', 0)),
            ("المدفوع", invoice.get('amount_paid', 0)),
            ("الباقي", invoice['balance'])
        ]
        
        for i, (label, value) in enumerate(totals_data):
            tk.Label(totals_frame, text=label, font=('Arial', 10, 'bold')).grid(row=i, column=0, sticky='e', padx=10)
            tk.Label(totals_frame, text=f"{value:,.2f}", font=('Arial', 10)).grid(row=i, column=1, sticky='w')

    def save_invoice(self, sales_col, customers_col):
        # Get customer ID
        customer = customers_col.find_one({"Name": self.customer_var.get()})
        
        # Prepare sales document
        invoice = {
            "invoice_number": self.generate_invoice_number(),
            "date": datetime.datetime.now(),
            "customer_id": customer['_id'],
            "employee_id": self.user_role['_id'],  # Assuming user_role contains logged-in user
            "items": [{
                "product_code": item['values'][0],
                "quantity": item['values'][2],
                "unit_price": item['values'][3],
                "total": item['values'][4]
            } for item in self.tree.get_children()],
            "total": sum(float(self.tree.item(item)['values'][4]) for item in self.tree.get_children()),
            "balance": 0  # Add your balance calculation logic
        }
        
        # Insert into MongoDB
        sales_col.insert_one(invoice)
        print("Invoice saved successfully!")

    def deselect_entry(self,tree):
        tree.selection_remove(tree.selection())
        # Clear form fields
        for field, widget in self.entries.items():
            if "date" in field.lower():
                widget.set_date(datetime.datetime.now())
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
    # def update_time(self, time_label):
    #     time_label.config(text=datetime.datetime.now().strftime('%B %d, %Y %I:%M %p'))
    #     self.root.after(1000, self.update_time, time_label)


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
        time_label = tk.Label(top_bar, text=datetime.datetime.now().strftime('%B %d, %Y %I:%M %p'),
                            font=("Arial", 20, "bold"), fg="black", bg="#dbb40f")

        time_label.place(relx=0.5, rely=0.5, anchor="center")
        # self.update_time(time_label)
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

def upload_pdf_to_cloudinary(file_path_param):
    # import cloudinary.uploader
    try:
        response = cloudinary.uploader.upload(file_path_param, resource_type="raw")
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

