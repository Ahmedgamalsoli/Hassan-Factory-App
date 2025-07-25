# ======================
# Used imports
# ======================

import tkinter as tk
import io
import re
import os
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
from reportlab.lib.pagesizes import letter
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
# from calculator import CalculatorPopup
from Login import LoginWindow
# from AuxiliaryClass import AlwaysOnTopInputDialog

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

COLORS = {
    "background": "#F5F7FA",       # Light grey background
    "primary": "#3B82F6",           # Dark blue for headers
    "main_frame": "#2A3F5F",           # Dark blue for headers
    "secondary": "#00C0A3",         # Teal for primary actions
    "accent": "#FF6F61",            # Coral for highlights
    "text": "#2A3F5F",              # Dark blue text
    "card": "#FFFFFF",              # White card backgrounds
    "chart1": "#00C0A3",            # Teal for Sales
    "chart2": "#FF6F61",            # Coral for Purchases
    "highlight": "#6C5CE7",         # Purple for interactive elements
    "table_header": "#FFFFFF",      # Dark blue table headers
    "positive": "#00C0A3",          # Teal for positive metrics
    "neutral": "#A0AEC0",            # Grey for secondary elements
    "top_bar": "#dbb40f",        # Dark blue for top bar
    "top_bar_icons": "#000000",  # White for top bar icons
}

# Determine the base directory
if getattr(sys, "frozen", False):
    # Running as an executable
    BASE_DIR = sys._MEIPASS
else:
    # Running as a script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

field_mapping = {
    # Customer_info
    'customer_code': ('Customer_info', 'code'),
    'customer_name': ('Customer_info', 'name'),
    'customer_phone1': ('Customer_info', 'phone1'),
    'customer_phone2': ('Customer_info', 'phone2'),
    'customer_address': ('Customer_info', 'address'),
    
    # Financials
    'Net_total': ('Financials', 'Net_total'),
    'Previous_balance': ('Financials', 'Previous_balance'),
    'Total_balance': ('Financials', 'Total_balance'),
    'Payed_cash': ('Financials', 'Payed_cash'),
    'Remaining_balance': ('Financials', 'Remaining_balance'),
    'Payment_method': ('Financials', 'Payment_method'),
    
    # Supplier_info
    'supplier_code': ('supplier_info', 'code'),
    'supplier_name': ('supplier_info', 'name'),
    'supplier_phone1': ('supplier_info', 'phone1'),
    'supplier_phone2': ('supplier_info', 'phone2'),
    'supplier_address': ('supplier_info', 'address'),
}

search_field_mapping = {
    # Customer_info
    'customer_code': ('Customer_info', 'code'),
    'customer_name': ('Customer_info', 'name'),
    'customer_phone1': ('Customer_info', 'phone1'),
    'customer_phone2': ('Customer_info', 'phone2'),
    'customer_address': ('Customer_info', 'address'),
    
    # Financials
    'Net_total': ('Financials', 'Net_total'),
    'Previous_balance': ('Financials', 'Previous_balance'),
    'Total_balance': ('Financials', 'Total_balance'),
    'Payed_cash': ('Financials', 'Payed_cash'),
    'Remaining_balance': ('Financials', 'Remaining_balance'),
    'Payment_method': ('Financials', 'Payment_method'),
    'transport_fees' : ('Financials', 'transport_fees'),

    # Supplier_info
    'supplier_code': ('supplier_info', 'code'),
    'supplier_name': ('supplier_info', 'name'),
    'supplier_phone1': ('supplier_info', 'phone1'),
    'supplier_phone2': ('supplier_info', 'phone2'),
    'supplier_address': ('supplier_info', 'address'),
    

    #Items
    'Product_code': ('Items', 'Product_code'),
    'product_name': ('Items', 'product_name'),
    'material_code': ('Items', 'material_code'),
    'material_name': ('Items', 'material_name'),
    'Unit': ('Items', 'Unit'),
    'QTY': ('Items', 'QTY'),
    'numbering': ('Items', 'numbering'),
    'Total_QTY': ('Items', 'Total_QTY'),
    'Unit_price': ('Items', 'Unit_price'),
    'Discount_Type': ('Items', 'Discount_Type'),
    'Discount_Value': ('Items', 'Discount_Value'),
    'Final_Price': ('Items', 'Final_Price'),
}


LOCKED_FIELDS = {
    "root": [ "Operation_Number","Code","employee_code", "material_code", "product_code", "Receipt_Number", "Operation_Number"],
    "Customer_info": ["code"],
    "supplier_info": ["code"],
    "Items": ["material_code","product_code"]
}


MANDATORTY_FIELDS = { # list all mandatory fields (fields that can't be empty)
    "Name", "Phone_number1", "Code", "Company_address", "Name", "Password", "Role", "Phone_number", "Address", "Salary",
    "product_name","category","stock_quantity","Unit_Price","product_code","Units",
    "material_name","material_code", "employee_code", "employee_name"
}

MANDATORY_DBS = {
    "Customers", "Employees", "Materials", "Products", "Suppliers" 
}

ZEROED_FIELDS = {
    "Sales_grade", "Growth_grade", "Frequency_grade", "Credit", "Debit", "Balance", "Sales"
}

PRIMARY_KEYS = {
    "Employees": "Id",
    "Products": "product_code",
    "Materials": "material_code",
    "Customers": "Code",
    "Suppliers": "Code",
    # "Employee_appointimets": "employee_code",
    "Sales": "Receipt_Number",
    "Purchases": "Receipt_Number",
    "Customer_Payments": "Operation_Number",
    "Supplier_Payments": "Operation_Number",
    # "Production": "timestamp",
    # "Employee_Salary": "timestamp",
    # "Employee_withdrawls": "timestamp",
    "general_exp_rev": "code",
}

PRIMARY_KEY_STARTERS = {
    "Customers": "CU",
    "Suppliers": "SU",
    "Products": "PR",
    "Employees": "EMP",
    "Sales": "INV",
    "Materials": "MAT",
    "Purchases": "INV",
    "Customer_Payments": "PM",
    "Supplier_Payments": "PM",
    # "Production": "PRD",
    # "Employee_Salary": "SAL",
    # "Employee_withdrawls": "WD",
    "general_exp_rev": "GEN",
}

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
        self.root.configure(bg=COLORS["background"])
        self.current_window = None

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
        
        # style.theme_create("modern", parent="alt", settings={
        #     "TFrame": {"configure": {"background": COLORS["background"]}},
        #     "TLabel": {
        #         "configure": {
        #             "background": COLORS["background"],
        #             "foreground": COLORS["text"],
        #             "font": self.custom_font
        #         }
        #     },
        #     "TButton": {
        #         "configure": {
        #             "anchor": "center",
        #             "relief": "flat",
        #             "background": COLORS["primary"],
        #             "foreground": COLORS["text"],
        #             "font": self.custom_font,
        #             "padding": 10
        #         },
        #         "map": {
        #             "background": [
        #                 ("active", COLORS["highlight"]),
        #                 ("disabled", "#95a5a6")
        #             ]
        #         }
        #     }
        # })



        style.map('Treeview', background=[('selected', '#2196F3')], foreground=[('selected', 'white')])
        
        # style.theme_use("modern")

        self.Connect_DB()
                    
        self.stop_event = threading.Event()
        
        self.image_refs = []
        self.filtered_transactions = []
        self.production_entries = []
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
            "Sales Invoice": {"Arabic": "فاتورة مبيعات", "English": "Sales Invoice"},
            "Update Sales Invoice": {"Arabic": "تعديل فاتورة مبيعات", "English": "Update Sales Invoice"},
            "New Purchase Invoice": {"Arabic": "فاتورة مشتريات جديدة", "English": "New Purchase Invoice"},
            "Purchase Invoice": {"Arabic": "فاتورة مشتريات", "English": "Purchase Invoice"},
            "Update Purchase Invoice": {"Arabic": "تعديل فاتورة مشتريات", "English": "Update Purchase Invoice"},
            "Receive Payment": {"Arabic": "حسابات وتوريدات العملاء", "English": "Customer Hub"},
            "Treasury": {"Arabic": "الخزينة", "English": "Treasury"},
            "Make Payment": {"Arabic": "حسابات وتوريدات الموردين", "English": "Supplier Hub"},
            "Customers": {"Arabic": "العملاء", "English": "Customers"},
            "Suppliers": {"Arabic": "الموردين", "English": "Suppliers"},
            "Customers number": {"Arabic": "عدد العملاء", "English": "Customers"},
            "Suppliers number": {"Arabic": "عدد الموردين", "English": "Suppliers"},
            "Products": {"Arabic": "المنتجات", "English": "Products"},
            "Materials": {"Arabic": "الخامات", "English": "Materials"},
            "Employees": {"Arabic": "الموظفين", "English": "Employees"},
            "Customer Name":{"Arabic": "اسم العميل", "English": "Customer:"},
            "Supplier Name":{"Arabic": "اسم المورد :", "English": "Supplier:"},
            "Previous Balance":{"Arabic": "الحساب السابق:", "English": "Previous Balance:"},
            "Paid Money":{"Arabic": "المبلغ المدفوع:", "English": "Paid Money:"},
            "Customer Code":{"Arabic": "كوود العميل", "English": "Customer Code:"},
            "Supplier Code":{"Arabic": "كوود المورد", "English": "Supplier Code:"},
            "Payment Method":{"Arabic": "طريقة الدفع:", "English": "Payment Method:"},
            "Product_code":{"Arabic": "كود المنتج", "English": "Product Code"},
            "product_name":{"Arabic": "اسم المنتج", "English": "Product Name"},
            "unit":{"Arabic": "وحدة", "English": "Unit"},
            "Unit":{"Arabic": "الوحدة", "English": "Unit"},
            "numbering":{"Arabic": "العدد", "English": "Numbering"},
            "QTY":{"Arabic": "الكمية", "English": "Quantity"},
            "Discount Type":{"Arabic": "نوع الخصم", "English": "Discount Type"},
            "Discount_Type":{"Arabic": "نوع الخصم", "English": "Discount Type"},
            "Discount Value":{"Arabic": "قيمة الخصم", "English": "Discount Value"},
            "Discount_Value":{"Arabic": "قيمة الخصم", "English": "Discount Value"},
            "Total_QTY":{"Arabic": "إجمالي الكمية", "English": "Total Quantity"},
            "Unit_Price":{"Arabic": "سعر الوحدة", "English": "Unit Price"},
            "Unit_price":{"Arabic": "سعر الوحدة", "English": "Unit Price"},
            "Total_Price":{"Arabic": "إجمالي السعر", "English": "Total Price"},
            "Material_code":{"Arabic": "كود الخام", "English": "Material Code"},
            "Material_name":{"Arabic": "اسم الخام", "English": "Material Name"},
            "➕ Add 3 More Rows":{"Arabic": "➕ أضف 3 صفوف أخرى", "English": "➕ Add 3 More Rows"},
            "➕ Add Row":{"Arabic": "➕ أضف صف", "English": "➕ Add Row"},
            "💾 Save Invoice":{"Arabic": "💾 حفظ الفاتورة", "English": "💾 Save Invoice"},
            "💾 Save Order":{"Arabic": "💾 حفظ الطلب", "English": "💾 Save Order"},
            "Search":{"Arabic": "بحث", "English": "Search"},
            "Name":{"Arabic": "الاسم", "English": "Name"},
            "Phone_number1":{"Arabic": "رقم التليفون 1", "English": "Phone Number 1"},
            "Phone_number2":{"Arabic": "رقم التليفون 2", "English": "Phone Number 2"},
            "Code":{"Arabic": "كوود", "English": "Code"},
            "Purchase_mgr_number":{"Arabic": "رقم مدير المشتريات", "English": "Purchase Mgr Number"},
            "Financial_mgr_number":{"Arabic": "رقم مدير المالية", "English": "Financial Mgr Number"},
            "Purchase_mgr_name":{"Arabic": "اسم مديرالمشتريات", "English": "Purchase Mgr Name"},
            "Financial_mgr_name":{"Arabic": "اسم مدير المالية", "English": "Financial Mgr Name"},
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
            "Purchases":{"Arabic": "عدد المشتريات", "English": "Purchases"},
            "Password":{"Arabic": "الباسورد", "English": "Password"},
            "Role":{"Arabic": "الوظيفة", "English": "Role"},
            "Join_Date":{"Arabic": "تاريخ الالتحاق", "English": "Join Date"},
            "National_id_pic":{"Arabic": "صورة البطاقة", "English": "National ID Picture"},
            "Phone_number":{"Arabic": "رقم التليفون", "English": "Phone Number"},
            "Address":{"Arabic": "العنوان", "English": "Address"},
            "Salary":{"Arabic": "المرتب", "English": "Salary"},
            "Salary:":{"Arabic": "المرتب:", "English": "Salary:"},
            "category":{"Arabic": "التصنيف", "English": "category"},
            "stock_quantity":{"Arabic": "كمية المخزون", "English": "stock Quantity"},
            "specs":{"Arabic": "المواصفات", "English": "Specs"},
            "Specs":{"Arabic": "المواصفات", "English": "Specs"},
            "product_code":{"Arabic": "كود المنتج", "English": "Product_code"},
            "Units":{"Arabic": "الوحدات", "English": "Units"},
            "prod_pic":{"Arabic": "صورة المنتج", "English": "product Picture"},
            "sales":{"Arabic": "المبيعات", "English": "Sales"},
            "purchases":{"Arabic": "المشتريات", "English": "Purchases"},
            "Employee Statistics":{"Arabic": "احصائيات الموظفين", "English": "Employees Statistics"},
            "Employee hours":{"Arabic": "مواعيد الموظفين", "English": "Employees hours"},
            "Employee Withdrawals":{"Arabic": "مسحوبات الموظفين", "English": "Employees Withdrawals"},
            "Material Code":{"Arabic":"كود الخامة","English":"Material Code"},
            "material_code":{"Arabic":"كود الخامة","English":"Material Code"},
            "material_name":{"Arabic":"اسم الخامة","English":"Material Name"},
            "Material Name":{"Arabic":"اسم الخامة","English":"Material Name"},
            "material_pic":{"Arabic":"صورة الخامة","English":"Material Pic"},
            "Material Available Qty":{"Arabic":"الكمية المتاحة","English":"Material Ava qty"},
            "Material Qty":{"Arabic":"الكمية المستخدمة","English":"Material_Qty"},
            "Product Code":{"Arabic":"كود المنتج","English":"Product Code"},
            "Product Name":{"Arabic":"اسم المنتج","English":"Product Name"},
            "Product Available Qty":{"Arabic":"الكمية المتاحة","English":"Product Ava Qty"},
            "Product Qty":{"Arabic":"الكمية المنتجة","English":"Product_Qty"},
            "Waste":{"Arabic":"الهالك","English":"Waste"},
            "Employee Name:":{"Arabic":"اسم الموظف:","English":"Employee Name:"},
            "Employee Code:":{"Arabic":"كود الموظف:","English":"Employee Code:"},
            "Check In/Out":{"Arabic":"حضور وانصراف","English":"Check In/Out"},
            "Employee Name":{"Arabic":"اسم الموظف","English":"Employee Name"},
            "Check-in Time":{"Arabic":"وقت الحضور","English":"Check-in Time"},
            "Duration":{"Arabic":"المدة","English":"Duration"},
            "Employee Selection":{"Arabic":"اختيار الموظفين","English":"Employee Selection"},
            "Withdrawal Details":{"Arabic":"تفاصيل السحب","English":"Withdrawal Details"},
            "Withdrawal Amount:":{"Arabic":"مبلغ السحب:","English":"Withdrawal Amount:"},
            "Previous Withdrawals:":{"Arabic":"المسحوبات السابقة:","English":"Previous Withdrawals:"},
            "💾 Save Withdrawal":{"Arabic":"💾 حفظ السحب","English":"💾 Save Withdrawal"},
            "Name:":{"Arabic":"الاسم:","English":"Name:"},
            "Code:":{"Arabic":"الكود:","English":"Code:"},
            "code":{"Arabic":"الكود","English":"code"},
            "Month/Year Selection":{"Arabic":"اختيار الشهر/السنة","English":"Month/Year Selection"},
            "Month:":{"Arabic":"الشهر:","English":"Month:"},
            "Year:":{"Arabic":"السنة:","English":"Year:"},
            "Working Hours":{"Arabic":"ساعات العمل","English":"Working Hours"},
            "Start Time:":{"Arabic":"وقت البدء:","English":"Start Time:"},
            "End Time:":{"Arabic":"وقت الانتهاء:","English":"End Time:"},
            "Date":{"Arabic":"التاريخ","English":"Date"},
            "From":{"Arabic":"من","English":"From"},
            "To":{"Arabic":"الي","English":"To"},
            "Delay":{"Arabic":"من وقت البدء","English":"Delay"},
            "More":{"Arabic":"من وقت النهاية","English":"More"},
            "Withdrawls":{"Arabic":"المسحوبات","English":"Withdrawals"},
            "Total Withdrawls:":{"Arabic":"اجمالي المسحوبات:","English":"Total Withdrawals:"},
            "Delay Amount:":{"Arabic":"حساب التأخير","English":"Delay Amount:"},
            "Overtime Amount:":{"Arabic":"حساب الوقت الزيادة","English":"Overtime Amount:"},
            "Payment Method:":{"Arabic":"طريقة الدفع:","English":"Payment Method:"},
            "Base Salary:":{"Arabic":"المرتب الاساسي:","English":"Base Salary:"},
            "Net Salary:":{"Arabic":"صافي المرتب:","English":"Net Salary:"},
            "Save Salary Record":{"Arabic":"💾 احفظ سجل الراتب","English":"💾 Save Salary Record"},
            "From Date:":{"Arabic":"من تاريخ:","English":"From Date:"},
            "To Date:":{"Arabic":"الي تاريخ:","English":"To Date:"},
            "Description":{"Arabic":"الوصف","English":"Description"},
            "description":{"Arabic":"الوصف","English":"Description"},
            "Payment_Method":{"Arabic":"طريقة الدفع","English":"Payment Method"},
            "Total Credit:":{"Arabic":"مجموع الدائن:","English":"Total Credit:"},
            "Total Debit:":{"Arabic":"مجموع المدين:","English":"Total Debit:"},
            "Balance:":{"Arabic":"الصافي:","English":"Balance:"},
            "Login":{"Arabic":"تسجيل الدخول","English":"Login"},
            "Username:":{"Arabic":"اسم المستخدم:","English":"Username:"},
            "Password:":{"Arabic":"الباسورد:","English":"Password:"},
            "Print Error":{"Arabic":"خطأ في الطباعة","English":"Print Error"},
            "Failed to print PDF:":{"Arabic":"فشل في طباعة ملف:","English":"Failed to print PDF:"},
            "No Internet Connection":{"Arabic":"لا يوجد اتصال بالإنترنت","English":"No Internet Connection"},
            "Error":{"Arabic":"خطأ","English":"Error"},
            "Failed to load reports:":{"Arabic":"فشل تحميل التقارير:","English":"Failed to load reports:"},
            "Please select an employee":{"Arabic":"الرجاء اختيار الموظف","English":"Please select an employee"},
            "Success":{"Arabic":"نجاح","English":"Success"},
            "Database Error":{"Arabic":"خطأ في قاعدة البيانات","English":"Database Error"},
            "checked":{"Arabic":"تم","English":"checked"},
            "out":{"Arabic":"تسجيل خروج","English":"out"},
            "in":{"Arabic":"تسجيل دخول","English":"in"},
            "successfully":{"Arabic":"بنجاح","English":"successfully"},
            "Please select an employee":{"Arabic":"الرجاء اختيار الموظف","English":"Please select an employee"},
            "Invalid amount entered":{"Arabic":"تم إدخال مبلغ غير صالح","English":"Invalid amount entered"},
            "Please select payment method":{"Arabic":"الرجاء اختيار طريقة الدفع","English":"Please select payment method"},
            "Withdrawal recorded successfully":{"Arabic":"تم تسجيل السحب بنجاح","English":"Withdrawal recorded successfully"},
            "Failed to save withdrawal:":{"Arabic":"فشل في حفظ السحب:","English":"Failed to save withdrawal:"},
            "Warning":{"Arabic":"تحذير","English":"Warning"},
            "Employee already took the salary in this month":{"Arabic":"لقد استلم الموظف راتبه في هذا الشهر بالفعل","English":"Employee already took the salary in this month"},
            "Enter the payment Method":{"Arabic":"أدخل طريقة الدفع","English":"Enter the payment Method"},
            "Salary record saved successfully":{"Arabic":"تم حفظ سجل الراتب بنجاح","English":"Salary record saved successfully"},
            "Failed to save salary:":{"Arabic":"فشل في حفظ الراتب:","English":"Failed to save salary:"},
            "Amount must be greater than zero":{"Arabic":"يجب أن يكون المبلغ أكبر من الصفر","English":"Amount must be greater than zero"},
            "Please select a payment method":{"Arabic":"الرجاء اختيار طريقة الدفع","English":"Please select a payment method"},
            "recorded successfully!":{"Arabic":"تم التسجيل بنجاح!","English":"recorded successfully!"},
            "Failed to save transaction:":{"Arabic":"فشل حفظ المعاملة:","English":"Failed to save transaction:"},
            "Failed to load products:":{"Arabic":"فشل تحميل المنتجات:","English":"Failed to load products:"},
            "Selection Needed":{"Arabic":"الاختيار مطلوب","English":"Selection Needed"},
            "Please select an invoice first":{"Arabic":"الرجاء تحديد الفاتورة أولاً","English":"Please select an invoice first"},
            "Not Found":{"Arabic":"لم يتم العثور عليه","English":"Not Found"},
            "Invoice not found in database":{"Arabic":"لم يتم العثور على الفاتورة في قاعدة البيانات","English":"Invoice not found in database"},
            "Confirm Delete":{"Arabic":"تأكيد الحذف","English":"Confirm Delete"},
            "Delete invoice":{"Arabic":"حذف الفاتورة","English":"Delete invoice"},
            "permanently?":{"Arabic":"نهائيا؟","English":"permanently?"},
            "Invoice not found":{"Arabic":"لم يتم العثور على الفاتورة","English":"Invoice not found"},
            "Invoice deleted successfully":{"Arabic":"تم حذف الفاتورة بنجاح","English":"Invoice deleted successfully"},
            "Failed to load materials:":{"Arabic":"فشل تحميل الخامات:","English":"Failed to load materials:"},
            "Invalid values in row":{"Arabic":"القيم غير صالحة في الصف","English":"Invalid values in row"},
            "Production order saved successfully":{"Arabic":"تم حفظ أمر الإنتاج بنجاح","English":"Production order saved successfully"},
            "Operation failed:":{"Arabic":"فشلت العملية:","English":"Operation failed:"},
            "Inventory Error":{"Arabic":"خطأ في المخزون","English":"Inventory Error"},
            "Failed to update inventory:":{"Arabic":"فشل تحديث المخزون:","English":"Failed to update inventory:"},
            "Update Error":{"Arabic":"خطأ التحديث","English":"Update Error"},
            "Failed to update product info:":{"Arabic":"فشل تحديث معلومات المنتج:","English":"Failed to update product info:"},
            "Failed to update Material info:":{"Arabic":"فشل في تحديث معلومات الخامات:","English":"Failed to update Material info:"},
            "Discount Error":{"Arabic":"خطأ الخصم","English":"Discount Error"},
            "All fields must be filled!":{"Arabic":"يجب ملء جميع الحقول!","English":"All fields must be filled!"},
            "Cash must be a valid number.":{"Arabic":"يجب أن يكون النقد رقمًا صالحًا.","English":"Cash must be a valid number."},
            "Entry":{"Arabic":"المدخل","English":"Entry"},
            "added.":{"Arabic":"تمت اضافته.","English":"added."},
            "Failed to process code:":{"Arabic":"فشل في معالجة الكود:","English":"Failed to process code:"},
            "No matching code found for name:":{"Arabic":"لم يتم العثور على رمز مطابق للاسم:","English":"No matching code found for name:"},
            "Failed to fetch code for":{"Arabic":"فشل في جلب الكود لـ","English":"Failed to fetch code for"},
            "Error displaying data:":{"Arabic":"خطأ في عرض البيانات:    ","English":"Error displaying data:"},
            "Upload Error":{"Arabic":"خطأ في التحميل","English":"Upload Error"},
            "All Data fields must be filled:":{"Arabic":"يجب ملء جميع حقول البيانات:","English":"All Data fields must be filled:"},
            "is not unique in field":{"Arabic":"ليس فريدًا في هذا المجال","English":"is not unique in field"},
            "Validation Error":{"Arabic":"خطأ التحقق","English":"Validation Error"},
            "Field":{"Arabic":"حقل","English":"Field"},
            "cannot be empty.":{"Arabic":"لا يمكن أن يكون فارغا.","English":"cannot be empty."},
            "Invalid date format for":{"Arabic":"تنسيق التاريخ غير صالح لـ","English":"Invalid date format for"},
            "Please enter a value for":{"Arabic":"الرجاء إدخال قيمة لـ","English":"Please enter a value for"},
            "Failed to upload image:":{"Arabic":"فشل تحميل الصورة:","English":"Failed to upload image:"},
            "No PDF was selected.":{"Arabic":"لم يتم تحديد ملف PDF.","English":"No PDF was selected."},
            "Failed to upload PDF:":{"Arabic":"فشل تحميل ملف PDF:","English":"Failed to upload PDF:"},
            "should be a number":{"Arabic":"يجب أن يكون رقمًا","English":"should be a number"},
            "Please enter a value for":{"Arabic":"الرجاء إدخال قيمة لـ","English":"Please enter a value for"},
            "should be a floating number":{"Arabic":"يجب أن يكون رقمًا عشريا","English":"should be a floating number"},
            "Record added successfully":{"Arabic":"تمت إضافة السجل بنجاح","English":"Record added successfully"},
            "Error adding record:":{"Arabic":"خطأ في إضافة السجل:","English":"Error adding record:"},
            "Please select a record to edit":{"Arabic":"الرجاء تحديد سجل لتعديله","English":"Please select a record to edit"},
            "No data found for selected record":{"Arabic":"لم يتم العثور على بيانات للسجل المحدد","English":"No data found for selected record"},
            "'Id' field not found in table columns":{"Arabic":"لم يتم العثور على حقل 'المعرف' في أعمدة الجدول","English":"'Id' field not found in table columns"},
            "Could not find record in database":{"Arabic":"لم يتم العثور على السجل في قاعدة البيانات","English":"Could not find record in database"},
            "Record updated successfully":{"Arabic":"تم تحديث السجل بنجاح","English":"Record updated successfully"},
            "Info":{"Arabic":"معلومات","English":"Info"},
            "No changes were made (record was identical)":{"Arabic":"لم يتم إجراء أي تغييرات (كان السجل متطابقًا)","English":"No changes were made (record was identical)"},
            "Error updating record:":{"Arabic":"خطأ في تحديث السجل:","English":"Error updating record:"},
            "Please select a record to delete":{"Arabic":"الرجاء تحديد سجل لحذفه","English":"Please select a record to delete"},
            "Unable to determine identifier column.":{"Arabic":"غير قادر على تحديد عمود المعرف.","English":"Unable to determine identifier column."},
            "Confirm":{"Arabic":"تأكيد","English":"Confirm"},
            "Unable to read selected row data.":{"Arabic":"غير قادر على قراءة بيانات الصف المحدد.","English":"Unable to read selected row data."},
            "Are you sure you want to delete this record?":{"Arabic":"هل أنت متأكد أنك تريد حذف هذا السجل؟","English":"Are you sure you want to delete this record?"},
            "No matching record found to delete.":{"Arabic":"لم يتم العثور على سجل مطابق للحذف.","English":"No matching record found to delete."},
            "Unit":{"Arabic":"الوحدة","English":"Unit"},
            "removed from record.":{"Arabic":"تمت إزالتها من السجل.","English":"removed from record."},
            "No changes were made to the document.":{"Arabic":"لم يتم إجراء أي تغييرات على الوثيقة.","English":"No changes were made to the document."},
            "Record deleted successfully.":{"Arabic":"تم حذف السجل بنجاح.","English":"Record deleted successfully."},
            "Error deleting record:":{"Arabic":"خطأ في حذف السجل:","English":"Error deleting record:"},
            "Enter value for":{"Arabic":"أدخل القيمة لـ","English":"Enter value for"},
            "Could not retrieve record for editing.":{"Arabic":"لم يتمكن من استرجاع السجل للتعديل.","English":"Could not retrieve record for editing."},
            "Access Denied":{"Arabic":"تم الرفض","English":"Access Denied"},
            "You do not have permission to access this page.":{"Arabic":"ليس لديك صلاحية الدخول لهذه الصفحة.","English":"You do not have permission to access this page."},
            "Login successful! Role:":{"Arabic":"تم تسجيل الدخول بنجاح! الدور:","English":"Login successful! Role:"},
            "Both fields are required.":{"Arabic":"كلا الحقلين مطلوبين.","English":"Both fields are required."},
            "Invalid username or password.":{"Arabic":"اسم المستخدم أو كلمة المرور غير صحيحة.","English":"Invalid username or password."},
            "An error occurred:":{"Arabic":"حدث خطأ:","English":"An error occurred:"},
            "Unknown role":{"Arabic":"دور غير معروف","English":"Unknown role"},
            "Access denied.":{"Arabic":"تم الرفض.","English":"Access denied."},
            "Sales vs Purchases":{"Arabic":"المبيعات مقابل المشتريات","English":"Sales vs Purchases"},
            "Top Client":{"Arabic":"أفضل عميل","English":"Top Client"},
            "Count":{"Arabic":"العدد","English":"Count"},
            "Metric":{"Arabic":"المقياس","English":"Metric"},
            "Value":{"Arabic":"القيمة","English":"Value"},
            "Number of Sales":{"Arabic":"عدد المبيعات","English":"Number of Sales"},
            "Number of Purchases":{"Arabic":"عدد المشتريات","English":"Number of Purchases"},
            "Group Chat - Employee Notes":{"Arabic":"دردشة جماعية - ملاحظات الموظف","English":"Group Chat - Employee Notes"},
            "Unknown":{"Arabic":"غير معروف","English":"Unknown"},
            "Application Assistant":{"Arabic":"مساعد التطبيق","English":"Application Assistant"},
            "Sales Report":{"Arabic":"تقرير المبيعات","English":"Sales Report"},
            "Purchase Report":{"Arabic":"تقرير المشتريات","English":"Purchase Report"},
            "Profit and Loss (P&L) Report":{"Arabic":"تقرير الربح والخسارة","English":"Profit and Loss Report"},
            "Customer Reports":{"Arabic":"تقارير العملاء","English":"Customer Reports"},
            "Supplier Reports":{"Arabic":"تقارير الموردين","English":"Supplier Reports"},
            "Inventory Report":{"Arabic":"تقرير المخزون","English":"Inventory Report"},
            "Payment & Collection Report":{"Arabic":"تقرير الدفع والتحصيل","English":"Payment & Collection Report"},
            "General Expenses Report":{"Arabic":"تقرير المصروفات العامة","English":"General Expenses Report"},
            "Employee Performance Report":{"Arabic":"تقرير أداء الموظفين","English":"Employee Performance Report"},
            "Export to Excel":{"Arabic":"تحويل الي اكسل","English":"Export to Excel"},
            "Export to PDF":{"Arabic":"تحويل الي pdf","English":"Export to PDF"},
            # "":{"Arabic":"","English":""},
            # "":{"Arabic":"","English":""},
            # "":{"Arabic":"","English":""},
            # "":{"Arabic":"","English":""},
            # "":{"Arabic":"","English":""},
            # "":{"Arabic":"","English":""},
            # "":{"Arabic":"","English":""},
            "Exit":{"Arabic":"خروج","English":"Exit"},
            "Customer Payments":{"Arabic":"مدفوعات العملاء","English":"Customer Payments"},
            "Supplier Payments":{"Arabic":"مدفوعات الموردين","English":"Supplier Payments"},
            "Employee Salary":{"Arabic":"مرتبات الموظفين","English":"Employee Salary"},
            "Employee Appointments":{"Arabic":"مواعيد الموظفين","English":"Employee Appointments"},
            "Employee Withdrawals":{"Arabic":"مسحوبات الموظفين","English":"Employee Withdrawals"},
            "Produnction":{"Arabic":"الانتاج","English":"Produnction"},
            "Transport":{"Arabic":"مصاريف النقل","English":"Transport"},
            "NOT SUPPORTED YET":{"Arabic":"غير مدعوم حتى الآن","English":"NOT SUPPORTED YET"},
            "General_Exp_And_Rev":{"Arabic":"ايرادات و مصروفات عامة","English":"General_Exp_And_Rev"},
            "Select Invoice":{"Arabic":"حدد الفاتورة","English":"Select Invoice"},
            "Load Invoice":{"Arabic":"تحميل الفاتورة","English":"Load Invoice"},
            "Delete Invoice":{"Arabic":"حذف الفاتورة","English":"Delete Invoice"},
            "🔄 Update Invoice":{"Arabic":"🔄 تحديث الفاتورة","English":"🔄 Update Invoice"},
            "Still checked in":{"Arabic":"لا يزال قيد التسجيل","English":"Still checked in"},
            "Customer & Supplier Overview":{"Arabic":"نظرة عامة على العملاء والموردين","English":"Customer & Supplier Overview"},
            
            ####################### DATABASES ##############################
            #Purchases DB
            "Receipt_Number":{"Arabic":"رقم الفاتورة","English":"Receipt Number"},
            "supplier_code":{"Arabic":"كود المورد","English":"Supplier Code"},
            "supplier_name":{"Arabic":"اسم المورد","English":"Supplier Name"},
            "supplier_phone1":{"Arabic":"هاتف المورد 1","English":"Supplier Phone 1"},
            "supplier_phone2":{"Arabic":"هاتف المورد 2","English":"Supplier Phone 2"},
            "supplier_address":{"Arabic":"عنوان المورد","English":"Supplier Address"},
            "Final_Price":{"Arabic":"السعر النهائي","English":"Final Price"},
            "Net_total":{"Arabic":"الإجمالي الصافي","English":"Net Total"},
            "Previous_balance":{"Arabic":"الرصيد السابق","English":"Previous Balance"},
            "Total_balance":{"Arabic":"الرصيد الكلي","English":"Total Balance"},
            "Payed_cash":{"Arabic":"المبلغ المدفوع","English":"Payed Cash"},
            "Remaining_balance":{"Arabic":"باقي المبلغ","English":"Remaining Balance"},
            "Payment_method":{"Arabic":"طريقة الدفع","English":"Payment Method"},
            "PDF_Path":{"Arabic":"ملف ال PDF","English":"PDF Path"},

            #Sales DB
            "customer_code":{"Arabic":"كود العميل","English":"Customer Code"},
            "customer_name":{"Arabic":"اسم العميل","English":"Customer Name"},
            "customer_phone1":{"Arabic":"هاتف العميل 1","English":"Customer Phone 1"},
            "customer_phone2":{"Arabic":"هاتف العميل 2","English":"Customer Phone 2"},
            "customer_address":{"Arabic":"عنوان العميل","English":"Customer Address"},

            #Employee Salary DB
            "employee_code":{"Arabic":"كود الموظف","English":"Employee Code"},
            "employee_name":{"Arabic":"اسم الموظف","English":"Employee Name"},
            "month_year":{"Arabic":"الشهر-السنة","English":"Month-Year"},
            "base_salary":{"Arabic":"المرتب الأساسي","English":"Base Salary"},
            "total_withdrawls":{"Arabic":"مجموع المسحوبات","English":"Total Withdrawals"},
            "delay_penalty":{"Arabic":"غرامات تأخير","English":"Delay Penalty"}, #alternative: Salary Deduction
            "overtime_bonus":{"Arabic":"أجر العمل الإضافي","English":"Overtime Bonus"},
            "net_salary":{"Arabic":"المرتب الكلي","English":"Net Salary"},
            "payment_method":{"Arabic":"طريقة الدفع","English":"Payment Method"},
            "timestamp":{"Arabic":"وقت التسجيل","English":"Timestamp"},
            
            #Employee Appointments DB
            "check_in":{"Arabic":"وقت التسجيل","English":"Check-In Time"},
            "check_out":{"Arabic":"وقت الخروج","English":"Check-Out Time"},
            "duration":{"Arabic":"المدة الزمنية","English":"Duration"},

            #Employee withdrawals DB
            "previous_withdrawls":{"Arabic":"مسحوبات سابقة","English":"Previous Withdrawls"},
            "amount_withdrawls":{"Arabic":"مسحوبات حالية","English":"Amount Withdrawls"},
            
            #Production DB
            "material_qty":{"Arabic":"كمية الخامة","English":"Material Qty"},
            "product_qty":{"Arabic":"كمية المنتج","English":"Product Qty"},
            "waste":{"Arabic":"هادر","English":"Waste"},
            #General_Exp_And_Rev DB
            "type":{"Arabic":"نوع","English":"Type"},
            "amount":{"Arabic":"المبلغ","English":"Amount"},
            "Amount":{"Arabic":"المبلغ","English":"Amount"},
            "date":{"Arabic":"تاريخ","English":"Date"},    


            ####################### General Expenses & Rev ##############################
            "Amount Paid:":{"Arabic":"القيمة المدفوعة:","English":"Amount Paid:"},
            "Amount Received:":{"Arabic":"القيمة المستلمة:","English":"Amount Received:"},
            "Description:":{"Arabic":"الوصف:","English":"Description:"},
            "💾 Record Expense":{"Arabic":"💾 تسجيل مصروف","English":"💾 Record Expense"},
            "💾 Record Revenue":{"Arabic":"💾 تسجيل إيراد","English":"💾 Record Revenue"},

            
            ####################### Treasury ##############################
            "From Date:":{"Arabic":"من","English":"From Date:"},
            "To Date:":{"Arabic":"إلى","English":"To Date:"},
            "Payment Method:":{"Arabic":"طريقة الدفع","English":"Payment Method"},
            "Search:":{"Arabic":"بحث","English":"Search:"},

            ####################### Customer Interactions (supply hub) ##############################
            "Cash":{"Arabic":"المبلغ:","English":"Cash:"},
            "Start Date":{"Arabic":"تاريخ بداية","English":"Start Date"},
            "End Date":{"Arabic":"تاريخ انتهاء","English":"End Date"},
            "Add Entry":{"Arabic":"أضف خانة","English":"Add Entry"},

            "Operation_Number":{"Arabic":"رقم العملية","English":"Operation Number"},

            "Total Debit":{"Arabic":"إجمالي الدائن","English":"Total Debit"},
            "Total Credit":{"Arabic":"إجمالي المدين","English":"Total Credit"},            

            # "Add Entry":{"Arabic":"الوقت","English":"Add Entry"},
            "Update Entry":{"Arabic":"تحديث خانة","English":"Update Entry"},
            "Delete Entry":{"Arabic":"حذف خانة","English":"Delete Entry"},
            "Deselect Entry":{"Arabic":"إلغاء التحديد","English":"Deselect Entry"},
            "Browse":{"Arabic":"استعرض ملفات","English":"Browse"},
            "Time":{"Arabic":"الوقت","English":"Time"},

            "invoice_no":{"Arabic":"رقم الفاتورة","English":"Invoice Number"},
            "credit":{"Arabic": "دائن", "English": "Credit"},
            "debit":{"Arabic": "مدين", "English": "Debit"},

            "Expenses":{"Arabic": "مصروفات", "English": "Expenses"},
            "Revenues":{"Arabic": "إيرادات", "English": "Revenues"},
        }        
        
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
        self.clean_materials_collection()
        self.clean_products_collection()
        self.clean_customers_collection()
        self.clean_employees_collection()
        self.clean_suppliers_collection()
        self.reverse_translations = {self.t(k): k for k in self.keys}
        
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
        self.logout_icon_path   = os.path.join(BASE_DIR, "Static", "images", "logout-dark.png")  # Path to logout icon
        self.exit_icon_path     = os.path.join(BASE_DIR, "Static", "images", "exit-dark.png")  # Path to exit icon
        self.calc_icon_path     = os.path.join(BASE_DIR, "Static", "images", "calculator-dark.png")  # Path to exit icon
        self.minimize_icon_path = os.path.join(BASE_DIR, "Static", "images", "minus-dark.png")  # Path to exit icon
        self.back_icon_path     = os.path.join(BASE_DIR, "Static", "images", "left-arrow-dark.png")  # Path to back icon
        self.dark_mode_img      = os.path.join(BASE_DIR, "Static", "images", "dark-mode.png")  # <- your image path
        self.light_mode_img     = os.path.join(BASE_DIR, "Static", "images", "light-mode.png")  # <- your image path
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
        self.update =False
        self.light = True  # Default to light mode
        self.update_purchase =False
        
        # icon_image = Image.open(icon_path).resize((16, 16))  # Resize to fit in the button
        # self.lang_icon = ImageTk.PhotoImage(icon_image)
    
    def start_with_login(self):
        self.login_window = LoginWindow(self.root, self)
        self.login_window.open_login_window()
        
    def start_without_login(self):
        self.login_window = LoginWindow(self.root, self)
        app.user_role="developer"
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
            messagebox.showerror(self.t("No Internet Connection"), str(e))

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

