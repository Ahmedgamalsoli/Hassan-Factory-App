
# ======================
# Used imports
# ======================

import tkinter as tk
import io
import re
import os
import config
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
class reports:
    def __init__(self, root, app):
        self.root = root
        self.app = app  # save reference to SalesSystemApp
    def manage_Reports_window(self):
                # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg=config.COLORS["background"])
        # Create the top bar
        self.app.topbar.topbar(show_back_button=True)

        button_frame = tk.Frame(self.root, bg=config.COLORS["background"])
        button_frame.pack(pady=30)

        # Define buttons with images, text, and commands
        if self.app.light:
            buttons = [
                {"text": self.app.t("Sales Report"), "image": "sales_rep-dark.png", 
                "command": lambda: self.app.trash(self.app.user_role)},
                {"text": self.app.t("Daily treasury report"), "image": "daily-report-dark.png", 
                "command": lambda: self.Treasury_window_report(self.app.user_role)},
                # {"text": self.app.t("Sales Report"), "image": "sales_rep-dark.png", 
                # "command": lambda: self.app.sales_report(self.app.user_role)},
                {"text": self.app.t("Purchase Report"), "image": "Purchase_rep-dark.png", 
                "command": lambda: self.app.trash(self.app.user_role)},
                {"text": self.app.t("Profit and Loss (P&L) Report"), "image": "p&l_repo-dark.png", 
                "command": lambda: self.app.trash(self.app.user_role)},
                {"text": self.app.t("Customer Reports"), "image": "Customer_repo-dark.png", 
                "command": lambda: self.app.trash(self.app.user_role)},
                {"text": self.app.t("Supplier Reports"), "image": "Supplier_repo-dark.png", 
                "command": lambda: self.app.trash(self.app.user_role)},
                {"text": self.app.t("Inventory Report"), "image": "Inventory_repo-dark.png", 
                "command": lambda: self.app.trash(self.app.user_role)},
                {"text": self.app.t("Payment & Collection Report"), "image": "payment_repo-dark.png", 
                "command": lambda: self.app.trash(self.app.user_role)},
                {"text": self.app.t("General Expenses Report"), "image": "General Expenses_repo-dark.png", 
                "command": lambda: self.app.trash(self.app.user_role)},
                {"text": self.app.t("Employee Performance Report"), "image": "Employee_Performance_repo-dark.png", 
                "command": lambda: self.app.trash(self.app.user_role)},
            ]
        elif not self.app.light:
            buttons = [
                {"text": self.app.t("Sales Report"), "image": "sales_rep-light.png", 
                "command": lambda: self.app.trash(self.app.user_role)},
                {"text": self.app.t("Daily treasury report"), "image": "daily-report-light.png", 
                "command": lambda: self.Treasury_window_report(self.app.user_role)},
                # {"text": self.t("Sales Report"), "image": "sales_rep-light.png", 
                # "command": lambda: self.sales_report(self.user_role)},
                {"text": self.app.t("Purchase Report"), "image": "Purchase_rep-light.png", 
                "command": lambda: self.app.trash(self.app.user_role)},
                {"text": self.app.t("Profit and Loss (P&L) Report"), "image": "p&l_repo-light.png", 
                "command": lambda: self.app.trash(self.app.user_role)},
                {"text": self.app.t("Customer Reports"), "image": "Customer_repo-light.png", 
                "command": lambda: self.app.trash(self.app.user_role)},
                {"text": self.app.t("Supplier Reports"), "image": "Supplier_repo-light.png", 
                "command": lambda: self.app.trash(self.app.user_role)},
                {"text": self.app.t("Inventory Report"), "image": "Inventory_repo-light.png", 
                "command": lambda: self.app.trash(self.app.user_role)},
                {"text": self.app.t("Payment & Collection Report"), "image": "payment_repo-light.png", 
                "command": lambda: self.app.trash(self.app.user_role)},
                {"text": self.app.t("General Expenses Report"), "image": "General Expenses_repo-light.png", 
                "command": lambda: self.app.trash(self.app.user_role)},
                {"text": self.app.t("Employee Performance Report"), "image": "Employee_Performance_repo-light.png", 
                "command": lambda: self.app.trash(self.app.user_role)},
            ]
        images = []  # Keep references to prevent garbage collection
        columns_per_row = 3  # Number of buttons per row
        button_size = 120
        try:
            for index, btn_info in enumerate(buttons):
                # Default transparent image
                img_path = os.path.join(BASE_DIR, "Static", "images", btn_info["image"])
                original_img = Image.open(img_path).convert("RGBA")
                transparent_img = original_img.resize((button_size, button_size), Image.LANCZOS)
                photo_transparent = ImageTk.PhotoImage(transparent_img)

                # Image with background
                bg_color = (0,0,0,0)  # F5F7FA in RGBA
                bg_img = Image.new("RGBA", original_img.size, bg_color)
                composited_img = Image.alpha_composite(bg_img, original_img)
                resized_composited = composited_img.resize((button_size, button_size), Image.LANCZOS)
                photo_with_bg = ImageTk.PhotoImage(resized_composited)

                # Save both images
                images.append(photo_transparent)
                images.append(photo_with_bg)

                # Calculate grid position
                row = index // columns_per_row
                column = index % columns_per_row

                # Create sub-frame for each button
                sub_frame = tk.Frame(button_frame, bg=config.COLORS["background"])
                sub_frame.grid(row=row, column=column, padx=20, pady=20)

                # Image button
                btn = tk.Button(sub_frame, image=photo_transparent, bd=0,
                                text=btn_info["text"], 
                                font=("Arial", 15, "bold"),
                                compound=tk.TOP,
                                bg=config.COLORS["background"],
                                fg=config.COLORS["text"],
                                activebackground=config.COLORS["highlight"],
                                command=btn_info["command"])
                btn.image_transparent = photo_transparent
                btn.image_with_bg = photo_with_bg
                btn.pack()
                
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=config.COLORS["primary"]))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=config.COLORS["background"]))

                # # Text label
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
    def Treasury_window_report(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        self.app.topbar.topbar(show_back_button=True)

        # Main container
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Results Treeview
        columns = ("date", "description", "credit", "debit", "payment_method")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        
        # Configure columns
        self.tree.heading("date", text=self.app.t("Date"))
        self.tree.heading("description", text=self.app.t("Description"))
        self.tree.heading("credit", text=self.app.t("Credit"))
        self.tree.heading("debit", text=self.app.t("Debit"))
        self.tree.heading("payment_method", text=self.app.t("Payment Method"))

        self.tree.column("date", width=120, anchor='center')
        self.tree.column("description", width=250, anchor='center')
        self.tree.column("credit", width=120, anchor='center')
        self.tree.column("debit", width=120, anchor='center')
        self.tree.column("payment_method", width=150, anchor='center')

        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Totals display
        totals_frame = tk.Frame(main_frame)
        totals_frame.pack(fill=tk.X, pady=10)

        self.total_credit_var = tk.StringVar()
        self.total_debit_var = tk.StringVar()
        self.balance_var = tk.StringVar()

        tk.Label(totals_frame, text=self.app.t("Total Credit:"), font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=10)
        tk.Label(totals_frame, textvariable=self.total_credit_var, font=('Arial', 10)).pack(side=tk.LEFT)

        tk.Label(totals_frame, text=self.app.t("Total Debit:"), font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=10)
        tk.Label(totals_frame, textvariable=self.total_debit_var, font=('Arial', 10)).pack(side=tk.LEFT)

        tk.Label(totals_frame, text=self.app.t("Balance:"), font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=10)
        tk.Label(totals_frame, textvariable=self.balance_var, font=('Arial', 10)).pack(side=tk.LEFT)
        if self.app.language == "Arabic":
            headers = ["التاريخ", "الوصف", 'المدين', 'الدائن',  "طريقة الدفع"]
        else:
            headers = ["date", "description", 'debit', 'credit',  "payment_method"]
        filename_excel = f"تقرير الخزنه اليومية_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filename_pdf = f"تقرير الخزنه اليومية_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        report_folder = "تقارير الخزنه اليومية"

        # If they're tkinter variables
        if hasattr(self.total_credit_var, 'get'):
            print(f"Actual Values - Credit: {self.total_credit_var.get()}, Debit: {self.total_debit_var.get()}, Balance: {self.balance_var.get()}")
        date=datetime.now().strftime('%Y-%m-%d')
        self.fetch_transactions()
        excel_btn = tk.Button(totals_frame,
                            text=self.app.t("Export to Excel"), 
                            command=lambda: self.app.export_to_excel(self.filtered_transactions_table,headers=headers,filename=filename_excel,
                                                                report_folder=report_folder,title=report_folder,
                                                                startdate =date,
                                                                enddate   =date,
                                                                footerline_out_of_table=[
                                                                    f"{self.app.t("Total Credit:")} {str(self.total_credit_var.get())}",
                                                                    f"{self.app.t("Total Debit:")} {str(self.total_debit_var.get())}",
                                                                    f"{self.app.t("Balance:")} {str(self.balance_var.get())}"
                                                                ], source="Treasury"
                                                                 ),bg="#21F35D", fg='white')
        # Create a variable to hold the selected page size
        self.page_size_var = tk.StringVar(value="A4")  # Default value

        # Create the OptionMenu (drop-down list)
        page_sizes = ["A1", "A2", "A3", "A4", "A5", "A6", "A7"]
        page_size_menu = tk.OptionMenu(totals_frame, self.page_size_var, *page_sizes)
        pdf_btn   = tk.Button(totals_frame, 
                            text=self.app.t("Export to PDF and Print"),
                            command=lambda: self.app.export_to_pdf(self.filtered_transactions_table,headers=headers,filename=filename_pdf,
                                                                report_folder=report_folder,title=report_folder,
                                                                startdate =date,
                                                                enddate   =date,
                                                                footerline_out_of_table=[
                                                                    f"إجمالي دائن: {str(self.total_credit_var.get())}",
                                                                    f"إجمالي مدين: {str(self.total_debit_var.get())}",
                                                                    f"الرصيد: {str(self.balance_var.get())}"
                                                                ], source="Treasury",page_size=config.PAGE_SIZES[self.page_size_var.get()]
                                                                ),bg="#2144F3", fg='white')
        excel_btn.pack(side=tk.LEFT, padx=10, pady=5)
        pdf_btn.pack(side=tk.LEFT, padx=10, pady=5)
        page_size_menu.pack(side=tk.LEFT, padx=10, pady=5)

    def parse_date(self, date_str):
        # print(date_str)
        if not date_str:
            return None
        # print(date_str)
        date_str = str(date_str).strip()  # Remove leading/trailing whitespace
        # print(date_str)
        # Remove surrounding quotes if present
        if date_str.startswith(('"', "'")) and date_str.endswith(('"', "'")):
            date_str = date_str[1:-1].strip()

        # Preprocessing for malformed timezone formats
        if 'T' in date_str and '+' not in date_str and 'Z' not in date_str:
            if date_str.endswith(':00'):
                date_str = date_str[:-3] + '+00:00'
            elif date_str.count(':') == 4:
                parts = date_str.rsplit(':', 1)
                date_str = f"{parts[0]}+00:00"

        # Fix timezone colon format using regex to target only timezone offsets
        tz_colon_match = re.search(r'([+-]\d{2}):(\d{2})$', date_str)
        if tz_colon_match:
            date_str = date_str[:-3] + date_str[-2:]

        formats = [
            "%d/%m/%Y %H:%M",          # Format: "23/05/2025 23:10"
            "%Y-%m-%dT%H:%M:%S.%f%z",  # ISO format with timezone
            "%Y-%m-%dT%H:%M:%S%z",     # ISO without milliseconds
            "%Y-%m-%d",                # Simple date format
            "%d/%m/%Y",                # Date without time
            "%d/%m/%y %H:%M"           # Short year format
        ]

        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                if dt.tzinfo is None:
                    dt = pytz.utc.localize(dt)
                else:
                    dt = dt.astimezone(pytz.utc)
                return dt
            except ValueError:
                continue
        
        try:
            # return datetime.fromisoformat(date_str).astimezone(pytz.utc)
            return datetime.fromisoformat(date_str)
        except:
            return None

    def fetch_transactions(self):
        self.tree.delete(*self.tree.get_children())
        self.totals = {'credit': 0.0, 'debit': 0.0}

        # Get today's date (make it timezone-aware)
        tz = pytz.timezone('UTC')
        today = datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0)
        
        transactions = []
        
        customer_payments = self.app.customer_payments.find()
        # print(customer_payments)
        for doc in customer_payments:
            Customer_info = doc.get("Customer_info", {})
            transactions.append({
                "date": self.parse_date(doc.get("Time", "")),
                "description":  "دفعة"+  " - " + Customer_info.get("name", ""),
                "credit": float(doc.get("Credit", 0)),
                "debit": 0.0,
                "payment_method": doc.get("Payment_method", "").lower().replace(" ", "_")
            })
        # # print(transactions)

        # 2. Employee Salary (Debit) done
        salaries = self.app.employee_salary_collection.find()
        # print(salaries)
        for doc in salaries:
            transactions.append({
                "date": self.parse_date(doc.get("timestamp", "")),
                "description": f"مرتب {doc.get('employee_name', '')}",
                "credit": 0.0,
                "debit": float(doc.get("net_salary", 0)),
                "payment_method": doc.get("payment_method", "").lower().replace(" ", "_")
            })
        # # print(transactions)
        # 3. Employee Withdrawals (Debit) done  
        withdrawals = self.app.employee_withdrawls_collection.find()
        for doc in withdrawals:
            transactions.append({
                "date": self.parse_date(doc.get("timestamp", "")),
                "description": f"سلفة {doc.get('employee_name', '')}",
                "credit": 0.0,
                "debit": float(doc.get("amount_withdrawls", 0)),
                "payment_method": doc.get("payment_method", "").lower().replace(" ", "_")
            })
        # print(transactions)
        # 4. Purchases (Debit)
        purchases = self.app.purchases_collection.find()
        for doc in purchases:
            financials = doc.get("Financials", {})  # Safely get the nested Financials object
            supplier_info = doc.get("supplier_info", {})
            transactions.append({
                "date": self.parse_date(doc.get("Date", "")),
                "description": supplier_info.get("name","") + " - " + doc.get("Receipt_Number", ""),
                "credit": 0.0,
                "debit": float(financials.get("Payed_cash", 0)),  # Access via Financials
                "payment_method": financials.get("Payment_method", "").lower().replace(" ", "_")  # Acce
            })
        # # print(transactions)
        # 5. Sales (Credit)
        sales = self.app.sales_collection.find()
        
        for doc in sales:
            financials = doc.get("Financials", {})  # Safely get the nested Financials object
            Customer_info2= doc.get("Customer_info", {})
            transactions.append({
                "date": self.parse_date(doc.get("Date", "")),
                "description": Customer_info2.get("name","") + "-" + doc.get("Receipt_Number", ""),
                "credit": float(financials.get("Payed_cash", 0)),
                "debit": 0.0,
                "payment_method": financials.get("Payment_method", "").lower().replace(" ", "_")  # Acce
            })
        # # print(transactions)
        # 6. Supplier Payments (Debit)
        supplier_payments = self.app.supplier_payments.find()
        for doc in supplier_payments:
            supplier_info=doc.get("supplier_info", {})
            transactions.append({
                "date": self.parse_date(doc.get("Time", "")),
                "description": "دفعة"+  " - " + supplier_info.get("name", ""),
                "credit": 0.0,
                "debit": float(doc.get("Debit", 0)),
                "payment_method": doc.get("Payment_method", "").lower().replace(" ", "_")
            })
        # 7 general exp. and rev.(depit)--> Expense , (credit) --> Revenue
        general_exp_rev = self.app.general_exp_rev_collection.find()
        for doc in general_exp_rev:
            if doc.get("type","")=="Expense":
                transactions.append({
                    "date": self.parse_date(doc.get("date", "")),
                    # "date": self.parse_date(doc.get("timestamp", "")),
                    "description": doc.get("description", ""),
                    "credit": 0.0,
                    "debit": float(doc.get("amount", 0)),
                    "payment_method": doc.get("payment_method", "").lower().replace(" ", "_")
                })
            if doc.get("type","")=="Revenue":
                transactions.append({
                    "date": self.parse_date(doc.get("date", "")),
                    "description": doc.get("description", ""),
                    "credit": float(doc.get("amount", 0)),
                    "debit": 0.0,
                    "payment_method": doc.get("payment_method", "").lower().replace(" ", "_")
                })

        # Filter transactions
        allowed_methods = ["cash", "instapay", "bank_account", "e_wallet"]
        self.filtered_transactions = []
        self.filtered_transactions_table = []
        
        # Separate today's transactions from older ones
        today_transactions = []
        previous_balance = {'credit': 0.0, 'debit': 0.0}
        
        for t in transactions:
            if t["date"] is None:
                continue
                
            if t["payment_method"] not in allowed_methods:
                continue
                
            # Make sure transaction date is timezone-aware for comparison
            trans_date = t["date"]
            if trans_date.tzinfo is None:  # If naive, make it aware
                trans_date = tz.localize(trans_date)
                
            if trans_date >= today:  # Today's transaction
                today_transactions.append(t)
            else:  # Older transaction
                previous_balance['credit'] += t['credit']
                previous_balance['debit'] += t['debit']
        
        # Add previous balance as first entry if exists
        if previous_balance['credit'] > 0 or previous_balance['debit'] > 0:
            prev_balance_desc = "الرصيد السابق" if self.app.language == "Arabic" else "Previous Balance"
            prev_entry = {
                "date": today,
                "description": prev_balance_desc,
                "credit": previous_balance['credit'],
                "debit": previous_balance['debit'],
                "payment_method": "balance_carry_forward"
            }
            self.filtered_transactions.append(prev_entry)
            self.totals['credit'] += previous_balance['credit']
            self.totals['debit'] += previous_balance['debit']
            
            # Add to treeview
            self.tree.insert("", "end", values=(
                today.strftime("%d/%m/%Y %H:%M"),
                prev_balance_desc,
                f"{previous_balance['credit']:,.2f} ج.م",
                f"{previous_balance['debit']:,.2f} ج.م",
                "رصيد سابق" if self.app.language == "Arabic" else "Opening Balance"
            ))
        # Format for table
        # Add to filtered_transactions_table at the TOP
        if self.app.language == "Arabic":
            self.filtered_transactions_table.insert(0, {  # insert at position 0 (top)
                "طريقة الدفع": "رصيد سابق",
                "المدين": f"{previous_balance['debit']:,.2f} ج.م", 
                "الدائن": f"{previous_balance['credit']:,.2f} ج.م",
                "الوصف": prev_balance_desc,
                "التاريخ": today.strftime("%d/%m/%Y %H:%M")
            })
        else:
            self.filtered_transactions_table.insert(0, {  # insert at position 0 (top)
                "payment_method": "Opening Balance",
                "debit": f"{previous_balance['debit']:,.2f} ج.م", 
                "credit": f"{previous_balance['credit']:,.2f} ج.م",
                "description": prev_balance_desc,
                "date": today.strftime("%d/%m/%Y %H:%M")
            })        
        # Add today's transactions
        for t in today_transactions:
            self.filtered_transactions.append(t)
            self.totals['credit'] += t['credit']
            self.totals['debit'] += t['debit']
            
            # Format for table
            if self.app.language == "Arabic":
                self.filtered_transactions_table.append({
                    "طريقة الدفع": t["payment_method"].replace("_", " ").title(),
                    "المدين": f"{t['debit']:,.2f} ج.م", 
                    "الدائن": f"{t['credit']:,.2f} ج.م",
                    "الوصف": t["description"],
                    "التاريخ": t["date"].strftime("%d/%m/%Y %H:%M")
                })
            else:
                self.filtered_transactions_table.append({
                    "payment_method": t["payment_method"].replace("_", " ").title(),
                    "debit": f"{t['debit']:,.2f} ج.م", 
                    "credit": f"{t['credit']:,.2f} ج.م",
                    "description": t["description"],
                    "date": t["date"].strftime("%d/%m/%Y %H:%M")
                })
                
            # Add to treeview
            self.tree.insert("", "end", values=(
                t["date"].strftime("%d/%m/%Y %H:%M"),
                t["description"],
                f"{t['credit']:,.2f} ج.م",
                f"{t['debit']:,.2f} ج.م",
                t["payment_method"].replace("_", " ").title()
            ))

        # Update totals display
        self.total_credit_var.set(f"{self.totals['credit']:,.2f} ج.م")
        self.total_debit_var.set(f"{self.totals['debit']:,.2f} ج.م")
        balance = self.totals['credit'] - self.totals['debit']
        self.balance_var.set(f"{balance:,.2f} ج.م")


    def show_sales_chart(self,container, labels, values):
        fig = Figure(figsize=(4, 3))
        ax = fig.add_subplot(111)
        ax.bar(labels, values, color='orange')
        ax.set_title("Top Customers")
        chart = FigureCanvasTkAgg(fig, master=container)
        chart.get_tk_widget().pack()


    def sales_report(self, user_role):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.app.topbar.topbar(show_back_button=True, Back_to_Reports_Window=True)

        # === Filters ===
        filter_frame = ttk.Frame(self.root)
        filter_frame.pack(pady=10)

        ttk.Label(filter_frame, text="Start Date:").grid(row=0, column=0)
        start_date = DateEntry(filter_frame)
        start_date.grid(row=0, column=1, padx=5)

        ttk.Label(filter_frame, text="End Date:").grid(row=0, column=2)
        end_date = DateEntry(filter_frame)
        end_date.grid(row=0, column=3, padx=5)

        # === Table ===
        table = ttk.Treeview(self.root, columns=("A", "B", "C"), show="headings", height=6)
        table.heading("A", text="Metric")
        table.heading("B", text="Value")
        table.heading("C", text="Details")
        table.pack(pady=10)

        data = self.generate_report_data()
        for row in data:
            table.insert("", "end", values=row)

        # === Chart ===
        chart_frame = tk.Frame(self.root)
        chart_frame.pack()
        self.show_sales_chart(chart_frame, ["عماد خطاب", "أحمد سالم"], [70000, 30000])

        # === Export Buttons ===
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        # headers = ["Metric", "Value", "Details", "Date"]
        
        ttk.Button(button_frame, text="Export to Excel", command=lambda: self.app.export_to_excel(data)).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Export to PDF and Print", command=lambda: self.app.export_to_pdf(data)).grid(row=0, column=1, padx=10)

    def generate_report_data(self):
        return [
            ["Total Sales", "72000", "From 45 invoices"],
            ["Top Customer", "عماد خطاب", "EGP 70,000"],
            ["Total Items Sold", "320", "25 Products"]
        ]