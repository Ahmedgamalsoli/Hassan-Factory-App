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
class TreasuryWindow:
    def __init__(self, root, app):
        self.root = root
        self.app = app  # save reference to SalesSystemApp

    def Treasury_window(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        self.app.topbar.topbar(show_back_button=True)

        # Main container
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Filter controls
        filter_frame = tk.Frame(main_frame)
        filter_frame.pack(fill=tk.X, pady=10)

        # Date filters
        date_frame = tk.Frame(filter_frame)
        date_frame.pack(side=tk.LEFT, padx=10)

        tk.Label(date_frame, text=self.app.AuxiliaryClass.t("From Date:")).pack(side=tk.LEFT)
        self.app.from_date = DateEntry(date_frame, date_pattern="dd/mm/yyyy")
        self.app.from_date.pack(side=tk.LEFT, padx=10)

        tk.Label(date_frame, text=self.app.AuxiliaryClass.t("To Date:")).pack(side=tk.LEFT, padx=(20,0))
        self.app.to_date = DateEntry(date_frame, date_pattern="dd/mm/yyyy")
        self.app.to_date.pack(side=tk.LEFT)

        # Payment method filter
        method_frame = tk.Frame(filter_frame)
        method_frame.pack(side=tk.LEFT, padx=20)

        tk.Label(method_frame, text=self.app.AuxiliaryClass.t("Payment Method:")).pack(side=tk.LEFT)
        self.app.payment_method = ttk.Combobox(
            method_frame,
            values=["All", "Cash", "Instapay", "Bank Account", "E Wallet"]
        )
        self.app.payment_method.set("All")
        self.app.payment_method.pack(side=tk.LEFT, padx=10)

        # Search button
        search_btn = tk.Button(filter_frame, text=self.app.AuxiliaryClass.t("Search"), command=self.fetch_transactions)
        search_btn.pack(side=tk.RIGHT, padx=10)

        # Results Treeview
        columns = ("date", "description", "credit", "debit", "payment_method")
        self.app.tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        
        # Configure columns
        self.app.tree.heading("date", text=self.app.AuxiliaryClass.t("Date"))
        self.app.tree.heading("description", text=self.app.AuxiliaryClass.t("Description"))
        self.app.tree.heading("credit", text=self.app.AuxiliaryClass.t("Credit"))
        self.app.tree.heading("debit", text=self.app.AuxiliaryClass.t("Debit"))
        self.app.tree.heading("payment_method", text=self.app.AuxiliaryClass.t("Payment Method"))

        self.app.tree.column("date", width=120, anchor='center')
        self.app.tree.column("description", width=250, anchor='center')
        self.app.tree.column("credit", width=120, anchor='center')
        self.app.tree.column("debit", width=120, anchor='center')
        self.app.tree.column("payment_method", width=150, anchor='center')

        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.app.tree.yview)
        self.app.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.app.tree.pack(fill=tk.BOTH, expand=True)

        # Totals display
        totals_frame = tk.Frame(main_frame)
        totals_frame.pack(fill=tk.X, pady=10)

        self.app.total_credit_var = tk.StringVar()
        self.app.total_debit_var = tk.StringVar()
        self.app.balance_var = tk.StringVar()

        tk.Label(totals_frame, text=self.app.AuxiliaryClass.t("Total Credit:"), font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=10)
        tk.Label(totals_frame, textvariable=self.app.total_credit_var, font=('Arial', 10)).pack(side=tk.LEFT)

        tk.Label(totals_frame, text=self.app.AuxiliaryClass.t("Total Debit:"), font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=10)
        tk.Label(totals_frame, textvariable=self.app.total_debit_var, font=('Arial', 10)).pack(side=tk.LEFT)

        tk.Label(totals_frame, text=self.app.AuxiliaryClass.t("Balance:"), font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=10)
        tk.Label(totals_frame, textvariable=self.app.balance_var, font=('Arial', 10)).pack(side=tk.LEFT)
        if self.app.language == "Arabic":
            headers = ["التاريخ", "الوصف", 'المدين', 'الدائن',  "طريقة الدفع"]
        else:
            headers = ["date", "description", 'debit', 'credit',  "payment_method"]
        filename_excel = f"تقرير الخزنه_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filename_pdf = f"تقرير الخزنه_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        report_folder = "تقارير الخزنه"

        # If they're tkinter variables
        if hasattr(self.app.total_credit_var, 'get'):
            print(f"Actual Values - Credit: {self.app.total_credit_var.get()}, Debit: {self.app.total_debit_var.get()}, Balance: {self.app.balance_var.get()}")

        excel_btn = tk.Button(totals_frame,
                            text=self.app.AuxiliaryClass.t("Export to Excel"), 
                            command=lambda: self.app.AuxiliaryClass.export_to_excel(self.app.filtered_transactions_table,headers=headers,filename=filename_excel,
                                                                report_folder=report_folder,title=report_folder,
                                                                startdate=self.app.from_date.get() if hasattr(self.app.from_date, 'get') else str(self.app.from_date),
                                                                enddate=self.app.to_date.get() if hasattr(self.app.to_date, 'get') else str(self.app.to_date),
                                                                footerline_out_of_table=[
                                                                    f"{self.app.AuxiliaryClass.t("Total Credit:")} {str(self.app.total_credit_var.get())}",
                                                                    f"{self.app.AuxiliaryClass.t("Total Debit:")} {str(self.app.total_debit_var.get())}",
                                                                    f"{self.app.AuxiliaryClass.t("Balance:")} {str(self.app.balance_var.get())}"
                                                                ], source= "Treasury"
                                                                 ),bg="#21F35D", fg='white')
        # Create a variable to hold the selected page size
        self.page_size_var = tk.StringVar(value="A4")  # Default value

        # Create the OptionMenu (drop-down list)
        page_sizes = ["A1", "A2", "A3", "A4", "A5", "A6", "A7"]
        page_size_menu = tk.OptionMenu(totals_frame, self.page_size_var, *page_sizes)
        
        pdf_btn   = tk.Button(totals_frame, 
                            text=self.app.AuxiliaryClass.t("Export to PDF and Print"),
                            command=lambda: self.app.AuxiliaryClass.export_to_pdf(self.app.filtered_transactions_table,headers=headers,filename=filename_pdf,
                                                                report_folder=report_folder,title=report_folder,
                                                                startdate=self.app.from_date.get() if hasattr(self.app.from_date, 'get') else str(self.app.from_date),
                                                                enddate=self.app.to_date.get() if hasattr(self.app.to_date, 'get') else str(self.app.to_date),
                                                                footerline_out_of_table=[
                                                                    f"إجمالي دائن: {str(self.app.total_credit_var.get())}",
                                                                    f"إجمالي مدين: {str(self.app.total_debit_var.get())}",
                                                                    f"الرصيد: {str(self.app.balance_var.get())}"
                                                                ], source= "Treasury",page_size=config.PAGE_SIZES[self.page_size_var.get()]
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
        self.app.tree.delete(*self.app.tree.get_children())
        self.app.totals = {'credit': 0.0, 'debit': 0.0}

        # Get filter parameters
        start_date = self.app.from_date.get_date()
        end_date = self.app.to_date.get_date()
        selected_method = self.app.payment_method.get().lower()

        # Convert dates to UTC datetime
        tz = pytz.timezone('UTC')
        start_date = tz.localize(datetime.combine(start_date, datetime.min.time()))
        end_date = tz.localize(datetime.combine(end_date, datetime.max.time()))
        start_date_str = start_date.strftime("%d/%m/%Y %H:%M")
        end_date_str = end_date.strftime("%d/%m/%Y %H:%M")
        transactions = []

        # 1. Customer Payments (Credit) done
        customer_payments = self.app.customer_payments.find({"Time": {"$gte": start_date, "$lte": end_date}})
        # print(customer_payments)
        for doc in customer_payments:
            Customer_info = doc.get("Customer_info", {})
            transactions.append({
                "date": self.parse_date(doc.get("Time", "")),
                "description": "دفعة"+  " - " + Customer_info.get("name", ""),
                "credit": float(doc.get("Credit", 0)),
                "debit": 0.0,
                "payment_method": doc.get("Payment_method", "").lower().replace(" ", "_")
            })
        # # print(transactions)

        # 2. Employee Salary (Debit) done
        salaries = self.app.employee_salary_collection.find({"timestamp": {"$gte": start_date, "$lte": end_date}})
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
        withdrawals = self.app.employee_withdrawls_collection.find({"timestamp": {"$gte": start_date, "$lte": end_date}})
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
        purchases = self.app.purchases_collection.find({"Date": {"$gte": start_date, "$lte": end_date}})
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
        sales = self.app.sales_collection.find({"Date": {"$gte": start_date, "$lte": end_date}})
        
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
        supplier_payments = self.app.supplier_payments.find({"Time": {"$gte": start_date, "$lte": end_date}})
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
        general_exp_rev = self.app.general_exp_rev_collection.find({"date": {"$gte": start_date, "$lte": end_date}})
        for doc in general_exp_rev:
            if doc.get("type","")=="Expense":
                transactions.append({
                    "date": self.parse_date(doc.get("date", "")),
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
        # print(transactions)
        # Filter transactions
        allowed_methods = ["cash", "instapay", "bank_account", "e_wallet"]
        self.app.filtered_transactions = []
        self.app.filtered_transactions_table = []
        for t in transactions:
            if selected_method != "all":
                if t["payment_method"] != selected_method.replace(" ", "_"):
                    continue
            if t["payment_method"] in allowed_methods and t["date"] is not None:
                self.app.filtered_transactions.append(t)
                if self.app.language == "Arabic":
                    self.app.filtered_transactions_table.append({
                        "طريقة الدفع": t["payment_method"].replace("_", " ").title(),
                        "المدين": f"{t['debit']:,.2f} ج.م", 
                        "الدائن": f"{t['credit']:,.2f} ج.م",
                        "الوصف": t["description"],
                        "التاريخ": t["date"].strftime("%d/%m/%Y %H:%M")
                    })
                else:
                    self.app.filtered_transactions_table.append({
                        "payment_method": t["payment_method"].replace("_", " ").title(),
                        "debit": f"{t['debit']:,.2f} ج.م", 
                        "credit": f"{t['credit']:,.2f} ج.م",
                        "description": t["description"],
                        "date": t["date"].strftime("%d/%m/%Y %H:%M")
                    })
        # Populate treeview and calculate totals
        for t in self.app.filtered_transactions:
            self.app.totals['credit'] += t['credit']
            self.app.totals['debit'] += t['debit']
            
            self.app.tree.insert("", "end", values=(
                t["date"].strftime("%d/%m/%Y %H:%M"),
                t["description"],
                f"{t['credit']:,.2f} ج.م",
                f"{t['debit']:,.2f}  ج.م",
                t["payment_method"].replace("_", " ").title()
            ))

        # Update totals display
        self.app.total_credit_var.set(f"{self.app.totals['credit']:,.2f} ج.م")
        self.app.total_debit_var.set (f"{self.app.totals['debit']:,.2f}  ج.م")
        # self.app.total_debit_var.set(f"${self.app.totals['debit']:,.2f}")
        balance = self.app.totals['credit'] - self.app.totals['debit']
        self.app.balance_var.set(f"{balance:,.2f} ج.م")
        
    
