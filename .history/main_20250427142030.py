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
        self.db_name = tk.StringVar()
        self.table_name = tk.StringVar()
        self.search_query = tk.StringVar()
        self.user_photo_path = ""  # Initialize with None or a default image path
        self.user_photo = ""
        self.user_name = ""  # Placeholder for dynamic user name
        self.user_role = ""  # Placeholder for user role
        self.all_customers = None  # Will be loaded on first search
        
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
                user = self.employees_collection.find_one({"username": username, "password": password})
                # print(user)
                if user:
                    self.user_role = user.get("role", "Unknown")
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
        columns = ("Code", "Product", "Qty", "Price", "Total")
        self.tree = ttk.Treeview(form_frame, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.grid(row=2, column=0, columnspan=3, pady=10)

        # Add Product Button
        tk.Button(form_frame, text="Add Product", command=lambda: self.add_product(products_col)).grid(row=3, column=0)

        # Save Invoice Button
        tk.Button(form_frame, text="Save Invoice", 
                command=lambda: self.save_invoice(sales_col, customers_col)).grid(row=3, column=1)
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
        
    def update_search(self, event, collection):
        # Cancel any previous scheduled search
        if hasattr(self, '_after_id'):
            self.root.after_cancel(self._after_id)
        
        # Get the current text immediately
        # current_search_term = self.customer_var.get()
        
        # Schedule the search with the current text
        self._after_id = self.root.after(300, self.perform_search, collection)

    def perform_search(self, collection, search_term):
        # Update filtered list using MongoDB regex search
        filtered_customers = [cust['Name'] for cust in collection.find(
            {"Name": {"$regex": f"^{search_term}", "$options": "i"}}
        )]
        
        # Update combobox values
        self.customer_cb['values'] = filtered_customers
        
        # Auto-open dropdown if there are results
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
            "date": datetime.now(),
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

    def get_fields_by_name(self, collection_name):
        """Returns the appropriate fields array based on the provided collection name.
        Args: collection_name (str): The name of the collection (e.g., "Employees", "Products").
        Returns: list: A list of field names for the corresponding collection, or an empty list if the name is not recognized.
        """
        if collection_name == "Employees":
            return ["Name", "Password", "Id", "Role", "Join_Date", "National_id_pic", "Phone_number", "Address", "Salary"]
        
        elif collection_name == "Products":
            return ["product_name", "category", "price", "stock_quantity", "supplier"]
        
        elif collection_name == "Sales":
            return ["sale_date", "product_id", "quantity", "total_price", "customer_id"]
        
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