############################################ Windows ########################################### 
    def open_group_chat_window(self):
        chat_win = tk.Toplevel(self.root)
        chat_win.title(self.t("Group Chat - Employee Notes"))
        chat_win.geometry("450x500")
        chat_win.resizable(False, False)

        # Set custom icon for the window (groupchat.ico)
        icon_path = os.path.join(BASE_DIR, "Static", "images", "groupchat.ico")
        if os.path.exists(icon_path):
            chat_win.iconbitmap(icon_path)

        # Group chat icon (draggable)
        icon_frame = tk.Frame(chat_win, width=60, height=60)
        icon_frame.place(x=10, y=10)
        icon_img_path = os.path.join(BASE_DIR, "Static", "images", "groupchat.ico")
        if os.path.exists(icon_img_path):
            icon_img = Image.open(icon_img_path).resize((60, 60), Image.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon_img)
            icon_label = tk.Label(icon_frame, image=icon_photo)
            icon_label.image = icon_photo
            icon_label.pack()
        else:
            icon_label = tk.Label(icon_frame, text="👥", font=("Arial", 32))
            icon_label.pack()

        # Make icon draggable
        def start_drag(event):
            icon_frame._drag_start_x = event.x
            icon_frame._drag_start_y = event.y

        def do_drag(event):
            x = icon_frame.winfo_x() + event.x - icon_frame._drag_start_x
            y = icon_frame.winfo_y() + event.y - icon_frame._drag_start_y
            icon_frame.place(x=x, y=y)

        icon_label.bind("<Button-1>", start_drag)
        icon_label.bind("<B2-Motion>", do_drag)

        # Chat area
        chat_frame = tk.Frame(chat_win)
        chat_frame.place(x=80, y=10, width=310, height=420)
        chat_display = tk.Text(chat_frame, state="disabled", wrap="word", font=("Arial", 12))
        chat_display.pack(fill="both", expand=True)

        # Entry area
        # Entry area
        entry_frame = tk.Frame(chat_win)
        entry_frame.place(x=10, y=440, width=380, height=50)

        # name_var = tk.StringVar(value=self.user_name if self.user_name else "")
        # tk.Label(entry_frame, text="Name:", font=("Arial", 10)).pack(side=tk.LEFT)
        # name_entry = tk.Entry(entry_frame, textvariable=name_var, width=12)
        # name_entry.pack(side=tk.LEFT, padx=5)

        msg_var = tk.StringVar()
        msg_entry = tk.Entry(entry_frame, textvariable=msg_var, width=28)
        msg_entry.pack(side=tk.LEFT, padx=5)

        def load_messages():
            chat_display.config(state="normal")
            chat_display.delete(1.0, tk.END)
            for msg in self.messages_collection.find().sort("timestamp", 1):
                # name = msg.get("name", "Unknown")
                name = msg.get("name", self.t("Unknown"))
                text = msg.get("text", "")
                time = msg.get("timestamp", "").strftime("%Y-%m-%d %H:%M") if msg.get("timestamp") else ""
                chat_display.insert(tk.END, f"[{time}] {self.t(name)}: {text}\n")
            chat_display.config(state="disabled")
            chat_display.see(tk.END)

        def send_message():
            # name = name_var.get().strip() or "Unknown"
            name = self.user_name if self.user_name else "Unknown"
            text = msg_var.get().strip()
            if text:
                self.messages_collection.insert_one({
                    "name": name,
                    "text": text,
                    "timestamp": datetime.now()
                })
                msg_var.set("")
                load_messages()


        send_btn = tk.Button(entry_frame, text="Send", command=send_message, font=("Arial", 11), width=8, bg="#2196F3", fg="white")
        send_btn.pack(side=tk.LEFT, padx=5)

        # Make refresh button larger and more visible
        refresh_btn = tk.Button(entry_frame, text="Refresh", command=load_messages, font=("Arial", 11), width=10, bg="#21F35D", fg="white")
        refresh_btn.pack(side=tk.LEFT, padx=8, ipadx=8, ipady=8)

        chat_display.config(state="normal")
        chat_display.insert("end", "Welcome! This is the group chat for employee notes.\n\n")
        chat_display.config(state="disabled")

        load_messages()

    def open_chatbot(self):
        chatbot_win = tk.Toplevel(self.root)
        chatbot_win.title("مساعد التطبيق")
        chatbot_win.title(self.t("Application Assistant"))
        chatbot_win.geometry("400x500")
        chatbot_win.resizable(False, False)
    
        # Set custom icon for the window (feather.ico)
        icon_path = os.path.join(BASE_DIR, "Static", "images", "chatbot_icon.ico")
        if os.path.exists(icon_path):
            chatbot_win.iconbitmap(icon_path)
    
        # Chatbot icon (draggable)
        icon_frame = tk.Frame(chatbot_win, width=60, height=60)
        icon_frame.place(x=10, y=10)
        icon_img_path = os.path.join(BASE_DIR, "Static", "images", "chatbot_icon.ico")
        if os.path.exists(icon_img_path):
            icon_img = Image.open(icon_img_path).resize((60, 60), Image.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon_img)
            icon_label = tk.Label(icon_frame, image=icon_photo)
            icon_label.image = icon_photo
            icon_label.pack()
        else:
            icon_label = tk.Label(icon_frame, text="🤖", font=("Arial", 32))
            icon_label.pack()
    
        # Make icon draggable
        def start_drag(event):
            icon_frame._drag_start_x = event.x
            icon_frame._drag_start_y = event.y
    
        def do_drag(event):
            x = icon_frame.winfo_x() + event.x - icon_frame._drag_start_x
            y = icon_frame.winfo_y() + event.y - icon_frame._drag_start_y
            icon_frame.place(x=x, y=y)
    
        icon_label.bind("<Button-1>", start_drag)
        icon_label.bind("<B1-Motion>", do_drag)
    
        # Chat area
        chat_frame = tk.Frame(chatbot_win)
        chat_frame.place(x=80, y=10, width=310, height=420)
        chat_text = tk.Text(chat_frame, state="disabled", wrap="word", font=("Arial", 12))
        chat_text.pack(fill="both", expand=True)
    
        # Entry and send button (hidden, not used)
        entry_frame = tk.Frame(chatbot_win)
        entry_frame.place(x=10, y=440, width=380, height=50)
    
        # ...inside open_chatbot...
                # Fixed questions and replies
        questions = [
            "كيف أضيف فاتورة مبيعات؟",
            "كيف أبحث عن عميل؟",
            "كيف أعدل بيانات منتج؟",
            "كيف أغير اللغة؟",
            "كيف أضيف موظف جديد؟",
            "كيف أبحث عن فاتورة مبيعات؟",
            "كيف أعدل فاتورة مبيعات؟",
            "كيف أضيف فاتورة مشتريات؟",
            "كيف أبحث عن مورد؟",
            "كيف أعدل بيانات مورد؟",
            "كيف أضيف منتج جديد؟",
            "كيف أبحث عن منتج؟",
            "كيف أعدل بيانات موظف؟",
            "كيف أضيف مصروف عام؟",
            "كيف أضيف إيراد عام؟",
            "كيف أبحث في قاعدة البيانات؟",
            "كيف أستخدم التقارير؟",
            "كيف أغير كلمة المرور؟",
            "كيف أعمل نسخة احتياطية للبيانات؟",
            "كيف أسترجع نسخة احتياطية؟",
            "كيف أضيف وردية يومية؟",
            "كيف أضيف أمر إنتاج؟",
            "كيف أبحث عن سجل موظف؟",
            "كيف أبحث عن سجل مورد؟",
            "كيف أبحث عن سجل منتج؟",
            "كيف أبحث عن سجل فاتورة؟",
            "مساعدة"
        ]
        replies = {
            "كيف أضيف فاتورة مبيعات؟": "من القائمة الرئيسية، اختر 'فاتورة مبيعات' ثم اضغط على 'فاتورة مبيعات جديدة'.",
            "كيف أبحث عن عميل؟": "استخدم مربع البحث في نافذة العملاء أو قاعدة البيانات.",
            "كيف أعدل بيانات منتج؟": "اذهب إلى قاعدة البيانات، اختر 'المنتجات' ثم اضغط على 'تعديل سجل'.",
            "كيف أغير اللغة؟": "اضغط على زر تغيير اللغة في الشريط العلوي.",
            "كيف أضيف موظف جديد؟": "من قاعدة البيانات، اختر 'الموظفين' ثم اضغط على 'إضافة سجل'.",
            "كيف أبحث عن فاتورة مبيعات؟": "من نافذة الفواتير، استخدم مربع البحث أو اختر رقم الفاتورة من القائمة.",
            "كيف أعدل فاتورة مبيعات؟": "من نافذة الفواتير، اختر الفاتورة ثم اضغط على 'تعديل'.",
            "كيف أضيف فاتورة مشتريات؟": "من القائمة الرئيسية، اختر 'فاتورة مشتريات' ثم اضغط على 'فاتورة مشتريات جديدة'.",
            "كيف أبحث عن مورد؟": "استخدم مربع البحث في نافذة الموردين أو قاعدة البيانات.",
            "كيف أعدل بيانات مورد؟": "اذهب إلى قاعدة البيانات، اختر 'الموردين' ثم اضغط على 'تعديل سجل'.",
            "كيف أضيف منتج جديد؟": "من قاعدة البيانات، اختر 'المنتجات' ثم اضغط على 'إضافة سجل'.",
            "كيف أبحث عن منتج؟": "استخدم مربع البحث في نافذة المنتجات أو قاعدة البيانات.",
            "كيف أعدل بيانات موظف؟": "اذهب إلى قاعدة البيانات، اختر 'الموظفين' ثم اضغط على 'تعديل سجل'.",
            "كيف أضيف مصروف عام؟": "من القائمة الرئيسية، اختر 'ايرادات و مصروفات عامة' ثم اضغط على 'تسجيل مصروف'.",
            "كيف أضيف إيراد عام؟": "من القائمة الرئيسية، اختر 'ايرادات و مصروفات عامة' ثم اضغط على 'تسجيل إيراد'.",
            "كيف أبحث في قاعدة البيانات؟": "استخدم مربع البحث في نافذة قاعدة البيانات وحدد الجدول المطلوب.",
            "كيف أستخدم التقارير؟": "من القائمة الرئيسية، اختر 'التقارير' ثم حدد التقرير المطلوب.",
            "كيف أغير كلمة المرور؟": "من نافذة المستخدمين، اختر اسمك ثم اضغط على 'تغيير كلمة المرور'.",
            "كيف أعمل نسخة احتياطية للبيانات؟": "من الإعدادات، اختر 'نسخة احتياطية' واتبع التعليمات.",
            "كيف أسترجع نسخة احتياطية؟": "من الإعدادات، اختر 'استرجاع نسخة احتياطية' واتبع التعليمات.",
            "كيف أضيف وردية يومية؟": "من قاعدة البيانات، اختر 'الورديات اليومية' ثم اضغط على 'إضافة وردية'.",
            "كيف أضيف أمر إنتاج؟": "من القائمة الرئيسية، اختر 'أمر إنتاج' ثم أدخل البيانات المطلوبة.",
            "كيف أبحث عن سجل موظف؟": "استخدم مربع البحث في نافذة الموظفين أو قاعدة البيانات.",
            "كيف أبحث عن سجل مورد؟": "استخدم مربع البحث في نافذة الموردين أو قاعدة البيانات.",
            "كيف أبحث عن سجل منتج؟": "استخدم مربع البحث في نافذة المنتجات أو قاعدة البيانات.",
            "كيف أبحث عن سجل فاتورة؟": "استخدم مربع البحث في نافذة الفواتير أو قاعدة البيانات.",
            "مساعدة": "اسألني عن إضافة أو تعديل أو بحث أو تقارير أو إعدادات أو أي وظيفة أخرى في التطبيق.",
        }
        # ...rest of open_chatbot...
    
        # Dropdown for questions
        selected_question = tk.StringVar()
        question_dropdown = ttk.Combobox(entry_frame, textvariable=selected_question, values=questions, font=("Arial", 14), state="readonly")
        question_dropdown.pack(fill="x", padx=8, pady=8)
    
        def on_select(event=None):
            q = selected_question.get()
            if not q:
                return
            chat_text.config(state="normal")
            chat_text.insert("end", f"أنت: {q}\n")
            reply = replies.get(q, "عذراً، لم أفهم سؤالك. جرب كلمة 'مساعدة'.")
            chat_text.insert("end", f"المساعد: {reply}\n\n")
            chat_text.config(state="disabled")
            chat_text.see("end")
    
        question_dropdown.bind("<<ComboboxSelected>>", on_select)
    
        # Optionally, show a welcome/help message
        chat_text.config(state="normal")
        chat_text.insert("end", "مرحباً! اختر سؤالاً من الأسئلة الشائعة بالأسفل.\n\n")
        chat_text.config(state="disabled")

