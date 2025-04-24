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
  
############################ Init ########################################################

    def __init__(self, root):
        self.root = root
        self.root.title("مصنع حسن سليم للمنتجات البلاستيكية")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="white")
        
        self.Connect_DB()
        
        self.language = "Arabic"  # default language
        self.translations = {
            "Add New Product": {"Arabic": "إضافة منتج جديد", "English": "Add New Product"},
            "place Orders": {"Arabic": "تنفيذ الطلبات", "English": "Place Orders"},
            "Expenses": {"Arabic": "المصاريف", "English": "Expenses"},
            "Returns": {"Arabic": "المرتجعات", "English": "Returns"},
            "Employees Appointments": {"Arabic": "مواعيد الموظفين", "English": "Employees Appointments"},
            "Daily Shifts": {"Arabic": "الورديات اليومية", "English": "Daily Shifts"},
            "View Product": {"Arabic": "عرض المنتجات", "English": "View Product"},
            "View Orders": {"Arabic": "عرض الطلبات", "English": "View Orders"},
            "View Customers": {"Arabic": "عرض العملاء", "English": "View Customers"},
            "Edit Product": {"Arabic": "تعديل المنتج", "English": "Edit Product"},
            "Accounting": {"Arabic": "الحسابات", "English": "Accounting"},
            "Reports": {"Arabic": "التقارير", "English": "Reports"},
            "Big Deals": {"Arabic": "الصفقات الكبيرة", "English": "Big Deals"},
            "Database": {"Arabic": "قاعدة البيانات", "English": "Database"},
            "Change Language": {"Arabic": "تغيير اللغة", "English": "Change Language"},
        }
        self.db_name = tk.StringVar()
        self.table_name = tk.StringVar()
        self.search_query = tk.StringVar()
        self.user_photo_path = ""  # Initialize with None or a default image path
        self.user_photo = ""
        self.user_name = ""  # Placeholder for dynamic user name
        self.user_role = ""  # Placeholder for user role

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
        self.users_collection = db['Users']
        self.products_collection = db['Products']
        self.sales_collection = db['Sales']
        self.customers_collection = db['Customers']
        self.suppliers_collection = db['Suppliers']
        self.shipping_collection = db['Shipping']
        self.orders_collection = db['Orders']
        self.expenses_collection = db['Expenses']
        self.employee_appointments_collection = db['Employee_appointments']
        self.daily_shifts_collection = db['Daily_shifts']
        self.accounts_collection = db['Accounts']
        self.transactions_collection = db['Transactions']
        self.big_deals_collection = db['Big_deals']
        self.TEX_Calculations_collection = db['TEX_Calculations']

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
                self.play_Error()
                messagebox.showerror("Error", "Both fields are required.")
                return

            try:
                user = self.users_collection.find_one({"username": username, "password": password})
                # print(user)
                if user:
                    self.user_role = user.get("role", "Unknown")
                    # messagebox.showinfo("Success", f"Login successful! Role: {self.user_role}")
                    self.silent_error_popup("Success", f"Login successful! Role: {self.user_role}")
                    open_main_menu(self.user_role)
                else:
                    self.silent_error_popup("Error", "Invalid username or password.")

            except Exception as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
                self.play_Error()


        login_button = tk.Button(login_frame, text="Login", font=("Arial", 12), bg="lightblue", command=validate_login)
        login_button.place(x=150, y=270, width=100)

        # Exit Button
        exit_button = tk.Button(login_frame, text="Exit", font=("Arial", 12), bg="lightgray", command=self.root.quit)
        exit_button.place(x=270, y=270, width=80)
        def open_main_menu(role):
            if role:
                self.main_menu()
            else:
                print("Unknown role. Access denied.")
                self.play_Error

    def main_menu(self):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # make the top bar with change language button
        self.topbar(show_back_button=False)

        # Buttons frame
        button_frame = tk.Frame(self.root, bg="White", bd=2, relief="solid")
        button_frame.pack(pady=20, padx=20, fill="x")
        # # we will implement it later
        # self.Dashboard(self.user_role)

        buttons = [
            {"text": self.t("Add New Product"), "command": lambda: self.trash(self.user_role)},
            {"text": self.t("place Orders"), "command": lambda: self.trash(self.user_role)},
            {"text": self.t("Expenses"), "command": lambda: self.trash(self.user_role)},
            {"text": self.t("Returns"), "command": lambda: self.trash(self.user_role)},
            {"text": self.t("Employees Appointments"), "command": lambda: self.trash(self.user_role)},
            {"text": self.t("Daily Shifts"), "command": lambda: self.trash(self.user_role)}
        ]

        if self.user_role == "employee":
            buttons.extend([
                {"text": self.t("View Product"), "command": lambda: self.trash(self.user_role)},
                {"text": self.t("View Orders"), "command": lambda: self.trash(self.user_role)},
                {"text": self.t("View Customers"), "command": lambda: self.trash(self.user_role)}
            ])

        if self.user_role == "admin":
            buttons.insert(1, {"text": self.t("Edit Product"), "command": lambda: self.trash(self.user_role)})
            buttons.extend([
                {"text": self.t("Accounting"), "command": lambda: self.trash(self.user_role)},
                {"text": self.t("Reports"), "command": lambda: self.trash(self.user_role)},
                {"text": self.t("Big Deals"), "command": lambda: self.trash(self.user_role)},
                {"text": self.t("Database"), "command": lambda: self.check_access_and_open(self.user_role, db_name="clothes_sales.db", table_name="Users")}
            ])

        for btn_info in buttons:
            btn = tk.Button(
                button_frame,
                text=btn_info["text"],
                font=("Arial", 11),
                bg="white",
                fg="black",
                bd=1,
                relief="solid",
                command=btn_info["command"]
            )
            btn.pack(side="left", padx=10, pady=10, ipadx=10, ipady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#e0e0e0"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="white"))

    def manage_database_window(self, db_name=None, table_name=None):
        self.db_name.set(db_name if db_name else "")
        self.table_name.set(table_name if table_name else "")

        for widget in self.root.winfo_children():
            widget.destroy()

        # تحميل صورة الخلفية
        self.topbar(show_back_button=True)

        tk.Label(self.root, text="Select Database:", bg="#4a90e2", fg="white", font=("Arial", 12)).place(x=120, y=70)
        db_dropdown = ttk.Combobox(self.root, textvariable=self.db_name, values=["clothes_sales.db"])
        db_dropdown.place(x=250, y=70)

        tk.Label(self.root, text="Select Table:", bg="#4a90e2", fg="white", font=("Arial", 12)).place(x=130, y=110)
        table_dropdown = ttk.Combobox(self.root, textvariable=self.table_name, values=["Users", "Products", "Sales", "Customers","Suppliers","Shipping","Orders","Expenses","Employee_appointments","Daily_shifts","Accounts","Transactions","Big_deals","TEX_Calculations"])
        table_dropdown.place(x=250, y=110)
        table_dropdown.bind("<<ComboboxSelected>>", lambda e: self.display_table())

        tk.Label(self.root, text="Search:", bg="#4a90e2", fg="white", font=("Arial", 12)).place(x=140, y=150)
        search_entry = tk.Entry(self.root, textvariable=self.search_query)
        search_entry.place(x=250, y=150)
        tk.Button(self.root, text="Search", command=self.display_table).place(x=410, y=145)

        self.tree = ttk.Treeview(self.root, show="headings")
        self.tree.place(x=0, y=190)

        tk.Button(self.root, text="Add Record", command=self.add_entry).place(width=120, height=40, x=100, y=450)
        tk.Button(self.root, text="Edit Record", command=self.edit_entry).place(width=120, height=40, x=250, y=450)
        tk.Button(self.root, text="Delete Record", command=self.delete_entry).place(width=120, height=40, x=400, y=450)

        self.display_table()


############################ Main Functions ########################################
    def display_table(self):
        db_name = self.db_name.get()
        collection_name = self.table_name.get()
        search_query = self.search_query.get()

        if not db_name or not collection_name:
            return
        
        current_collection = self.get_collection_by_name(collection_name)
    
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
                columns = list(data[0].keys())
                if '_id' in columns:
                    columns.remove('_id')
                    columns.insert(0, self.t("ID")) # ROW ID

                self.tree["columns"] = columns
                for col in columns:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=150, anchor="center", stretch=False)

                for row_data in data:
                    values = []
                    record_id = row_data.get('_id', '')
                    values.append(str(record_id)) # Display ObjectId as string
                    for col in columns[1:]: # Start from the second column as the first is 'ID'
                        values.append(row_data.get(col, ''))
                    self.tree.insert("", "end", values=values)
            # else:
            #     self.tree["columns"] = []
            #     self.tree.delete(*self.tree.get_children())
            #     messagebox.showinfo("Info", "No data found in this collection.")

        except Exception as e:
            messagebox.showerror("Error", f"Error displaying data: {e}")

    def add_entry(self):
        db_name = self.db_name.get() #TODO
        collection_name = self.table_name.get()
        print("collection_name")
        print(collection_name)
        if not db_name or not collection_name:
            messagebox.showwarning("Warning", "Please select a database and table first")
            return
        
        current_collection = self.get_collection_by_name(collection_name)


        first_document = current_collection.find_one()
        fields = [key for key in first_document.keys() if key != '_id']

        new_entry = {}
        for field in fields:
            value = simpledialog.askstring("Input", f"Enter value for {field}:")
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
        db_name = self.db_name.get() #TODO
        collection_name = self.table_name.get()
        if not db_name or not collection_name:
            messagebox.showwarning("Warning", "Please select a database and table first")
            return

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

        fields = [key for key in first_document.keys() if key != '_id']
        updated_values = {}

        for field in fields:
            current_value = first_document.get(field, '')
            new_value = simpledialog.askstring("Edit", f"Enter new value for {field}:", initialvalue=current_value)
            if new_value is None: #TODO this part could be removed ... (keep old value for example)
                return
            updated_values[field] = new_value

        try:
            current_collection.update_one({"_id": record_id}, {"$set": updated_values})
            self.display_table()
            messagebox.showinfo("Success", "Record updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating record: {e}")

    def delete_entry(self):
        db_name = self.db_name.get()
        collection_name = self.table_name.get()

        if not db_name or not collection_name:
            messagebox.showwarning("Warning", "Please select a database and collection first")
            return

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
        Args: collection_name (str): The name of the collection to access (e.g., "Users", "Products").
        Returns: pymongo.collection.Collection or None: The corresponding MongoDB collection object,
                                                   or None if the name is not recognized."""
        if collection_name == "Users":
            return self.users_collection
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
        time_label.config(text=datetime.now().strftime('%I:%M %p'))
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
            print(f"Error loading exit icon: {e}")
            self.play_Error

        # Logout icon
        try:
            logout_image = Image.open(self.logout_icon_path)
            logout_image = logout_image.resize((40, 40), Image.LANCZOS)
            self.logout_photo = ImageTk.PhotoImage(logout_image)
            logout_icon = tk.Button(top_bar, image=self.logout_photo, bg="#dbb40f", bd=0, command=self.open_login_window)
            logout_icon.pack(side="right", padx=10)
        except Exception as e:
            print(f"Error loading logout icon: {e}")
            self.play_Error

        # Left side: Language or Back button
        if show_back_button:
            try:
                back_image = Image.open(self.back_icon_path)
                back_image = back_image.resize((40, 40), Image.LANCZOS)
                self.back_photo = ImageTk.PhotoImage(back_image)
                back_icon = tk.Button(top_bar, image=self.back_photo, bg="#dbb40f", bd=0, command=self.main_menu)
                back_icon.pack(side="left", padx=10)
            except Exception as e:
                print(f"Error loading back icon: {e}")
                self.play_Error
        else:
            lang_btn = tk.Button(top_bar, text=self.t("Change Language"), bg="#dbb40f", fg="black",
                                font=("Arial", 10, "bold"), bd=0, command=self.toggle_language)
            lang_btn.pack(side="left", padx=10)

        # Time label
        time_label = tk.Label(top_bar, text=datetime.now().strftime('%I:%M %p'),
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

    def play_(self):
        sound_path = os.path.join(BASE_DIR, 'Static', 'sounds', 'Error.mp3')
        threading.Thread(target=playsound, args=(sound_path,), daemon=True).start()

    def play_success(self):
        sound_path = "C:\Main Files\SW Work\مصنع حسن سليم للمنتجات البلاستيكية system\Static\sounds\Test.mp3"
        threading.Thread(target=playsound, args=(sound_path,), daemon=True).start()
    
    def silent_error_popup(self, title, message):
        self.play_Error()

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

        tk.Label(popup, text=message, fg="red", font=("Arial", 12)).pack(pady=10)
        tk.Button(popup, text="OK", width=10, command=popup.destroy).pack(pady=20)

######################### Main #########################################################

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesSystemApp(root)
    app.open_login_window()  # Start with the login window
    try:
        root.mainloop()
    except Exception as e:
        print("Error during mainloop:", e)