# To use: add a button in your main menu or topbar to call self.open_chatbot()
    def main_menu(self):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create the top bar
        self.topbar(show_back_button=False)


        # Main container
        
        main_container = tk.Frame(self.root, bg=COLORS["background"])
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Visualization frames
        left_viz_frame = self.create_card_frame(main_container)
        left_viz_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Button frame
        button_frame = self.create_card_frame(main_container, padding=20)
        button_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)
        
        right_viz_frame = self.create_card_frame(main_container)    
        right_viz_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
        
        # Configure grid weights
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=2)
        main_container.grid_columnconfigure(2, weight=1)
        main_container.grid_rowconfigure(0, weight=1)

        # Create visualizations
        self.create_left_visualization(left_viz_frame)
        self.create_right_visualization(right_viz_frame)
        if self.light:
            # Define buttons with images, text, and commands
            buttons = [
                # {"text": self.t("New Sales Invoice"), "image": "Sales.png",
                # "command": lambda: self.new_sales_invoice(self.user_role)},
                {"text": self.t("Sales Invoice"), "image": "sales_invoice-dark.png",
                "command": lambda: self.manage_sales_invoices_window()},
                # {"text": self.t("New Purchase Invoice"), "image": "Purchase.png", 
                # "command": lambda: self.new_Purchase_invoice(self.user_role)},
                {"text": self.t("Purchase Invoice"), "image": "purchases_invoice-dark.png", 
                "command": lambda: self.manage_purchases_invoices_window()},
                {"text": self.t("Receive Payment"), "image": "customer_payment-dark.png", 
                "command": lambda: self.customer_interactions(self.user_role)},
                {"text": self.t("Make Payment"), "image": "supplier_payment-dark.png", 
                "command": lambda: self.supplier_interactions(self.user_role)},
                {"text": self.t("Production Order"), "image": "production-dark.png", 
                "command": lambda: self.new_production_order(self.user_role)},
                {"text": self.t("Employee interactions"), "image": "employee-dark.png", 
                "command": lambda: self.manage_Employees_window()},
                {"text": self.t("Treasury"), "image": "treasury-dark.png", 
                "command": lambda: self.Treasury_window(self.user_role)},
                {"text": self.t("General_Exp_And_Rev"), "image": "financial-dark.png", 
                "command": lambda: self.general_exp_rev(self.user_role)},
                {"text": self.t("Reports"), "image": "report-dark.png", 
                "command": lambda: self.manage_Reports_window()},
            ]
            
            if self.user_role == "admin" or self.user_role == "developer":
                buttons.extend([
                    {"text": self.t("Database"), "image": "database-dark.png", 
                    "command": lambda: self.check_access_and_open(self.user_role)}
                ])
        elif not self.light:
            # Define buttons with images, text, and commands
            buttons = [
                # {"text": self.t("New Sales Invoice"), "image": "Sales.png",
                # "command": lambda: self.new_sales_invoice(self.user_role)},
                {"text": self.t("Sales Invoice"), "image": "sales_invoice-light.png",
                "command": lambda: self.manage_sales_invoices_window()},
                # {"text": self.t("New Purchase Invoice"), "image": "Purchase.png", 
                # "command": lambda: self.new_Purchase_invoice(self.user_role)},
                {"text": self.t("Purchase Invoice"), "image": "purchases_invoice-light.png", 
                "command": lambda: self.manage_purchases_invoices_window()},
                {"text": self.t("Receive Payment"), "image": "customer_payment-light.png", 
                "command": lambda: self.customer_interactions(self.user_role)},
                {"text": self.t("Make Payment"), "image": "supplier_payment-light.png", 
                "command": lambda: self.supplier_interactions(self.user_role)},
                {"text": self.t("Production Order"), "image": "production-light.png", 
                "command": lambda: self.new_production_order(self.user_role)},
                {"text": self.t("Employee interactions"), "image": "employee-light.png", 
                "command": lambda: self.manage_Employees_window()},
                {"text": self.t("Treasury"), "image": "treasury-light.png", 
                "command": lambda: self.Treasury_window(self.user_role)},
                {"text": self.t("General_Exp_And_Rev"), "image": "financial-light.png", 
                "command": lambda: self.general_exp_rev(self.user_role)},
                {"text": self.t("Reports"), "image": "report-light.png", 
                "command": lambda: self.manage_Reports_window()},
            ]

            if self.user_role == "admin" or self.user_role == "developer":
                buttons.extend([
                    {"text": self.t("Database"), "image": "database-light.png", 
                    "command": lambda: self.check_access_and_open(self.user_role)}
                ])
        
        # Create button container with centered alignment
        button_container = tk.Frame(button_frame, bg=COLORS["card"])
        button_container.pack(fill=tk.BOTH, expand=True)  # Expand to fill available space
        
        # Create frame for the button grid (centered horizontally, aligned to top)
        grid_container = tk.Frame(button_container, bg=COLORS["card"])
        grid_container.pack(side="top", pady=20)  # Align to top with padding
        
        # Center the grid horizontally
        grid_container.grid_columnconfigure(0, weight=1)  # Left spacer
        grid_container.grid_columnconfigure(2, weight=1)  # Right spacer
        
        # Create a centered frame inside grid_container
        centered_frame = tk.Frame(grid_container, bg=COLORS["card"])
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
                btn_frame = tk.Frame(centered_frame, bg=COLORS["card"])
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
                            bg=COLORS["card"],
                            fg=COLORS["text"],
                            activebackground=COLORS["highlight"],
                            font=("Arial", 15, "bold"),
                            borderwidth=0,
                            command=btn_info["command"])
                btn.image = photo_img  # Keep reference
                btn.pack(expand=True, fill=tk.BOTH)  # Make button expand to fill frame
                
                # Hover effect
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS["primary"]))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLORS["card"]))
                
        except Exception as e:
            print(f"Error loading images: {e}")
            # Fallback to text buttons if images fail
            text_frame = tk.Frame(centered_frame, bg=COLORS["card"])
            text_frame.grid(row=0, column=0, sticky="nsew")
            
            for i, btn_info in enumerate(buttons):
                row = i // columns_per_row
                column = i % columns_per_row
                
                btn = tk.Button(text_frame, 
                            text=btn_info["text"], 
                            command=btn_info["command"],
                            padx=10, pady=5,
                            bg=COLORS["card"],
                            fg=COLORS["text"],
                            activebackground=COLORS["highlight"],
                            font=("Segoe UI", 10))
                btn.grid(row=row, column=column, padx=5, pady=5)


        def start_drag(event):
            widget = event.widget
            widget.startX = event.x
            widget.startY = event.y

        def do_drag(event):
            widget = event.widget
            if hasattr(widget, 'startX') and hasattr(widget, 'startY'):
                x = widget.winfo_x() + event.x - widget.startX
                y = widget.winfo_y() + event.y - widget.startY
                widget.place(x=x, y=y)



        # Remove previous chatbot icon if exists
        if hasattr(self, 'chatbot_main_btn') and self.chatbot_main_btn.winfo_exists():
            self.chatbot_main_btn.destroy()

        try:
            chatbot_icon_path = os.path.join(BASE_DIR, "Static", "images", "chatbot_icon.png")
            chatbot_img = Image.open(chatbot_icon_path).resize((60, 60), Image.LANCZOS)
            self.chatbot_main_photo = ImageTk.PhotoImage(chatbot_img)
            self.chatbot_main_btn = tk.Label(self.root, image=self.chatbot_main_photo, bg=COLORS["card"], cursor="hand2")
            self.chatbot_main_btn.place(x=20, y=780)  # Initial position



            self.chatbot_main_btn.bind("<Button-1>", start_drag)
            self.chatbot_main_btn.bind("<B1-Motion>", do_drag)
            self.chatbot_main_btn.bind("<ButtonRelease-1>", lambda e: self.open_chatbot())



        except Exception as e:
            print(f"Error loading chatbot icon for main window: {e}")

        if hasattr(self, 'groupchat_main_btn') and self.groupchat_main_btn.winfo_exists():
            self.groupchat_main_btn.destroy()
        try:
            groupchat_icon_path = os.path.join(BASE_DIR, "Static", "images", "groupchat.ico")
            groupchat_img = Image.open(groupchat_icon_path).resize((60, 60), Image.LANCZOS)
            self.groupchat_main_photo = ImageTk.PhotoImage(groupchat_img)
            self.groupchat_main_btn = tk.Label(self.root, image=self.groupchat_main_photo, bg=COLORS["card"], cursor="hand2")
            self.groupchat_main_btn.place(x=100, y=780)  # Initial position

            self.groupchat_main_btn.bind("<Button-1>", start_drag)
            self.groupchat_main_btn.bind("<B1-Motion>", do_drag)
            self.groupchat_main_btn.bind("<ButtonRelease-1>", lambda e: self.open_group_chat_window())
        except Exception as e:
            print(f"Error loading groupchat icon for main window: {e}")
        
    def create_left_visualization(self, parent):
        try:
        
            data = {
                'customers': self.get_customer_count() if hasattr(self, 'get_customer_count') else 0,
                'suppliers': self.get_supplier_count() if hasattr(self, 'get_supplier_count') else 0,
                'sales': float(self.get_sales_count()) if hasattr(self, 'get_sales_count') else 0.0,
                'purchases': float(self.get_purchase_count()) if hasattr(self, 'get_purchase_count') else 0.0
            }

            # Create figure with basic styling

            plt.style.use('dark_background')  # Modern dark theme
            fig = plt.Figure(figsize=(6, 10), dpi=70, facecolor=COLORS["card"])
            # fig.subplots_adjust(hspace=0.4)
            fig.subplots_adjust(hspace=0.4, left=0.15, right=0.85)
            # fig.patch.set_facecolor('#FFFFFF')  # White background

            # Bar Chart
            ax1 = fig.add_subplot(211)
            try:
                arabic_title0 = self.t("Customers")
                reshaped_text0 = arabic_reshaper.reshape(arabic_title0)
                bidi_text0 = get_display(reshaped_text0)
                arabic_title1 = self.t("Suppliers")
                reshaped_text1 = arabic_reshaper.reshape(arabic_title1)
                bidi_text1 = get_display(reshaped_text1)
                bars = ax1.bar([bidi_text0, bidi_text1], 
                            [data['customers'], data['suppliers']], 
                            color=['#2E86C1', '#17A589'])
                arabic_title2 = self.t("Customer & Supplier Overview")
                reshaped_text2 = arabic_reshaper.reshape(arabic_title2)
                bidi_text2 = get_display(reshaped_text2)                
                arabic_title3 = self.t("Count")
                reshaped_text3 = arabic_reshaper.reshape(arabic_title3)
                bidi_text3 = get_display(reshaped_text3)                
                ax1.set_title(bidi_text2, fontsize=20,color=COLORS["text"], fontname="Arial")
                ax1.set_facecolor(COLORS["text"])
                ax1.tick_params(colors=COLORS["text"], labelsize=13,)
                ax1.set_ylabel("xx",text=bidi_text3,color=COLORS["text"], fontsize=18, fontname="Arial")
                for label in ax1.get_xticklabels():
                    label.set_fontsize(15)         # Change to your desired size
                    label.set_fontname("Arial")    # Use a font that supports Arabic
                    label.set_color(COLORS["text"])
                    label.set_weight("bold") 
                # Add simple data labels
                for bar in bars:
                    height = bar.get_height()
                    ax1.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}',
                            ha='center', va='bottom',
                            color=COLORS["text"], fontsize=10)
                    
            except Exception as bar_error:
                print(f"Bar chart error: {bar_error}")

            # Summary Table
            ax2 = fig.add_subplot(212)
            ax2.axis('off')
            arabic_title4 = self.t("Metric")
            reshaped_text4 = arabic_reshaper.reshape(arabic_title4)
            bidi_text4 = get_display(reshaped_text4) 

            arabic_title5 = self.t("Value")
            reshaped_text5 = arabic_reshaper.reshape(arabic_title5)
            bidi_text5 = get_display(reshaped_text5) 

            arabic_title6 = self.t("Customers number")
            reshaped_text6 = arabic_reshaper.reshape(arabic_title6)
            bidi_text6 = get_display(reshaped_text6) 

            arabic_title7 = self.t("Suppliers number")
            reshaped_text7 = arabic_reshaper.reshape(arabic_title7)
            bidi_text7 = get_display(reshaped_text7) 

            arabic_title8 = self.t("Number of Sales")
            reshaped_text8 = arabic_reshaper.reshape(arabic_title8)
            bidi_text8 = get_display(reshaped_text8) 

            arabic_title9 = self.t("Number of Purchases")
            reshaped_text9 = arabic_reshaper.reshape(arabic_title9)
            bidi_text9 = get_display(reshaped_text9) 

            table_data = [
                [bidi_text4, bidi_text5],
                [bidi_text6, f"{int(data['customers'])}"],
                [bidi_text7, f"{int(data['suppliers'])}"],
                [bidi_text8, f"{data['sales']:.2f}"],
                [bidi_text9, f"{data['purchases']:.2f}"]
            ]
            
            # Simple table without advanced styling
            # rowHeights = [0.25]
            table = ax2.table(
                cellText=table_data,
                loc='center',
                cellLoc='center',
                colWidths=[0.4, 0.4],  # Reduced column widths
                # rowHeights=rowHeights,  # Custom heights
                
                # edges='closed'
            )
            # Additional adjustments for better spacing
            # fig.subplots_adjust(left=0.2, bottom=0.1, right=0.8, top=0.9, hspace=0.4)
            table.auto_set_font_size(False)
            if self.language == "Arabic":
                table.set_fontsize(15)
            else:
                table.set_fontsize(13)
            # table.set_fontname("Arial")
            table.set_zorder(100)
            table.scale(1, 2)  # Less aggressive scaling

            for (row, col), cell in table.get_celld().items():
                cell.set_facecolor(COLORS["card"])
                cell.set_text_props(fontname="Arial")
                # cell.set_facecolor("black") # background content
                cell.set_text_props(color=COLORS["text"])
                # cell.set_text_props(color="black") #text in header
                if row == 0:
                    cell.set_facecolor(COLORS["main_frame"])
                    cell.set_text_props(weight='bold',color="white")

            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas.draw()
            canvas.get_tk_widget().config(bg=COLORS["card"])
            canvas.get_tk_widget().pack(fill="x", expand=True)
            # canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            print(f"Visualization failed: {str(e)}")
            # Create error label as fallback
            tk.Label(parent, text="Data visualization unavailable", fg="red").pack()

    def create_right_visualization(self, parent):
        try:
            # Safe data retrieval
            
            sales = float(self.get_sales_count()) if hasattr(self, 'get_sales_count') else 0.0
            purchases = float(self.get_purchase_count()) if hasattr(self, 'get_purchase_count') else 0.0
            top_client = self.get_top_client() if hasattr(self, 'get_top_client') else None
            fig = plt.Figure(figsize=(6, 8), dpi=60)
            fig.subplots_adjust(hspace=0.5)
            fig.patch.set_facecolor(COLORS["card"])  
            # ...existing code...
            # Pie Chart
            ax1 = fig.add_subplot(211)
            try:
                # If both sales and purchases are zero, show a blank circle
                if sales == 0 and purchases == 0:
                    # Draw a blank pie with one wedge (invisible label)
                    ax1.pie(
                        [1],
                        labels=[''],
                        colors=[COLORS["main_frame"]],
                        startangle=90,
                        wedgeprops={'width': 1}
                    )
                else:
                    arabic_title1 = self.t("Sales")
                    reshaped_text1 = arabic_reshaper.reshape(arabic_title1)
                    bidi_text1 = get_display(reshaped_text1)
                    arabic_title2 = self.t("Purchases")
                    reshaped_text2 = arabic_reshaper.reshape(arabic_title2)
                    bidi_text2 = get_display(reshaped_text2)
                    ax1.pie(
                        [sales, purchases],
                        labels=[bidi_text1, bidi_text2],
                        autopct='%1.1f%%',
                        colors=['#28B463', '#E74C3C'],
                        textprops={'color': COLORS["text"], 'fontsize': 16, 'fontname': 'Arial'},
                        wedgeprops={'width': 1}
                    )
                ax1.axis('equal')  # Ensures the pie is drawn as a circle
                # Before setting the title:
                arabic_title = self.t("Sales vs Purchases")
                reshaped_text = arabic_reshaper.reshape(arabic_title)
                bidi_text = get_display(reshaped_text)
                ax1.set_title(bidi_text, fontsize=20, color=COLORS["text"], fontname="Arial")  # Use a font that supports Arabic
                # ax1.set_title(self.t("المبيعات مقابل المشتريات"), fontsize=14, color=COLORS["text"])
            except Exception as pie_error:
                print(f"Pie chart error: {pie_error}")
            # ...existing code...
            # Top Client Chart
            ax2 = fig.add_subplot(212)
            try:
                if top_client and isinstance(top_client, (list, tuple)) and len(top_client) >= 2:
                    name, value = top_client[0], float(top_client[1])  # ✅ Uses corrected field
                    arabic_title5 = name
                    reshaped_text5 = arabic_reshaper.reshape(arabic_title5)
                    bidi_text5 = get_display(reshaped_text5)     
                    bar = ax2.bar(bidi_text5, [value], color='#8E44AD')
                    # ax2.tick_params(axis='x', labelsize = 20)  # Set x, -axis label font size (bidi_text5)
                    for label in ax2.get_xticklabels():
                        label.set_fontsize(18)     
                        label.set_fontname("Arial")    # Font family (supports Arabic)
                        label.set_color(COLORS["text"])   
                        label.set_weight("bold")  # Font size
                    arabic_title3 = self.t("Top Client")
                    reshaped_text3 = arabic_reshaper.reshape(arabic_title3)
                    bidi_text3 = get_display(reshaped_text3)
                    ax2.set_title(bidi_text3, fontsize=20,color=COLORS["text"],fontname="Arial")  # Use a font that supports Arabic
                    ax2.set_facecolor(COLORS["text"])
                    ax2.tick_params(colors=COLORS["text"])
                    arabic_title4 = self.t("Amount")
                    reshaped_text4 = arabic_reshaper.reshape(arabic_title4)
                    bidi_text4 = get_display(reshaped_text4)
                    ax2.set_ylabel(bidi_text4,fontsize=18,color=COLORS["text"],fontname="Arial")
                    # Add value label
                    for rect in bar:
                        height = rect.get_height()
                        ax2.text(rect.get_x() + rect.get_width()/2., height,
                                f'${height:.2f}',
                                ha='center', va='bottom',
                                color=COLORS["text"], fontsize=10)
                else:
                    ax2.text(0.5, 0.5, 'No client data',
                            ha='center', va='center',
                            fontsize=10, color='gray')
                    ax2.axis('off')
            except Exception as bar_error:
                print(f"Client chart error: {bar_error}")

            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

        except Exception as e:
            print(f"Visualization failed: {str(e)}")
            tk.Label(parent, text="Right visualization unavailable", fg="red").pack()
    
    def create_card_frame(self, parent, padding=0):
        frame = tk.Frame(parent, bg=COLORS["card"], bd=0,
                        highlightbackground=COLORS["main_frame"],
                        highlightthickness=3)
        if padding:
            frame.grid_propagate(False)
            frame.config(width=400, height=600)
        return frame

    def create_main_buttons(self, parent,buttons):
        # buttons = [
        #     {"text": "New Sales Invoice", "image": "Sales.png",
        #     "command": lambda: self.trash(self.user_role)},
        #     {"text": "New Purchase Invoice", "image": "Purchase.png", 
        #     "command": lambda: self.trash(self.user_role)},
        #     {"text": "Production Order", "image": "Production Order.png", 
        #     "command": lambda: self.trash(self.user_role)},
        #     {"text": "Employee Interactions", "image": "Employees.png", 
        #     "command": lambda: self.trash(self.user_role)},
        #     {"text": "Treasury", "image": "Treasury.png", 
        #     "command": lambda: self.trash(self.user_role)},
        #     {"text": "Database", "image": "Database.png", 
        #     "command": lambda: self.trash(self.user_role)},
        #     # {"text": "Analytics", "image": "Analytics.png", 
        #     # "command": lambda: self.trash(self.user_role)},
        # ]

        columns_per_row = 3
        button_size = 100

        try:
            for index, btn_info in enumerate(buttons):
                row = index // columns_per_row
                column = index % columns_per_row

                btn_frame = tk.Frame(parent, bg=COLORS["card"])
                btn_frame.grid(row=row, column=column, padx=15, pady=15)

                # button_frame = tk.Frame(parent, bg=COLORS["card"])
                # button_frame.pack(pady=30)
                
                # Load and process image
                img_path = os.path.join(BASE_DIR, "Static", "images", btn_info["image"])
                img = Image.open(img_path).resize((button_size, button_size), Image.LANCZOS)
                photo_img = ImageTk.PhotoImage(img)

                # Create modern button
                btn = tk.Button(btn_frame,
                            image=photo_img,
                            text=btn_info["text"],
                            compound=tk.TOP,
                            bg=COLORS["card"],
                            fg=COLORS["text"],
                            activebackground=COLORS["highlight"],
                            font=("Segoe UI", 10),
                            borderwidth=0,
                            command=btn_info["command"])
                btn.image = photo_img
                btn.pack()

                # Hover effect
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS["primary"]))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLORS["card"]))
                
        except Exception as e:
            print(f"Button error: {e}")

    # Database query methods
    def get_customer_count(self):
        try:
            return self.customers_collection.count_documents({})
        except PyMongoError as e:
            print(f"Database error: {e}")
            return 0

    def get_supplier_count(self):
        try:
            return self.suppliers_collection.count_documents({})
        except PyMongoError as e:
            print(f"Database error: {e}")
            return 0

    def get_sales_count(self):
        try:
            return self.sales_collection.count_documents({})
        except PyMongoError as e:
            print(f"Database error: {e}")
            return 0

    def get_purchase_count(self):
        try:
            return self.purchases_collection.count_documents({})
        except PyMongoError as e:
            print(f"Database error: {e}")
            return 0
    def get_top_client(self):
        try:
            pipeline = [
                # Convert Credit string to a numeric value
                # {
                #     "$addFields": {
                #         "creditNumeric": {
                #             "$toDouble": {
                #                 "$arrayElemAt": [
                #                     {"$split": ["$Credit", "_"]}, 
                #                     0
                #                 ]
                #             }
                #         }
                #     }
                # },
                # Sort by creditNumeric (descending)
                {"$sort": {"Debit": -1}},
                # Get the top client
                {"$limit": 1},
                # Project the correct identifier field: "Company address"
                {"$project": {"Name": 1, "Debit": 1, "_id": 0}}  # 🔑 Fix here
            ]
            result = list(self.customers_collection.aggregate(pipeline))
            # print(1)
            if result:
                print(f"{result[0]["Name"]} ,{result[0]["Debit"]}")
                return (result[0]["Name"], result[0]["Debit"])  # 🔑 Fix here
            return ("No clients found", 0)
            
        except PyMongoError as e:
            print(f"Database error: {e}")
            return ("Error", 0)
        
    # Modify your show_visualizations method:
    def show_visualizations(self,user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()
        print(1)
        # Create the top bar
        self.topbar(show_back_button=True)
        print(1)
        try:
            print(1)
            # Create new window
            # vis_window = tk.Toplevel(self.root)
            # vis_window.title("Business Analytics")
            # vis_window.state("zoomed")  # Maximized window
            print(1)
            # Create main container
            main_frame = tk.Frame(self.root, bg="white")
            main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
            print(1)
            # Get data from database
            data = {
                'customers': self.get_customer_count(),
                'suppliers': self.get_supplier_count(),
                'sales': self.get_sales_count(),
                'purchases': self.get_purchase_count(),
                'top_client': self.get_top_client()
            }
            print(1)
            # Create figure
            fig = plt.Figure(figsize=(16, 10), dpi=100)
            fig.suptitle("Business Performance Dashboard", fontsize=16, y=0.95)
            print(1)
            # Create subplots
            ax1 = fig.add_subplot(221)
            ax2 = fig.add_subplot(222)
            ax3 = fig.add_subplot(223)
            ax4 = fig.add_subplot(224)
            print(1)
            # Chart 1: Customers vs Suppliers
            ax1.bar(['Customers', 'Suppliers'], 
                    [data['customers'], data['suppliers']], 
                    color=['#1f77b4', '#ff7f0e'])
            ax1.set_title(self.t("Customer & Supplier Count"), pad=15,font="Arial")
            ax1.set_ylabel("Count")
            print(1)
            # Chart 2: Sales/Purchases Ratio
            ax2.pie([data['sales'], data['purchases']],
                    labels=['Sales', 'Purchases'],
                    autopct='%1.1f%%',
                    colors=['#2ca02c', '#d62728'],
                    startangle=90)
            ax2.set_title("Sales vs Purchases Ratio", pad=15)
            print(1)
            # Chart 3: Top Client
            if data['top_client']:
                ax3.bar(data['top_client'][0], data['top_client'][1],
                        color='#9467bd')
                ax3.set_title("Top Performing Client", pad=15)
                ax3.set_ylabel("Sales Amount")
            print(1)
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


        except Exception as e:
            print(f"Error generating visualizations: {e}")
            tk.messagebox.showerror(self.t("Error"), f"{self.t("Failed to load reports:")} {str(e)}")           


    def manage_sales_invoices_window(self):
                # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg=COLORS["background"])
        # Create the top bar
        self.topbar(show_back_button=True)

        # Main button frame
        button_frame = tk.Frame(self.root, bg=COLORS["background"])
        button_frame.pack(pady=30)

        # Define buttons with images, text, and commands
        if self.light:
            buttons = [
                {"text": self.t("New Sales Invoice"), "image": "new_invoice-dark.png",
                "command": lambda: self.sales_invoice(self.user_role,"add")},
                {"text": self.t("Update Sales Invoice"), "image": "update_invoice-dark.png",
                "command": lambda: self.sales_invoice(self.user_role,"update")}
            ]
        elif not self.light:
            buttons = [
                {"text": self.t("New Sales Invoice"), "image": "new_invoice-light.png",
                "command": lambda: self.sales_invoice(self.user_role,"add")},
                {"text": self.t("Update Sales Invoice"), "image": "update_invoice-light.png",
                "command": lambda: self.sales_invoice(self.user_role,"update")}
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
                sub_frame = tk.Frame(button_frame, bg=COLORS["background"])
                sub_frame.grid(row=row, column=column, padx=20, pady=20)

                # Image button
                btn = tk.Button(sub_frame, image=photo_img, bd=0,
                                text=btn_info["text"], 
                                font=("Arial", 15, "bold"),
                                compound=tk.TOP,
                                bg=COLORS["background"],
                                fg=COLORS["text"],
                                activebackground=COLORS["highlight"],
                                command=btn_info["command"])
                btn.image = photo_img  # Keep reference
                btn.pack(expand=True, fill=tk.BOTH)  # Make button expand to fill frame
                
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS["primary"]))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLORS["background"]))

                # # Text label
                # lbl = tk.Label(sub_frame, text=btn_info["text"], 
                #             font=("Arial", 15, "bold"), bg=COLORS["background"], fg=COLORS["text"])
                # lbl.pack(pady=5)

        except Exception as e:
            print(f"Error loading images: {e}")
            # Fallback to text buttons if images fail
            fallback_frame = tk.Frame(self.root, bg=COLORS["background"])
            fallback_frame.pack(pady=20)
            for btn_info in buttons:
                tk.Button(fallback_frame, text=btn_info["text"], 
                        command=btn_info["command"]).pack(side="left", padx=10)
                
    def manage_purchases_invoices_window(self):
                # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg=COLORS["background"])
        # Create the top bar
        self.topbar(show_back_button=True)

        # Main button frame
        button_frame = tk.Frame(self.root, bg=COLORS["background"])
        button_frame.pack(pady=30)

        # Define buttons with images, text, and commands
        if self.light:
            buttons = [
                {"text": self.t("New Purchase Invoice"), "image": "new_invoice-dark.png", 
                "command": lambda: self.new_Purchase_invoice(self.user_role,"add")},
                {"text": self.t("Update Purchase Invoice"), "image": "update_invoice-dark.png",
                "command": lambda: self.new_Purchase_invoice(self.user_role,"update")}
            ]
        elif not self.light:
            buttons = [
                {"text": self.t("New Purchase Invoice"), "image": "new_invoice-light.png", 
                "command": lambda: self.new_Purchase_invoice(self.user_role,"add")},
                {"text": self.t("Update Purchase Invoice"), "image": "update_invoice-light.png",
                "command": lambda: self.new_Purchase_invoice(self.user_role,"update")}
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
                sub_frame = tk.Frame(button_frame, bg=COLORS["background"])
                sub_frame.grid(row=row, column=column, padx=20, pady=20)

                # Image button
                btn = tk.Button(sub_frame, image=photo_img, bd=0,
                                text=btn_info["text"], 
                                font=("Arial", 15, "bold"),
                                compound=tk.TOP,
                                bg=COLORS["background"],
                                fg=COLORS["text"],
                                activebackground=COLORS["highlight"],
                                command=btn_info["command"])
                btn.image = photo_img  # Keep reference
                btn.pack()
                
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS["primary"]))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLORS["background"]))

                # # Text label
                # lbl = tk.Label(sub_frame, text=btn_info["text"], 
                #             font=("Arial", 15, "bold"), bg=COLORS["background"], fg="#003366")
                # lbl.pack(pady=5)

        except Exception as e:
            print(f"Error loading images: {e}")
            # Fallback to text buttons if images fail
            fallback_frame = tk.Frame(self.root, bg=COLORS["background"])
            fallback_frame.pack(pady=20)
            for btn_info in buttons:
                tk.Button(fallback_frame, text=btn_info["text"], 
                        command=btn_info["command"]).pack(side="left", padx=10)
                

    def manage_database_window(self):
                # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg=COLORS["background"])
        # Create the top bar
        self.topbar(show_back_button=True)

        # Main button frame
        button_frame = tk.Frame(self.root, bg=COLORS["background"])
        button_frame.pack(pady=30)

        # Define buttons with images, text, and commands
        if self.light:
            buttons = [
                {"text": self.t("Customers"), "image": "cus_db-dark.png", 
                "command": lambda: self.new_customer(self.user_role)},
                {"text": self.t("Suppliers"), "image": "supp_db-dark.png", 
                "command": lambda: self.new_supplier(self.user_role)},
                {"text": self.t("Employees"), "image": "emp_db-dark.png", 
                "command": lambda: self.new_employee(self.user_role)},
                {"text": self.t("Products"), "image": "prod_db-dark.png", 
                "command": lambda: self.new_products(self.user_role)},
                {"text": self.t("Materials"), "image": "mat_db-dark.png", 
                "command": lambda: self.new_material(self.user_role)},
                {"text": self.t("Employee Salary"), "image": "emp_salary_db-dark.png", 
                "command": lambda: self.new_emp_salary(self.user_role)},
                {"text": self.t("Employee Appointments"), "image": "emp_hour-dark.png", 
                "command": lambda: self.new_emp_appointment(self.user_role)},
                {"text": self.t("Employee Withdrawals"), "image": "emp_with-dark.png", 
                "command": lambda: self.new_emp_withdrawal(self.user_role)},
                {"text": self.t("General_Exp_And_Rev"), "image": "financial-dark.png", 
                "command": lambda: self.new_general_exp(self.user_role)}
            ]
        elif not self.light:
            buttons = [
                {"text": self.t("Customers"), "image": "cus_db-light.png", 
                "command": lambda: self.new_customer(self.user_role)},
                {"text": self.t("Suppliers"), "image": "supp_db-light.png", 
                "command": lambda: self.new_supplier(self.user_role)},
                {"text": self.t("Employees"), "image": "emp_db-light.png", 
                "command": lambda: self.new_employee(self.user_role)},
                {"text": self.t("Products"), "image": "prod_db-light.png", 
                "command": lambda: self.new_products(self.user_role)},
                {"text": self.t("Materials"), "image": "mat_db-light.png", 
                "command": lambda: self.new_material(self.user_role)},
                {"text": self.t("Employee Salary"), "image": "emp_salary_db-light.png", 
                "command": lambda: self.new_emp_salary(self.user_role)},
                {"text": self.t("Employee Appointments"), "image": "emp_hour-light.png", 
                "command": lambda: self.new_emp_appointment(self.user_role)},
                {"text": self.t("Employee Withdrawals"), "image": "emp_with-light.png", 
                "command": lambda: self.new_emp_withdrawal(self.user_role)},
                {"text": self.t("General_Exp_And_Rev"), "image": "financial-light.png", 
                "command": lambda: self.new_general_exp(self.user_role)}
            ]
        if self.user_role == "developer":
            if self.light:
                buttons.extend([
                    {"text": self.t("purchases"), "image": "purchases_invoice-dark.png", 
                    "command": lambda: self.new_purchases(self.user_role)},
                    {"text": self.t("sales"), "image": "sales_invoice-dark.png", 
                    "command": lambda: self.new_sales(self.user_role)},
                    {"text": self.t("Customer Payments"), "image": "customer_payment-dark.png", 
                    "command": lambda: self.new_customer_payment(self.user_role)},
                    {"text": self.t("Supplier Payments"), "image": "supplier_payment-dark.png", 
                    "command": lambda: self.new_supplier_payment(self.user_role)},
                    {"text": self.t("Produnction"), "image": "production-dark.png", 
                    "command": lambda: self.new_production(self.user_role)},

                ])
            elif not self.light:
                buttons.extend([
                    {"text": self.t("purchases"), "image": "purchases_invoice-light.png", 
                    "command": lambda: self.new_purchases(self.user_role)},
                    {"text": self.t("sales"), "image": "sales_invoice-light.png", 
                    "command": lambda: self.new_sales(self.user_role)},
                    {"text": self.t("Customer Payments"), "image": "customer_payment-light.png", 
                    "command": lambda: self.new_customer_payment(self.user_role)},
                    {"text": self.t("Supplier Payments"), "image": "supplier_payment-light.png", 
                    "command": lambda: self.new_supplier_payment(self.user_role)},
                    {"text": self.t("Produnction"), "image": "production-light.png", 
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
                sub_frame = tk.Frame(button_frame, bg=COLORS["background"])
                sub_frame.grid(row=row, column=column, padx=20, pady=20)

                # Image button
                btn = tk.Button(sub_frame, image=photo_img, bd=0,
                                text=btn_info["text"], 
                                font=("Arial", 15, "bold"),
                                compound=tk.TOP,
                                bg=COLORS["background"],
                                fg=COLORS["text"],
                                activebackground=COLORS["highlight"],
                                command=btn_info["command"])
                btn.image = photo_img  # Keep reference
                btn.pack()
                
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS["primary"]))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLORS["background"]))

                # Text label
                # lbl = tk.Label(sub_frame, text=btn_info["text"], 
                #             font=("Arial", 15, "bold"), bg=COLORS["background"], fg="#003366")
                # lbl.pack(pady=5)

        except Exception as e:
            print(f"Error loading images: {e}")
            # Fallback to text buttons if images fail
            fallback_frame = tk.Frame(self.root, bg=COLORS["background"])
            fallback_frame.pack(pady=20)
            for btn_info in buttons:
                tk.Button(fallback_frame, text=btn_info["text"], 
                        command=btn_info["command"]).pack(side="left", padx=10)
                

    def manage_Employees_window(self):
                # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg=COLORS["background"])
        # Create the top bar
        self.topbar(show_back_button=True)

        button_frame = tk.Frame(self.root, bg=COLORS["background"])
        button_frame.pack(pady=30)



        # Define buttons with images, text, and commands
        if self.light:
            buttons = [
                {"text": self.t("Employee hours"), "image": "emp_hour-dark.png", 
                "command": lambda: self.employee_hours_window(self.user_role)},
                {"text": self.t("Employee Withdrawals"), "image": "emp_with-dark.png", 
                "command": lambda: self.employee_withdrowls_window(self.user_role)},
                {"text": self.t("Employee Statistics"), "image": "emp_salary-dark.png", 
                "command": lambda: self.employee_statistics_window(self.user_role)},
            ]
        elif not self.light:
            buttons = [
                {"text": self.t("Employee hours"), "image": "emp_hour-light.png", 
                "command": lambda: self.employee_hours_window(self.user_role)},
                {"text": self.t("Employee Withdrawals"), "image": "emp_with-light.png", 
                "command": lambda: self.employee_withdrowls_window(self.user_role)},
                {"text": self.t("Employee Statistics"), "image": "emp_salary-light.png", 
                "command": lambda: self.employee_statistics_window(self.user_role)},
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
                sub_frame = tk.Frame(button_frame, bg=COLORS["background"])
                sub_frame.grid(row=row, column=column, padx=20, pady=20)

                # Image button
                btn = tk.Button(sub_frame, image=photo_transparent, bd=0,
                                text=btn_info["text"], 
                                font=("Arial", 15, "bold"),
                                compound=tk.TOP,
                                bg=COLORS["background"],
                                fg=COLORS["text"],
                                activebackground=COLORS["highlight"],
                                command=btn_info["command"])
                btn.image_transparent = photo_transparent
                btn.image_with_bg = photo_with_bg
                btn.pack()
                
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS["primary"]))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLORS["background"]))

                # # Text label
                # lbl = tk.Label(sub_frame, text=btn_info["text"], 
                #             font=("Arial", 15, "bold"), bg=COLORS["background"], fg="#003366")
                # lbl.pack(pady=5)

        except Exception as e:
            print(f"Error loading images: {e}")
            # Fallback to text buttons if images fail
            fallback_frame = tk.Frame(self.root, bg=COLORS["background"])
            fallback_frame.pack(pady=20)
            for btn_info in buttons:
                tk.Button(fallback_frame, text=btn_info["text"], 
                        command=btn_info["command"]).pack(side="left", padx=10)
    def manage_Reports_window(self):
                # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg=COLORS["background"])
        # Create the top bar
        self.topbar(show_back_button=True)

        button_frame = tk.Frame(self.root, bg=COLORS["background"])
        button_frame.pack(pady=30)

        # Define buttons with images, text, and commands
        if self.light:
            buttons = [
                {"text": self.t("Sales Report"), "image": "sales_rep-dark.png", 
                "command": lambda: self.sales_report(self.user_role)},
                {"text": self.t("Purchase Report"), "image": "Purchase_rep-dark.png", 
                "command": lambda: self.trash(self.user_role)},
                {"text": self.t("Profit and Loss (P&L) Report"), "image": "p&l_repo-dark.png", 
                "command": lambda: self.trash(self.user_role)},
                {"text": self.t("Customer Reports"), "image": "Customer_repo-dark.png", 
                "command": lambda: self.trash(self.user_role)},
                {"text": self.t("Supplier Reports"), "image": "Supplier_repo-dark.png", 
                "command": lambda: self.trash(self.user_role)},
                {"text": self.t("Inventory Report"), "image": "Inventory_repo-dark.png", 
                "command": lambda: self.trash(self.user_role)},
                {"text": self.t("Payment & Collection Report"), "image": "payment_repo-dark.png", 
                "command": lambda: self.trash(self.user_role)},
                {"text": self.t("General Expenses Report"), "image": "General Expenses_repo-dark.png", 
                "command": lambda: self.trash(self.user_role)},
                {"text": self.t("Employee Performance Report"), "image": "Employee_Performance_repo-dark.png", 
                "command": lambda: self.trash(self.user_role)},
            ]
        elif not self.light:
            buttons = [
                {"text": self.t("Sales Report"), "image": "sales_rep-light.png", 
                "command": lambda: self.sales_report(self.user_role)},
                {"text": self.t("Purchase Report"), "image": "Purchase_rep-light.png", 
                "command": lambda: self.trash(self.user_role)},
                {"text": self.t("Profit and Loss (P&L) Report"), "image": "p&l_repo-light.png", 
                "command": lambda: self.trash(self.user_role)},
                {"text": self.t("Customer Reports"), "image": "Customer_repo-light.png", 
                "command": lambda: self.trash(self.user_role)},
                {"text": self.t("Supplier Reports"), "image": "Supplier_repo-light.png", 
                "command": lambda: self.trash(self.user_role)},
                {"text": self.t("Inventory Report"), "image": "Inventory_repo-light.png", 
                "command": lambda: self.trash(self.user_role)},
                {"text": self.t("Payment & Collection Report"), "image": "payment_repo-light.png", 
                "command": lambda: self.trash(self.user_role)},
                {"text": self.t("General Expenses Report"), "image": "General Expenses_repo-light.png", 
                "command": lambda: self.trash(self.user_role)},
                {"text": self.t("Employee Performance Report"), "image": "Employee_Performance_repo-light.png", 
                "command": lambda: self.trash(self.user_role)},
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
                sub_frame = tk.Frame(button_frame, bg=COLORS["background"])
                sub_frame.grid(row=row, column=column, padx=20, pady=20)

                # Image button
                btn = tk.Button(sub_frame, image=photo_transparent, bd=0,
                                text=btn_info["text"], 
                                font=("Arial", 15, "bold"),
                                compound=tk.TOP,
                                bg=COLORS["background"],
                                fg=COLORS["text"],
                                activebackground=COLORS["highlight"],
                                command=btn_info["command"])
                btn.image_transparent = photo_transparent
                btn.image_with_bg = photo_with_bg
                btn.pack()
                
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS["primary"]))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLORS["background"]))

                # # Text label
                # lbl = tk.Label(sub_frame, text=btn_info["text"], 
                #             font=("Arial", 15, "bold"), bg=COLORS["background"], fg="#003366")
                # lbl.pack(pady=5)

        except Exception as e:
            print(f"Error loading images: {e}")
            # Fallback to text buttons if images fail
            fallback_frame = tk.Frame(self.root, bg=COLORS["background"])
            fallback_frame.pack(pady=20)
            for btn_info in buttons:
                tk.Button(fallback_frame, text=btn_info["text"], 
                        command=btn_info["command"]).pack(side="left", padx=10)

    def employee_hours_window(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()
        

        self.topbar(show_back_button=True, Back_to_Employee_Window=True)
        
        # Database collections
        employees_col = self.get_collection_by_name("Employees")
        appointments_col = self.get_collection_by_name("Employee_appointimets")
        
        # Create mappings
        self.employee_code_name = {}
        self.employee_name_code = {}
        for emp in employees_col.find():
            code = emp.get('Id', '')
            name = emp.get('Name', '')
            self.employee_code_name[code] = name
            self.employee_name_code[name] = code

        # Main frame
        # self.root.configure(bg="#f0f0f0")
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Selection frame
        selection_frame = tk.Frame(main_frame)
        selection_frame.pack(fill=tk.X, pady=10)

        # Employee name dropdown
        tk.Label(selection_frame, text=self.t("Employee Name:")).pack(side=tk.LEFT, padx=5)
        self.name_var = tk.StringVar()
        name_cb = ttk.Combobox(selection_frame, textvariable=self.name_var, width=25)
        name_cb.pack(side=tk.LEFT, padx=5)
        name_cb.bind('<<ComboboxSelected>>', self.update_employee_code)

        # Employee code dropdown
        tk.Label(selection_frame, text=self.t("Employee Code:")).pack(side=tk.LEFT, padx=5)
        self.code_var = tk.StringVar()
        code_cb = ttk.Combobox(selection_frame, textvariable=self.code_var, width=15)
        code_cb.pack(side=tk.LEFT, padx=5)
        code_cb.bind('<<ComboboxSelected>>', self.update_employee_name)

        # Update dropdown values
        name_cb['values'] = list(self.employee_name_code.keys())
        code_cb['values'] = list(self.employee_code_name.keys())

        # Check-in/out button
        tk.Button(selection_frame, text=self.t("Check In/Out"), command=lambda: self.toggle_check_in_out(employees_col, appointments_col)).pack(side=tk.RIGHT, padx=10)
        # tk.Button(selection_frame, text=self.t("Check In/Out"), command=lambda: self.toggle_check_in_out(employees_col, appointments_col)).pack(side=tk.RIGHT, padx=10)

        # Checked-in employees treeview
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ("Employee Name", "Check-in Time", "Duration")
        self.checkin_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        for col in columns:
            self.checkin_tree.heading(col, text=self.t(col))
            self.checkin_tree.column(col, width=150, anchor='center')
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.checkin_tree.yview)
        self.checkin_tree.configure(yscrollcommand=vsb.set)
        
        self.checkin_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # Load initial check-ins
        self.update_checkin_tree(appointments_col)

    def update_employee_code(self, event):
        name = self.name_var.get()
        if name in self.employee_name_code:
            self.code_var.set(self.employee_name_code[name])

    def update_employee_name(self, event):
        code = self.code_var.get()
        if code in self.employee_code_name:
            self.name_var.set(self.employee_code_name[code])

    def toggle_check_in_out(self, employees_col, appointments_col):
        code = self.code_var.get()
        name = self.name_var.get()
        
        if not code or not name:
            messagebox.showerror(self.t("Error"), self.t("Please select an employee"))
            return
        
        # Check existing appointment
        existing = appointments_col.find_one({
            'employee_code': code,
             '$or': [
                {'check_out': {'$exists': False}},
                {'check_out': None}
            ]
        })
        
        try:
            if existing:
                # Check out
                print("out")
                check_out_time = datetime.now()
                duration = check_out_time - existing['check_in']
                
                appointments_col.update_one(
                    {'_id': existing['_id']},
                    {'$set': {
                        'check_out': check_out_time,
                        'duration': duration.total_seconds() / 3600  # in hours
                    }}
                )
            else:
                # Check in
                print("in")
                appointments_col.insert_one({
                    'employee_code': code,
                    'employee_name': name,
                    'check_in': datetime.now(),
                    'check_out': None,
                    'duration': None
                })
            print("sss")
            self.update_checkin_tree(appointments_col)
            messagebox.showinfo(self.t("Success"), f"{name} {self.t("checked")} {self.t('out') if existing else self.t('in')} {self.t("successfully")}")
            
        except PyMongoError as e:
            messagebox.showerror(self.t("Database Error"), str(e))

    def update_checkin_tree(self, appointments_col):
        # Clear existing data
        for item in self.checkin_tree.get_children():
            self.checkin_tree.delete(item)
        
        # Get active check-ins
        active_appointments = appointments_col.find({
            '$or': [
            {'check_out': {'$exists': False}},
            {'check_out': None}
        ]
        }).sort('check_in', -1)
        
        for appt in active_appointments:
            # Convert string to datetime object
            check_in_value = appt.get('check_in', '')
            formatted_time = "Invalid timestamp"
            
            try:
                if isinstance(check_in_value, datetime):
                    formatted_time = check_in_value.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    # Handle string representations
                    if '.' in check_in_value:  # Handle milliseconds
                        check_in_time = datetime.strptime(check_in_value, "%Y-%m-%d %H:%M:%S.%f")
                    else:
                        check_in_time = datetime.strptime(check_in_value, "%Y-%m-%d %H:%M:%S")
                    formatted_time = check_in_time.strftime("%Y-%m-%d %H:%M:%S")
                    
            except (ValueError, TypeError, AttributeError) as e:
                print(f"Timestamp error: {str(e)}")
            
            self.checkin_tree.insert('', 'end', values=(
                appt.get('employee_name', ''),
                formatted_time,
                self.t('Still checked in')
            ))

    def employee_withdrowls_window(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        self.topbar(show_back_button=True, Back_to_Employee_Window=True)

        # Database collections
        employees_col = self.get_collection_by_name("Employees")
        withdrawals_col = self.get_collection_by_name("Employee_withdrawls")
        # Create mappings
        self.employee_code_map = {}
        self.employee_name_map = {}
        for emp in employees_col.find():
            code = emp.get('Id', '')
            name = emp.get('Name', '')
            self.employee_code_map[code] = name
            self.employee_name_map[name] = code
        # Main frame with left alignment
        main_frame = tk.Frame(self.root, padx=40, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True, anchor='nw')

        # Configure grid layout
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=3)

        # Employee Selection Section
        tk.Label(main_frame, text=self.t("Employee Selection"), font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10, sticky='w')
        tk.Label(main_frame, text=self.t("Employee Selection"), font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10, sticky='w')
        
        # Employee Name Dropdown
        tk.Label(main_frame, text=self.t("Employee Name:"), font=('Helvetica', 12)).grid(row=1, column=0, pady=5, sticky='w')
        tk.Label(main_frame, text=self.t("Employee Name:"), font=('Helvetica', 12)).grid(row=1, column=0, pady=5, sticky='w')
        self.withdraw_name_var = tk.StringVar()
        name_cb = ttk.Combobox(main_frame, textvariable=self.withdraw_name_var, 
                            width=30, font=('Helvetica', 12))
        name_cb.grid(row=1, column=1, pady=5, padx=10, sticky='w')
        name_cb.bind('<<ComboboxSelected>>', self.update_withdraw_code)

        # Employee Code Dropdown
        tk.Label(main_frame, text=self.t("Employee Code:"), font=('Helvetica', 12)).grid(row=2, column=0, pady=5, sticky='w')
        tk.Label(main_frame, text=self.t("Employee Code:"), font=('Helvetica', 12)).grid(row=2, column=0, pady=5, sticky='w')
        self.withdraw_code_var = tk.StringVar()
        code_cb = ttk.Combobox(main_frame, textvariable=self.withdraw_code_var, 
                            width=30, font=('Helvetica', 12))
        code_cb.grid(row=2, column=1, pady=5, padx=10, sticky='w')
        code_cb.bind('<<ComboboxSelected>>', self.update_withdraw_name)

        # Salary Display
        tk.Label(main_frame, text=self.t("Salary:"), font=('Helvetica', 12)).grid(row=3, column=0, pady=5, sticky='w')
        tk.Label(main_frame, text=self.t("Salary:"), font=('Helvetica', 12)).grid(row=3, column=0, pady=5, sticky='w')
        self.salary_var = tk.StringVar()
        salary_entry = tk.Entry(main_frame, textvariable=self.salary_var, 
                            state='readonly', width=33, font=('Helvetica', 12))
        salary_entry.grid(row=3, column=1, pady=5, padx=10, sticky='w')

        # Withdrawal Details Section (updated row numbers)
        tk.Label(main_frame, text=self.t("Withdrawal Details"), font=('Helvetica', 14, 'bold')).grid(row=4, column=0, columnspan=2, pady=10, sticky='w')
        tk.Label(main_frame, text=self.t("Withdrawal Details"), font=('Helvetica', 14, 'bold')).grid(row=4, column=0, columnspan=2, pady=10, sticky='w')

        # Amount Entry
        tk.Label(main_frame, text=self.t("Withdrawal Amount:"), font=('Helvetica', 12)).grid(row=5, column=0, pady=5, sticky='w')
        tk.Label(main_frame, text=self.t("Withdrawal Amount:"), font=('Helvetica', 12)).grid(row=5, column=0, pady=5, sticky='w')
        self.amount_entry = tk.Entry(main_frame, width=33, font=('Helvetica', 12))
        self.amount_entry.grid(row=5, column=1, pady=5, padx=10, sticky='w')

        # Payment Method
        tk.Label(main_frame, text=self.t("Payment Method"), font=('Helvetica', 12)).grid(row=6, column=0, pady=5, sticky='w')
        tk.Label(main_frame, text=self.t("Payment Method"), font=('Helvetica', 12)).grid(row=6, column=0, pady=5, sticky='w')
        self.payment_method = ttk.Combobox(main_frame, 
                                        values=["Cash", "Instapay", "E_wallet", "Bank Account"],
                                        width=30, 
                                        font=('Helvetica', 12),
                                        state="readonly")
        self.payment_method.grid(row=6, column=1, pady=5, padx=10, sticky='w')

        # Previous Withdrawals
        tk.Label(main_frame, text=self.t("Previous Withdrawals:"), font=('Helvetica', 12)).grid(row=7, column=0, pady=5, sticky='w')
        tk.Label(main_frame, text=self.t("Previous Withdrawals:"), font=('Helvetica', 12)).grid(row=7, column=0, pady=5, sticky='w')
        self.prev_withdrawals = tk.Entry(main_frame, 
                                    state='readonly', 
                                    width=33, 
                                    font=('Helvetica', 12))
        self.prev_withdrawals.grid(row=7, column=1, pady=5, padx=10, sticky='w')

        # Save Button (updated row number)
        save_btn = tk.Button(main_frame, 
                            text=self.t("💾 Save Withdrawal"), 
                            font=('Helvetica', 12, 'bold'),
                            width=20,
                            command=lambda: self.save_withdrawal(withdrawals_col, employees_col),
                            bg='#2196F3', fg='white')
        save_btn.grid(row=8, column=0, columnspan=2, pady=20)

        # Update dropdown values
        name_cb['values'] = list(self.employee_name_map.keys())
        code_cb['values'] = list(self.employee_code_map.keys())

        # Bind selection updates
        self.withdraw_name_var.trace_add('write', self.update_previous_withdrawals)
        self.withdraw_code_var.trace_add('write', self.update_previous_withdrawals)

    def update_withdraw_code(self, event):
        name = self.withdraw_name_var.get()
        if name in self.employee_name_map:
            self.withdraw_code_var.set(self.employee_name_map[name])

    def update_withdraw_name(self, event):
        code = self.withdraw_code_var.get()
        if code in self.employee_code_map:
            self.withdraw_name_var.set(self.employee_code_map[code])

    def update_previous_withdrawals(self, *args):
        code = self.withdraw_code_var.get()
        name = self.withdraw_name_var.get()
        
        if not code and name in self.employee_name_map:
            code = self.employee_name_map[name]
        elif not name and code in self.employee_code_map:
            name = self.employee_code_map[code]
        
        if code:
            # Update previous withdrawals
            total = self.calculate_previous_withdrawals(code)
            self.prev_withdrawals.config(state='normal')
            self.prev_withdrawals.delete(0, tk.END)
            self.prev_withdrawals.insert(0, f"{total:.2f}")
            self.prev_withdrawals.config(state='readonly')
            
            # Update salary display
            employees_col = self.get_collection_by_name("Employees")
            code = int(code)
            emp = employees_col.find_one({'Id': code})
            if emp:
                salary = emp.get('Salary', 0)
                salary = float(salary)
                self.salary_var.set(f"{salary:.2f}")
            else:
                self.salary_var.set("0.00")

    def calculate_previous_withdrawals(self, employee_code):
        withdrawals_col = self.get_collection_by_name("Employee_withdrawls")
        total = 0
        for withdrawal in withdrawals_col.find({'employee_code': employee_code}):
            total += withdrawal.get('amount_withdrawls', 0)
        return total

    def save_withdrawal(self, withdrawals_col, employees_col):
        code = self.withdraw_code_var.get()
        name = self.withdraw_name_var.get()
        amount = self.amount_entry.get()
        method = self.payment_method.get()

        if not code or not name:
            messagebox.showerror(self.t("Error"), self.t("Please select an employee"))
            return
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(self.t("Error"), self.t("Invalid amount entered"))
            return

        if not method:
            messagebox.showerror(self.t("Error"), self.t("Please select payment method"))
            return

        try:
            # Calculate previous total before this withdrawal
            previous_total = self.calculate_previous_withdrawals(code)
            
            # Save withdrawal record with cumulative tracking
            withdrawal_data = {
                'employee_code': code,
                'employee_name': name,
                'previous_withdrawls': previous_total,  # Total before this withdrawal
                'amount_withdrawls': amount,
                # 'cumulative_total': previous_total + amount,  # New total after this withdrawal
                'payment_method': method,
                'timestamp': datetime.now()
            }
            withdrawals_col.insert_one(withdrawal_data)

            # Update employee's total withdrawals
            employees_col.update_one(
                {'employee_code': code},
                {'$set': {'previous_withdrawls': previous_total + amount}}
            )

            messagebox.showinfo(self.t("Success"), self.t("Withdrawal recorded successfully"))
            self.amount_entry.delete(0, tk.END)
            self.payment_method.set('')
            self.update_previous_withdrawals()

        except PyMongoError as e:
            messagebox.showerror(self.t("Database Error"), f"{self.t("Failed to save withdrawal:")} {str(e)}")

    def employee_statistics_window(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.topbar(show_back_button=True, Back_to_Employee_Window=True)
        
        # Database connections
        employees_col = self.get_collection_by_name("Employees")
        
        # Employee mappings
        self.employee_code_map = {}
        self.employee_name_map = {}
        for emp in employees_col.find():
            code = int(emp.get('Id', ''))
            name = emp.get('Name', '')
            self.employee_code_map[code] = {
                'name': name,
                'salary': float(emp.get('Salary', 0))
            }
            self.employee_name_map[name] = {
                'code': code,
                'salary': float(emp.get('Salary', 0))
            }

        # Main container
        main_frame = ttk.Frame(self.root, padding=(20, 10))
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Employee Selection
        selection_frame = ttk.LabelFrame(main_frame, text=self.t("Employee Selection"), padding=10)
        selection_frame.grid(row=0, column=0, sticky='ew', pady=5)
        
        ttk.Label(selection_frame, text=self.t("Name:")).grid(row=0, column=0, padx=5, sticky='e')
        self.emp_name_var = tk.StringVar()
        self.name_cb = ttk.Combobox(selection_frame, textvariable=self.emp_name_var, width=25)
        self.name_cb.grid(row=0, column=1, padx=5, sticky='ew')
        self.name_cb.bind('<<ComboboxSelected>>', self.update_salary_name)
        # code_cb.grid(row=2, column=1, pady=5, padx=10, sticky='w')
        # code_cb.bind('<<ComboboxSelected>>', self.update_withdraw_name)
        ttk.Label(selection_frame, text=self.t("Code:")).grid(row=0, column=2, padx=(15,5), sticky='e')
        self.emp_code_var = tk.StringVar()
        self.code_cb = ttk.Combobox(selection_frame, textvariable=self.emp_code_var, width=10)
        self.code_cb.grid(row=0, column=3, padx=5, sticky='ew')
        self.code_cb.bind('<<ComboboxSelected>>', self.update_salary_code)

        # Date Selection
        date_frame = ttk.LabelFrame(main_frame, text=self.t("Month/Year Selection"), padding=10)
        date_frame.grid(row=1, column=0, sticky='ew', pady=5)
        
        ttk.Label(date_frame, text=self.t("Month:")).grid(row=0, column=0, padx=5, sticky='e')
        self.month_var = tk.StringVar()
        self.month_cb = ttk.Combobox(date_frame, textvariable=self.month_var, 
                                values=["January", "February", "March", "April", "May", "June",
                                        "July", "August", "September", "October", "November", "December"],
                                width=12)
        self.month_cb.grid(row=0, column=1, padx=5, sticky='w')
        
        ttk.Label(date_frame, text=self.t("Year:")).grid(row=0, column=2, padx=(15,5), sticky='e')
        self.year_var = tk.StringVar()
        self.year_cb = ttk.Combobox(date_frame, textvariable=self.year_var, 
                                values=[str(year) for year in range(2020, 2040)],
                                width=6)
        self.year_cb.grid(row=0, column=3, padx=5, sticky='w')

        # Working Hours
        hours_frame = ttk.LabelFrame(main_frame, text=self.t("Working Hours"), padding=10)
        hours_frame.grid(row=2, column=0, sticky='ew', pady=5)
        
        ttk.Label(hours_frame, text=self.t("Start Time:")).grid(row=0, column=0, padx=5, sticky='e')
        self.start_time_var = tk.StringVar()
        ttk.Entry(hours_frame, textvariable=self.start_time_var, width=10).grid(row=0, column=1, padx=5, sticky='w')
        ttk.Label(hours_frame, text="(e.g., 9:00 AM)").grid(row=0, column=2, padx=5, sticky='w')
        
        ttk.Label(hours_frame, text=self.t("End Time:")).grid(row=0, column=3, padx=(15,5), sticky='e')
        self.end_time_var = tk.StringVar()
        ttk.Entry(hours_frame, textvariable=self.end_time_var, width=10).grid(row=0, column=4, padx=5, sticky='w')
        ttk.Label(hours_frame, text="(e.g., 5:00 PM)").grid(row=0, column=5, padx=5, sticky='w')

        # Attendance Table
        table_frame = ttk.Frame(main_frame)
        table_frame.grid(row=3, column=0, sticky='nsew', pady=10)
        
        columns = ("Date", "From", "To", "Duration", "Delay", "More", "Withdrawls")
        self.table = ttk.Treeview(table_frame, columns=columns, show='headings', selectmode='browse')
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.configure(yscrollcommand=vsb.set)
        
        for col in columns:
            self.table.heading(col, text=self.t(col), anchor='center')
            self.table.column(col, width=100, anchor='center')

        # Totals Section
        totals_frame = ttk.Frame(main_frame)
        totals_frame.grid(row=4, column=0, sticky='ew', pady=5)
        
        ttk.Label(totals_frame, text=self.t("Total Withdrawls:")).grid(row=0, column=0, padx=5, sticky='e')
        self.total_withdrawls = ttk.Entry(totals_frame, width=12, state='readonly')
        self.total_withdrawls.grid(row=0, column=1, padx=5, sticky='w')
        
        ttk.Label(totals_frame, text=self.t("Delay Amount:")).grid(row=0, column=2, padx=(20,5), sticky='e')
        self.delay_amount = ttk.Entry(totals_frame, width=12)
        self.delay_amount.grid(row=0, column=3, padx=5, sticky='w')
        
        ttk.Label(totals_frame, text=self.t("Overtime Amount:")).grid(row=0, column=4, padx=(20,5), sticky='e')
        self.overtime_amount = ttk.Entry(totals_frame, width=12)
        self.overtime_amount.grid(row=0, column=5, padx=5, sticky='w')

        # Payment Section
        payment_frame = ttk.Frame(main_frame)
        payment_frame.grid(row=5, column=0, sticky='ew', pady=5)
        
        ttk.Label(payment_frame, text=self.t("Payment Method:")).grid(row=0, column=0, padx=5, sticky='e')
        self.payment_method = ttk.Combobox(payment_frame, 
                                        values=["Cash", "Instapay", "E_wallet", "Bank_account"],
                                        state="readonly",
                                        width=15)
        self.payment_method.grid(row=0, column=1, padx=5, sticky='w')
        
        ttk.Label(payment_frame, text=self.t("Base Salary:")).grid(row=0, column=2, padx=(20,5), sticky='e')
        self.salary = ttk.Entry(payment_frame, width=15, state='readonly')
        self.salary.grid(row=0, column=3, padx=5, sticky='w')
        
        ttk.Label(payment_frame, text=self.t("Net Salary:")).grid(row=0, column=4, padx=(20,5), sticky='e')
        self.net_salary = ttk.Entry(payment_frame, width=15, state='readonly')
        self.net_salary.grid(row=0, column=5, padx=5, sticky='w')

        # Save Button
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=6, column=0, pady=15)
        ttk.Button(btn_frame, text=self.t("Save Salary Record"), command=self.save_salary).pack()

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # Initialize data
        self.name_cb['values'] = list(self.employee_name_map.keys())
        self.code_cb['values'] = list(self.employee_code_map.keys())

        # Bind events
        # self.emp_name_var.trace_add('write', self.update_employee_info)
        # self.emp_code_var.trace_add('write', self.update_employee_info)
        self.month_var.trace_add('write', self.load_attendance_data)
        self.year_var.trace_add('write', self.load_attendance_data)
        self.delay_amount.bind('<KeyRelease>', self.calculate_net_salary)
        self.overtime_amount.bind('<KeyRelease>', self.calculate_net_salary)
        self.start_time_var.trace_add('write', self.load_attendance_data)
        self.end_time_var.trace_add('write', self.load_attendance_data)
    
    def update_salary_code(self, event):
        # Update name based on selected code
        code = self.emp_code_var.get()
        if code in self.employee_code_map:
            # Get corresponding name from code map
            new_name = self.employee_code_map[code]['name']
            if self.emp_name_var.get() != new_name:
                self.emp_name_var.set(new_name)
        self.load_attendance_data()

    def update_salary_name(self, event):
        # Update code based on selected name
        name = self.emp_name_var.get()
        if name in self.employee_name_map:
            # Get corresponding code from name map
            new_code = self.employee_name_map[name]['code']
            if self.emp_code_var.get() != new_code:
                self.emp_code_var.set(new_code)
        self.load_attendance_data()

    def update_employee_info(self, *args):
        code = self.emp_code_var.get()
        name = self.emp_name_var.get()
        
        if name in self.employee_name_map:
            new_code = self.employee_name_map[name]['code']
            if new_code != code:
                self.emp_code_var.set(new_code)
        
        if code in self.employee_code_map:
            new_name = self.employee_code_map[code]['name']
            if new_name != name:
                self.emp_name_var.set(new_name)
        
        self.load_attendance_data()

    def parse_time(self, time_str):
        try:
            return datetime.strptime(time_str, "%I:%M %p")
        except ValueError:
            return None

    def load_attendance_data(self, *args):
        self.table.delete(*self.table.get_children())
        
        # Get selected month/year
        month = self.month_var.get()
        year = self.year_var.get()
        employee_code = self.emp_code_var.get()
        
        if not all([month, year, employee_code]):
            return
        
        # Get date range
        start_date = datetime.strptime(f"1 {month} {year}", "%d %B %Y")
        end_date = (start_date + timedelta(days=32)).replace(day=1)
        
        # Get collections
        withdrawals_col = self.get_collection_by_name("Employee_withdrawls")
        hours_col = self.get_collection_by_name("Employee_appointimets")  # Fixed typo
        
        # Get data
        withdrawals = list(withdrawals_col.find({
            'employee_code': employee_code,
            'timestamp': {'$gte': start_date, '$lt': end_date}
        }))
        
        attendance = list(hours_col.find({
            'employee_code': employee_code,
            'check_in': {'$gte': start_date, '$lt': end_date}
        }))
        
        # Get scheduled hours
        start_time = self.parse_time(self.start_time_var.get())
        end_time = self.parse_time(self.end_time_var.get())
        
        # Initialize withdrawals tracking
        daily_withdrawals = defaultdict(float)
        total_withdrawls = 0.0

        # Process all withdrawals first
        for w in withdrawals:
            w_date = w['timestamp'].date()
            amount = w.get('amount_withdrawls', 0.0)
            daily_withdrawals[w_date] += amount
            total_withdrawls += amount

        # Generate daily records
        current_date = start_date
        while current_date < end_date:
            current_date_date = current_date.date()
            current_date_str = current_date.strftime("%Y-%m-%d")
            
            # Find attendance for this date
            daily_attendance = next((a for a in attendance 
                                if a['check_in'].date() == current_date_date), None)
            
            # Get withdrawal amount from pre-processed data
            withdrawal = daily_withdrawals.get(current_date_date, 0.0)
            
            # Initialize defaults
            from_time = "--"
            to_time = "--"
            duration = "--"
            delay = "--"
            overtime = "--"
            tags = []

            if daily_attendance:
                # Process attendance data
                check_in = daily_attendance.get('check_in')
                check_out = daily_attendance.get('check_out')
                
                # With this:
                from_time = check_in.strftime("%H:%M") if check_in else "--"
                to_time = check_out.strftime("%H:%M") if check_out else "--"
                
                if check_in and check_out:
                    # Calculate duration
                    duration_delta = check_out - check_in
                    hours = duration_delta.seconds // 3600
                    minutes = (duration_delta.seconds // 60) % 60
                    duration = f"{hours:02}:{minutes:02}"
                    
                    # Calculate time differences
                    if start_time:
                        scheduled_start = datetime.combine(current_date_date, start_time.time())
                        if check_in < scheduled_start:
                            delay_min = (scheduled_start - check_in).seconds // 60
                            delay = f"{delay_min} mins early"
                            tags.append('before_start')
                        elif check_in > scheduled_start:
                            delay_min = (check_in - scheduled_start).seconds // 60
                            delay = f"{delay_min} mins late"
                            tags.append('after_start')

                    if end_time and check_out:
                        scheduled_end = datetime.combine(current_date_date, end_time.time())
                        if check_out > scheduled_end:
                            overtime_min = (check_out - scheduled_end).seconds // 60
                            overtime = f"{overtime_min} mins overtime"
                            tags.append('after_end')
                        elif check_out < scheduled_end:
                            overtime_min = (scheduled_end - check_out).seconds // 60
                            overtime = f"{overtime_min} mins early"
                            tags.append('before_end')

            # Insert row with accumulated withdrawal
            self.table.insert('', 'end', values=(
                current_date_str,
                from_time,
                to_time,
                duration,
                delay,
                overtime,
                f"{withdrawal:.2f}"
            ), tags=tags)
            
            current_date += timedelta(days=1)
        
        # Update totals
        self.total_withdrawls.config(state='normal')
        self.total_withdrawls.delete(0, tk.END)
        self.total_withdrawls.insert(0, f"{total_withdrawls:.2f}")
        self.total_withdrawls.config(state='readonly')
        self.calculate_net_salary()

    def calculate_net_salary(self, event=None):
        try:
            base_salary = self.employee_code_map.get(int(self.emp_code_var.get()), {}).get('salary', 0)
            base_salary = float(base_salary)
            print(base_salary)
            total_withdrawls = float(self.total_withdrawls.get())
            delay_penalty = float(self.delay_amount.get() or 0)
            overtime_bonus = float(self.overtime_amount.get() or 0)

            net_salary = base_salary - total_withdrawls - delay_penalty + overtime_bonus
            
            self.net_salary.config(state='normal')
            self.net_salary.delete(0, tk.END)
            self.net_salary.insert(0, f"{net_salary:.2f}")
            self.net_salary.config(state='readonly')
            self.salary.config(state='normal')
            self.salary.delete(0, tk.END)
            self.salary.insert(0, f"{base_salary:.2f}")
            self.salary.config(state='readonly')
        except ValueError:
            pass

    def save_salary(self):
        try:
            salary_data = {
                'employee_code': self.emp_code_var.get(),
                'employee_name': self.emp_name_var.get(),
                'month_year': f"{self.month_var.get()} {self.year_var.get()}",
                'base_salary': self.employee_code_map.get(int(self.emp_code_var.get()), {}).get('salary', 0),
                'total_withdrawls': float(self.total_withdrawls.get()),
                'delay_penalty': float(self.delay_amount.get() or 0),
                'overtime_bonus': float(self.overtime_amount.get() or 0),
                'net_salary': float(self.net_salary.get()),
                'payment_method': self.payment_method.get(),
                'timestamp': datetime.now()
            }
            previous_total = self.calculate_previous_withdrawals(self.emp_code_var.get())
            # For string inputs like "$1000"
            try:
                withdrawal_amount = -abs(float(self.total_withdrawls.get().replace('$', '').strip()))
            except (ValueError, AttributeError):
                withdrawal_amount = 0.0
            withdrawal_data = {
                'employee_code': self.emp_code_var.get(),
                'employee_name': self.emp_name_var.get(),
                'previous_withdrawls': previous_total,  # Total before this withdrawal
                'amount_withdrawls': withdrawal_amount,
                # 'cumulative_total': previous_total + amount,  # New total after this withdrawal
                'payment_method': self.payment_method.get(),
                'timestamp': datetime.now()
            }
            
            

            
            # Input validation
            if not all([salary_data['employee_code'], salary_data['month_year']]):
                raise ValueError("Missing required fields")
            
            salary_col = self.get_collection_by_name("Employee_Salary")
            # Database collections
            withdrawals_col = self.get_collection_by_name("Employee_withdrawls")
            
            # Check for existing salary record
            existing = salary_col.find_one({
                "employee_code": salary_data["employee_code"],
                "month_year": salary_data["month_year"]
            })
            
            if existing:
                messagebox.showwarning(self.t("Warning"), 
                    self.t("Employee already took the salary in this month"))
                return
            if not self.payment_method.get():
                messagebox.showinfo(self.t("Warning"),self.t("Enter the payment Method"))
                return
            # Insert new record if not exists
            salary_col.insert_one(salary_data)
            withdrawals_col.insert_one(withdrawal_data)
            # self.save_withdrawal(withdrawals_col,employees_col)
            messagebox.showinfo(self.t("Success"), self.t("Salary record saved successfully"))
            
        except Exception as e:
            messagebox.showerror(self.t("Error"), f"{self.t("Failed to save salary:")} {str(e)}")

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


    def general_exp_rev(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        self.topbar(show_back_button=True)
        
        # Create main container frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create paned window for resizable split
        paned_window = tk.PanedWindow(main_frame, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=4)
        paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Expense Frame (left side)
        expense_frame = tk.LabelFrame(paned_window, text=self.t("Expenses"), font=("Arial", 12, "bold"), padx=10, pady=10)
        # Revenue Frame (right side)
        revenue_frame = tk.LabelFrame(paned_window, text=self.t("Revenues"), font=("Arial", 12, "bold"), padx=10, pady=10)
        
        paned_window.add(expense_frame)
        paned_window.add(revenue_frame)
        
        # Force Tkinter to calculate window dimensions
        self.root.update_idletasks()
        
        # Set separator to half of the screen immediately
        width = main_frame.winfo_width()
        if width > 100:  # Ensure we have a reasonable width
            paned_window.sash_place(0, width // 2, 0)
        
        # Common payment methods
        payment_methods = ["cash", "instapay", "bank_account", "e_wallet"]
        
        # ======================
        # EXPENSE SECTION
        # ======================
        expense_frame.columnconfigure(1, weight=1)
        for i in range(4):
            expense_frame.rowconfigure(i, weight=1)
        
        tk.Label(expense_frame, text=self.t("Amount Paid:"), font=("Arial", 10)).grid(row=0, column=0, sticky='e', pady=5)
        self.expense_amount = tk.DoubleVar()
        expense_entry = tk.Entry(expense_frame, textvariable=self.expense_amount)
        expense_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        tk.Label(expense_frame, text=self.t("Payment Method:"), font=("Arial", 10)).grid(row=1, column=0, sticky='e', pady=5)
        self.expense_payment = tk.StringVar()
        expense_payment_cb = ttk.Combobox(expense_frame, textvariable=self.expense_payment, 
                                        values=payment_methods, state="readonly")
        expense_payment_cb.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        expense_payment_cb.current(0)  # Default to Cash
        
        tk.Label(expense_frame, text=self.t("Description:"), font=("Arial", 10)).grid(row=2, column=0, sticky='e', pady=5)
        self.expense_desc = tk.StringVar()
        expense_desc_entry = tk.Entry(expense_frame, textvariable=self.expense_desc)
        expense_desc_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        
        expense_submit = tk.Button(expense_frame, 
                            text=self.t("💾 Record Expense"), 
                            font=('Helvetica', 12, 'bold'),
                            width=20,
                            command=lambda: self.save_transaction("Expense"),
                            bg='#2196F3', fg='white')
        expense_submit.grid(row=3, column=0, columnspan=2, pady=10, sticky='ew')
        
        # ======================
        # REVENUE SECTION
        # ======================
        revenue_frame.columnconfigure(1, weight=1)
        for i in range(4):
            revenue_frame.rowconfigure(i, weight=1)
        
        tk.Label(revenue_frame, text=self.t("Amount Received:"), font=("Arial", 10)).grid(row=0, column=0, sticky='e', pady=5)
        self.revenue_amount = tk.DoubleVar()
        revenue_entry = tk.Entry(revenue_frame, textvariable=self.revenue_amount)
        revenue_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        tk.Label(revenue_frame, text=self.t("Payment Method:"), font=("Arial", 10)).grid(row=1, column=0, sticky='e', pady=5)
        self.revenue_payment = tk.StringVar()
        revenue_payment_cb = ttk.Combobox(revenue_frame, textvariable=self.revenue_payment, 
                                        values=payment_methods, state="readonly")
        revenue_payment_cb.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        revenue_payment_cb.current(0)  # Default to Cash
        
        tk.Label(revenue_frame, text=self.t("Description:"), font=("Arial", 10)).grid(row=2, column=0, sticky='e', pady=5)
        self.revenue_desc = tk.StringVar()
        revenue_desc_entry = tk.Entry(revenue_frame, textvariable=self.revenue_desc)
        revenue_desc_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        
        revenue_submit = tk.Button(revenue_frame, 
                            text=self.t("💾 Record Revenue"), 
                            font=('Helvetica', 12, 'bold'),
                            width=20,
                            command=lambda: self.save_transaction("Revenue"),
                            bg="#21F35D", fg='white')
        revenue_submit.grid(row=3, column=0, columnspan=2, pady=10, sticky='ew')        
        # Configure grid weights
        for frame in [expense_frame, revenue_frame]:
            frame.grid_columnconfigure(1, weight=1)
            for i in range(4):
                frame.grid_rowconfigure(i, weight=1)

    # New method to save transactions to MongoDB
    def save_transaction(self, transaction_type):
        if transaction_type == "Expense":
            amount = self.expense_amount.get()
            payment = self.expense_payment.get()
            desc = self.expense_desc.get()
        else:  # Revenue
            amount = self.revenue_amount.get()
            payment = self.revenue_payment.get()
            desc = self.revenue_desc.get()
        
        if amount <= 0:
            messagebox.showerror(self.t("Error"), self.t("Amount must be greater than zero"))
            return
            
        if not payment:
            messagebox.showerror(self.t("Error"), self.t("Please select a payment method"))
            return
        code = self.get_next_code(self.general_exp_rev_collection)    
        # Create document for MongoDB
        transaction = {
            "type": transaction_type,
            "amount": amount,
            "payment_method": payment,
            "description": desc,
            "date": datetime.now(),
            "code":code
        }
        
        # Save to MongoDB
        try:
            collection = self.general_exp_rev_collection
            collection.insert_one(transaction)
            messagebox.showinfo(self.t("Success"), f"{transaction_type} {self.t("recorded successfully!")}")
            
            # Clear fields
            if transaction_type == "Expense":
                self.expense_amount.set(0)
                self.expense_payment.set("cash")
                self.expense_desc.set("")
            else:
                self.revenue_amount.set(0)
                self.revenue_payment.set("cash")
                self.revenue_desc.set("")
                
        except Exception as e:
            messagebox.showerror(self.t("Database Error"), f"{self.t("Failed to save transaction:")} {str(e)}")

    def Treasury_window(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        self.topbar(show_back_button=True)

        # Main container
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Filter controls
        filter_frame = tk.Frame(main_frame)
        filter_frame.pack(fill=tk.X, pady=10)

        # Date filters
        date_frame = tk.Frame(filter_frame)
        date_frame.pack(side=tk.LEFT, padx=10)

        tk.Label(date_frame, text=self.t("From Date:")).pack(side=tk.LEFT)
        self.from_date = DateEntry(date_frame, date_pattern="dd/mm/yyyy")
        self.from_date.pack(side=tk.LEFT, padx=10)

        tk.Label(date_frame, text=self.t("To Date:")).pack(side=tk.LEFT, padx=(20,0))
        self.to_date = DateEntry(date_frame, date_pattern="dd/mm/yyyy")
        self.to_date.pack(side=tk.LEFT)

        # Payment method filter
        method_frame = tk.Frame(filter_frame)
        method_frame.pack(side=tk.LEFT, padx=20)

        tk.Label(method_frame, text=self.t("Payment Method:")).pack(side=tk.LEFT)
        self.payment_method = ttk.Combobox(
            method_frame,
            values=["All", "Cash", "Instapay", "Bank Account", "E Wallet"]
        )
        self.payment_method.set("All")
        self.payment_method.pack(side=tk.LEFT, padx=10)

        # Search button
        search_btn = tk.Button(filter_frame, text=self.t("Search"), command=self.fetch_transactions)
        search_btn.pack(side=tk.RIGHT, padx=10)

        # Results Treeview
        columns = ("date", "description", "credit", "debit", "payment_method")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        
        # Configure columns
        self.tree.heading("date", text=self.t("Date"))
        self.tree.heading("description", text=self.t("Description"))
        self.tree.heading("credit", text=self.t("Credit"))
        self.tree.heading("debit", text=self.t("Debit"))
        self.tree.heading("payment_method", text=self.t("Payment Method"))

        self.tree.column("date", width=120)
        self.tree.column("description", width=250)
        self.tree.column("credit", width=120)
        self.tree.column("debit", width=120)
        self.tree.column("payment_method", width=150)

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

        tk.Label(totals_frame, text=self.t("Total Credit:"), font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=10)
        tk.Label(totals_frame, textvariable=self.total_credit_var, font=('Arial', 10)).pack(side=tk.LEFT)

        tk.Label(totals_frame, text=self.t("Total Debit:"), font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=10)
        tk.Label(totals_frame, textvariable=self.total_debit_var, font=('Arial', 10)).pack(side=tk.LEFT)

        tk.Label(totals_frame, text=self.t("Balance:"), font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=10)
        tk.Label(totals_frame, textvariable=self.balance_var, font=('Arial', 10)).pack(side=tk.LEFT)

        headers = ["date", "description", 'credit', 'debit', "payment_method"]
        filename_excel = f"تقرير الخزنه_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filename_pdf = f"تقرير الخزنه_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        report_folder = "تقارير الخزنه"
        excel_btn = ttk.Button(totals_frame, text=self.t("Export to Excel"), command=lambda: self.export_to_excel(self.filtered_transactions,headers,filename_excel))
        pdf_btn = ttk.Button(totals_frame, text=self.t("Export to PDF"), command=lambda: self.export_to_pdf(self.filtered_transactions,headers=headers,filename=filename_pdf,report_folder=report_folder,title=report_folder))
        excel_btn.pack(side=tk.LEFT, padx=10, pady=5)
        pdf_btn.pack(side=tk.LEFT, padx=10, pady=5)
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

        # Get filter parameters
        start_date = self.from_date.get_date()
        end_date = self.to_date.get_date()
        selected_method = self.payment_method.get().lower()

        # Convert dates to UTC datetime
        tz = pytz.timezone('UTC')
        start_date = tz.localize(datetime.combine(start_date, datetime.min.time()))
        end_date = tz.localize(datetime.combine(end_date, datetime.max.time()))
        start_date_str = start_date.strftime("%d/%m/%Y %H:%M")
        end_date_str = end_date.strftime("%d/%m/%Y %H:%M")
        transactions = []

        # 1. Customer Payments (Credit) done
        customer_payments = self.customer_payments.find({"Time": {"$gte": start_date, "$lte": end_date}})
        # print(customer_payments)
        for doc in customer_payments:
            transactions.append({
                "date": self.parse_date(doc.get("Time", "")),
                "description": doc.get("Operation_Number", ""),
                "credit": float(doc.get("Credit", 0)),
                "debit": 0.0,
                "payment_method": doc.get("Payment_method", "").lower().replace(" ", "_")
            })
        # # print(transactions)

        # 2. Employee Salary (Debit) done
        salaries = self.employee_salary_collection.find({"timestamp": {"$gte": start_date, "$lte": end_date}})
        # print(salaries)
        for doc in salaries:
            transactions.append({
                "date": self.parse_date(doc.get("timestamp", "")),
                "description": f"Salary {doc.get('month_year', '')}",
                "credit": 0.0,
                "debit": float(doc.get("net_salary", 0)),
                "payment_method": doc.get("payment_method", "").lower().replace(" ", "_")
            })
        # # print(transactions)
        # 3. Employee Withdrawals (Debit) done  
        withdrawals = self.employee_withdrawls_collection.find({"timestamp": {"$gte": start_date, "$lte": end_date}})
        for doc in withdrawals:
            transactions.append({
                "date": self.parse_date(doc.get("timestamp", "")),
                "description": f"Withdrawal {doc.get('employee_code', '')}",
                "credit": 0.0,
                "debit": float(doc.get("amount_withdrawls", 0)),
                "payment_method": doc.get("payment_method", "").lower().replace(" ", "_")
            })
        # print(transactions)
        # 4. Purchases (Debit)
        purchases = self.purchases_collection.find({"Date": {"$gte": start_date, "$lte": end_date}})
        for doc in purchases:
            financials = doc.get("Financials", {})  # Safely get the nested Financials object
            transactions.append({
                "date": self.parse_date(doc.get("Date", "")),
                "description": doc.get("Receipt_Number", ""),
                "credit": 0.0,
                "debit": float(financials.get("Payed_cash", 0)),  # Access via Financials
                "payment_method": financials.get("Payment_method", "").lower().replace(" ", "_")  # Acce
            })
        # # print(transactions)
        # 5. Sales (Credit)
        sales = self.sales_collection.find({"Date": {"$gte": start_date, "$lte": end_date}})
        for doc in sales:
            financials = doc.get("Financials", {})  # Safely get the nested Financials object
            transactions.append({
                "date": self.parse_date(doc.get("Date", "")),
                "description": doc.get("Receipt_Number", ""),
                "credit": float(financials.get("Payed_cash", 0)),
                "debit": 0.0,
                "payment_method": financials.get("Payment_method", "").lower().replace(" ", "_")  # Acce
            })
        # # print(transactions)
        # 6. Supplier Payments (Debit)
        supplier_payments = self.supplier_payments.find({"Time": {"$gte": start_date, "$lte": end_date}})
        for doc in supplier_payments:
            transactions.append({
                "date": self.parse_date(doc.get("Time", "")),
                "description": doc.get("Operation_Number", ""),
                "credit": 0.0,
                "debit": float(doc.get("Debit", 0)),
                "payment_method": doc.get("Payment_method", "").lower().replace(" ", "_")
            })
        # 7 general exp. and rev.(depit)--> Expense , (credit) --> Revenue
        general_exp_rev = self.general_exp_rev_collection.find({"date": {"$gte": start_date, "$lte": end_date}})
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
        # print(transactions)
        # Filter transactions
        allowed_methods = ["cash", "instapay", "bank_account", "e_wallet"]
        self.filtered_transactions = []
        for t in transactions:
            if selected_method != "all":
                if t["payment_method"] != selected_method.replace(" ", "_"):
                    continue
            if t["payment_method"] in allowed_methods and t["date"] is not None:
                self.filtered_transactions.append(t)

        # Populate treeview and calculate totals
        for t in self.filtered_transactions:
            self.totals['credit'] += t['credit']
            self.totals['debit'] += t['debit']
            
            self.tree.insert("", "end", values=(
                t["date"].strftime("%d/%m/%Y %H:%M"),
                t["description"],
                f"{t['credit']:,.2f} ج.م",
                f"{t['debit']:,.2f}  ج.م",
                t["payment_method"].replace("_", " ").title()
            ))

        # Update totals display
        self.total_credit_var.set(f"{self.totals['credit']:,.2f} ج.م")
        self.total_debit_var.set (f"{self.totals['debit']:,.2f}  ج.م")
        # self.total_debit_var.set(f"${self.totals['debit']:,.2f}")
        balance = self.totals['credit'] - self.totals['debit']
        self.balance_var.set(f"{balance:,.2f} ج.م")
        

    def sales_invoice(self, user_role, add_or_update):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Initialize product mappings
        self.update = False
        self.product_map = {}
        self.name_to_code = {}
        
        # Create top bar
        self.topbar(show_back_button=True, Back_to_Sales_Window=True)

        # MongoDB collections
        customers_col = self.get_collection_by_name("Customers")
        sales_col = self.get_collection_by_name("Sales")
        products_col = self.get_collection_by_name("Products")

        # Main form frame with responsive sizing
        form_frame = tk.Frame(self.root, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure columns - 10 columns with equal weight
        for i in range(10):
            form_frame.columnconfigure(i, weight=1)

        # ===== INVOICE SELECTION FOR UPDATE MODE =====
        current_row = 0
        self.selected_invoice_id = None
        
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
            tk.Label(invoice_frame, text=self.t("Select Invoice"), 
                    font=("Arial", 10, "bold")).grid(row=0, column=0, sticky='w')
            self.invoice_var = tk.StringVar()
            invoice_cb = ttk.Combobox(invoice_frame, textvariable=self.invoice_var, values=invoice_numbers)
            invoice_cb.grid(row=0, column=1, padx=5, sticky='ew', columnspan=3)
            
            # Load button
            load_btn = tk.Button(invoice_frame, text=self.t("Load Invoice"), 
                                command=lambda: self.load_invoice_data(sales_col),
                                bg='#2196F3', fg='white')
            load_btn.grid(row=0, column=4, padx=5, sticky='ew')
            
            # Delete button
            delete_btn = tk.Button(invoice_frame, text=self.t("Delete Invoice"), 
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
        tk.Label(customer_frame, text=self.t("Customer Name"), 
                font=("Arial", 10, "bold")).grid(row=0, column=0, sticky='w')
        self.customer_name_var = tk.StringVar()
        self.customer_name_cb = ttk.Combobox(customer_frame, 
                                            textvariable=self.customer_name_var, 
                                            values=sorted(all_customers))
        self.customer_name_cb.grid(row=0, column=1, padx=5, sticky='ew')

        # Customer Code Combobox
        tk.Label(customer_frame, text=self.t("Customer Code"), 
                font=("Arial", 10, "bold")).grid(row=0, column=2, sticky='w')
        self.customer_code_var = tk.StringVar()
        self.customer_code_cb = ttk.Combobox(customer_frame, 
                                            textvariable=self.customer_code_var, 
                                            values=sorted(all_codes))
        self.customer_code_cb.grid(row=0, column=3, padx=5, sticky='ew')

        # Previous Balance Field
        tk.Label(customer_frame, text=self.t("Balance"), 
                font=("Arial", 10, "bold")).grid(row=0, column=4, sticky='e')
        self.previous_balance_var = tk.StringVar()
        self.previous_balance_entry = tk.Entry(customer_frame, 
                                            textvariable=self.previous_balance_var, 
                                            state='readonly', width=10)
        self.previous_balance_entry.grid(row=0, column=5, sticky='ew', padx=5)

        # Paid Money Field
        tk.Label(customer_frame, text=self.t("Paid Money"), 
                font=("Arial", 10, "bold")).grid(row=0, column=6, sticky='e')
        self.payed_cash_var = tk.DoubleVar()
        self.payed_cash_entry = tk.Entry(customer_frame, 
                                        textvariable=self.payed_cash_var,
                                        width=10)
        self.payed_cash_entry.grid(row=0, column=7, sticky='ew', padx=5)

        # Transportation Fees Field
        tk.Label(customer_frame, text=self.t("Transport"), 
                font=("Arial", 10, "bold")).grid(row=0, column=10, sticky='e')
        self.transport_fees_var = tk.DoubleVar(value=0.0)
        self.transport_fees_entry = tk.Entry(customer_frame, 
                                        textvariable=self.transport_fees_var,
                                        width=8)
        self.transport_fees_entry.grid(row=0, column=11, sticky='ew', padx=5)

        # Payment Method Dropdown
        tk.Label(customer_frame, text=self.t("Payment Method"), 
                font=("Arial", 10, "bold")).grid(row=0, column=8, sticky='e')
        self.payment_method_var = tk.StringVar()
        payment_methods = ['Cash', 'E_Wallet', 'bank_account', 'Instapay']
        payment_cb = ttk.Combobox(customer_frame, 
                                textvariable=self.payment_method_var, 
                                values=payment_methods, 
                                state='readonly',
                                width=8)
        payment_cb.grid(row=0, column=9, sticky='ew', padx=5)
        payment_cb.current(0)  # Set default to Cash
        
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
            messagebox.showerror(self.t("Database Error"), f"{self.t("Failed to load products:")} {str(e)}")
            return

        # ===== ITEMS GRID SECTION =====
        # Make items grid expandable
        form_frame.grid_rowconfigure(current_row + 1, weight=1)
        
        # Invoice Items Grid
        columns = self.get_fields_by_name("Sales_Header")
        num_columns = len(columns)
        
        # Create header frame
        header_frame = tk.Frame(form_frame, bg='#f0f0f0')
        header_frame.grid(row=current_row, column=0, columnspan=10, sticky='ew', pady=(20, 0))
        current_row += 1
        
        # Configure header columns
        for col_idx in range(num_columns):
            header_frame.columnconfigure(col_idx, weight=1, uniform='cols')
            tk.Label(header_frame, text=self.t(columns[col_idx]), relief='ridge', 
                    bg='#f0f0f0', anchor='w', padx=5).grid(row=0, column=col_idx, sticky='ew')

        # Scrollable Canvas
        canvas_container = tk.Frame(form_frame)
        canvas_container.grid(row=current_row, column=0, columnspan=10, sticky='nsew')
        canvas_container.grid_rowconfigure(0, weight=1)
        canvas_container.grid_columnconfigure(0, weight=1)
        current_row += 1
        
        canvas = tk.Canvas(canvas_container, highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
        self.rows_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.rows_frame, anchor="nw", tags="inner_frame")
        
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def configure_canvas(event):
            canvas_width = event.width
            canvas.itemconfig("inner_frame", width=canvas_width)
        
        self.rows_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_canvas)

        self.entries = []

        # Add initial rows
        self.add_three_rows()

        # ===== BUTTONS SECTION =====
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=current_row, column=0, columnspan=10, pady=10, sticky='ew')
        
        # Configure button frame columns
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        add_btn = tk.Button(button_frame, text=self.t("➕ Add 3 More Rows"), 
                        command=self.add_three_rows, bg='#4CAF50', fg='white')
        add_btn.grid(row=0, column=0, padx=5, sticky='w')
        
        if add_or_update == "add":
            save_btn = tk.Button(button_frame, text=self.t("💾 Save Invoice"), 
                                command=lambda: self.save_invoice(sales_col, customers_col, products_col),
                                bg='#2196F3', fg='white')
            save_btn.grid(row=0, column=1, padx=5, sticky='e')
        else:
            self.update = True
            update_btn = tk.Button(button_frame, text=self.t("🔄 Update Invoice"), 
                                command=lambda: self.save_invoice(sales_col, customers_col, products_col),
                                bg='#FF9800', fg='white')
            update_btn.grid(row=0, column=1, padx=5, sticky='e')
        # Modified create_row function to accept initial values

    def load_invoice_data(self, sales_col):
        """Load selected invoice data into the form"""
        invoice_number = self.invoice_var.get()
        if not invoice_number:
            messagebox.showwarning(self.t("Selection Needed"), self.t("Please select an invoice first"))
            return
        
        # Fetch invoice data from MongoDB
        invoice_data = sales_col.find_one({"Receipt_Number": invoice_number})
        if not invoice_data:
            messagebox.showerror(self.t("Not Found"), self.t("Invoice not found in database"))
            return
        
        # Store invoice ID for later reference
        self.selected_invoice_id = str(invoice_data["_id"])
        
        # Extract nested dictionaries
        self.customer_info = invoice_data.get("Customer_info", {})
        self.financials = invoice_data.get("Financials", {})
        self.items = invoice_data.get("Items", [])
        # self.products_set  = {item.get("Product_code") for item in self.items if "Product_code" in item}
        # self.Total_Qty_set = {item.get("Total_QTY") for item in self.items if "Product_code" in item}

        # Populate customer information
        self.customer_name_var.set(self.customer_info.get("name", ""))
        self.customer_code_var.set(self.customer_info.get("code", ""))
        self.previous_balance_var.set(str(self.financials.get("Previous_balance", 0)))
        
        # Populate financial fields
        self.payed_cash_var.set(str(self.financials.get("Payed_cash", 0)))  # Ensure string conversion
        self.transport_fees_var.set(str(self.financials.get("transport_fees", 0)))  # Ensure string conversion
        
        # Set payment method
        payment_method = self.financials.get("payment_method", "Cash")
        if payment_method in ["Cash", "E_Wallet", "bank_account", "Instapay"]:
            self.payment_method_var.set(payment_method)
        
        # Clear existing items 
        self.entries.clear()
        for widget in self.rows_frame.winfo_children():
            widget.destroy()
        
        # Add rows with invoice items
        # Calculate the number of sets needed (each set contains 3 rows)
        num_sets = (len(self.items) + 2) // 3  # Round up to nearest multiple of 3
        # Process each set of items
        for set_index in range(num_sets):
            start_index = set_index * 3
            end_index = start_index + 3
            item_set = self.items[start_index:end_index]  # Get next 3 items (or remaining)
            self.add_three_rows(initial_data=item_set)  # Pass items to populate
    def load_invoice_data_purchase(self, sales_col):
        """Load selected invoice data into the form"""
        invoice_number = self.invoice_var.get()
        if not invoice_number:
            messagebox.showwarning(self.t("Selection Needed"), self.t("Please select an invoice first"))
            return
        
        # Fetch invoice data from MongoDB
        invoice_data = sales_col.find_one({"Receipt_Number": invoice_number})
        if not invoice_data:
            messagebox.showerror(self.t("Not Found"), self.t("Invoice not found in database")   )
            return
        
        # Store invoice ID for later reference
        self.selected_invoice_id = str(invoice_data["_id"])
        
        # Extract nested dictionaries
        self.supplier_info = invoice_data.get("supplier_info", {})
        self.financials_purchases = invoice_data.get("Financials", {})
        self.items_purchase = invoice_data.get("Items", [])
        # self.products_set  = {item.get("Product_code") for item in self.items if "Product_code" in item}
        # self.Total_Qty_set = {item.get("Total_QTY") for item in self.items if "Product_code" in item}

        # Populate customer information
        self.supplier_name_var.set(self.supplier_info.get("name", ""))
        self.supplier_code_var.set(self.supplier_info.get("code", ""))
        self.previous_balance_var.set(str(self.financials_purchases.get("Previous_balance", 0)))
        
        # Populate financial fields
        self.payed_cash_var.set(str(self.financials_purchases.get("Payed_cash", 0)))  # Ensure string conversion
        # self.transport_fees_var.set(str(financials.get("transport_fees", 0)))  # Ensure string conversion
        
        # Set payment method
        payment_method = self.financials_purchases.get("Payment_method", "Cash")   
        if payment_method in ["Cash", "E_Wallet", "bank_account", "Instapay"]:
            self.payment_method_var.set(payment_method)
        
        # Clear existing items 
        self.entries.clear()
        for widget in self.rows_frame.winfo_children():
            widget.destroy()
        
        # Add rows with invoice items
        # Calculate the number of sets needed (each set contains 3 rows)
        num_sets = (len(self.items_purchase) + 2) // 3  # Round up to nearest multiple of 3
        # Process each set of items
        for set_index in range(num_sets):
            start_index = set_index * 3
            end_index = start_index + 3
            item_set = self.items_purchase[start_index:end_index]  # Get next 3 items (or remaining)
            self.add_three_rows_purchase(initial_data=item_set)  # Pass items to populate

    def delete_invoice(self,products_col, sales_col, customers_col,source):
        """Delete selected invoice from the database"""
        invoice_number = self.invoice_var.get()
        if not invoice_number:
            messagebox.showwarning(self.t("Selection Needed"), self.t("Please select an invoice first"))
            return
        
        # Confirm deletion
        if not messagebox.askyesno(self.t("Confirm Delete"), f"{self.t("Delete invoice")} {invoice_number} {self.t("permanently?")}"):
            return
        
        # Fetch invoice to get customer and amount details
        invoice_data = sales_col.find_one({"Receipt_Number": invoice_number})
        self.financials = invoice_data.get("Financials", {})

        # product_qty_map = {}

        if source == "sales":
            Customer_info = invoice_data.get("Customer_info", {})
            customer_name = Customer_info.get("name",{})
            customer = customers_col.find_one({"Name": customer_name})
            self.pending_customer_id = customer["_id"]
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
            self.pending_customer_id = supplier["_id"]   
            for item in invoice_data.get("Items",[]):
                material_code = item.get("material_code")
                total_qty = item.get("Total_QTY", 0)
                if material_code:
                    products_col.update_one(
                        {"material_code": material_code},
                        {"$inc": {"stock_quantity": -total_qty}}
                    )
        prev_total_amount = self.financials.get("Net_total")
        prev_payed_cash = self.financials.get("Payed_cash")
        prev_added_balance = prev_total_amount - prev_payed_cash
        if source == "sales":
            customers_col.update_one(
                {"_id": self.pending_customer_id},
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
                {"_id": self.pending_customer_id},
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
            messagebox.showerror(self.t("Not Found"), self.t("Invoice not found"))
            return
        
        # Delete from MongoDB
        sales_col.delete_one({"Receipt_Number": invoice_number})
        
        # # Revert customer balance
        # self.revert_customer_balance(customers_col, invoice_data)
        
        messagebox.showinfo(self.t("Success"), self.t("Invoice deleted successfully"))
        # Clear the form or reset UI as needed
        self.invoice_var.set("")
        self.selected_invoice_id = None

        if source == "sales":
            self.sales_invoice(self.user_role,"update")
        else:
            self.new_Purchase_invoice(self.user_role,"update")

    def create_row(self, parent, row_number, bg_color, initial_values=None):
        columns = self.get_fields_by_name("Sales_Header")
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

                # if(col_idx < 3 or col_idx == 5):
                    # value = value.strip()

                # if not((col =="Product_code" or
                #    col =="Discount Type" or
                #    col =="product_name" or
                #    col =="unit"
                #    )):
                #     value = str(value)
                #     value = value.strip()

                # if (col =="Product_code" or
                #    col =="Discount_Type" or
                #    col =="product_name" or
                #    col =="unit"
                #    ):
                # value = str(value)
                # value = value.strip()
                # value = value.strip()
                if col == "Product_code" and (value not in self.product_codes):
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
                cb = ttk.Combobox(row_frame, textvariable=vars, values=self.product_codes)
                cb.bind('<<ComboboxSelected>>', lambda e, r=row_number: self.update_product_info(r, "code"))
                cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_combobox_change(e, r, "code"))
                cb.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                value = value.strip()
                cb.set(value)
                row_entries.append(vars)
                ###########################
                # var = tk.StringVar(value=value)
                # entry = tk.Entry(row_frame, textvariable=var)
                # entry.bind('<KeyRelease>', lambda e, r=row_number: self.calculate_totals(r))
                # entry.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                # row_entries.append(entry)
            elif col == "product_name":
                var = tk.StringVar(value=value)
                row_entry_vars.append(var)
                cb = ttk.Combobox(row_frame, textvariable=var, values=self.product_names)
                # var = tk.StringVar(value=value)
                cb.bind('<<ComboboxSelected>>', lambda e, r=row_number: self.update_product_info(r, "name"))
                # var = tk.StringVar(value=value)
                cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_combobox_change(e, r, "name"))
                # var = tk.StringVar(value=value)
                cb.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                # x = var.get()
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

    def add_three_rows(self, initial_data=None):
        current_row_count = len(self.entries)
        for i in range(3):
            bg_color = 'white' if (current_row_count + i) % 2 == 0 else '#f0f0f0'
            row_data = initial_data[i] if initial_data and i < len(initial_data) else None
            row_entries = self.create_row(self.rows_frame, current_row_count + i, bg_color, row_data)
            self.entries.append(row_entries)
            
            # If we have initial data, update product info
            if row_data: #Seif: row_data is always empty
                # First try to update by product code if available
                # if row_data.get("Product_code"):
                #     print(f"Updating row {current_row_count + i} by code: {row_data['Product_code']}")
                #     self.update_product_info(current_row_count + i, "code") #Seif: This function ends up clearing the fields data
                # # Then try by product name
                # elif row_data.get("product_name"):
                #     print(f"Updating row {current_row_count + i} by name: {row_data['product_name']}")
                #     self.update_product_info(current_row_count + i, "name")
                
                # Calculate totals for this row
                self.calculate_totals(current_row_count + i)

    def add_three_rows_purchase(self, initial_data=None):
        current_row_count = len(self.entries)
        for i in range(3):
            bg_color = 'white' if (current_row_count + i) % 2 == 0 else '#f0f0f0'
            row_data = initial_data[i] if initial_data and i < len(initial_data) else None
            row_entries = self.create_row_purchase(self.rows_frame, current_row_count + i, bg_color, row_data)
            self.entries.append(row_entries)
            
            # If we have initial data, update product info
            if row_data: #Seif: row_data is always empty
                # First try to update by product code if available
                # if row_data.get("Product_code"):
                #     print(f"Updating row {current_row_count + i} by code: {row_data['Product_code']}")
                #     self.update_product_info(current_row_count + i, "code") #Seif: This function ends up clearing the fields data
                # # Then try by product name
                # elif row_data.get("product_name"):
                #     print(f"Updating row {current_row_count + i} by name: {row_data['product_name']}")
                #     self.update_product_info(current_row_count + i, "name")
                
                # Calculate totals for this row
                self.calculate_totals(current_row_count + i)
                
    def new_Purchase_invoice(self, user_role, add_or_update):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Initialize product mappings
        self.update_purchase = False
        self.material_map = {}
        self.name_to_code = {}
        
        # Create top bar
        self.topbar(show_back_button=True,Back_to_Purchases_Window=True)

        # MongoDB collections
        suppliers_col = self.get_collection_by_name("Suppliers")
        purchases_col = self.get_collection_by_name("Purchases")
        materials_col = self.get_collection_by_name("Materials")

        # Main form frame with responsive sizing
        form_frame = tk.Frame(self.root, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure columns - 10 columns with equal weight
        for i in range(10):
            form_frame.columnconfigure(i, weight=1)

        # ===== INVOICE SELECTION FOR UPDATE MODE =====
        current_row = 0
        self.selected_invoice_id = None
        
        if add_or_update == "update":
            # Create invoice selection frame
            invoice_frame = tk.Frame(form_frame, bd=1, relief=tk.SOLID, padx=5, pady=5)
            invoice_frame.grid(row=current_row, column=0, columnspan=12, sticky='ew', pady=5)
            current_row += 1
            
            # Configure invoice frame columns
            for i in range(12):
                invoice_frame.columnconfigure(i, weight=1 if i % 2 == 1 else 0)
            
            # Fetch invoice numbers
            invoice_numbers = [str(doc["Receipt_Number"]) for doc in purchases_col.find({}, {"Receipt_Number": 1})]
            
            # Invoice selection
            tk.Label(invoice_frame, text=self.t("Select Invoice"), 
                    font=("Arial", 10, "bold")).grid(row=0, column=0, sticky='w')
            self.invoice_var = tk.StringVar()
            invoice_cb = ttk.Combobox(invoice_frame, textvariable=self.invoice_var, values=invoice_numbers)
            invoice_cb.grid(row=0, column=1, padx=5, sticky='ew', columnspan=3)
            
            # Load button
            load_btn = tk.Button(invoice_frame, text=self.t("Load Invoice"), 
                                command=lambda: self.load_invoice_data_purchase(purchases_col),
                                bg='#2196F3', fg='white')
            load_btn.grid(row=0, column=4, padx=5, sticky='ew')
            
            # Delete button
            delete_btn = tk.Button(invoice_frame, text=self.t("Delete Invoice"), 
                                command=lambda: self.delete_invoice(materials_col,purchases_col, suppliers_col,"purchase"),
                                bg='red', fg='white')
            delete_btn.grid(row=0, column=5, padx=5, sticky='ew')

        # ===== Supplier SECTION =====
        # Create Supplier frame
        supplier_frame = tk.Frame(form_frame, bd=1, relief=tk.SOLID, padx=5, pady=5)
        supplier_frame.grid(row=current_row, column=0, columnspan=12, sticky='ew', pady=5)
        current_row += 1
        
        # Configure Supplier frame columns
        for i in range(12):
            supplier_frame.columnconfigure(i, weight=1 if i % 2 == 1 else 0)        

        # Create bidirectional supplier mappings
        self.supplier_code_map = {}  # name -> code
        self.code_name_map = {}      # code -> name
        self.supplier_balance_map = {}  # name -> balance

        # Populate supplier data
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
        tk.Label(supplier_frame, text=self.t("Supplier Name"), 
                font=("Arial", 10, "bold")).grid(row=0, column=0, sticky='w')
        self.supplier_name_var = tk.StringVar()
        self.supplier_name_cb = ttk.Combobox(supplier_frame, 
                                            textvariable=self.supplier_name_var, 
                                            values=sorted(all_suppliers))
        self.supplier_name_cb.grid(row=0, column=1, padx=5, sticky='ew')

        # Supplier Code Combobox
        tk.Label(supplier_frame, text=self.t("Supplier Code"), 
                font=("Arial", 10, "bold")).grid(row=0, column=2, sticky='w')
        self.supplier_code_var = tk.StringVar()
        self.supplier_code_cb = ttk.Combobox(supplier_frame, 
                                            textvariable=self.supplier_code_var, 
                                            values=sorted(all_codes))
        self.supplier_code_cb.grid(row=0, column=3, padx=5, sticky='ew')

        # Balance and Payment Fields
        tk.Label(supplier_frame, text=self.t("Previous Balance"), 
                font=("Arial", 10, "bold")).grid(row=0, column=4, sticky='e')
        self.previous_balance_var = tk.StringVar()
        self.previous_balance_entry = tk.Entry(supplier_frame, 
                                            textvariable=self.previous_balance_var, 
                                            state='readonly')
        self.previous_balance_entry.grid(row=0, column=5, sticky='ew', padx=5)

        tk.Label(supplier_frame, text=self.t("Paid Money"), 
                font=("Arial", 10, "bold")).grid(row=0, column=6, sticky='e')
        self.payed_cash_var = tk.DoubleVar()
        self.payed_cash_entry = tk.Entry(supplier_frame, 
                                        textvariable=self.payed_cash_var)
        self.payed_cash_entry.grid(row=0, column=7, sticky='ew', padx=5)

        # Payment Method Dropdown
        tk.Label(supplier_frame, text=self.t("Payment Method"), 
                font=("Arial", 10, "bold")).grid(row=0, column=8, sticky='e')
        self.payment_method_var = tk.StringVar()
        payment_methods = ['Cash', 'E_Wallet', 'Bank_account', 'Instapay']
        payment_cb = ttk.Combobox(supplier_frame, 
                                textvariable=self.payment_method_var, 
                                values=payment_methods, 
                                state='readonly')
        payment_cb.grid(row=0, column=9, sticky='ew', padx=5)
        payment_cb.current(0)  # Set default to Cash

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

        # Load material data
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
            messagebox.showerror(self.t("Database Error"), f"{self.t("Failed to load materials:")} {str(e)}")
            return

        # ===== ITEMS GRID SECTION =====
        # Make items grid expandable
        form_frame.grid_rowconfigure(current_row + 1, weight=1)
        
        # Invoice Items Grid - Responsive Configuration
        columns = self.get_fields_by_name("Materials_Header")
        num_columns = len(columns)
        
        # Create header frame with uniform columns
        header_frame = tk.Frame(form_frame, bg='#f0f0f0')
        header_frame.grid(row=current_row, column=0, columnspan=10, sticky='ew', pady=(20, 0))
        current_row += 1

        # Configure header columns with uniform weights
        for col_idx in range(num_columns):
            header_frame.columnconfigure(col_idx, weight=1, uniform='cols')
            tk.Label(header_frame, text=self.t(columns[col_idx]), relief='ridge', 
                    bg='#f0f0f0', anchor='w', padx=5).grid(row=0, column=col_idx, sticky='ew')

        # Scrollable Canvas with responsive sizing
        canvas_container = tk.Frame(form_frame)
        canvas_container.grid(row=current_row, column=0, columnspan=10, sticky='nsew')
        canvas_container.grid_rowconfigure(0, weight=1)
        canvas_container.grid_columnconfigure(0, weight=1)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(canvas_container, highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
        
        # Create a frame inside the canvas for the rows
        self.rows_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.rows_frame, anchor="nw", tags="inner_frame")
        
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
        self.rows_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_canvas)

        # Set initial width
        canvas.update_idletasks()
        canvas_width = canvas.winfo_width()
        if canvas_width > 1:
            canvas.itemconfig("inner_frame", width=canvas_width)

        self.entries = []


        self.add_three_rows_purchase()

        # Buttons Frame
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=10, pady=10, sticky='ew')
        
        # Configure button frame columns
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        add_btn = tk.Button(button_frame, text=self.t("➕ Add 3 More Rows"), 
                        command=self.add_three_rows_purchase, bg='#4CAF50', fg='white')
        add_btn.grid(row=0, column=0, padx=5, sticky='w')
        if add_or_update == "add":
            save_btn = tk.Button(button_frame, text=self.t("💾 Save Invoice"), 
                                command=lambda: self.save_invoice_purchase(purchases_col, suppliers_col, materials_col),
                                bg='#2196F3', fg='white')
            save_btn.grid(row=0, column=1, padx=5, sticky='e')
        else:
            self.update_purchase = True
            update_btn = tk.Button(button_frame, text=self.t("🔄 Update Invoice"), 
                                command=lambda: self.save_invoice_purchase(purchases_col, suppliers_col, materials_col),
                                bg='#FF9800', fg='white')
            update_btn.grid(row=0, column=1, padx=5, sticky='e')        
      

    def create_row_purchase(self,parent, row_number, bg_color, initial_values=None):

        # Invoice Items Grid - Responsive Configuration
        columns = self.get_fields_by_name("Materials_Header")
        num_columns = len(columns)       
        row_frame = tk.Frame(parent, bg=bg_color)
        row_frame.pack(fill=tk.X)  # Use pack with fill to ensure full width
        
        # Configure columns with uniform weights (same as header)
        for col_idx in range(num_columns):
            row_frame.columnconfigure(col_idx, weight=1, uniform='cols')
        
        row_entries = []
        row_entry_vars = []
        key_map = {
            "Material_code": "material_code",
            "Material_name": "material_name",
            "unit": "Unit",
            "Unit_Price": "Unit_price",
            "QTY": "QTY",
            "Discount_Type": "Discount_Type",
            "Discount Value": "Discount_Value",
            "Total_QTY": "Total_QTY",
            "Numbering": "numbering",
            "Total_Price": "Final_Price"
        }
        for col_idx, col in enumerate(columns):
            value = ""
            if initial_values:
                db_key = key_map.get(col, col)
                value = initial_values.get(db_key, "")
                if col == "Material_code" and (value not in self.product_codes):
                    print(f"[WARN] '{value}' not in dropdown list!")
                # Handle special cases
                if col == "Discount_Type" and not value:
                    value = "Percentage"
                elif col == "Discount Value" and not value:
                    value = 0
            if col == "Material_code":
                value = value.strip()
                var = tk.StringVar(value=value)
                # row_entry_vars.append(var)
                cb = ttk.Combobox(row_frame, textvariable=var, values=self.product_codes)
                cb.bind('<<ComboboxSelected>>', lambda e, r=row_number: self.update_material_info(r, "code"))
                cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_combobox_change_purchase(e, r, "code"))
                cb.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                value = value.strip()
                # print("\n")
                # print(value)
                # print("\n")
                cb.set(value)
                # row_entries.append(cb)
                # row_entries.append(value)
                row_entries.append(var)
            elif col == "Material_name":
                value = value.strip()
                var = tk.StringVar(value=value)
                # row_entry_vars.append(var)
                cb = ttk.Combobox(row_frame, textvariable=var, values=self.product_names)
                var = tk.StringVar(value=value)
                cb.bind('<<ComboboxSelected>>', lambda e, r=row_number: self.update_material_info(r, "name"))
                var = tk.StringVar(value=value)
                cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_combobox_change_purchase(e, r, "name"))
                var = tk.StringVar(value=value)
                cb.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                value = value.strip()
                cb.set(value)
                row_entries.append(cb)
                # row_entries.append(var)
                # row_entries.append(value)
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
                # cb.set(var)
                if value == "":
                    value = "Percentage"
                cb.set(value)
                row_entries.append(cb)
                # row_entries.append(value)
                # row_entries.append(var)
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
                entry.bind('<KeyRelease>', lambda e, r=row_number: self.calculate_totals(r))
                row_entries.append(entry)
            else:
                var = tk.StringVar(value=value)
                entry = tk.Entry(row_frame, textvariable=var)
                entry.bind('<KeyRelease>', lambda e, r=row_number: self.calculate_totals(r))
                entry.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                row_entries.append(entry)
        
        return row_entries
        #     if col == "Material_code":
        #         var = tk.StringVar(value=value)
        #         row_entry_vars.append(vars)
        #         var = tk.StringVar(value=value)
        #         print(1111111111111)
        #         cb = ttk.Combobox(row_frame, textvariable=var, values=self.product_codes)
        #         cb.bind('<<ComboboxSelected>>', lambda e, r=row_number: self.update_material_info(r, "code"))
        #         cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_combobox_change_purchase(e, r, "code"))
        #         cb.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
        #         row_entries.append(cb)
        #         value = value.strip()
        #         cb.set(value)
        #         row_entries.append(vars)
        #     elif col == "Material_name":
        #         var = tk.StringVar(value=value)
        #         row_entry_vars.append(vars)
        #         cb = ttk.Combobox(row_frame, textvariable=var, values=self.product_names)
        #         cb.bind('<<ComboboxSelected>>', lambda e, r=row_number: self.update_material_info(r, "name"))
        #         cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_combobox_change_purchase(e, r, "name"))
        #         cb.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
        #         row_entries.append(cb)
        #         value = value.strip()
        #         cb.set(value)
        #         row_entries.append(var)
        #     elif col == "unit":
        #         var = tk.StringVar()
        #         cb = ttk.Combobox(row_frame, textvariable=var, values=[])
        #         cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_unit_change(e, r))
        #         cb.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
        #         row_entries.append(cb)
        #     elif col == "Discount Type":
        #         var = tk.StringVar()
        #         cb = ttk.Combobox(row_frame, textvariable=var, 
        #                         values=["Percentage", "Value"], 
        #                         state="readonly")
        #         cb.current(0)
        #         cb.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
        #         row_entries.append(cb)
        #     elif col == "Discount Value":
        #         var = tk.StringVar()
        #         entry = tk.Entry(row_frame, textvariable=var)
        #         entry.bind('<KeyRelease>', lambda e, r=row_number: self.calculate_totals(r))
        #         entry.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
        #         row_entries.append(entry)
        #     elif col in ["Unit_Price", "Total_QTY", "Total_Price"]:
        #         entry = tk.Entry(row_frame, relief='flat', state='readonly')
        #         entry.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
        #         row_entries.append(entry)
        #     else:
        #         entry = tk.Entry(row_frame, relief='sunken')
        #         entry.bind('<KeyRelease>', lambda e, r=row_number: self.calculate_totals(r))
        #         entry.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
        #         row_entries.append(entry)
        
        # return row_entries
    
    def new_production_order(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Initialize mappings
        self.material_code_map = {}  # code -> {name, stock}
        self.material_name_map = {}  # name -> {code, stock}
        self.product_code_map = {}   # code -> {name, stock}
        self.product_name_map = {}   # name -> {code, stock}

        # Create top bar
        self.topbar(show_back_button=True)

        # Database collections
        materials_col = self.get_collection_by_name("Materials")
        products_col = self.get_collection_by_name("Products")
        production_col = self.get_collection_by_name("Production")

        # Load material data
        for mat in materials_col.find():
            code = mat.get('material_code', '')
            name = mat.get('material_name', '')
            stock = mat.get('stock_quantity', 0)
            self.material_code_map[code] = {'name': name, 'stock_quantity': stock}
            self.material_name_map[name] = {'code': code, 'stock_quantity': stock}

        # Load product data
        for prod in products_col.find():
            code = prod.get('product_code', '')
            name = prod.get('product_name', '')
            stock = prod.get('stock_quantity', 0)
            self.product_code_map[code] = {'name': name, 'stock_quantity': stock}
            self.product_name_map[name] = {'code': code, 'stock_quantity': stock}

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
                    text=self.t(columns[col_idx]),
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
        self.rows_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.rows_frame, anchor="nw", tags="inner_frame")
        
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
        self.rows_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_canvas)

        # Set initial width
        canvas.update_idletasks()
        canvas_width = canvas.winfo_width()
        if canvas_width > 1:
            canvas.itemconfig("inner_frame", width=canvas_width)

        self.production_entries = []

        # Create initial rows
        for _ in range(1):
            self.add_production_row()

        # Control buttons
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=num_columns, pady=10, sticky='ew')
        
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        tk.Button(button_frame, text=self.t("➕ Add Row"),
                command=self.add_production_row,
                bg='#4CAF50', fg='white').grid(row=0, column=0, padx=5, sticky='w')
        tk.Button(button_frame, text=self.t("💾 Save Order"),
                command=self.save_production_order,
                bg='#2196F3', fg='white').grid(row=0, column=1, padx=5, sticky='e')
        
        self.update_combobox_values()

    def add_production_row(self):
        row_idx = len(self.production_entries)
        row_frame = tk.Frame(self.rows_frame, bg='white' if row_idx % 2 == 0 else '#f0f0f0')
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
        
        self.production_entries.append(entries)
        self.update_combobox_values()

    def update_combobox_values(self):
        material_codes = list(self.material_code_map.keys())
        material_names = list(self.material_name_map.keys())
        product_codes = list(self.product_code_map.keys())
        product_names = list(self.product_name_map.keys())
        
        for row in self.production_entries:
            row[0]['values'] = material_codes
            row[1]['values'] = material_names
            row[4]['values'] = product_codes
            row[5]['values'] = product_names

    def update_material_code(self, row_idx):
        code = self.production_entries[row_idx][0].get()
        if code in self.material_code_map:
            material = self.material_code_map[code]
            self.production_entries[row_idx][1].set(material['name'])
            self.production_entries[row_idx][2].config(state='normal')
            self.production_entries[row_idx][2].delete(0, tk.END)
            self.production_entries[row_idx][2].insert(0, str(material['stock_quantity']))
            self.production_entries[row_idx][2].config(state='readonly')

    def update_material_name(self, row_idx):
        name = self.production_entries[row_idx][1].get()
        if name in self.material_name_map:
            material = self.material_name_map[name]
            self.production_entries[row_idx][0].set(material['code'])
            self.production_entries[row_idx][2].config(state='normal')
            self.production_entries[row_idx][2].delete(0, tk.END)
            self.production_entries[row_idx][2].insert(0, str(material['stock_quantity']))
            self.production_entries[row_idx][2].config(state='readonly')

    def update_product_code(self, row_idx):
        code = self.production_entries[row_idx][4].get()
        if code in self.product_code_map:
            product = self.product_code_map[code]
            self.production_entries[row_idx][5].set(product['name'])
            self.production_entries[row_idx][6].config(state='normal')
            self.production_entries[row_idx][6].delete(0, tk.END)
            self.production_entries[row_idx][6].insert(0, str(product['stock_quantity']))
            self.production_entries[row_idx][6].config(state='readonly')

    def update_product_name(self, row_idx):
        name = self.production_entries[row_idx][5].get()
        if name in self.product_name_map:
            product = self.product_name_map[name]
            self.production_entries[row_idx][4].set(product['code'])
            self.production_entries[row_idx][6].config(state='normal')
            self.production_entries[row_idx][6].delete(0, tk.END)
            self.production_entries[row_idx][6].insert(0, str(product['stock_quantity']))
            self.production_entries[row_idx][6].config(state='readonly')

    def save_production_order(self):
        production_col = self.get_collection_by_name("Production")
        materials_col = self.get_collection_by_name("Materials")
        products_col = self.get_collection_by_name("Products")
        
        try:
            orders = []
            for idx, row in enumerate(self.production_entries):
                # Validate data
                try:
                    material_code = row[0].get()
                    material_qty = float(row[3].get())
                    product_code = row[4].get()
                    product_qty = float(row[7].get())
                    waste = float(row[8].get())
                except ValueError:
                    messagebox.showerror(self.t("Error"), f"{self.t("Invalid values in row")} {idx+1}")
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
            
            messagebox.showinfo(self.t("Success"), self.t("Production order saved successfully"))
            self.new_production_order(None)  # Refresh form

        except PyMongoError as e:
            messagebox.showerror(self.t("Database Error"), f"{self.t("Operation failed:")} {str(e)}")

    def update_inventory(self):
        # Update material and product stocks
        try:
            for row in self.production_entries:
                material_code = row[0].get()
                material_qty = float(row[3].get() or 0)
                
                product_code = row[4].get()
                product_qty = float(row[7].get() or 0)
                
                # Update material stock
                if material_code:
                    self.db.materials.update_one(
                        {'code': material_code},
                        {'$inc': {'stock_quantity': -material_qty}}
                    )

                # Update product stock
                if product_code:
                    self.db.products.update_one(
                        {'code': product_code},
                        {'$inc': {'stock_quantity': product_qty}}
                    )
                    
        except PyMongoError as e:
            messagebox.showerror(self.t("Inventory Error"), 
                f"{self.t("Failed to update inventory:")} {str(e)}")
###########################################################################
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
            self.update_material_info(row_idx, field_type)

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
              
                product_code = self.entries[row_idx][0]
                print("\n")
                print(product_code)
                print("\n")
                product_code = product_code.get().strip()
                product_info = self.product_map.get(product_code, {})
                product_name = product_info.get('name', '')
            else:
                print(2)
                product_name = self.entries[row_idx][1].get().strip()
                product_code = self.name_to_code.get(product_name, '')
                product_info = self.product_map.get(product_code, {})

            # Clear fields if no product found
            if not product_code:
                self.clear_row_fields(row_idx)
                print(3)
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
            # self.entries[row_idx][8].config(state='readonly')
            
            self.calculate_totals(row_idx)
        except Exception as e:
            messagebox.showerror(self.t("Update Error"), f"{self.t("Failed to update product info:")} {str(e)}")
            self.clear_row_fields(row_idx)
            
    def update_material_info(self, row_idx, source):
        """Update fields based on code or name selection"""
        try:
            material_code = self.entries[row_idx][0]
            print("1")
            if source == "code":
                ########### Print the type:
                print("\n")
                print("material_code entry:", material_code)
                print("type:", type(material_code))
                print("\n")
                
                ######## Check for index error:
                if row_idx >= len(self.entries):
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
            self.entries[row_idx][1].delete(0, tk.END)
            self.entries[row_idx][1].insert(0, material_name)

            
            # Update unit combobox values (index 2)
            unit_combobox = self.entries[row_idx][2]
            unit_combobox['values'] = material_info.get('units', [])
            if material_info.get('units'):
                unit_combobox.current(0)
            
            # Update Unit Price (index 8)
            self.entries[row_idx][8].config(state='normal')
            self.entries[row_idx][8].delete(0, tk.END)
            self.entries[row_idx][8].insert(0, f"{material_info.get('price', 0):.2f}")
            # self.entries[row_idx][8].config(state='readonly')
            
            self.calculate_totals(row_idx)
        except Exception as e:
            messagebox.showerror(self.t("Update Error"), f"{self.t("Failed to update Material info:")} {str(e)}")
            self.clear_row_fields(row_idx)

    def calculate_totals(self, row_idx):
        try:
            # Get values using correct column indices
            numbering = float(self.entries[row_idx][3].get() or 0)  # index 3
            qty = float(self.entries[row_idx][4].get() or 0)        # index 4
            x = self.entries[row_idx][4]
            y= float(self.entries[row_idx][4].get())
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
                messagebox.showerror(self.t("Discount Error"), str(e))
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
    
    def new_sales(self,user_role):
        self.table_name.set("Sales")
        for widget in self.root.winfo_children():
            widget.destroy()

        self.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.display_general_table(self.sales_collection, "Sales")

    def new_purchases(self,user_role):
        self.table_name.set("Purchases")
        for widget in self.root.winfo_children():
            widget.destroy()

        self.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.display_general_table(self.purchases_collection, "Purchases")
    
    def new_customer_payment(self,user_role):
        self.table_name.set("Customer_Payments")
        for widget in self.root.winfo_children():
            widget.destroy()
    
        self.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.display_general_table(self.customer_payments, "Customer_Payments")
    
    def new_supplier_payment(self,user_role):
        self.table_name.set("Supplier_Payments")
        for widget in self.root.winfo_children():
            widget.destroy()
    
        self.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.display_general_table(self.supplier_payments, "Supplier_Payments")
    
    def new_emp_salary(self,user_role):
        self.table_name.set("Employee_Salary")
        for widget in self.root.winfo_children():
            widget.destroy()

        self.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.display_general_table(self.employee_salary_collection, "Employee_Salary")
    
    def new_emp_appointment(self,user_role):
        self.table_name.set("Employee_appointimets")
        for widget in self.root.winfo_children():
            widget.destroy()
    
        self.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.display_general_table(self.employees_appointments_collection, "Employee_appointimets")
    
    def new_emp_withdrawal(self,user_role):
        self.table_name.set("Employee_withdrawls")
        for widget in self.root.winfo_children():
            widget.destroy()
    
        self.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.display_general_table(self.employee_withdrawls_collection, "Employee_withdrawls")
    
    def new_production(self,user_role):
        self.table_name.set("Production")
        for widget in self.root.winfo_children():
            widget.destroy()

        self.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.display_general_table(self.production_collection, "Production")

    def new_general_exp(self,user_role):
        self.table_name.set("general_exp_rev")
        for widget in self.root.winfo_children():
            widget.destroy()

        self.topbar(show_back_button=True,Back_to_Database_Window=True)
        self.display_general_table(self.general_exp_rev_collection, "general_exp_rev")

    def supplier_interactions(self, user_role):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.topbar(show_back_button=True, Back_to_Database_Window=False)
        
        self.supplier_collection = self.get_collection_by_name("Suppliers")
        self.supplier_payment_collection = self.get_collection_by_name("Supplier_Payments")
        self.purchases_collection = self.get_collection_by_name("Purchases")

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
        tk.Label(left_frame, text=self.t("Cash"), font=("Arial", 12)).pack(pady=10, anchor="w", padx=10)
        self.cash_entry = tk.Entry(left_frame, font=("Arial", 12))
        self.cash_entry.pack(pady=5, padx=10, fill="x")

        tk.Label(left_frame, text=self.t("Payment Method"), font=("Arial", 12)).pack(pady=10, anchor="w", padx=10)
        selected_method = tk.StringVar()
        self.payment_entry = ttk.Combobox(left_frame, textvariable=selected_method, 
                                        values=['Cash', 'E_Wallet', 'Bank_account', 'Instapay'], 
                                        state="readonly", width=18)
        self.payment_entry.pack(pady=5, padx=10, fill="x")
        self.payment_entry.set("Cash")  

        add_btn = tk.Button(left_frame, text=self.t("Add Entry"), width=35, 
                           command=lambda: self.add_supplier_payment(tree))
        add_btn.pack(pady=20, padx=10)

        # Right part (table)
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="left", fill="both", expand=True)

        # ==== Drop-down Section ====
        tk.Label(right_frame, text=self.t("Supplier Code")).grid(row=0, column=4)
        self.supplier_code_cb = ttk.Combobox(right_frame, values=supplier_codes)
        self.supplier_code_cb.grid(padx=(10,20), row=1, column=4)

        tk.Label(right_frame, text=self.t("Supplier Name")).grid(padx=(10,20), row=0, column=5)
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

        tk.Label(right_frame, text=self.t("Start Date")).grid(padx=(10,20), row=0, column=7)
        self.start_date_entry = DateEntry(right_frame, font=("Arial", 12), date_pattern='dd-MM-yyyy', width=14)
        self.start_date_entry.grid(padx=(10,20), row=1, column=7)
        self.start_date_entry.set_date(date(2022, 1, 1))

        tk.Label(right_frame, text=self.t("End Date")).grid(padx=(10,20), row=0, column=8)
        self.end_date_entry = DateEntry(right_frame, font=("Arial", 12), date_pattern='dd-MM-yyyy', width=14)
        self.end_date_entry.grid(padx=(10,20), row=1, column=8)
        # self.end_date_entry.set_date(date(2025, 7, 7))
        self.end_date_entry.set_date(date.today())

        search_btn = tk.Button(
            right_frame,
            text=self.t("Search"),
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
            tree.heading(col, text=self.t(col))
            # tree.heading(col, text=col.capitalize())
            tree.column(col, width=150)

        # ==== Footer Totals ====
        tk.Label(right_frame, text=self.t("Total Debit")).grid(row=13, column=3, sticky="e")
        self.total_debit_entry = tk.Entry(right_frame)
        self.total_debit_entry.grid(row=13, column=4, sticky="w")

        tk.Label(right_frame, text=self.t("Total Credit")).grid(row=13, column=5, sticky="e")
        self.total_credit_entry = tk.Entry(right_frame)
        self.total_credit_entry.grid(row=13, column=6, sticky="w")

        tk.Label(right_frame, text=self.t("Balance")).grid(row=13, column=7, sticky="e")
        self.balance_entry = tk.Entry(right_frame)
        self.balance_entry.grid(row=13, column=8, sticky="w")

        # Initial update with empty query
        self.update_totals(self.purchases_collection, self.supplier_payment_collection, tree=tree)

    def add_supplier_payment(self, tree):
        debit = self.cash_entry.get().strip()
        payment_method = self.payment_entry.get().strip()
        supplier_code = self.supplier_code_cb.get().strip()
        supplier_name = self.supplier_name_cb.get().strip()
        supplier_payment_collection = self.get_collection_by_name("Supplier_Payments")
        purchases_collection = self.get_collection_by_name("Purchases")
        
        if not debit or not payment_method or not supplier_code or not supplier_name:
            messagebox.showerror(self.t("Error"), self.t("All fields must be filled!"))
            return

        try:
            debit_val = float(debit)
        except ValueError:
            messagebox.showerror(self.t("Error"), self.t("Cash must be a valid number."))
            return

        operation_number = self.get_next_operation_number(supplier_payment_collection)
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

        # self.supplier_collection = self.get_collection_by_name("Suppliers")
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
            collection=self.get_collection_by_name("Suppliers"),
            invoices_collection=purchases_collection,
            payment_collection=supplier_payment_collection,
            field_path="supplier_info.code",
            tree=tree
        )

        messagebox.showinfo(self.t("Success"), f"{self.t("Entry")} {operation_number} {self.t("added.")}")

    def get_next_operation_number(self, payment_collection):
        last_entry = payment_collection.find_one(
            {"Operation_Number": {"$regex": r"^PM-?\d+"}},
            sort=[("Operation_Number", -1)]
        )
        if last_entry and "Operation_Number" in last_entry:
            last_num = int(last_entry["Operation_Number"].split("-")[1])
            return f"PM-{last_num+1:05d}"
        return "PM-00001"

    def get_next_code(self, payment_collection):
        last_entry = payment_collection.find_one(
            {"code": {"$regex": r"^GEN-?\d+"}},
            sort=[("code", -1)]
        )
        if last_entry and "code" in last_entry:
            last_num = int(last_entry["code"].split("-")[1])
            return f"GEN-{last_num+1:05d}"
        return "GEN-00001"

    def get_next_prim_key(self, collection, collection_name):
        primary_key_field = PRIMARY_KEYS.get(collection_name)
        prefix = PRIMARY_KEY_STARTERS.get(collection_name)

        # Find the last document sorted by primary key descending
        last_entry = collection.find_one(
            {primary_key_field: {"$regex": rf"^{prefix}-?\d+"}},
            sort=[(primary_key_field, -1)]
        )

        if last_entry and primary_key_field in last_entry:
            raw_value = last_entry[primary_key_field]
            number_part = ''.join(filter(str.isdigit, raw_value))
            next_number = int(number_part) + 1 if number_part else 1
        else:
            next_number = 1

        padded_number = f"{next_number:05d}" if prefix in ["PM", "GEN", "INV", "PR"] else f"{next_number:03d}"

        return f"{prefix}-{padded_number}"

    def add_customer_payment(self, tree):
        credit = self.cash_entry.get().strip()
        payment_method = self.payment_entry.get().strip()
        customer_code = self.customer_code_cb.get().strip()
        customer_name = self.customer_name_cb.get().strip()
        customer_payment_collection = self.get_collection_by_name("Customer_Payments")
        sales_collection = self.get_collection_by_name("Sales")
        
        if not credit or not payment_method or not customer_code or not customer_name:
            messagebox.showerror(self.t("Error"), self.t("All fields must be filled!"))
            return

        try:
            credit_val = float(credit)
        except ValueError:
            messagebox.showerror(self.t("Error"), self.t("Cash must be a valid number."))
            return

        operation_number = self.get_next_operation_number(customer_payment_collection)
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
            collection=self.get_collection_by_name("Customers"),
            invoices_collection=sales_collection,
            payment_collection=customer_payment_collection,
            field_path="Customer_info.code",
            tree=tree
        )

        messagebox.showinfo(self.t("Success"), f"{self.t("Entry")} {operation_number} {self.t("added.")}")
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
                messagebox.showerror(self.t("Database Error"), f"{self.t("Failed to process code:")} {selected_code}.\n{self.t("Error")}: {str(e)}")
        self.update_totals(invoices_collection, payment_collection, payment_query, invoice_query, tree, selected_code)

    def on_name_selected(self, event, code_cb, name_cb, collection, invoices_collection, payment_collection, field_path, tree):
        selected_name = name_cb.get().strip()
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
                messagebox.showwarning(self.t("Warning"), f"{self.t("No matching code found for name:")} {selected_name}")
        except Exception as e:
            messagebox.showerror(self.t("Database Error"), f"{self.t("Failed to fetch code for")} {selected_name}.\n{self.t("Error")}: {str(e)}")

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
                    tree.insert("", tk.END, values=(formatted, "Other", new_debit, new_credit, "Cash"))
                
                if tree:
                    # tree.delete(*tree.get_children())
                    for row in sample_data:
                        tree.insert("", tk.END, values=row)

    def customer_interactions(self, user_role):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.topbar(show_back_button=True,Back_to_Database_Window=False)
        
        self.customer_collection         = self.get_collection_by_name("Customers")
        self.customer_payment_collection = self.get_collection_by_name("Customer_Payments")
        self.sales_collection            = self.get_collection_by_name("Sales")

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
        tk.Label(left_frame, text=self.t("Cash"), font=("Arial", 12)).pack(pady=10, anchor="w", padx=10)
        self.cash_entry = tk.Entry(left_frame, font=("Arial", 12))
        self.cash_entry.pack(pady=5, padx=10, fill="x")

        tk.Label(left_frame, text=self.t("Payment Method"), font=("Arial", 12)).pack(pady=10, anchor="w", padx=10)
        selected_method = tk.StringVar()
        self.payment_entry = ttk.Combobox(left_frame, textvariable=selected_method, values=['Cash', 'E_Wallet', 'Bank_account', 'Instapay'], state="readonly", width=18)
        self.payment_entry.pack(pady=5, padx=10, fill="x")
        self.payment_entry.set(self.t("Cash"))  

        add_btn = tk.Button(left_frame, text=self.t("Add Entry"), width=35, command=lambda: self.add_customer_payment(tree))
        add_btn.pack(pady=20 , padx=10)

        #Right part (table)
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="left", fill="both", expand=True)

        # ==== Drop-down Section ====
        tk.Label(right_frame, text=self.t("Customer Code")).grid(padx=(10,20), row=0, column=4)
        self.customer_code_cb = ttk.Combobox(right_frame, values=customer_codes)
        self.customer_code_cb.grid(padx=(10,20), row=1, column=4)

        tk.Label(right_frame, text=self.t("Customer Name")).grid(padx=(10,20), row=0, column=5)
        self.customer_name_cb = ttk.Combobox(right_frame, values=customer_names)
        self.customer_name_cb.grid(padx=(10,20), row=1, column=5)

        self.customer_code_cb.bind("<<ComboboxSelected>>", lambda event: self.on_code_selected(event, self.customer_code_cb, self.customer_name_cb, self.customer_collection, self.sales_collection, self.customer_payment_collection, "Customer_info.code", tree))
        self.customer_name_cb.bind("<<ComboboxSelected>>", lambda event: self.on_name_selected(event, self.customer_code_cb, self.customer_name_cb, self.customer_collection, self.sales_collection, self.customer_payment_collection, "Customer_info.code", tree))
        
        tk.Label(right_frame, text=self.t("Start Date")).grid(padx=(10,20), row=0, column=7)
        self.start_date_entry = DateEntry(right_frame, font=("Arial", 12), date_pattern='dd-MM-yyyy', width=14)
        self.start_date_entry.grid(padx=(10,20), row=1, column=7)
        self.start_date_entry.set_date(date(2022, 1, 1))

        tk.Label(right_frame, text=self.t("End Date")).grid(padx=(10,20), row=0, column=8)
        self.end_date_entry = DateEntry(right_frame, font=("Arial", 12), date_pattern='dd-MM-yyyy', width=14)
        self.end_date_entry.grid(padx=(10,20), row=1, column=8)
        # self.end_date_entry.set_date(date(2025, 7, 7))
        self.end_date_entry.set_date(date.today())
        
        search_btn = tk.Button(
            right_frame,
            text=self.t("Search"),
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
        tree = ttk.Treeview(tree_container, columns=self.t(columns), show="headings", height=8, yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)

        # Configure scrollbar to control tree
        scrollbar.config(command=tree.yview)
        
        for col in columns:
            tree.heading(col, text=self.t(col))
            # tree.heading(col, text=col.capitalize())
            tree.column(col, width=150)

        # ==== Footer Totals ====
        tk.Label(right_frame, text=self.t("Total Debit")).grid(row=13, column=3, sticky="e")
        self.total_debit_entry = tk.Entry(right_frame)
        self.total_debit_entry.grid(row=13, column=4, sticky="w")

        tk.Label(right_frame, text=self.t("Total Credit")).grid(row=13, column=5, sticky="e")
        self.total_credit_entry = tk.Entry(right_frame)
        self.total_credit_entry.grid(row=13, column=6, sticky="w")

        tk.Label(right_frame, text=self.t("Balance")).grid(row=13, column=7, sticky="e")
        self.balance_entry = tk.Entry(right_frame)
        self.balance_entry.grid(row=13, column=8, sticky="w")

        # Initial update with empty query
        self.update_totals(self.sales_collection, self.customer_payment_collection, tree=tree)

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
            messagebox.showerror(self.t("Error"), f"{self.t("Error displaying data:")}\n{e}")

    def display_general_table(self, current_collection, collection_name):
        
        if self.language == "Arabic":
            alignment = "e"
            label_col = 1
            entry_col = 0
        else:
            alignment = "w"
            label_col = 0
            entry_col = 1
        
        img_label= None
        columns = self.get_fields_by_name(collection_name)
        
        normal_fields = [label for label in columns if label != "Id" and "pic" not in label.lower()]
        pic_fields = [label for label in columns if "pic" in label.lower()]
        ordered_fields = normal_fields + pic_fields

        main_frame = tk.Frame(root, padx=20, pady=50)
        main_frame.pack(fill="both", expand=True)

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

        if 'Customer_info' in ordered_fields:
            ordered_fields.remove('Customer_info')
            if 'customer_code' not in ordered_fields:
                ordered_fields.append('customer_code')
            if 'customer_name' not in ordered_fields:
                ordered_fields.append('customer_name')
        if 'supplier_info' in ordered_fields:
            ordered_fields.remove('supplier_info')
            if 'supplier_code' not in ordered_fields:
                ordered_fields.append('supplier_code')
            if 'supplier_name' not in ordered_fields:
                ordered_fields.append('supplier_name')

        self.entries = {}
        row_index = 0

        for label in ordered_fields:
            if label in ["Id", "Operation_Number", "Customer_info", "supplier_info", "Time"]:
                continue
            elif label in ["code"] and collection_name == "general_exp_rev":
                continue
            
            #anchor="e" → aligns text to the right within the label ... "w" alternative
            # justify="right" → right-justifies multi-line text
            # sticky="e" → aligns the label to the right of the grid cell
            if label in MANDATORTY_FIELDS and collection_name in MANDATORY_DBS:
                if self.language == "English":
                    tk.Label(form_frame, text=f"{self.t(label)}⭐", font=("Arial", 12), anchor=alignment).grid(row=row_index, column=label_col, sticky=alignment, pady=5, padx=2)
                else:
                    tk.Label(form_frame, text=f"⭐{self.t(label)}", font=("Arial", 12), anchor=alignment).grid(row=row_index, column=label_col, sticky=alignment, pady=5, padx=2)
            else:
                tk.Label(form_frame, text=f"{self.t(label)}", font=("Arial", 12), anchor=alignment).grid(row=row_index, column=label_col, sticky=alignment, pady=5, padx=2)

            if "date" in label.lower() or "timestamp" in label.lower() or "check_out" in label.lower() or "check_in" in label.lower():
                entry = DateEntry(form_frame, font=("Arial", 12), date_pattern='dd-MM-yyyy', width=18)
                entry.grid(row=row_index, column=entry_col, pady=5)
                self.entries[label] = entry
                row_index += 1

            elif "payment_method" in label.lower():
                selected_method = tk.StringVar()
                dropdown = ttk.Combobox(form_frame, textvariable=selected_method, values=['Cash', 'E_Wallet', 'Bank_account', 'Instapay'], state="readonly", width=27)
                dropdown.grid(row=row_index, column=entry_col, pady=5)
                dropdown.set("Cash")
                self.entries[label] = dropdown
                row_index += 1

            elif "pic" in label.lower():
                frame = tk.Frame(form_frame)
                frame.grid(row=row_index, column=entry_col, pady=5)
                
                # Image Label in a *new row* below the current field
                img_label = tk.Label(form_frame)
                img_label.grid(row=row_index + 1, column=0, columnspan=3, pady=5)

                def browse_file(e=entry, img_lbl=img_label):  # Pass the current entry as argument
                    filepath = filedialog.askopenfilename(
                        title="Select a file",
                        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All files", "*.*")]
                    )
                    if filepath:
                        load_image_preview(filepath, img_lbl)

                browse_btn = tk.Button(frame, text=self.t("Browse"),width=25, command=lambda e=entry: browse_file(e))
                browse_btn.pack(side="left", padx=5)
                self.entries[label] = img_label

            elif "pdf_path" in label.lower():
                frame = tk.Frame(form_frame)
                frame.grid(row=row_index, column=entry_col, pady=5)

                file_label = tk.Label(form_frame, text="No file selected", anchor="w")
                file_label.grid(row=row_index + 1, column=0, columnspan=3, pady=5)

                def browse_file(lbl=file_label):
                    filepath = filedialog.askopenfilename(
                        title="Select a file",
                        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
                    )
                    if filepath:
                        filename = filepath.split("/")[-1]
                        lbl.config(text=f"Selected: {filename}")
                        lbl.filepath = filepath

                browse_btn = tk.Button(frame, text=self.t("Browse"), width=25, command=browse_file)
                browse_btn.pack(side="left", padx=5)

                self.entries[label] = file_label
                row_index += 2  # Skip a row for the file label

            else:
                entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
                entry.grid(row=row_index, column=entry_col, pady=5)
                self.entries[label] = entry
                if label in ZEROED_FIELDS:
                    entry.insert(0, "0")
                elif label == PRIMARY_KEYS.get(collection_name):
                    prim_key_val = self.get_next_prim_key(current_collection, collection_name)
                    entry.insert(0,prim_key_val)
                row_index += 1


        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True)

        search_frame = tk.Frame(right_frame)
        search_frame.pack(fill="x", pady=(0, 10))

        self.selected_field = tk.StringVar()
        

        if self.language =="Arabic":
            self.selected_field.set(self.t(ordered_fields[0]))
            translated_columns = [self.t(col) for col in ordered_fields]
        else: 
            self.selected_field.set((ordered_fields[0]))
            translated_columns = ordered_fields
        
        field_dropdown = ttk.Combobox(search_frame, textvariable=self.selected_field, values=translated_columns, width=20)
        field_dropdown.pack(side="left", padx=(0, 5))

        local_search_query = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=local_search_query)
        search_entry.pack(side="left", padx=(0, 5))

        table_frame = tk.Frame(right_frame)
        table_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(table_frame, columns=ordered_fields, show="headings")
        for col in ordered_fields:
            tree.heading(col, text=self.t(col))
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
            width=14,
            command=lambda: self.refresh_generic_table(tree, current_collection, collection_name, local_search_query.get())
        ).pack(side="left")
        
        # Bottom buttons
        self.root.configure(bg="#f0f0f0")  # Set background color for the root window
        button_frame = tk.LabelFrame(root, text="Actions", padx=10, pady=10, font=("Arial", 12, 'bold'))
        button_frame.pack(pady=10)

        btn_add = tk.Button(button_frame, text=self.t("Add Entry"), font=("Arial", 12), width=15, command=lambda: self.add_generic_entry(tree, current_collection,collection_name))
        btn_edit = tk.Button(button_frame, text=self.t("Update Entry"), font=("Arial", 12), width=15, command=lambda: self.edit_generic_entry(tree, current_collection,collection_name))
        btn_delete = tk.Button(button_frame, text=self.t("Delete Entry"), font=("Arial", 12), width=15, command=lambda: self.delete_generic_entry(tree, current_collection))
        btn_deselect = tk.Button(button_frame, text=self.t("Deselect Entry"), font=("Arial", 12), width=15, command=lambda:self.deselect_entry(tree))

        btn_add.grid(row=0, column=0, padx=10)
        btn_edit.grid(row=0, column=1, padx=10)
        btn_delete.grid(row=0, column=2, padx=10)
        btn_deselect.grid(row=0, column=3, padx=10)

        # Load initial table content
        self.refresh_generic_table(tree, current_collection, collection_name, search_text="")
        # self.root.configure(bg=COLORS["background"])

    def on_tree_selection(self, event, tree, columns, collection_name, img_label):
        first_document = None
        current_collection = None
        id_index = 0
        selected_item = tree.selection()
        if not selected_item:
            for field, entry in self.entries.items():
                if isinstance(entry, ttk.Combobox):
                    entry.set('')
                elif isinstance(entry, DateEntry):
                    entry.set_date(datetime.now())
                elif "pdf_path" in field.lower():
                    entry.config(text="")
                elif hasattr(entry, 'image') and img_label:
                    img_label.config(image='')
                    img_label.image = None
                else:
                    entry.delete(0, tk.END)
            
            if(img_label):
                img_label.config(image="")
                img_label.image = None
            return
        try:
            lower_columns = [col.lower() for col in columns]
            if "id" in lower_columns:
                id_index = columns.index("Id")  # Dynamically get the index of "Id" #TODO need something different to loop on
            elif any(('code' in col) or ('receipt_number' in col) for col in lower_columns):
                for idx, col in enumerate(lower_columns):
                    if 'code' in col or 'receipt_number' in col:
                        id_index = idx
                        break
            unique_id = tree.item(selected_item)['values'][id_index]

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
            if field in field_mapping: 
                parent, child = field_mapping[field]
                value = first_document.get(parent, {}).get(child, "")
            else:
                value = first_document.get(field, "")
            
            items = first_document.get("Items", [])
            
            if isinstance(entry, ttk.Combobox):
                if value == '':
                    value = first_document.get(child, "")
                entry.set(value)

            if isinstance(value, datetime):
                value = value.strftime('%d-%m-%Y')
                entry.delete(0, tk.END)
                entry.insert(0, value)
            elif field in ['product_name', 'Product_code', 'Unit', 'QTY', 'numbering',
                    'Total_QTY', 'Unit_price', 'Discount_Type', 'Discount_Value', 'Final_Price'] \
                    and collection_name == "Sales":

                if isinstance(items, list):
                    values = [str(item.get(field, '')) for item in items]
                    value = ', '.join(values)
                else:
                    value = ''
                entry.delete(0, tk.END)
                entry.insert(0, value)
            elif field in ['material_name', 'material_code', 'Unit', 'QTY', 'numbering',
                    'Total_QTY', 'Unit_price', 'Discount_Type', 'Discount_Value', 'Final_Price'] \
                    and collection_name == "Purchases":

                if isinstance(items, list):
                    values = [str(item.get(field, '')) for item in items]
                    value = ', '.join(values)
                else:
                    value = ''
                entry.delete(0, tk.END)
                entry.insert(0, value)
            elif field == "Units" and isinstance(value, list):
                value_str = ' , '.join(map(str, value))
                entry.delete(0, tk.END)
                entry.insert(0, value_str)
            # If it's a pic field, load preview
            elif "pic" in field.lower():
                if img_label and value:
                    load_image_preview_from_url(value, img_label)
            elif "pdf_path" in field.lower():
                empty = 0 #dummy code
            else:
                entry.delete(0, tk.END)
                entry.insert(0, value)

    def refresh_generic_table(self, tree, current_collection, collection_name, search_text):
        try:
            # Clear existing rows
            for row in tree.get_children():
                tree.delete(row)

            if search_text:
                # raw_selected_field = self.selected_field.get()
                if self.language == "Arabic":
                    raw_selected_field = self.show_original()
                else: 
                    raw_selected_field = self.selected_field.get()
                
                mogno_selected_field = self.get_mongo_field_path(raw_selected_field)
                first_document = current_collection.find_one()
                
                if first_document:
                    search_fields = self.get_fields_by_name(collection_name)
                    
                    if "Items." in mogno_selected_field:
                        field_inside_items = mogno_selected_field.split(".")[1]
                        query = { "Items": { "$elemMatch": {} } }
                        
                        if field_inside_items in ['Net_total','Previous_balance','Total_balance','Payed_cash','Remaining_balance','Unit','QTY','numbering','Total_QTY','Unit_price','Discount_Value','Final_Price']:
                            query["Items"]["$elemMatch"][field_inside_items] = float(search_text)
                        else: 
                            query["Items"]["$elemMatch"][field_inside_items] = {
                                "$regex": search_text,
                                "$options": "i"
                            }
                        
                        try:
                            data = list(current_collection.find(query).sort("Id", 1))
                        except PyMongoError as e:
                            print(f"An error occurred: {e}")
                    else:
                        or_conditions = [{"$expr": {"$regexMatch": {"input": {"$toString": f"${mogno_selected_field}"}, "regex": search_text, "options": "i"}}} for field in search_fields]
                        data = list(current_collection.find({"$or": or_conditions}).sort("Id", 1))
                else:
                    data = []
            else:
                data = list(current_collection.find().sort("Id", 1))


            if data:
                columns = self.get_fields_by_name(collection_name)
                if '_id' in columns:
                    columns.remove('_id')
                if 'Customer_info' in columns:
                    columns.remove('Customer_info')
                    if 'customer_code' not in columns:
                        columns.append('customer_code')
                    if 'customer_name' not in columns:
                        columns.append('customer_name')
                if 'supplier_info' in columns:
                    columns.remove('supplier_info')
                    if 'supplier_code' not in columns:
                        columns.append('supplier_code')
                    if 'supplier_name' not in columns:
                        columns.append('supplier_name')
                        
                tree["columns"] = columns

                for col in columns:
                    tree.heading(col, text=self.t(col))
                    tree.column(col, width=152, anchor="center", stretch=False)

                
                for row_data in data:
                    units = row_data.get('Units', [])
                    items = row_data.get('Items', {})
                    
                    if(collection_name == "Customer_Payments"):
                        customer_info = row_data.get('Customer_info', {})
                        row_data['customer_code'] = customer_info.get('code', '')
                        row_data['customer_name'] = customer_info.get('name', '')
                    
                    elif(collection_name == "Supplier_Payments"):
                        customer_info = row_data.get('supplier_info', {})
                        row_data['supplier_code'] = customer_info.get('code', '')
                        row_data['supplier_name'] = customer_info.get('name', '')
                    
                    elif(collection_name in ["Sales", "Purchases"] ):
                        prefix = "Customer" if collection_name == "Sales" else "supplier"
                        info_obj = row_data.get(f'{prefix}_info', {})
                        financials = row_data.get('Financials', {})
                        
                        #start extracting Data from these objects
                        # cust_info
                        row_data[f'{prefix.lower()}_code']    = info_obj.get('code', '')
                        row_data[f'{prefix.lower()}_name']    = info_obj.get('name', '')
                        row_data[f'{prefix.lower()}_phone1']  = info_obj.get('phone1', '')
                        row_data[f'{prefix.lower()}_phone2']  = info_obj.get('phone2', '')
                        row_data[f'{prefix.lower()}_address'] = info_obj.get('address', '')
                        #financials
                        row_data['Net_total'] = financials.get('Net_total', '')
                        row_data['Previous_balance'] = financials.get('Previous_balance', '')
                        row_data['Total_balance'] = financials.get('Total_balance', '')
                        row_data['Payed_cash'] = financials.get('Payed_cash', '')
                        row_data['Remaining_balance'] = financials.get('Remaining_balance', '')
                        row_data['Payment_method'] = financials.get('Payment_method', '')

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
                    elif isinstance(items, list) and len(items) > 0 and collection_name in ["Sales", "Purchases"]:
                        prefix = "Customer" if collection_name == "Sales" else "supplier"
                        keys = []
                        if prefix == "Customer":
                            keys = ['Product_code', 'product_name', 'Unit', 'QTY', 'numbering', \
                                    'Total_QTY', 'Unit_price', 'Discount_Type', 'Discount_Value', 'Final_Price'] 
                        else:
                            keys = ['material_code', 'material_name', 'Unit', 'QTY', 'numbering', \
                                    'Total_QTY', 'Unit_price', 'Discount_Type', 'Discount_Value', 'Final_Price'] 
                        for item in items:
                            values = []
    
                            for key in keys:
                                row_data[key] = item.get(key, '')

                            for col in columns:
                                value = row_data.get(col,'')
                                
                                values.append(value)

                            tree.insert("", "end", values=values)
                    else:
                        # Fallback to insert normally if Units is not a list or is empty
                        values = []
                        for col in columns:
                            value = row_data.get(col, '')
                            if isinstance(value, datetime) and col != "timestamp":
                                value = value.strftime('%d-%m-%Y')
                            values.append(value)
                        
                        tree.insert("", "end", values=values)
            else:
                tree["columns"] = ("No Data",)
                tree.heading("No Data", text="No Data Available")
                tree.column("No Data", width=300, anchor="center", stretch=True)
                tree.insert("", "end", values=("This collection has no documents.",))

        except Exception as e:
            messagebox.showerror(self.t("Error"), f"{self.t("Error displaying data:")}\n{e}")    

    def add_generic_entry(self, tree, current_collection, collection_name):
        fields = self.get_fields_by_name(collection_name)
        info_obj = {}
        items = []
        financials_obj = {}
        temp = None

        new_entry = {}
        if collection_name in ["general_exp_rev"]:
            code = self.get_next_code(current_collection)
            new_entry["code"] = code

        # Handle customer/supplier info
        if collection_name in ["Customer_Payments", "Supplier_Payments"]:
            prefix = "Customer" if collection_name == "Customer_Payments" else "supplier"
            
            operation_number = self.get_next_operation_number(current_collection)
            
            new_entry["Operation_Number"] = operation_number
            current_time = datetime.now()
            new_entry["Time"] = current_time

            # Get the code and name from entries
            code = self.entries.get(f"{prefix.lower()}_code", None)
            name = self.entries.get(f"{prefix.lower()}_name", None)
            
            if code:
                code_value = code.get()
            else:
                code_value = ""
                
            if name:
                name_value = name.get()
            else:
                name_value = ""

            # Create the nested info object
            info_object = {
                "code": code_value,
                "name": name_value
            }
            new_entry[f"{prefix}_info"] = info_object
        
        if collection_name in ["Sales","Purchases"]:
            prefix = "Customer" if collection_name == "Sales" else "supplier"
            
            code = self.entries.get(f"{prefix.lower()}_code")
            name = self.entries.get(f"{prefix.lower()}_name")
            phone1 = self.entries.get(f"{prefix.lower()}_phone1")
            phone2 = self.entries.get(f"{prefix.lower()}_phone2")
            address = self.entries.get(f"{prefix.lower()}_address")

            info_obj = {
                "code": code.get().strip() if code else "",
                "name": name.get().strip() if name else "",
                "phone1": phone1.get().strip() if phone1 else "",
                "phone2": phone2.get().strip() if phone2 else "",
                "address": address.get().strip() if address else "",
            }

            # --- Financials ---
            def safe_float(entry):
                try:
                    return float(entry.get().strip()) if entry and entry.get().strip() else 0.0
                except ValueError:
                    return 0.0

            def safe_str(entry):
                return entry.get().strip() if entry else ""

            net_total = safe_float(self.entries.get("Net_total"))
            prev_balance = safe_float(self.entries.get("Previous_balance"))
            total_balance = safe_float(self.entries.get("Total_balance"))
            payed_cash = safe_float(self.entries.get("Payed_cash"))
            remaining_balance = safe_float(self.entries.get("Remaining_balance"))
            payment_method = safe_str(self.entries.get("Payment_method"))

            financials_obj = {
                "Net_total": net_total,
                "Previous_balance": prev_balance,
                "Total_balance": total_balance,
                "Payed_cash": payed_cash,
                "Remaining_balance": remaining_balance,
                "Payment_method": payment_method
            }

            def split_entry(name):
                entry = self.entries.get(name)
                return entry.get().strip().split(",") if entry and entry.get().strip() else []
            
            var = None
            if prefix.lower() == "customer":
                Product_codes     = split_entry("Product_code")
                product_names     = split_entry("product_name")
                var=product_names
            else :
                material_codes     = split_entry("material_code")
                material_names     = split_entry("material_name")
                var=material_names
            Units             = split_entry("Unit")
            QTYs              = split_entry("QTY")
            Total_QTYs        = split_entry("Total_QTY")
            Unit_prices       = split_entry("Unit_price")
            numberings        = split_entry("numbering")
            Discount_Types    = split_entry("Discount_Type")
            Discount_Values   = split_entry("Discount_Value")
            Final_Prices      = split_entry("Final_Price")

            for i in range(len(var)):
                try:
                    item = {}
                    # Add product/material info depending on prefix
                    item = { 
                        "Unit": Units[i].strip(),
                        "QTY": float(QTYs[i].strip()),
                        "numbering": float(numberings[i].strip()),
                        "Total_QTY": float(Total_QTYs[i].strip()),
                        "Unit_price": float(Unit_prices[i].strip()),
                        "Discount_Type": Discount_Types[i].strip(),
                        "Discount_Value": float(Discount_Values[i].strip()),
                        "Final_Price": float(Final_Prices[i].strip())
                    }
                    
                    if prefix.lower() == "customer":
                        item["Product_code"] = Product_codes[i].strip()
                        item["product_name"] = product_names[i].strip()
                    else:
                        item["material_code"] = material_codes[i].strip()
                        item["material_name"] = material_names[i].strip()
                    

                    items.append(item)
                except (IndexError, ValueError) as e:
                    messagebox.showerror(self.t("Upload Error"), f"{self.t("All Data fields must be filled:")} {e}")
                    return
                
            # new_entry["Date"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            temp = datetime.now()
            # value_date = datetime.strptime(temp, '%d-%m-%Y').date()
            # new_entry["Date"] = datetime.combine(value_date, time.min)


        for field, widget in self.entries.items():
            #add fields not added when using add entry here
            # if field in ["product_name","product_code"] and collection_name == "Products":
            # if (field in ["product_name","product_code","material_code","material_name"] and (collection_name == "Sales" or collection_name == "Purchases")):
            #     dummy=0
            
            if field == PRIMARY_KEYS.get(collection_name):
                prim_key_val = widget.get()
                is_unique = self.is_primary_key_unique(current_collection, collection_name, prim_key_val)

                if is_unique:
                    value = prim_key_val
                else:
                    messagebox.showerror(self.t("Data Error"), f"{prim_key_val} {self.t("is not unique in field")} {field}")
                    return
                
            elif field == "Date" and collection_name in ["Sales","Purchases"]:
                continue
            
            elif field in ZEROED_FIELDS:
                value = widget.get()
                if not value:
                    value = 0
            elif field in [
                "customer_code", "customer_name", "customer_phone1", "customer_phone2", "customer_address",
                "Net_total", "Previous_balance", "Total_balance", "Payed_cash", "Remaining_balance", "Payment_method",
                "Product_code", "product_name", "Unit", "QTY", "Total_QTY", "Unit_price", "numbering",
                "Discount_Type", "Discount_Value", "Final_Price",
                "supplier_code", "supplier_name", "Id",
                "supplier_phone1","supplier_phone2","supplier_address","material_code","material_name"
                ] and collection_name in ["Sales","Purchases","Customer_Payments", "Supplier_Payments"]:
                value = widget.get()
                if not str(value).strip():
                    messagebox.showerror(self.t("Validation Error"), f"{self.t("Field")} '{field}' {self.t("cannot be empty.")}")
                    return  # stop processing if any critical field is empty
                continue  # Skip these fields
            
            if "date" in field.lower() or "timestamp" in field.lower() or "check_out" in field.lower() or "check_in" in field.lower():
                value = widget.get()
                if value:
                    try:
                        value_date = datetime.strptime(value, '%d-%m-%Y').date()
                        value = datetime.combine(value_date, time.min)
                        # Add this only for Employee_withdrawls
                        if collection_name in ["Employee_withdrawls", "Employee_Salary", "Production"]:
                            random_hours   = random.randint(0, 23)
                            random_minutes = random.randint(0, 59)
                            random_seconds = random.randint(0, 59)
                            value += timedelta(hours=random_hours, minutes=random_minutes, seconds=random_seconds)

                    except Exception as e:
                        messagebox.showerror(self.t("Error"), f"{self.t("Invalid date format for")} {field}: {e}")
                        return
                else:
                    messagebox.showwarning(self.t("Warning"), f"{self.t("Please enter a value for")} {field}")
                    return
            elif "pic" in field.lower():
                local_image_path = getattr(widget, 'image_path', None)
                if not local_image_path:
                    messagebox.showerror(self.t("Invalid Input"), self.t("No img was selected"))
                    return
                try:
                    value = upload_file_to_cloudinary(local_image_path)
                except Exception as e:
                    messagebox.showerror(self.t("Upload Error"), f"{self.t("Failed to upload image:")} {e}")
                    return
            elif "pdf_path" in field.lower():
                local_pdf_path = getattr(widget, 'filepath', None)

                if not local_pdf_path:
                    messagebox.showerror(self.t("Invalid Input"), self.t("No PDF was selected."))
                    return

                try:
                    value = self.upload_pdf_to_cloudinary(local_pdf_path)

                    # ✅ Clear filepath attribute and display text after successful upload
                    if hasattr(widget, 'filepath'):
                        widget.filepath = None
                    widget.config(text="")  # Clear displayed filename or label
                except Exception as e:
                    messagebox.showerror(self.t("Upload Error"), f"{self.t("Failed to upload PDF:")} {e}")
                    return

            elif any(word in field.lower() for word in ["instapay","bank_account","e-wallet"]) or (current_collection.name == "Customers" and field=="Sales") :
                value = widget.get() 
                if value:
                    try: 
                        value = int(value)
                    except Exception as e:
                        messagebox.showerror(self.t("Error"), f"{field} {self.t("should be a number")}")
                        return
            elif any(word in field.lower() for word in ["stock_quantity", "salary", "credit", "debit", "balance", "Unit_Price", "duration", "net_total", "previous_balance", "payed_cash", "remaining_balance", "base_salary", "total_withdrawls", "delay_penalty", "overtime_bonus", "net_salary", "amount_withdrawls", "previous_withdrawls", "waste", "product_qty", "material_qty", "amount"]):
                value = widget.get() 
                if not value:
                    messagebox.showwarning(self.t("Warning"), f"{self.t("Please enter a value for")} {field}")
                    return
                try: 
                    value = float(value)
                except Exception as e:
                    messagebox.showerror(self.t("Error"), f"{field} {self.t("should be a floating number")}")
                    return
            else:
                value = widget.get()
                if not value and (field in MANDATORTY_FIELDS) :
                    messagebox.showwarning(self.t("Warning"), f"{self.t("Please enter a value for")} {self.t(field)}")
                    return
                if any(word in field.lower() for word in ["units"]):
                    # Parse comma-separated input to list
                    value = [item.strip() for item in value.split(',') if item.strip()]

            new_entry[field] = value

        try:
            # Generate unique Id
            if "Id" in fields:
                # Convert string IDs to integers and find the maximum
                existing_ids = [int(doc["Id"]) for doc in current_collection.find({}, {"Id": 1})]
                
                new_id = max(existing_ids, default=0) + 1
                new_entry["Id"] = new_id

            #TODO this line is never reached on adding
            if collection_name in ["Sales","Purchases"]:
                new_entry["Date"] = temp
                new_entry[f"{prefix}_info"] = info_obj
                new_entry["Items"] = items
                new_entry["Financials"] = financials_obj

            current_collection.insert_one(new_entry)
            self.refresh_generic_table(tree, current_collection, collection_name, search_text="")
            messagebox.showinfo(self.t("Success"), self.t("Record added successfully"))

            # Clear form fields after successful addition
            for field, widget in self.entries.items():
                if "date" in field.lower():
                    widget.set_date(datetime.now())
                elif "pic" in field.lower():
                    widget.config(image='')
                    widget.image = None
                elif "pdf_path" in field.lower():
                    widget.config(text="")
                else:
                    widget.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror(self.t("Error"), f"{self.t("Error adding record:")} {e}")
  
    def edit_generic_entry(self, tree, current_collection, collection_name):
        selected_item = tree.selection()

        if not selected_item:
            messagebox.showwarning(self.t("Warning"), self.t("Please select a record to edit"))
            return

        selected_data = tree.item(selected_item)["values"]
        if not selected_data:
            messagebox.showwarning(self.t("Warning"), self.t("No data found for selected record"))
            return

        columns = tree["columns"]  # This returns a tuple/list of column names
        try:
            lower_columns = [col.lower() for col in columns]
            if current_collection.name in ["Customer_Payments","Supplier_Payments","Sales", "Purchases"]:
                id_index = 0
            elif "id" in lower_columns:
                id_index = columns.index("Id")  # Dynamically get the index of "Id" #TODO need something different to loop on
            elif any('code' in col for col in lower_columns):
                for idx, col in enumerate(lower_columns):
                    if 'code' in col:
                        id_index = idx
                        break
        except ValueError:
            messagebox.showerror(self.t("Error"), self.t("'Id' field not found in table columns"))
            return

        record_id = selected_data[id_index]
        existing_record = current_collection.find_one({columns[id_index]: record_id})

        if not existing_record:
            try:
                record_id = str(record_id)
                existing_record = current_collection.find_one({columns[id_index]: record_id})
                existing_record.pop("_id", None)
            except ValueError:
                pass

        if not existing_record: #recheck existing record after potential update
            messagebox.showerror(self.t("Error"), self.t("Could not find record in database"))
            return

        updated_entry = {}
        prefix = ""
        # Handle special cases for Customer_Payments and Supplier_Payments
        if collection_name in ["Customer_Payments", "Supplier_Payments"]:
            prefix = "Customer" if collection_name == "Customer_Payments" else "supplier"
            info_object = existing_record.get(f"{prefix}_info", {})
            
            # Update info object if code/name fields were modified
            code_field = f"{prefix.lower()}_code"
            name_field = f"{prefix.lower()}_name"

            if code_field in self.entries:
                code_value = self.entries[code_field].get()
                if code_value:
                    info_object["code"] = code_value
            
            if name_field in self.entries:
                name_value = self.entries[name_field].get()
                if name_value:
                    info_object["name"] = name_value
            
            updated_entry[f"{prefix}_info"] = info_object

        if collection_name in ['Sales','Purchases']:
            prefix = "Customer" if collection_name == "Sales" else "supplier"

            financials_obj = existing_record.get("Financials",{})
            info_obj = existing_record.get(f"{prefix}_info",{})
            items = existing_record.get("Items",{})
            big_obj = {
                "Financials": financials_obj,
                f"{prefix}_info": info_obj,
                "Items": items
            }

            for field, widget in self.entries.items():  
                if field in ["Product_code","material_code"] and isinstance(items,list):
                    item_codes = None
                    if field == "Product_code":
                        item_codes = self.entries["Product_code"].get()
                    else: 
                        item_codes = self.entries["material_code"].get()

                    split_item_codes = item_codes.split(',')
                    num_items = len(split_item_codes)
                    idx = 0
                    
                    while num_items > idx:
                        item = items[idx] if idx < len(items) else {}
                        for key in item.keys():
                            value = self.entries[key].get() #check out this line
                            if isinstance(value, str):
                                split_values = value.split(',')
                                if idx < len(split_values):
                                    if key in ["QTY", "numbering", "Total_QTY", "Unit_price", "Discount_Value", "Final_Price"]:
                                        item[key] = float(split_values[idx].strip())
                                    else: 
                                        item[key] = split_values[idx].strip()
                                else:
                                    item[key] = ''
                            else:
                                if key in ["QTY", "numbering", "Total_QTY", "Unit_price", "Discount_Value", "Final_Price"]:
                                    item[key] = float(value)  # or handle non-string cases differently
                                else:
                                    item[key] = value
                                    
                        if(len(items) < num_items):
                            items.append(item)
                        else:
                            items[idx] = item
                        idx += 1

                    big_obj["Items"] = items
   
                elif field in ["product_name", "Unit", "QTY", "Total_QTY", "Unit_price", "numbering",
                                "Discount_Type", "Discount_Value", "Final_Price", "material_name"]:
                    continue

                elif field in field_mapping:
                    parent, child = field_mapping[field]
                    value = widget.get()
                    parent, child = field_mapping[field]
                    if parent in big_obj:
                        if child in ["QTY", "numbering", "Total_QTY", "Unit_price", "Discount_Value", "Final_Price", "Net_total", "Previous_balance", "Total_balance", "Payed_cash", "Remaining_balance"]:
                            big_obj[parent][child] = float(value)
                        else:
                            big_obj[parent][child] = value

            updated_entry["Financials"]    = big_obj["Financials"]
            updated_entry[f"{prefix}_info"] = big_obj[f"{prefix}_info"]
            updated_entry["Items"]         = big_obj["Items"]

        for field, widget in self.entries.items():
            if collection_name in ['Sales', 'Purchases'] and field in ["customer_code", "customer_name", "customer_phone1", 
                "customer_phone2", "customer_address", "Net_total", "Previous_balance", "Total_balance", "Payed_cash",
                "Remaining_balance", "Payment_method", "Product_code", "product_name", "Unit", "QTY", "Total_QTY", 
                "Unit_price", "numbering", "Discount_Type", "Discount_Value", "Final_Price", "supplier_code", "supplier_name", "Id"
                "supplier_phone1","supplier_phone2","supplier_address","material_code","material_name"]  :
                continue
            elif collection_name in ['Customer_Payments', 'Supplier_Payments'] and field in ["customer_code", "customer_name","supplier_code", "supplier_name"]:
                continue
            elif field in ["Id", "Date"]:
                continue  # Skip Id and special fields (handled above)

            existing_value = existing_record.get(field, None)

            if "date" in field.lower() or "timestamp" in field.lower() or "check_out" in field.lower() or "check_in" in field.lower():
                value = widget.get()
                if value and collection_name != "Sales":
                    try:
                        value_date = datetime.strptime(value, '%d-%m-%Y').date()
                        value = datetime.combine(value_date, time.min)
                    except Exception as e:
                        messagebox.showerror(self.t("Error"), f"{self.t("Invalid date format for")} {field}: {e}")
                        return
                else:
                    value = existing_value  # Keep old date if no new input

            elif "pic" in field.lower():
                local_image_path = getattr(widget, 'image_path', None)

                if local_image_path:
                    try:
                        value = upload_file_to_cloudinary(local_image_path)
                    except Exception as e:
                        messagebox.showerror(self.t("Upload Error"), f"{self.t("Failed to upload image:")} {e}")
                        return
                else:
                    value = existing_value  # Keep old image URL if no new selection
            
            elif "pdf_path" in field.lower():
                local_pdf_path = getattr(widget, 'filepath', None)

                if local_pdf_path:
                    try:
                        value = self.upload_pdf_to_cloudinary(local_pdf_path)
                    except Exception as e:
                        messagebox.showerror(self.t("Upload Error"), f"{self.t("Failed to upload PDF:")} {e}")
                        return
                else:
                    value = existing_value  # Keep old PDF URL if no new selection
            elif any(word in field.lower() for word in ["instapay","bank_account","e-wallet"]) or (current_collection.name == "Customers" and field=="Sales") :
                value = widget.get() 
                if not value:
                    value = existing_value  # Keep old text if no new input

                try: 
                    if value:
                        value = int(value)
                except Exception as e:
                    messagebox.showerror(self.t("Error"), f"{field} {self.t("should be a number")}")
                    return

            elif any(word in field.lower() for word in ["stock_quantity", "salary", "credit", "debit", "balance", "Unit_Price", "duration", "net_total", "previous_balance", "payed_cash", "remaining_balance", "base_salary", "total_withdrawls", "delay_penalty", "overtime_bonus", "net_salary", "amount_withdrawls", "previous_withdrawls", "waste", "product_qty", "material_qty", "amount"]):
                value = widget.get()
                if not value:
                    value = existing_value  # Keep old text if no new input
                try: 
                    if value:
                        value = float(value)
                except Exception as e:
                    messagebox.showerror(self.t("Error"), f"{field} {self.t("should be a floating number")}")
                    return
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
            self.revert_locked_fields(existing_record, updated_entry)

            identifier_field = columns[id_index]
            result = current_collection.update_one({identifier_field: record_id}, {"$set": updated_entry})
            
            if result.modified_count > 0:
                messagebox.showinfo(self.t("Success"), self.t("Record updated successfully"))
            else:
                messagebox.showinfo(self.t("Info"), self.t("No changes were made (record was identical)"))

            # Refresh table
            self.refresh_generic_table(tree, current_collection, collection_name, search_text="")

            # Clear form fields after update
            for field, widget in self.entries.items():
                if "date" in field.lower():
                    widget.set_date(datetime.now())
                elif "pdf_path" in field.lower():
                    widget.config(text="")
                elif "pic" in field.lower():
                    widget.config(image='')
                    widget.image = None
                    widget.image_path = None
                else:
                    widget.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror(self.t("Error"), f"{self.t("Error updating record:")} {e}")
    
    def revert_locked_fields(self, existing, updated):
        for key, locked_fields in LOCKED_FIELDS.items():
            if key == "root":
                for field in locked_fields:
                    if field in updated:
                        updated[field] = existing.get(field)
                # break

            elif key == "Items":
                # Handle list of objects
                existing_items = existing.get("Items", [])
                updated_items = updated.get("Items", [])

                for idx, item in enumerate(updated_items):
                    if idx < len(existing_items):
                        for field in locked_fields:
                            if field in item:
                                if field in ["QTY", "numbering", "Total_QTY", "Unit_price", "Discount_Value", "Final_Price"]:
                                    item[field] = float(existing_items[idx].get(field))
                                else: 
                                    item[field] = existing_items[idx].get(field)
                    updated_items[idx] = item
                if len(updated_items) > 0:
                    updated["Items"] = updated_items
                # updated["Items"] = updated_items

            elif key in ["Customer_info", "supplier_info"]:
                # Handle normal nested dicts like Financials, Customer_info, etc.
                nested_existing = existing.get(key, {})
                nested_updated = updated.get(key, {})
                for field in locked_fields:
                    if field in nested_updated:
                        nested_updated[field] = nested_existing.get(field)
                if len(nested_updated) > 0:
                    updated[key] = nested_updated
    
    def delete_generic_entry(self, tree, current_collection):   
        selected_item = tree.selection()
        id_index = None
        field_name = None

        if not selected_item:
            messagebox.showwarning(self.t("Warning"), self.t("Please select a record to delete"))
            return
        columns = tree["columns"]  # Tuple/list of column names
        try:
            # lower_columns = [col.lower() for col in columns]
            # original_columns = [self.get_original_key(col) for col in columns]
            
            # # Find which column is used as identifier (id / code)
            # primary_key_field = PRIMARY_KEYS.get(current_collection.name)
            
            # Find which column is used as identifier (id / code)
            if current_collection.name in ["Customer_Payments","Supplier_Payments", "Sales", "Purchases"]:
                id_index = 0
            elif current_collection.name in ["Production", "Employee_Salary", "Employee_withdrawls"]:
                id_index = columns.index("timestamp")

            elif current_collection.name in ["Employee_appointimets"]:
                id_index = columns.index("duration")
            elif "id" in [col.lower() for col in columns]:
                id_index = columns.index("Id")
            elif any('code' in col.lower() for col in columns):
                for idx, col in enumerate(columns):
                    if 'code' in col.lower():
                        id_index = idx
                        break
            else:
                messagebox.showerror(self.t("Error"), self.t("Unable to determine identifier column."))
                return

            if id_index is None:
                messagebox.showerror(self.t("Error"), self.t("Unable to determine identifier column."))
                return
            
            raw_unique_id = None
            unique_id = None
            
            field_name = columns[id_index]
            if field_name == "timestamp":
                #change to datetime obj
                raw_unique_id = tree.item(selected_item)["values"][id_index]
                unique_id = datetime.strptime(raw_unique_id, "%Y-%m-%d %H:%M:%S.%f")
            elif field_name == "duration":
                unique_id = float(tree.item(selected_item)["values"][id_index])
            else:
                unique_id = tree.item(selected_item)["values"][id_index]

        except (IndexError, ValueError):
            if field_name == "timestamp":
                try:
                    unique_id = datetime.strptime(raw_unique_id, "%Y-%m-%d %H:%M:%S")
                except:
                    messagebox.showerror(self.t("Error"), self.t("Unable to read selected row data."))
                    return
            else:
                messagebox.showerror(self.t("Error"), self.t("Unable to read selected row data."))
                return

        if not messagebox.askyesno(self.t("Confirm"), self.t("Are you sure you want to delete this record?")):
            return

        try:
            # ARRAY_FIELDS = ['units']  # Fields you want to treat as arrays (custom handling)

            query = {field_name: unique_id}
            document = current_collection.find_one(query)
            
            if not document:
                try:
                    query = {field_name: str(unique_id)}
                    document = current_collection.find_one(query)
                except ValueError:
                    pass

            if not document:
                messagebox.showwarning(self.t("Not Found"), self.t("No matching record found to delete."))
                return

            # Step 2: Check if document contains any ARRAY_FIELDS (like 'units')
            handled = False
            values = tree.item(selected_item)["values"]
            
            prefix = None
            item_code = None
            unit_value = None
            
            if("Units" in columns):
                index = columns.index('Units')
                unit_value = values[index]

            if("Product_code" in columns or "material_code" in columns) and current_collection.name in ["Sales","Purchases"]:
                prefix = "Product" if current_collection.name == "Sales" else "material"
                idx1 = columns.index(f'{prefix}_code')
                idx2 = columns.index('Unit')
                item_code = values[idx1]
                unit_value = values[idx2]

            # for array_field in ARRAY_FIELDS:
            units_list = document.get('Units', None)
            items_list = document.get('Items', None)
            print(f"units_list: {isinstance(units_list, list)} , unique_id {unique_id}")
            if isinstance(units_list, list):
                # Found Units array and unique_id is inside → handle it
                if len(units_list) > 1:
                    handled = True
                    update_result = current_collection.update_one(
                        {"_id": document["_id"]},
                        {"$pull": {'Units': unit_value}}
                    )
                    if update_result.modified_count > 0:
                        self.deselect_entry(tree)
                        self.refresh_generic_table(tree, current_collection, self.table_name.get(), search_text="")
                        messagebox.showinfo(self.t("Success"), f"{self.t("Unit")} '{unique_id}' {self.t("removed from record.")}")
                    else:
                        messagebox.showwarning(self.t("Warning"), self.t("No changes were made to the document."))

            if isinstance(items_list,list):
                if len(items_list) > 1 and current_collection.name in ['Sales','Purchases']:
                    update_result = current_collection.update_one(
                        {"_id": document["_id"]},
                        {
                            "$pull": {
                                "Items": {
                                    "$and": [
                                        {f"{prefix}_code": item_code},
                                        {"Unit": str(unit_value)}
                                    ]
                                }
                            }
                        }
                    )                  
                    if update_result.modified_count > 0:
                        self.deselect_entry(tree)
                        self.refresh_generic_table(tree, current_collection, self.table_name.get(), search_text="")
                        messagebox.showinfo(self.t("Success"), f"{self.t("Unit")} '{unique_id}' {self.t("removed from record.")}")
                    else:
                        messagebox.showwarning(self.t("Warning"), self.t("No changes were made to the document."))

                else:
                    delete_result = current_collection.delete_one({"_id": document["_id"]})
                    if delete_result.deleted_count > 0:
                        self.deselect_entry(tree)
                        self.refresh_generic_table(tree, current_collection, self.table_name.get(), search_text="")
                        messagebox.showinfo(self.t("Success"), self.t("Record deleted successfully."))
                    else:
                        messagebox.showwarning(self.t("Warning"), self.t("No matching record found to delete."))
                return  # After handling Units logic, exit

            # Step 3: If no ARRAY_FIELDS handling triggered → do standard delete
            if not handled:
                delete_result = current_collection.delete_one(query)
                if delete_result.deleted_count > 0:
                    self.deselect_entry(tree) 
                    self.refresh_generic_table(tree, current_collection, self.table_name.get(), search_text="")
                    messagebox.showinfo(self.t("Success"), self.t("Record deleted successfully."))
                else:
                    messagebox.showwarning(self.t("Warning"), self.t("No matching record found to delete."))

        except Exception as e:
            messagebox.showerror(self.t("Error"), f"{self.t("Error deleting record:")} {e}")         

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
                        messagebox.showerror(self.t("Error"), f"{self.t("Invalid date format for")} {field}")
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
                    messagebox.showerror(self.t("Upload Error"), f"{self.t("Failed to upload image:")} {e}")
                    return
            else:
                dialog = AlwaysOnTopInputDialog(self.root, f"{self.t("Enter value for")} {field}:")
                value = dialog.get_result()
                if value is None:
                    return

            new_entry[field] = value

        try:
            current_collection.insert_one(new_entry)
            self.display_table()
            messagebox.showinfo(self.t("Success"), self.t("Record added successfully"))
        except Exception as e:
            messagebox.showerror(self.t("Error"), f"{self.t("Error adding record:")} {e}")

    def edit_entry(self):
        collection_name = self.table_name.get()
        current_collection = self.get_collection_by_name(collection_name)
        
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning(self.t("Warning"), self.t("Please select a record to edit"))
            return

        #TODO fix this ID no longer available in tree
        try:
            unique_id = self.tree.item(selected_item)['values'][2]  # Assuming this holds the custom unique ID
        except IndexError:
            messagebox.showerror(self.t("Error"), self.t("Unable to read selected row data."))
            return
        
        # Get the fields to edit (excluding _id)
        first_document = current_collection.find_one({"Id": unique_id})
        if not first_document:
            messagebox.showerror(self.t("Error"), self.t("Could not retrieve record for editing."))
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
                        messagebox.showerror(self.t("Error"), f"{self.t("Invalid date format for")} {field}")
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
            messagebox.showinfo(self.t("Success"), self.t("Record updated successfully"))
        except Exception as e:
            messagebox.showerror(self.t("Error"), f"{self.t("Error updating record:")} {e}")

    def delete_entry(self):
        collection_name = self.table_name.get()
        current_collection = self.get_collection_by_name(collection_name)

        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning(self.t("Warning"), self.t("Please select a record to delete"))
            return

        try:
            unique_id = self.tree.item(selected_item)['values'][2]  # Assuming this holds the custom unique ID
        except IndexError:
            messagebox.showerror(self.t("Error"), self.t("Unable to read selected row data."))
            return

        if messagebox.askyesno(self.t("Confirm"), self.t("Are you sure you want to delete this record?")):
            try:
                delete_result = current_collection.delete_one({"Id": unique_id})
                if delete_result.deleted_count == 0:
                    messagebox.showwarning(self.t("Not Found"), self.t("No matching record found to delete."))
                else:
                    self.display_table()
                    messagebox.showinfo(self.t("Success"), self.t("Record deleted successfully"))
            except Exception as e:
                messagebox.showerror(self.t("Error"), f"{self.t("Error deleting record:")} {e}")

############################ Utility Functions ########################################
    def check_access_and_open(self, role):
        allowed_roles = ["admin","developer"]  # Define roles that can access this
        if role in allowed_roles:
            # self.manage_old_database_window(db_name, table_name)
            self.manage_database_window()
        else:
            messagebox.showwarning(self.t("Access Denied"), self.t("You do not have permission to access this page."))

    def get_collection_by_name(self, collection_name):
        """Returns the appropriate MongoDB collection object based on the provided name.
        Args: collection_name (str): The name of the collection to access (e.g., "Employees", "Products").
        Returns: pymongo.collection.Collection or None: The corresponding MongoDB collection object,
                                                   or None if the name is not recognized."""
        if collection_name == "Employees":
            return self.employees_collection
        if collection_name == "Employee_appointimets":
            return self.employees_appointments_collection
        if collection_name == "Employee_withdrawls":
            return self.employee_withdrawls_collection
        if collection_name == "Employee_Salary":
            return self.employee_salary_collection
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
        elif collection_name == "Daily_shifts":
            return self.daily_shifts_collection
        elif collection_name == "Accounts":
            return self.accounts_collection
        elif collection_name == "Transactions":
            return self.transactions_collection
        elif collection_name == "Big_deals":
            return self.big_deals_collection
        elif collection_name == "Production":
            return self.production_collection
        elif collection_name == "Customer_Payments":
            return self.customer_payments
        elif collection_name == "Supplier_Payments":
            return self.supplier_payments
        elif collection_name == "TEX_Calculations":
            return self.TEX_Calculations_collection
        elif collection_name == "general_exp_rev":
            return self.general_exp_rev_collection
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
        
        # elif collection_name == "Sales_Header":
        #     return [self.t("Product_code"), self.t("product_name"), self.t("unit"),self.t("numbering"),self.t("QTY"),self.t("Discount Type"),self.t("Discount Value"),self.t("Total_QTY"),self.t("Unit_Price"),self.t("Total_Price")]
       
        # elif collection_name == "Materials_Header":
        #     return [self.t("Material_code"), self.t("Material_name"), self.t("unit"),self.t("numbering"),self.t("QTY"),self.t("Discount Type"),self.t("Discount Value"),self.t("Total_QTY"),self.t("Unit_Price"),self.t("Total_Price")]
      
        elif collection_name == "Sales_Header":
            return ["Product_code", "product_name", "unit","numbering","QTY","Discount_Type","Discount Value","Total_QTY","Unit_Price","Total_Price"]
        
        elif collection_name == "Materials":
            return ["material_name", "category","stock_quantity","specs","material_code","Units","material_pic","Unit_Price"]

        elif collection_name == "Materials_Header":
            return ["Material_code", "Material_name", "unit","numbering","QTY","Discount_Type","Discount Value","Total_QTY","Unit_Price","Total_Price"]
       
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
        
        # elif collection_name == "Employee_appointimets":
        elif collection_name == "Employee_appointimets":
            return ["employee_code", "employee_name", "check_in", "check_out", "duration"]
        
        elif collection_name == "Daily_shifts":
            return ["shift_id", "employee_id", "shift_date", "start_time", "end_time"]
        
        elif collection_name == "Accounts":
            return ["account_id", "account_name", "balance", "account_type"]
        
        elif collection_name == "Transactions":
            return ["transaction_id", "account_id", "transaction_date", "amount", "transaction_type"]
        
        elif collection_name == "Big_deals":
            return ["deal_id", "deal_date", "customer_id", "product_id", "deal_value"]
        
        elif collection_name == "Sales":
            return ["Receipt_Number", "Date", "customer_code", "customer_name", "customer_phone1","customer_phone2","customer_address",
                    "Product_code","product_name","Unit", "QTY","numbering","Total_QTY", "Unit_price", "Discount_Type", "Discount_Value",
                    "Final_Price","Net_total", "Previous_balance", "Total_balance", "Payed_cash", "Remaining_balance", "Payment_method", "PDF_Path"]
        
        elif collection_name == "Purchases":
            return ["Receipt_Number", "Date", "supplier_code", "supplier_name", "supplier_phone1","supplier_phone2","supplier_address",
                    "material_code","material_name","Unit","QTY", "numbering","Total_QTY", "Unit_price", "Discount_Type", "Discount_Value",
                    "Final_Price", "Net_total", "Previous_balance", "Total_balance", "Payed_cash", "Remaining_balance", "Payment_method", "PDF_Path"]
        
        elif collection_name == "Customer_Payments":
            return ["Operation_Number", "Time", "Credit", "Debit","Payment_method", "Customer_info"]

        elif collection_name == "Supplier_Payments":
            return ["Operation_Number", "Time", "Credit", "Debit","Payment_method", "supplier_info"]

        elif collection_name == "Production":
            return ["material_code", "material_qty", "product_code","product_qty", "timestamp", "waste"]

        elif collection_name == "TEX_Calculations":
            return ["calculation_id", "product_id", "calculation_date", "value"]
        
        elif collection_name == "Employee_Salary":
            return ["employee_code", "employee_name", "month_year", "base_salary","total_withdrawls" , "delay_penalty", "overtime_bonus", "net_salary", "payment_method", "timestamp"]
        
        elif collection_name == "Employee_withdrawls":
            return ["employee_code", "employee_name", "previous_withdrawls", "amount_withdrawls", "payment_method", "timestamp"]

        elif collection_name == "general_exp_rev":
            return ["code", "type", "amount", "payment_method", self.t("description"), "date"]
        
        else:
            print(f"Warning: Collection name '{collection_name}' not recognized.")
            return []
    def clean_materials_collection(self):
        """Remove leading/trailing spaces and newlines from all string attributes in Materials collection."""
        materials_col = self.get_collection_by_name("Materials")
        for doc in materials_col.find():
            updated_fields = {}
            for key, value in doc.items():
                if isinstance(value, str):
                    cleaned = value.strip()
                    updated_fields[key] = cleaned
            # Also clean items in arrays if needed
            if updated_fields:
                materials_col.update_one({"_id": doc["_id"]}, {"$set": updated_fields})
    def clean_customers_collection(self):
        """Remove leading/trailing spaces and newlines from all string attributes in Customers collection."""
        customers_col = self.get_collection_by_name("Customers")
        for doc in customers_col.find():
            updated_fields = {}
            for key, value in doc.items():
                if isinstance(value, str):
                    cleaned = value.strip()
                    updated_fields[key] = cleaned
            if updated_fields:
                customers_col.update_one({"_id": doc["_id"]}, {"$set": updated_fields})
    
    def clean_suppliers_collection(self):
        """Remove leading/trailing spaces and newlines from all string attributes in Suppliers collection."""
        suppliers_col = self.get_collection_by_name("Suppliers")
        for doc in suppliers_col.find():
            updated_fields = {}
            for key, value in doc.items():
                if isinstance(value, str):
                    cleaned = value.strip()
                    updated_fields[key] = cleaned
            if updated_fields:
                suppliers_col.update_one({"_id": doc["_id"]}, {"$set": updated_fields})
    
    def clean_products_collection(self):
        """Remove leading/trailing spaces and newlines from all string attributes in Products collection."""
        products_col = self.get_collection_by_name("Products")
        for doc in products_col.find():
            updated_fields = {}
            for key, value in doc.items():
                if isinstance(value, str):
                    cleaned = value.strip()
                    updated_fields[key] = cleaned
            if updated_fields:
                products_col.update_one({"_id": doc["_id"]}, {"$set": updated_fields})
    
    def clean_employees_collection(self):
        """Remove leading/trailing spaces and newlines from all string attributes in Employees collection."""
        employees_col = self.get_collection_by_name("Employees")
        for doc in employees_col.find():
            updated_fields = {}
            for key, value in doc.items():
                if isinstance(value, str):
                    cleaned = value.strip()
                    updated_fields[key] = cleaned
            if updated_fields:
                employees_col.update_one({"_id": doc["_id"]}, {"$set": updated_fields})
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
                        
                    except (ValueError, IndexError):
                        last_number = 0
                        
            
            new_number = last_number + 1
            # print(4)
            return f"INV-{new_number:05d}"
        
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
                    except (ValueError, IndexError):
                        last_number = 0
            
            new_number = last_number + 1
            # print(4)
            return f"INV-{new_number:05d}"
        
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل توليد الرقم التسلسلي: {str(e)}")
            return None

    def save_invoice(self, sales_col, customers_col, products_col):
        """Prepare invoice data and show preview without saving"""
        try:
            # التحقق من وجود بيانات العميل
            customer_name = self.customer_name_var.get().strip()
            customer_code = self.customer_code_var.get().strip()
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
            payed_cash = float(self.payed_cash_var.get() or 0)
            transportation_fees = float(self.transport_fees_var.get() or 0)

            # جمع بيانات العناصر والتحقق من المخزون
            items = []
            total_amount = transportation_fees
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
                    stock = float(stock)
                    if self.update:
                        for item in self.items:
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
                    if self.update:

                            if product_Code is not None and total_Qty is not None:    
                                Stock = Product.get("stock_quantity", 0)
                                stock_updates[product_Code] = Stock + total_Qty 
                                if product_Code == product_code:
                                    stock_updates[product_Code] -= total_qty
                                else:
                                    stock_updates[product_code] = stock - total_qty
                    else:
                        stock_updates[product_code] = stock - total_qty
                    # if not stock_updates.get(product_code):
                    #     stock_updates[product_code] = 0
                    
                    
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
            if self.update:
                invoice_number = self.invoice_var.get()
            else:
                invoice_number = self.generate_invoice_number()
            if not invoice_number:
                return
            # Extract nested dictionaries
            # customer_info = invoice_data.get("Customer_info", {})
            # financials = invoice_data.get("Financials", {})
            # items = invoice_data.get("Items", [])
            
            # # Populate customer information
            # self.customer_name_var.set(customer_info.get("name", ""))
            # self.customer_code_var.set(customer_info.get("code", ""))
            # self.previous_balance_var.set(str(financials.get("Previous_balance", 0)))
            print("\n###############################################################################################\n")
            # Previous_balance=0
            # for sales in self.sales_collection.find():
            #     customer_info = sales.get("Customer_info", {})
            #     name = customer_info.get("name", "Unknown")
            #     if customer_name == name:
            #         financials = sales.get("Financials", {})
            #         prev_Net_total = float(financials.get("Net_total", 0))
            #         prev_Payed_cash = float(financials.get("Payed_cash", 0))  
            #         Previous_balance = Previous_balance + prev_Net_total - prev_Payed_cash
            #         print(f"Customer: {name}, Previous Balance: {Previous_balance}")
            # for payments in self.customer_payments.find():
            #     customer_info = payments.get("Customer_info", {})
            #     name = customer_info.get("name", "Unknown")
            #     if customer_name == name:
            #         prev_payments = float(payments.get("Credit",0))
            #         Previous_balance = Previous_balance - prev_payments
            #         print(f"Customer: {name}, Previous Balance: {Previous_balance}")
            # if self.update:
            #     Previous_balance = self.customer_info.get("Balance", 0) #the old financials
            # else:
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
                    "Payment_method": self.payment_method_var.get()
                },
                "PDF_Path": "",
            }

            # Store prepared invoice data for preview/final save
            self.pending_invoice_data = invoice_data
            self.pending_stock_updates = stock_updates
            self.pending_customer_id = customer["_id"]
            self.pending_collections = (sales_col, customers_col, products_col)
            
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
            tree.heading(col, text=self.t(col))
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
        if not hasattr(self, 'pending_invoice_data') or not self.pending_invoice_data:
            messagebox.showerror("خطأ", "لا توجد بيانات فاتورة معلقة!")
            preview_window.destroy()
            return
        
        try:
            sales_col, customers_col, products_col = self.pending_collections
            invoice_data = self.pending_invoice_data
            total_amount = invoice_data['Financials']['Net_total']
            payed_cash = invoice_data['Financials']['Payed_cash']
            # transportation_fees = invoice_data['Financials']['transportation_fees']
            
            # 1. Update stock
            for code, new_stock in self.pending_stock_updates.items():
                products_col.update_one(
                    {"product_code": code},
                    {"$set": {"stock_quantity": new_stock}}
                )
            # 2. Update customer
            # Fetch the customer document
            customer = customers_col.find_one({"_id": self.pending_customer_id})

            # balance = customers_col.get("_id": self.pending_customer_id, "Balance", 0)
            # new_balance = (invoice_data['Financials']['Previous_balance'] + total_amount) - payed_cash
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
                    {"_id": self.pending_customer_id},
                    {"$set": update_fields}
                )
            if self.update:
                Prev_customer_name = self.customer_info.get("name", "")
                prev_total_amount = self.financials.get("Net_total") # the old financials
                prev_payed_cash = self.financials.get("Payed_cash") # the old financials
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
                {"_id": self.pending_customer_id},
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
            if self.update:
                sales_col.delete_one({"Receipt_Number":self.invoice_var.get()})
            sales_col.insert_one(invoice_data)
            
            
            # 5. Show success and clean up
            messagebox.showinfo("نجاح", f"تم حفظ فاتورة البيع رقم {invoice_data['Receipt_Number']}")
            self.clear_invoice_form()
            
            # 6. Clear pending data
            del self.pending_invoice_data
            del self.pending_stock_updates
            del self.pending_customer_id
            del self.pending_collections
            
            preview_window.destroy()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ الفاتورة: {str(e)}")
            preview_window.destroy()
    def save_invoice_purchase(self, purchase_col, suppliers_col, materials_col):
        """Prepare purchase invoice data and show preview without saving"""
        try:
            # التحقق من وجود بيانات المورد
            supplier_name = self.supplier_name_var.get().strip()
            if not supplier_name:
                messagebox.showerror("خطأ", "يرجى اختيار مورد")
                return

            # البحث عن المورد في قاعدة البيانات
            supplier = suppliers_col.find_one({"Name": supplier_name})
            if not supplier:
                messagebox.showerror("خطأ", "المورد غير مسجل!")
                return

            # التحقق من المبلغ المدفوع
            payed_cash = float(self.payed_cash_var.get() or 0)

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
                    messagebox.showerror("خطأ", f"الخامة {material_code} غير موجود!")
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
                    stock = float(stock)
                    # if total_qty > stock:
                    #     messagebox.showerror("نقص في المخزون", 
                    #         f"الكمية المطلوبة ({total_qty}) تتجاوز المخزون ({stock}) للمنتج {material_code}")
                    #     return
                    if self.update_purchase:
                        for item in self.items_purchase:
                            Material_code =item.get("material_code")
                            Material = materials_col.find_one({"material_code": Material_code})
                            total_Qty = float(item.get("Total_QTY"))
                            if Material_code is not None and total_Qty is not None:    
                                Stock = Material.get("stock_quantity", 0)
                                stock_updates[Material_code] = Stock - total_Qty
                                if Material_code == material_code:
                                    stock_updates[Material_code] += total_qty
                                else:
                                    stock_updates[material_code] = stock + total_qty                        
                    else:
                        stock_updates[material_code] = stock + total_qty
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
            if self.update_purchase:
                invoice_number = self.invoice_var.get()
            else:
                invoice_number = self.generate_invoice_number_purchase()
            if not invoice_number:
                return
            
            print("\n###############################################################################################\n")
            # Previous_balance=0
            # for purchases in self.purchases_collection.find():   
            #     supplier_info = purchases.get("supplier_info", {})
            #     name = supplier_info.get("name", "Unknown")
            #     if supplier_name == name:
            #         financials = purchases.get("Financials", {})
            #         prev_Net_total = float(financials.get("Net_total", 0))
            #         prev_Payed_cash = float(financials.get("Payed_cash", 0))
            #         Previous_balance = Previous_balance + prev_Net_total - prev_Payed_cash
            #         print(f"Supplier: {name}, Previous Balance: {Previous_balance}")
            # for payments in self.supplier_payments.find():
            #     supplier_info = payments.get("supplier_info", {})
            #     name = supplier_info.get("name", "Unknown")
            #     if supplier_name == name:
            #         prev_payments = float(payments.get("Debit",0))
            #         Previous_balance = Previous_balance - prev_payments
            #         print(f"Supplier: {name}, Previous Balance: {Previous_balance}")
            # if self.update_purchase:
            #     Previous_balance = self.supplier_info.get("Balance", 0) #the old financials
            # else:
            Previous_balance = supplier.get("Balance", 0)
            print("\n###############################################################################################\n")
            
            # إنشاء بيانات الفاتورة الكاملة
            invoice_data = {
                "Receipt_Number": invoice_number,
                "Date": datetime.now(),
                "supplier_info": {
                    "code": supplier.get("Code", "SUP-001"),
                    "name": supplier.get("Name", "غير معروف"),
                    "phone1": supplier.get("Phone_number1", ""),
                    "phone2": supplier.get("Phone_number2", ""),
                    "address": supplier.get("Company_address", "")
                },
                "Items": items,
                "Financials": {
                    "Net_total": total_amount,
                    "Previous_balance": Previous_balance,
                    "Total_balance": total_amount + Previous_balance,
                    "Payed_cash": payed_cash,
                    "Remaining_balance": (total_amount + Previous_balance) - payed_cash,
                    "Payment_method": self.payment_method_var.get()
                },
                "PDF_Path": "",
            }

            # Store prepared invoice data for preview/final save
            self.pending_invoice_data = invoice_data
            self.pending_stock_updates = stock_updates
            self.pending_supplier_id = supplier["_id"]
            self.pending_collections = (purchase_col, suppliers_col, materials_col)
            
            # Show preview instead of saving immediately
            self.show_invoice_preview_purchase(invoice_data)
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في العملية: {str(e)}")

    def show_invoice_preview_purchase(self, invoice_data):
        """Display purchase invoice preview window"""
        preview_win = tk.Toplevel(self.root)
        preview_win.title("معاينة فاتورة الشراء")
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
            text=f"فاتورة شراء رقم: {invoice_data['Receipt_Number']}", 
            font=("Arial", 16, "bold"),
            fg="#2c3e50"
        ).pack(side=tk.TOP, anchor=tk.CENTER)
        
        tk.Label(
            header_frame, 
            text=f"التاريخ: {invoice_data['Date']}", 
            font=("Arial", 12)
        ).pack(side=tk.TOP, anchor=tk.CENTER, pady=5)
        
        # Supplier info section
        supp_frame = ttk.LabelFrame(main_frame, text="معلومات المورد")
        supp_frame.pack(fill=tk.X, pady=10, padx=20)
        
        supp_grid = tk.Frame(supp_frame)
        supp_grid.pack(fill=tk.X, padx=10, pady=10)
        
        labels = [
            ("اسم المورد:", invoice_data['supplier_info']['name']),
            ("كود المورد:", invoice_data['supplier_info']['code']),
            ("التليفون:", invoice_data['supplier_info']['phone1']),
            ("العنوان:", invoice_data['supplier_info']['address'])
        ]
        
        for i, (label, value) in enumerate(labels):
            tk.Label(supp_grid, text=label, font=("Arial", 11, "bold"), 
                    anchor="e", width=10).grid(row=i//2, column=(i%2)*2, sticky="e", padx=5, pady=2)
            tk.Label(supp_grid, text=value, font=("Arial", 11), 
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
            tree.heading(col, text=self.t(col))
            tree.column(col, width=col_widths[idx], anchor="center")
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add items to tree
        for i, item in enumerate(invoice_data["Items"], 1):
            discount = f"{item['Discount_Value']}{'%' if item['Discount_Type'] == 'Percentage' else ' ج.م'}"
            tree.insert("", "end", values=(
                i,
                item["material_name"],
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
            ("المدفوع:", f"{invoice_data['Financials']['Payed_cash']:,.2f}  ج.م"),
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
            command=lambda: self.finalize_purchase_invoice(preview_win),
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

    def finalize_purchase_invoice(self, preview_window):
        """Finalize purchase invoice saving process and generate PDF"""
        if not hasattr(self, 'pending_invoice_data') or not self.pending_invoice_data:
            messagebox.showerror("خطأ", "لا توجد بيانات فاتورة معلقة!")
            preview_window.destroy()
            return
        
        try:
            purchase_col, suppliers_col, materials_col = self.pending_collections
            invoice_data = self.pending_invoice_data
            total_amount = invoice_data['Financials']['Net_total']
            payed_cash = invoice_data['Financials']['Payed_cash']
            
            # 1. Update stock
            for code, new_stock in self.pending_stock_updates.items():
                materials_col.update_one(
                    {"material_code": code},
                    {"$set": {"stock_quantity": new_stock}}
                )
            
            # 2. Update supplier
            new_balance = total_amount - payed_cash

            # Fetch the customer document
            supplier = suppliers_col.find_one({"_id": self.pending_supplier_id})

            # Prepare conversion updates if needed
            update_fields = {}

            # Fields to check and convert
            fields = ["Sales", "Balance", "Debit", "Credit"]

            for field in fields:
                value = supplier.get(field)
                if isinstance(value, str):
                    try:
                        if field == "Sales":
                            update_fields[field] = int(float(value))  # Sales to int
                        else:
                            update_fields[field] = float(value)       # Others to double
                    except ValueError:
                        update_fields[field] = 0  # fallback to 0 if conversion fails
            if update_fields:
                suppliers_col.update_one(
                    {"_id": self.pending_supplier_id},
                    {"$set": update_fields}
                )
            if self.update_purchase:
                prev_supplier_name = self.supplier_info.get("name", "")
                prev_total_amount = self.financials_purchases.get("Net_total")
                prev_payed_cash = self.financials_purchases.get("Payed_cash")
                prev_added_balance = prev_total_amount - prev_payed_cash
                # Now perform the main update
                suppliers_col.update_one(
                    {"Name": prev_supplier_name},
                    {   
                        "$inc": {
                            "Sales": -1,
                            "Balance": - prev_added_balance,
                            "Debit": - prev_payed_cash,
                            "Credit": - prev_total_amount
                        }
                    }
                )

            suppliers_col.update_one(
                {"_id": self.pending_supplier_id},
                {
                    "$set": {
                        "Last_purchase": datetime.now(),
                    },
                    
                    "$inc": {
                        "Sales": 1,
                        "Balance": new_balance,
                        "Debit": payed_cash,
                        "Credit": total_amount
                    }
                }
            )
            
            # 3. Generate PDF
            pdf_path = self.generate_pdf_purchase(invoice_data)
            if not pdf_path:
                preview_window.destroy()
                return
                
            # 4. Save invoice with PDF path
            if self.update_purchase:
                purchase_col.delete_one({"Receipt_Number":self.invoice_var.get()})
            invoice_data["PDF_Path"] = pdf_path
            purchase_col.insert_one(invoice_data)
            
            # 5. Show success and clean up
            messagebox.showinfo("نجاح", f"تم حفظ فاتورة الشراء رقم {invoice_data['Receipt_Number']}")
            self.clear_invoice_form_purchase()
            
            # 6. Clear pending data
            del self.pending_invoice_data
            del self.pending_stock_updates
            del self.pending_supplier_id
            del self.pending_collections
            
            preview_window.destroy()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ الفاتورة: {str(e)}")
            preview_window.destroy()

    def clear_invoice_form_purchase(self):
        """Clear the purchase invoice form"""
        try:
            # تنظيف Combobox المورد
            self.supplier_name_var.set('')
            
            # تنظيف حقول العناصر
            for row in self.entries:
                for entry in row:
                    if isinstance(entry, ttk.Combobox):
                        entry.set('')
                    elif isinstance(entry, tk.Entry):
                        entry.delete(0, tk.END)
            
            # تنظيف الحقول المالية
            # self.payed_cash_var.set('0.0')
            # self.payment_method_var.set('نقدي')
            
            # إعادة تعيين القائمة
            self.entries = []
            # إعادة إنشاء الصفوف الأساسية
            # إذا كنت تستخدم دالة لإضافة الصفوف
            # self.new_Purchase_invoice(self.user_role)
            if self.update_purchase:
                self.new_Purchase_invoice(self.user_role,"update")
            else:
                self.new_Purchase_invoice(self.user_role,"add")
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تنظيف الحقول: {str(e)}")

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
                if self.update:
                    self.sales_invoice(self.user_role,"update")
                else:
                    self.sales_invoice(self.user_role,"add")
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
                if self.update_purchase:
                    self.new_Purchase_invoice(self.user_role,"update")
                else:
                    self.new_Purchase_invoice(self.user_role,"add")
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل في تنظيف الحقول: {str(e)}")
                
    def generate_old_pdf(self, invoice_data):
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

            # Load Arabic font
            try:
                arabic_font_path = resource_path(os.path.join("Static", "Fonts", "Amiri-Regular.ttf"))
                if not os.path.exists(arabic_font_path):
                    raise FileNotFoundError(f"Font file not found: {arabic_font_path}")
                pdfmetrics.registerFont(TTFont('Arabic', arabic_font_path))
            except Exception as e:
                print(f"Error loading Arabic font: {e}")
                # Fallback to a default font if Arabic font fails to load
                pdfmetrics.registerFont(TTFont('Arabic', 'Arial'))

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
            logo_path = os.path.join(BASE_DIR,"Static", "images", "Logo.jpg")
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
                arabic_font_path = resource_path(os.path.join("Static", "Fonts", "Amiri-Regular.ttf"))
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
            
            try:
                os.startfile(pdf_path, "print")
            except OSError as e:
                messagebox.showerror(self.t("Print Error"), f"{self.t("Failed to print PDF:")}\n{e}")

            pdf_path = self.upload_pdf_to_cloudinary(pdf_path)
            return pdf_path

        except Exception as e:
            messagebox.showerror("خطأ PDF", f"فشل في توليد الملف: {str(e)}")
            return None
    def generate_pdf_old_purchase(self, invoice_data):
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

            try:
                arabic_font_path = resource_path(os.path.join("Static", "Fonts", "Amiri-Regular.ttf"))
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
            invoice_folder = os.path.join(desktop, "purchase_invoice")

            # Create folder if it doesn't exist
            if not os.path.exists(invoice_folder):
                os.makedirs(invoice_folder)

            # Generate file name
            invoice_number = str(invoice_data['Receipt_Number']).replace("INV-", "").strip()
            file_name = f"فاتورة شراء_{invoice_number}.pdf"

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
            invoice_title = f"فاتورة شراء رقم {invoice_number}"
            
            # رسم الإطار حول العنوان
            frame_width = 4*cm
            frame_height = 1*cm
            frame_x = (width - frame_width) / 2  # مركز أفقي
            frame_y = height - 2.5*cm
            c.setLineWidth(1)
            c.rect(frame_x, frame_y, frame_width, frame_height)
            
            # كتابة العنوان المركزي
            c.setFont("Arabic-Bold", 12)  # تأكد من وجود خط عريض
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
                width - 6*cm,    # العدد
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
    def generate_pdf_purchase(self, invoice_data):
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
            from reportlab.lib import colors  # Added for colors

            # Load Arabic font
            try:
                arabic_font_path = resource_path(os.path.join("Static", "Fonts", "Amiri-Regular.ttf"))
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
            invoice_folder = os.path.join(desktop, "purchase_invoice")

            # Create folder if it doesn't exist
            if not os.path.exists(invoice_folder):
                os.makedirs(invoice_folder)

            # Generate file name
            invoice_number = str(invoice_data['Receipt_Number']).replace("INV-", "").strip()
            file_name = f"فاتورة شراء_{invoice_number}.pdf"

            # Full PDF path
            pdf_path = os.path.join(invoice_folder, file_name)

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
            invoice_title = f"فاتورة شراء رقم {invoice_number}"
            
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
                f"اسم المورد:    {invoice_data['supplier_info']['name']}",
                f"الكود:         {invoice_data['supplier_info']['code']}",
                f"العنوان:       {invoice_data['supplier_info']['address']}",
                f"التليفون:      {invoice_data['supplier_info']['phone1']}"
            ]
            
            for line in customer_fields:
                c.drawRightString(width - 0.4*cm, customer_y, format_arabic(line))
                customer_y -= 0.8*cm

            # ========== جدول العناصر ==========
            headers = ["كود الصنف", "     الصنف", "العدد", "الوحدة", "سعر الوحدة", "الكمية", "الإجمالي"]
            col_positions = [
                width - 0.4*cm,    # كود الصنف
                width - 2*cm,       # الصنف
                width - 6*cm,       # العدد
                width - 7.5*cm,     # الوحدة
                width - 9.5*cm,     # السعر
                width - 11.5*cm,    # الكمية
                width - 13*cm       # الإجمالي
            ]
            
            # رأس الجدول مع لون خلفية
            table_y = customer_y - 0.25*cm
            
            # رسم خلفية ملونة للرأس
            header_height = 0.65*cm
            c.setFillColor(colors.lightblue)
            c.rect(
                col_positions[-1] - 2.0*cm,
                table_y - header_height + 0.2*cm,
                col_positions[0] - col_positions[-1] + 5.0*cm,
                header_height,
                fill=1,
                stroke=0
            )
            
            c.setFont("Arabic-Bold", 10)
            c.setFillColor(colors.black)
            for i, header in enumerate(headers):
                c.drawRightString(col_positions[i], table_y - 0.3*cm, format_arabic(header))

            # بيانات الجدول مع دعم الأسطر المتعددة
            c.setFont("Arabic", 8)
            row_height = 0.7*cm
            max_product_width = 3.5*cm  # أقصى عرض لعمود "الصنف"
            
            # تحديد موضع الصف الأول للبيانات
            table_y -= row_height
            
            # دالة لتقسيم النص الطويل
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
            
            for item in invoice_data["Items"]:
                material_name = item.get("material_name", "")
                material_code = item.get("material_code", "")
                
                # تقسيم اسم المادة إذا كان طويلاً
                product_width = c.stringWidth(format_arabic(material_name), "Arabic", 8)
                if product_width > max_product_width:
                    product_lines = split_text(material_name, max_product_width)
                else:
                    product_lines = [material_name]
                
                # حساب ارتفاع الصف بناءً على عدد الأسطر
                item_height = row_height * len(product_lines)
                
                # رسم خلفية بيضاء للصف
                c.setFillColor(colors.white)
                c.rect(
                    col_positions[-1] - 0.5*cm,
                    table_y - item_height + 0.1*cm,
                    col_positions[0] - col_positions[-1] + 1.0*cm,
                    item_height - 0.2*cm,
                    fill=1,
                    stroke=0
                )
                c.setFillColor(colors.black)
                
                # رسم كل سطر من أسطر المادة
                for i, line in enumerate(product_lines):
                    line_y = table_y - (i * row_height)
                    
                    # رسم محتويات الصف
                    columns = [
                        material_code if i == 0 else "",  # عرض الكود في السطر الأول فقط
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
                ("الباقي:", invoice_data['Financials']['Remaining_balance'])
            ]
            
            c.setFont("Arabic-Bold", 12)
            for label, value in totals:
                text = f"{format_arabic(f'{value:,.2f}')} {format_arabic(label)}"
                c.drawRightString(width - 0.3*cm, totals_y, text)
                totals_y -= 0.8*cm

            # ========== التوقيعات ==========
            c.setFont("Arabic", 10)
            c.drawRightString(width - 2.2*cm, totals_y - 0.5*cm, format_arabic("____________________"))
            c.drawString(1.5*cm, totals_y - 0.5*cm, format_arabic("____________________"))
            
            c.save()

            try:
                os.startfile(pdf_path, "print")
            except OSError as e:
                messagebox.showerror(self.t("Print Error"), f"{self.t("Failed to print PDF:")}\n{e}")

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

    def get_mongo_field_path(self, key):
        if key in search_field_mapping:
            parts = search_field_mapping[key]
            return ".".join(parts)
        return key  # fallback: return as-is if not nested

    def deselect_entry(self,tree):
        tree.selection_remove(tree.selection())
        # Clear form fields
        for field, widget in self.entries.items():
            if "date" in field.lower():
                widget.set_date(datetime.now())
            elif "pdf_path" in field.lower():
                widget.config(text="")
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

    def is_primary_key_unique(self, collection, collection_name, new_prim_key):
        primary_key_field = PRIMARY_KEYS.get(collection_name)

        existing = collection.find_one({primary_key_field: new_prim_key})
        return existing is None

    # To get the text button based on language
    def t(self, text):
        return self.translations.get(text, {}).get(self.language, text)
    
    def show_original(self):
        """Print the English key for the selected translated value."""
        selected_translated = self.selected_field.get()
        original_key = self.reverse_translations.get(selected_translated, "Unknown")
        return original_key
    
    def get_original_key(self, translated_label):
        """Return the original field key from a translated label."""
        return self.reverse_translations.get(translated_label, translated_label)

    # Function tot oggle from Arabic to English and Vicaverse
    def toggle_language(self):
        self.language = "English" if self.language == "Arabic" else "Arabic"
        self.main_menu()   
    def toggle_theme(self):
        if self.light:
            self.light = False
        elif not self.light:
            self.light = True
        if COLORS["background"] == "#F5F7FA":
            COLORS["background"]    = "#121212"   # Dark background (not pure black)
            COLORS["primary"]       = "#3B82F6"   # Soft light text (from light mode #2A3F5F)
            COLORS["main_frame"]    = "#2A3F5F"   # Soft light text (from light mode #2A3F5F)
            COLORS["secondary"]     = "#00C0A3"   # Keep same – good contrast on dark
            COLORS["accent"]        = "#FF6F61"   # Keep same – bright accent
            COLORS["text"]          = "#FFFFFF"   # Bright white for main text
            COLORS["card"]          = "#1E1E1E"   # Dark card background (soft contrast)
            COLORS["chart1"]        = "#00C0A3"   # Same – stands out on dark
            COLORS["chart2"]        = "#FF6F61"   # Same – bright red works well
            COLORS["highlight"]     = "#9B6EF3"   # Softer version of #6C5CE7 for dark
            COLORS["table_header"]  = "#2C2C2C"   # Dark header with slight elevation
            COLORS["positive"]      = "#03DAC6"   # Material-style teal (greenish)
            COLORS["neutral"]       = "#888888"   # Neutral gray for muted UI
            COLORS["top_bar"]       = "#23272A"   # <-- New dark mode top bar color
            COLORS["top_bar_icons"] = "#fbd307"   # <-- New dark mode user info color
        else:
            COLORS["background"]    = "#F5F7FA"
            COLORS["primary"]       = "#3B82F6"
            COLORS["main_frame"]    = "#2A3F5F"
            COLORS["secondary"]     = "#00C0A3"
            COLORS["accent"]        = "#FF6F61"
            COLORS["text"]          = "#2A3F5F"
            COLORS["card"]          = "#FFFFFF"
            COLORS["chart1"]        = "#00C0A3"
            COLORS["chart2"]        = "#FF6F61"
            COLORS["highlight"]     = "#6C5CE7"
            COLORS["table_header"]  = "#2A3F5F"
            COLORS["positive"]      = "#00C0A3"
            COLORS["neutral"]       = "#A0AEC0"
            COLORS["top_bar"]       = "#dbb40f"   # <-- Original light mode top bar color
            COLORS["top_bar_icons"] = "#000000"   # <-- Original light mode user info color
        self.main_menu()

    #Function to update the time 
    # def update_time(self, time_label):
    #     time_label.config(text=datetime.now().strftime('%B %d, %Y %I:%M %p'))
    #     self.root.after(1000, self.update_time, time_label)


    # Function to make the top bar part
    def topbar(
            self,
            show_back_button=False, 
            Back_to_Database_Window = False, 
            Back_to_Employee_Window = False, 
            Back_to_Sales_Window = False,
            Back_to_Purchases_Window = False,
            Back_to_Reports_Window = False
            ):
        # Top Bar
        top_bar = tk.Frame(self.root, bg=COLORS["top_bar"], height=60)
        top_bar.pack(fill="x")
        # Exit icon
        try:    
            if self.light:
                self.exit_icon_path     = os.path.join(BASE_DIR, "Static", "images", "exit-dark.png")
            elif not self.light:
                self.exit_icon_path     = os.path.join(BASE_DIR, "Static", "images", "exit-light.png")
            exit_image = Image.open(self.exit_icon_path)
            exit_image = exit_image.resize((35, 35), Image.LANCZOS)
            self.exit_photo = ImageTk.PhotoImage(exit_image)
            exit_icon = tk.Label(top_bar, image=self.exit_photo, bg=COLORS["top_bar"])
            exit_icon.pack(side="right", padx=10)
            exit_icon.bind("<Button-1>", lambda e: self.root.quit())
        except Exception as e:
            self.silent_popup("Error", "Error loading exit icon: {e}", self.play_Error)

        # Logout icon
        try:
            # login_window_instance = LoginWindow()
            if self.light:
                self.logout_icon_path = os.path.join(BASE_DIR, "Static", "images", "logout-dark.png")
            elif not self.light:
                self.logout_icon_path = os.path.join(BASE_DIR, "Static", "images", "logout-light.png")
            logout_image = Image.open(self.logout_icon_path)
            logout_image = logout_image.resize((40, 40), Image.LANCZOS)
            self.logout_photo = ImageTk.PhotoImage(logout_image)
            logout_icon = tk.Button(top_bar, image=self.logout_photo, bg=COLORS["top_bar"], bd=0, command=self.login_window.open_login_window)
            logout_icon.pack(side="right", padx=10)
        except Exception as e:
            self.silent_popup("Error", "Error loading Logout icon: {e}", self.play_Error)
        # Minimize icon
        try:
            if self.light:
                self.minimize_icon_path = os.path.join(BASE_DIR, "Static", "images", "minus-dark.png")
            elif not self.light:
                self.minimize_icon_path = os.path.join(BASE_DIR, "Static", "images", "minus-light.png")
            minimze_image = Image.open(self.minimize_icon_path)
            minimze_image = minimze_image.resize((40, 40), Image.LANCZOS)
            self.minimize_photo = ImageTk.PhotoImage(minimze_image)
            minimize_icon = tk.Button(top_bar, image=self.minimize_photo, bg=COLORS["top_bar"], bd=0, command=root.iconify)
            minimize_icon.pack(side="right", padx=10)
        except Exception as e:
            self.silent_popup("Error", "Error loading Minimize icon: {e}", self.play_Error)


        if show_back_button:
            try:
                if self.light:
                    self.back_icon_path = os.path.join(BASE_DIR, "Static", "images", "left-arrow-dark.png")
                elif not self.light:
                    self.back_icon_path = os.path.join(BASE_DIR, "Static", "images", "left-arrow-light.png")
                back_image = Image.open(self.back_icon_path)
                back_image = back_image.resize((40, 40), Image.LANCZOS)
                self.back_photo = ImageTk.PhotoImage(back_image)
                if Back_to_Database_Window:
                    back_icon = tk.Button(top_bar, image=self.back_photo, bg=COLORS["top_bar"], bd=0, command=self.manage_database_window)
                elif Back_to_Employee_Window:
                    back_icon = tk.Button(top_bar, image=self.back_photo, bg=COLORS["top_bar"], bd=0, command=self.manage_Employees_window)
                elif Back_to_Sales_Window:
                    back_icon = tk.Button(top_bar, image=self.back_photo, bg=COLORS["top_bar"], bd=0, command=self.manage_sales_invoices_window)
                elif Back_to_Purchases_Window:
                    back_icon = tk.Button(top_bar, image=self.back_photo, bg=COLORS["top_bar"], bd=0, command=self.manage_purchases_invoices_window)
                elif Back_to_Reports_Window:
                    back_icon = tk.Button(top_bar, image=self.back_photo, bg=COLORS["top_bar"], bd=0, command=self.manage_Reports_window)
                else:
                    back_icon = tk.Button(top_bar, image=self.back_photo, bg=COLORS["top_bar"], bd=0, command=self.main_menu)
                back_icon.pack(side="left", padx=10)
            except Exception as e:
                self.silent_popup("Error", "Error loading back icon: {e}", self.play_Error)
        else:
            lang_btn = tk.Button(top_bar, text=self.t("Change Language"), bg=COLORS["top_bar"], fg=COLORS["top_bar_icons"],
                                font=("Arial", 10, "bold"), bd=0, command=self.toggle_language)
            lang_btn.pack(side="left", padx=10)
            if self.light:
                lang_image = Image.open(self.dark_mode_img)
            elif not self.light:
                lang_image = Image.open(self.light_mode_img)
            lang_image = lang_image.resize((40, 40), Image.LANCZOS)
            self.lang_photo = ImageTk.PhotoImage(lang_image)
            lang_btn = tk.Button(top_bar, text=self.t("Change Language"),image=self.lang_photo, bg=COLORS["top_bar"], fg="black",
                                font=("Arial", 10, "bold"), bd=0, command=self.toggle_theme)
            lang_btn.pack(side="left", padx=10)

        # Left side: Language or Back button
        # tk.Button(top_bar, text="Open Calculator", command=open_calculator, font=("Arial", 14)).pack(side="left", padx=10)
        if self.light:
            self.calc_icon_path = os.path.join(BASE_DIR, "Static", "images", "calculator-dark.png")
        elif not self.light:
            self.calc_icon_path = os.path.join(BASE_DIR, "Static", "images", "calculator-light.png")
        calc_image = Image.open(self.calc_icon_path)
        calc_image = calc_image.resize((35, 35), Image.LANCZOS)
        self.calc_photo = ImageTk.PhotoImage(calc_image)
        calc_icon = tk.Label(top_bar, image=self.calc_photo, bg=COLORS["top_bar"])
        calc_icon.pack(side="left", padx=10)
        calc_icon.bind("<Button-1>", lambda event: open_calculator())
        
        # Time label
        time_label = tk.Label(top_bar, text=datetime.now().strftime('%B %d, %Y %I:%M %p'),
                            font=("Arial", 20, "bold"), fg=COLORS["top_bar_icons"], bg=COLORS["top_bar"])

        time_label.place(relx=0.5, rely=0.5, anchor="center")
        # self.update_time(time_label)
        #TODO
        # User info frame
        user_frame = tk.Frame(top_bar, bg=COLORS["top_bar"])
        user_frame.pack(side="right", padx=10)

        username_label = tk.Label(user_frame, text=self.user_name, font=("Arial", 20), fg=COLORS["top_bar_icons"], bg=COLORS["top_bar"])
        username_label.pack(side="left")
    
    def generate_report_data(self):
        return [
            ["Total Sales", "72000", "From 45 invoices"],
            ["Top Customer", "عماد خطاب", "EGP 70,000"],
            ["Total Items Sold", "320", "25 Products"]
        ]

    def export_to_excel(self, data, headers=["Metric", "Value", "Details"], filename="sales_report.xlsx"):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(headers)
        
        print(f"\nExporting to {filename}")  # Debug
        print(f"Headers: {headers}")  # Debug
        print(f"First 3 rows: {data[:3] if data else 'EMPTY'}")  # Debug
        
        for i, row in enumerate(data, 1):
            try:
                if isinstance(row, dict):
                    # Convert dict to ordered list
                    export_row = [str(row.get(header, "")) for header in headers]
                else:
                    # Convert to list and stringify all values
                    export_row = [str(item) for item in row]
                
                print(f"Row {i}: {export_row}")  # Debug
                ws.append(export_row)
                
            except Exception as e:
                print(f"Error processing row {i}: {e}\nRow content: {row}")
                continue
        
        wb.save(filename)
        print(f"Successfully saved to {filename}")  # Debug
        os.startfile(filename)


    def export_to_pdf(self, data, headers=None, title="Report", filename="report.pdf", report_folder="reports",
                    page_size=letter, font_size=12):
        """
        Complete PDF export function with full Arabic support
        
        Args:
            data: Data to export (list of dicts or lists)
            headers: Column headers (list)
            title: Report title (string)
            filename: Output filename (string)
            report_folder: Folder name on desktop (string)
            page_size: Page size (default: letter)
            font_size: Base font size (default: 12)
        
        Returns:
            str: Path to generated PDF if successful, None otherwise
        """
        def load_arabic_fonts():
            """Helper function to load Arabic fonts with fallback"""
            try:
                # Try to load custom Arabic font (Amiri)
                arabic_font_path = os.path.join("Static", "Fonts", "Amiri-Regular.ttf")
                if os.path.exists(arabic_font_path):
                    pdfmetrics.registerFont(TTFont('Arabic', arabic_font_path))
                    pdfmetrics.registerFont(TTFont('Arabic-Bold', arabic_font_path))
                    return True
            except Exception as e:
                print(f"Arabic font loading error: {e}")

            # Fallback to Arial if available
            try:
                pdfmetrics.registerFont(TTFont('Arabic', 'Arial'))
                pdfmetrics.registerFont(TTFont('Arabic-Bold', 'Arial-Bold'))
                return False
            except:
                return False

        def format_arabic(text):
            """Format Arabic text with proper shaping and direction"""
            if isinstance(text, str):
                reshaped = arabic_reshaper.reshape(text)
                return get_display(reshaped)
            return str(text)

        try:
            # 1. Load Arabic fonts
            arabic_font_available = load_arabic_fonts()
            font_name = 'Arabic' if arabic_font_available else 'Helvetica'
            
            # 2. Create output directory
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            report_folder_path = os.path.join(desktop, report_folder)
            os.makedirs(report_folder_path, exist_ok=True)
            pdf_path = os.path.join(report_folder_path, filename)
            
            # 3. Prepare PDF document
            doc = SimpleDocTemplate(pdf_path, pagesize=page_size)
            elements = []
            styles = getSampleStyleSheet()
            
            # 4. Configure styles for Arabic
            title_style = styles['Title']
            title_style.fontName = f'{font_name}-Bold'
            title_style.fontSize = font_size + 4
            title_style.alignment = 2  # Right alignment
            
            normal_style = styles['Normal']
            normal_style.fontName = font_name
            normal_style.alignment = 2
            
            # 5. Add title and spacing
            elements.append(Paragraph(format_arabic(title), title_style))
            elements.append(Spacer(1*inch, 0.25*inch))
            
            # 6. Prepare table data
            table_data = []
            
            # Process headers
            if headers:
                arabic_headers = [format_arabic(h) for h in headers]
                table_data.append(arabic_headers)
            
            # Process data rows
            for row in data:
                if isinstance(row, dict):
                    row_data = [format_arabic(row.get(h, "")) for h in headers] if headers else [format_arabic(v) for v in row.values()]
                else:
                    row_data = [format_arabic(item) for item in row]
                table_data.append(row_data)
            
            # 7. Create and style table
            table = Table(table_data, repeatRows=1)
            table.hAlign = 'RIGHT'
            
            style = TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4F81BD')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'RIGHT'),
                ('FONTNAME', (0,0), (-1,-1), font_name),
                ('FONTNAME', (0,0), (-1,0), f'{font_name}-Bold'),
                ('FONTSIZE', (0,0), (-1,-1), font_size),
                ('BOTTOMPADDING', (0,0), (-1,0), 12),
                ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#DCE6F1')),
                ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ('VALIGN', (0,0), (-1,-1), 'TOP')
            ])
            table.setStyle(style)
            elements.append(table)
            
            # 8. Generate PDF
            doc.build(elements)
            
            # 9. Try to open/print the file
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(pdf_path, "print")
                elif os.name == 'posix':  # Mac/Linux
                    subprocess.run(['lp', pdf_path], check=False)
            except Exception as e:
                messagebox.showerror(self.t("Print Error"), f"{self.t("Failed to print PDF:")}\n{e}")

            # 10. Show success message (in Arabic)
            messagebox.showinfo("نجاح", f"تم حفظ الملف بنجاح في:\n{pdf_path}")
            
            return pdf_path
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تصدير الملف:\n{str(e)}")
            return None

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

        self.topbar(show_back_button=True, Back_to_Reports_Window=True)

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
        
        ttk.Button(button_frame, text="Export to Excel", command=lambda: self.export_to_excel(data)).grid(row=0, column=0, padx=10)
        ttk.Button(button_frame, text="Export to PDF", command=lambda: self.export_to_pdf(data)).grid(row=0, column=1, padx=10)
    def trash(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # make the top bar with change language button
        self.topbar(show_back_button=True)
        
        # Create a main frame to center the message
        main_frame = tk.Frame(self.root)
        main_frame.pack(expand=True, fill='both')
        
        # Add big "Not Supported Yet" text
        not_supported_label = tk.Label(
            main_frame,
            text=self.t("NOT SUPPORTED YET"),
            font=("Arial", 32, "bold"),
            fg="red",
            pady=50
        )
        not_supported_label.pack(expand=True)


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

# class CalculatorPopup(tk.Toplevel):
#     def __init__(self, parent, target_entry=None):
#         super().__init__(parent)
#         self.title("Calculator")
#         self.target_entry = target_entry
#         self.geometry("300x400")

#         # Set window icon (shows in title bar and taskbar)
#         icon_path = os.path.join(BASE_DIR, "Static", "images", "Calculator.ico")
#         try:
#             if os.path.exists(icon_path):
#                 self.iconbitmap(icon_path)
#         except Exception as e:
#             print(f"Calculator icon error: {e}")

#         # Add a label at the top (with icon and text)
#         label_frame = tk.Frame(self)
#         label_frame.pack(fill="x", pady=8)

#         if os.path.exists(icon_path):
#             try:
#                 icon_img = Image.open(icon_path).resize((32, 32), Image.LANCZOS)
#                 icon_photo = ImageTk.PhotoImage(icon_img)
#                 icon_label = tk.Label(label_frame, image=icon_photo, bg="#fbd307")
#                 icon_label.image = icon_photo
#                 icon_label.pack(side="left", padx=5)
#             except Exception as e:
#                 print(f"Calculator icon image error: {e}")

#         title_label = tk.Label(label_frame, text="الآلة الحاسبة", font=("Arial", 16, "bold"), fg="#23272A", bg="#fbd307")
#         title_label.pack(side="left", padx=5)

#         self.create_widgets()
#         # ...existing code...
        
#     def create_widgets(self):
#         # Display
#         self.display = tk.Entry(self, font=('Arial', 24), justify='right', bd=10, bg="#23272A", fg="#FFFFFF")
#         self.display.grid(row=0, column=0, columnspan=4, sticky="nsew")
    
#         # Button layout with colors
#         buttons = [
#             # text, row, col, bg, fg
#             ('C', 1, 0, '#e74c3c', '#fff'),
#             ('(', 1, 1, '#ffa500', '#23272A'),
#             (')', 1, 2, '#ffa500', '#23272A'),
#             ('÷', 1, 3, '#ffa500', '#23272A'),
#             ('7', 2, 0, '#444', '#fff'),
#             ('8', 2, 1, '#444', '#fff'),
#             ('9', 2, 2, '#444', '#fff'),
#             ('x', 2, 3, '#ffa500', '#23272A'),
#             ('4', 3, 0, '#444', '#fff'),
#             ('5', 3, 1, '#444', '#fff'),
#             ('6', 3, 2, '#444', '#fff'),
#             ('-', 3, 3, '#ffa500', '#23272A'),
#             ('1', 4, 0, '#444', '#fff'),
#             ('2', 4, 1, '#444', '#fff'),
#             ('3', 4, 2, '#444', '#fff'),
#             ('+', 4, 3, '#ffa500', '#23272A'),
#             ('+/-', 5, 0, '#444', '#fff'),
#             ('0', 5, 1, '#444', '#fff'),
#             ('.', 5, 2, '#444', '#fff'),
#             ('=', 5, 3, '#27ae60', '#fff'),
#         ]
    
#         # Create buttons
#         for (text, row, col, bg, fg) in buttons:
#             btn = tk.Button(self, text=text, font=('Arial', 18, 'bold'), bg=bg, fg=fg,
#                             bd=0, activebackground=bg, activeforeground=fg,
#                             command=lambda t=text: self.on_button_click(t))
#             btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
    
#         # Configure grid weights
#         for i in range(6):
#             self.grid_rowconfigure(i, weight=1)
#         for i in range(4):
#             self.grid_columnconfigure(i, weight=1)
    
#     def on_button_click(self, text):
#         current = self.display.get()
        
#         if text == '=':
#             try:
#                 result = str(eval(current))
#                 self.display.delete(0, tk.END)
#                 self.display.insert(0, result)
#                 if self.target_entry:
#                     self.target_entry.delete(0, tk.END)
#                     self.target_entry.insert(0, result)
#             except:
#                 self.display.delete(0, tk.END)
#                 self.display.insert(0, "Error")
#         elif text == 'C':
#             self.display.delete(0, tk.END)
#         else:
#             self.display.insert(tk.END, text)

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


def open_calculator():
    calc_win = tk.Toplevel()
    calc_win.title("Calculator")
    calc_win.configure(bg="#2e2e2e")
    calc_win.resizable(False, False)

    # Set window icon (shows in title bar and taskbar)
    icon_path = os.path.join(BASE_DIR, "Static", "images", "calculator-1.ico")
    if os.path.exists(icon_path):
        try:
            calc_win.iconbitmap(icon_path)
        except Exception as e:
            print(f"Calculator icon error: {e}")

    # ...rest of your calculator code...

    entry = tk.Entry(calc_win, width=18, font=('Helvetica', 28), bd=0, bg="#1e1e1e", fg="white", justify='right')
    entry.grid(row=0, column=0, columnspan=4, pady=(10, 20), padx=10, ipady=20)

    # Button styles
    btn_config = {
        "font": ('Helvetica', 18),
        "bd": 0,
        "width": 5,
        "height": 2,
        "bg": "#3c3f41",
        "fg": "white",
        "activebackground": "#505354",
        "activeforeground": "white"
    }

    special_btn_config = {
        "=": {"bg": "#4caf50", "activebackground": "#45a049"},
        "C": {"bg": "#f44336", "activebackground": "#e53935"},
        "÷": {"bg": "#ff9800"},
        "x": {"bg": "#ff9800"},
        "-": {"bg": "#ff9800"},
        "+": {"bg": "#ff9800"},
        "()": {"bg": "#ff9800"},
        "%": {"bg": "#ff9800"},
    }

    def calculate(expression):
        """Safely evaluate a mathematical expression with percentage support"""
        try:
            # Replace symbols with Python operators
            expression = expression.replace('x', '*').replace('÷', '/')
            
            # Handle percentages by replacing them with their decimal equivalents
            # This needs to handle cases where % follows a number in an expression
            tokens = []
            current_token = ''
            
            for char in expression:
                if char.isdigit() or char == '.':
                    current_token += char
                else:
                    if current_token:
                        tokens.append(current_token)
                        current_token = ''
                    tokens.append(char)
            
            if current_token:
                tokens.append(current_token)
            
            # Process the tokens to handle percentages
            processed_tokens = []
            i = 0
            while i < len(tokens):
                token = tokens[i]
                if token == '%':
                    if i > 0 and tokens[i-1].replace('.', '').isdigit():
                        # Convert the previous number to percentage (divide by 100)
                        num = float(tokens[i-1]) / 100
                        processed_tokens[-1] = str(num)
                    else:
                        processed_tokens.append(token)
                else:
                    processed_tokens.append(token)
                i += 1
            
            # Rebuild the expression
            processed_expr = ''.join(processed_tokens)
            
            # Evaluate the expression
            return str(eval(processed_expr))
        except:
            return "Error"

    def on_click(value):
        current = entry.get()
        
        if value == '=':
            try:
                result = calculate(current)
                entry.delete(0, tk.END)
                entry.insert(tk.END, result)
            except:
                entry.delete(0, tk.END)
                entry.insert(tk.END, "Error")
        elif value == 'C':
            entry.delete(0, tk.END)
        elif value == '()':
            if '(' not in current:
                entry.insert(tk.END, '(')
            elif ')' not in current[current.index('('):]:
                entry.insert(tk.END, ')')
            else:
                entry.insert(tk.END, 'x(')
        elif value == '+/-':
            if current.startswith('-'):
                entry.delete(0)
            else:
                entry.insert(0, '-')
        elif value == '%':
            entry.insert(tk.END, '%')
        else:
            entry.insert(tk.END, value)

    buttons = [
        'C'  , '()', '%', '÷',
        '7'  , '8' , '9', 'x',
        '4'  , '5' , '6', '-',
        '1'  , '2' , '3', '+',
        '+/-', '0' , '.', '='
    ]

    row, col = 1, 0
    for btn in buttons:
        style = btn_config.copy()
        if btn in special_btn_config:
            style.update(special_btn_config[btn])

        pady_val = 5
        if row == 5:
            pady_val = 20  

        tk.Button(calc_win, text=btn, command=lambda b=btn: on_click(b), **style).grid(
            row=row, column=col, padx=5, pady=pady_val
        )

        col += 1
        if col >3:
            col = 0
            row += 1

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


##################################################################### Main #########################################################

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesSystemApp(root)       # Create main app first
    app.start_without_login()
    # app.start_with_login()     # Then launch the login screen through app

    try:
        root.mainloop()
    except Exception as e:
        print("Error during mainloop:", e)