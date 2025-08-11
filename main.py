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
import matplotlib
import matplotlib.pyplot as plt

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
from supplier_interactions import SupplierInteractions
from customer_interactions import CustomerInteractions

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

# PAGE_SIZES = {
#     "A1": A1,
#     "A2": A2,
#     "A3": A3,
#     "A4": A4,
#     "A5": A5,
#     "A6": A6,
#     "A7": A7,
# }

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
        
        # style.theme_create("modern", parent="alt", settings={
        #     "TFrame": {"configure": {"background": config.COLORS["background"]}},
        #     "TLabel": {
        #         "configure": {
        #             "background": config.COLORS["background"],
        #             "foreground": config.COLORS["text"],
        #             "font": self.custom_font
        #         }
        #     },
        #     "TButton": {
        #         "configure": {
        #             "anchor": "center",
        #             "relief": "flat",
        #             "background": config.COLORS["primary"],
        #             "foreground": config.COLORS["text"],
        #             "font": self.custom_font,
        #             "padding": 10
        #         },
        #         "map": {
        #             "background": [
        #                 ("active", config.COLORS["highlight"]),
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
        self.filtered_transactions_table = []
        self.production_entries = []
        # elif collection_name == "Sales_Header":
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
            "Export to PDF and Print":{"Arabic":"حفظ الملف وطباعته","English":"Export to PDF and Print"},
            "Daily treasury report":{"Arabic":"تقرير الخزنة اليومية","English":"Daily treasury report"},
            "Please select month and year":{"Arabic":"الرجاء تحديد الشهر والسنة","English":"Please select month and year"},
            "Logs":{"Arabic":"سجلات","English":"Logs"},
            "action":{"Arabic":"العملية","English":"Action"},
            "Action":{"Arabic":"العملية","English":"Action"},
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

            "Total Debit":{"Arabic":"إجمالي المدين","English":"Total Debit"},
            "Total Credit":{"Arabic":"إجمالي الدائن","English":"Total Credit"},            

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
            "Expense":{"Arabic": "مصروف", "English": "Expense"},
            "Revenue":{"Arabic": "إيراد", "English": "Revenue"},
            
            "Checked out with Id":{"Arabic": "تسجيل انصراف ب كود ", "English": "Checked out with Id"},
            "Checked in with Id":{"Arabic": "تسجيل دخول ب كود ", "English": "Checked in with Id"},
            "Generated PDF":{"Arabic": "توليد PDF", "English": "Generated PDF"},
            "Generated Pdf Purchase Invoice with Id":{"Arabic": "تم توليد فاتورة شراء PDF برقم", "English": "Generated Pdf Purchase Invoice with Id"},
            "Generated Excel":{"Arabic": "توليد Excel", "English": "Generated Excel"},
            "report":{"Arabic": "تقرير", "English": "report"},
            "Deleted a record from":{"Arabic": "حذف سجل من", "English": "Deleted a record from"},
            "Updated a record in":{"Arabic": "تحديث سجل في", "English": "Updated a record in"},
            "Added new record to":{"Arabic": "إضافة سجل جديد إلى", "English": "Added new record to"},
            "Added new record in":{"Arabic": "إضافة سجل جديد في", "English": "Added new record in"},

            "Recorded Expense of":{"Arabic": "تسجيل مصروفات", "English": "Recorded Expense of"},
            "Recorded Revenue of":{"Arabic": "تسجيل إيرادات", "English": "Recorded Revenue of"},
            "in general_exp_rev Database":{"Arabic": "في قاعدة بيانات المصروفات والايرادات العامة", "English": "in general_exp_rev Database"},

            "Paid salary for":{"Arabic": "تم دفع المرتب إلى", "English": "Paid salary for"},
            "with code":{"Arabic": "ب كود", "English": "with code"},
            "Completed withdrawal in Employee_withdrawls Database for":{"Arabic": "تم إتمام", "English": "Completed withdrawal in Employee_withdrawls Database for"},
            "with Id":{"Arabic": "ب كود", "English": "with Id"},

            "Database with Unique Id": {"Arabic": "قاعدة بيانات ذات معرف فريد", "English": "Database with Unique Id"},
            "Completed withdrawal in Employee_withdrawls Database for":{"Arabic": "تم إتمام عملية السحب في قاعدة بيانات المسحوبات إلى", "English": "Completed withdrawal in Employee_withdrawls Database for"},
            "with Id":{"Arabic": "ب كود", "English": "with Id"},

            "Exit the application":{"Arabic": "قفل التطبيق", "English": "Exit the application"},
            "logout from the application":{"Arabic": "سجل خروج من التطبيق", "English": "logout from the application"},
            "login to the application":{"Arabic": "سجل دخول الي التطبيق", "English": "login to the application"},



            "Updated new invoice to":{"Arabic": "تم تحديث الفاتورة الجديدة إلى", "English": "Updated new invoice to"},
            "Added invoice to":{"Arabic": "تمت إضافة الفاتورة إلى", "English": "Added invoice to"},
            "Generated Pdf Purchase Invoice with Id":{"Arabic": "فاتورة شراء تم إنشاؤها بصيغة PDF مع معرف", "English": "Generated Pdf Purchase Invoice with Id"},
            "for supplier":{"Arabic": "للمورد", "English": "for supplier"},
            "Deleted":{"Arabic": "تم الحذف", "English": "Deleted"},


            "Updated invoice to":{"Arabic": "تم تحديث الفاتورة إلى", "English": "Updated invoice to"},
            "Added new invoice to":{"Arabic": "تمت إضافة فاتورة جديدة إلى", "English": "Added new invoice to"},
            "Generated Pdf Sales Invoice with Id":{"Arabic": "فاتورة مبيعات مُنشأة بصيغة PDF مع رقم تعريفي", "English": "Generated Pdf Sales Invoice with Id"},
            "for Customer":{"Arabic": "للعميل", "English": "for Customer"},

            "Employee:":{"Arabic": "الموظف:", "English": "Employee:"},
            # "":{"Arabic": "", "English": ""},
            # "":{"Arabic": "", "English": ""},
            # "":{"Arabic": "", "English": ""},




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
        self.user_id = None  # Placeholder for user ID
        self.all_customers = None  # Will be loaded on first search
        self._after_id = None

        # self.app.start_date_entry = None
        # self.app.end_date_entry = None
        # self.app.total_debit_entry = None
        # self.app.total_credit_entry = None
        # self.app.balance_entry = None

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
        self.SupplierInteractions = SupplierInteractions(self.root, self)
        self.CustomerInteractions = CustomerInteractions(self.root, self)
        # icon_image = Image.open(icon_path).resize((16, 16))  # Resize to fit in the button
        # self.lang_icon = ImageTk.PhotoImage(icon_image)
    
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
                {"text": self.t("Sales Invoice"), "image": "sales_invoice-dark.png",
                "command": lambda: self.SalesInvoice.manage_sales_invoices_window()},
                {"text": self.t("Purchase Invoice"), "image": "purchases_invoice-dark.png", 
                "command": lambda: self.PurchaseInvoice.manage_purchases_invoices_window()},
                {"text": self.t("Receive Payment"), "image": "customer_payment-dark.png", 
                "command": lambda: self.customer_interactions(self.user_role)},
                {"text": self.t("Make Payment"), "image": "supplier_payment-dark.png", 
                "command": lambda: self.supplier_interactions(self.user_role)},
                {"text": self.t("Production Order"), "image": "production-dark.png", 
                "command": lambda: self.ProductionOrder.new_production_order(self.user_role)},
                {"text": self.t("Employee interactions"), "image": "employee-dark.png", 
                "command": lambda: self.EmployeeWindow.manage_Employees_window()},
                {"text": self.t("Treasury"), "image": "treasury-dark.png", 
                "command": lambda: self.TreasuryWindow.Treasury_window(self.user_role)},
                {"text": self.t("General_Exp_And_Rev"), "image": "financial-dark.png", 
                "command": lambda: self.GeneralExpRev.general_exp_rev(self.user_role)},
                {"text": self.t("Reports"), "image": "report-dark.png", 
                "command": lambda: self.reports.manage_Reports_window()},
                {"text": self.t("Logs"), "image": "logs-dark.png", 
                "command": lambda: self.Logs_window()},
            ]
            
            if self.user_role == "admin" or self.user_role == "developer":
                buttons.extend([
                    {"text": self.t("Database"), "image": "database-dark.png", 
                    "command": lambda: self.check_access_and_open(self.user_role)}
                ])
        elif not self.light:
            # Define buttons with images, text, and commands
            buttons = [
                {"text": self.t("Sales Invoice"), "image": "sales_invoice-light.png",
                "command": lambda: self.SalesInvoice.manage_sales_invoices_window()},
                {"text": self.t("Purchase Invoice"), "image": "purchases_invoice-light.png", 
                "command": lambda: self.PurchaseInvoice.manage_purchases_invoices_window()},
                {"text": self.t("Receive Payment"), "image": "customer_payment-light.png", 
                "command": lambda: self.CustomerInteractions.customer_interactions(self.user_role)},
                {"text": self.t("Make Payment"), "image": "supplier_payment-light.png", 
                "command": lambda: self.SupplierInteractions.supplier_interactions(self.user_role)},
                {"text": self.t("Production Order"), "image": "production-light.png", 
                "command": lambda: self.ProductionOrder.new_production_order(self.user_role)},
                {"text": self.t("Employee interactions"), "image": "employee-light.png", 
                "command": lambda: self.EmployeeWindow.manage_Employees_window()},
                {"text": self.t("Treasury"), "image": "treasury-light.png", 
                "command": lambda: self.TreasuryWindow.Treasury_window(self.user_role)},
                {"text": self.t("General_Exp_And_Rev"), "image": "financial-light.png", 
                "command": lambda: self.GeneralExpRev.general_exp_rev(self.user_role)},
                {"text": self.t("Reports"), "image": "report-light.png", 
                "command": lambda: self.reports.manage_Reports_window()},
                {"text": self.t("Logs"), "image": "logs-light.png", 
                "command": lambda: self.Logs_window()},
            ]

            if self.user_role == "admin" or self.user_role == "developer":
                buttons.extend([
                    {"text": self.t("Database"), "image": "database-light.png", 
                    "command": lambda: self.check_access_and_open(self.user_role)}
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
            # chatbot_icon_path = os.path.join(BASE_DIR, "Static", "images", "chatbot_icon.png")
            # chatbot_img = Image.open(chatbot_icon_path).resize((60, 60), Image.LANCZOS)
            # self.chatbot_main_photo = ImageTk.PhotoImage(chatbot_img)
            # self.chatbot_main_btn = tk.Label(self.root, image=self.chatbot_main_photo, bg=config.COLORS["card"], cursor="hand2")
            # self.chatbot_main_btn.place(x=20, y=780)  # Initial position
            # chatbot_icon_path = os.path.join(BASE_DIR, "Static", "images", "chatbot.gif")
            # self.chatbot_main_photo = tk.PhotoImage(file=chatbot_icon_path)
            # self.chatbot_main_btn = tk.Label(self.root, image=self.chatbot_main_photo, bg=config.COLORS["card"], cursor="hand2")
            # self.chatbot_main_btn.place(x=20, y=780)

            # self.chatbot_main_btn.bind("<Button-1>", start_drag)
            # self.chatbot_main_btn.bind("<B1-Motion>", do_drag)
            # self.chatbot_main_btn.bind("<ButtonRelease-1>", lambda e: self.open_chatbot())
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


    def employee_hours_window(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()
        

        self.topbar.topbar(show_back_button=True, Back_to_Employee_Window=True)
        
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
                check_out_time = datetime.now()
                duration = check_out_time - existing['check_in']
                
                appointments_col.update_one(
                    {'_id': existing['_id']},
                    {'$set': {
                        'check_out': check_out_time,
                        'duration': duration.total_seconds() / 3600  # in hours
                    }}
                )
                config.report_log(self.logs_collection, self.user_name, None, f"{existing['employee_name']} {self.t("Checked out with Id")} {existing['employee_code']}", None)

            else:
                # Check in
                appointments_col.insert_one({
                    'employee_code': code,
                    'employee_name': name,
                    'check_in': datetime.now(),
                    'check_out': None,
                    'duration': None
                })
                config.report_log(self.logs_collection, self.user_name, None, f"{name} {self.t("Checked in with Id")} {code}", None)

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

        self.topbar.topbar(show_back_button=True, Back_to_Employee_Window=True)

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
            
            config.report_log(self.logs_collection, self.user_name, None, f"{self.t("Completed withdrawal in Employee_withdrawls Database for")} {withdrawal_data['employee_name']} {self.t("with Id")} {withdrawal_data['employee_code']}", None)

            self.amount_entry.delete(0, tk.END)
            self.payment_method.set('')
            self.update_previous_withdrawals()

        except PyMongoError as e:
            messagebox.showerror(self.t("Database Error"), f"{self.t("Failed to save withdrawal:")} {str(e)}")

    def employee_statistics_window(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.topbar.topbar(show_back_button=True, Back_to_Employee_Window=True)
        
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

        ttk.Label(date_frame, text=self.t("From Date:")).grid(row=0, column=4, padx=5, sticky='e')
        self.from_date_var = tk.StringVar()
        self.to_date_var = tk.StringVar()
        # Replace the Entry widgets with:
        DateEntry(date_frame, textvariable=self.from_date_var, date_pattern='dd-mm-yyyy').grid(row=0, column=5)
        ttk.Label(date_frame, text=self.t("To Date:")).grid(row=0, column=6, padx=5, sticky='e')
        DateEntry(date_frame, textvariable=self.to_date_var, date_pattern='dd-mm-yyyy').grid(row=0, column=7)
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
        self.from_date_var.trace_add('write', self.load_attendance_data)
        self.to_date_var.trace_add('write', self.load_attendance_data)
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
        
        # Get selected dates
        from_date_str = self.from_date_var.get()
        to_date_str = self.to_date_var.get()
        employee_code = self.emp_code_var.get()
        
        if not all([from_date_str, to_date_str, employee_code]):
            return
        
        # Parse dates (assuming format DD-MM-YYYY as in your image)
        try:
            from_date = datetime.strptime(from_date_str, "%d-%m-%Y")
            to_date = datetime.strptime(to_date_str, "%d-%m-%Y")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use DD-MM-YYYY")
            return
        
        # Get collections
        withdrawals_col = self.get_collection_by_name("Employee_withdrawls")
        hours_col = self.get_collection_by_name("Employee_appointimets")
        
        # Get data - include end date by adding 1 day to to_date
        withdrawals = list(withdrawals_col.find({
            'employee_code': employee_code,
            'timestamp': {'$gte': from_date, '$lte': to_date + timedelta(days=1)}
        }))
        
        attendance = list(hours_col.find({
            'employee_code': employee_code,
            'check_in': {'$gte': from_date, '$lte': to_date + timedelta(days=1)}
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
        current_date = from_date
        while current_date <= to_date:
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
            if not self.month_var.get() or not self.year_var.get():
                messagebox.showinfo(self.t("Warning"), self.t("Please select month and year")) 
                return           
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
            config.report_log(self.logs_collection, self.user_name, None, f"{self.t("Paid salary for")} {salary_data['employee_name']} {self.t("with code")} {salary_data['employee_code']}", None)
            
        except Exception as e:
            messagebox.showerror(self.t("Error"), f"{self.t("Failed to save salary:")} {str(e)}")

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
            messagebox.showinfo(self.t("Success"), f"{self.t(transaction_type)} {self.t("recorded successfully!")}")
            config.report_log(self.logs_collection, self.user_name, None, f"{self.t(f"Recorded {transaction_type} of")} {amount} {self.t(f"in {self.general_exp_rev_collection.name} Database")}", None)

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

        tk.Label(filter_frame, text=self.t("From Date:")).pack(side=tk.LEFT)
        from_date = DateEntry(filter_frame, date_pattern="dd/mm/yyyy")
        from_date.pack(side=tk.LEFT, padx=5)
        
        # self.end_date_entry = DateEntry(right_frame, font=("Arial", 12), date_pattern='dd-MM-yyyy', width=14)
        
        tk.Label(filter_frame, text=self.t("To Date:")).pack(side=tk.LEFT)
        to_date = DateEntry(filter_frame, date_pattern="dd/mm/yyyy")
        to_date.pack(side=tk.LEFT, padx=5)

        employees_names = self.employees_collection.find({}, {"Name": 1})
        names = [doc.get("Name", "") for doc in employees_names]
        
        tk.Label(filter_frame, text=self.t("Employee:")).pack(side=tk.LEFT)
        employee_var = tk.StringVar()
        employee_cb = ttk.Combobox(filter_frame, textvariable=employee_var, values= names)
        employee_cb.pack(side=tk.LEFT, padx=5)

        search_btn = tk.Button(filter_frame, text=self.t("Search"), command=lambda: self.load_logs(tree, from_date.get_date(), to_date.get_date(), employee_var.get()))
        search_btn.pack(side=tk.LEFT, padx=10)

        # Logs Table
        columns = ("date", "employee_name", "action")
        tree = ttk.Treeview(main_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=self.t(col.replace("_", " ").title()))
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


############################ Utility Functions ########################################
    def check_access_and_open(self, role):
        allowed_roles = ["admin","developer"]  # Define roles that can access this
        if role in allowed_roles:
            # self.manage_old_database_window(db_name, table_name)
            self.manage_database_window()
        else:
            messagebox.showwarning(self.t("Access Denied"), self.t("You do not have permission to access this page."))

    def clean_materials_collection(self):
        """Remove leading/trailing spaces and newlines from all string attributes in Materials collection."""
        materials_col = config.get_collection_by_name("Materials")
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
        customers_col = config.get_collection_by_name("Customers")
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
        suppliers_col = config.get_collection_by_name("Suppliers")
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
        products_col = config.get_collection_by_name("Products")
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
        employees_col = config.get_collection_by_name("Employees")
        for doc in employees_col.find():
            updated_fields = {}
            for key, value in doc.items():
                if isinstance(value, str):
                    cleaned = value.strip()
                    updated_fields[key] = cleaned
            if updated_fields:
                employees_col.update_one({"_id": doc["_id"]}, {"$set": updated_fields})

    def on_canvas_press(self, event):
        self.tree.scan_mark(event.x, event.y)

    def on_canvas_drag(self, event):
        self.tree.scan_dragto(event.x, event.y, gain=1)

    # Update scroll region dynamically
    def update_scroll_region(self, event=None):
        self.tree.configure(scrollregion=self.tree.bbox("all"))


    # To get the text button based on language
    def t(self, text):
        return self.translations.get(text, {}).get(self.language, text)

    # Function to toggle from Arabic to English and Vicaverse
    def toggle_language(self):
        self.language = "English" if self.language == "Arabic" else "Arabic"
        self.main_menu()   

    def toggle_theme(self):
        if self.light:
            self.light = False
        elif not self.light:
            self.light = True
        if config.COLORS["background"] == "#F5F7FA":
            config.COLORS["background"]    = "#121212"   # Dark background (not pure black)
            config.COLORS["primary"]       = "#3B82F6"   # Soft light text (from light mode #2A3F5F)
            config.COLORS["main_frame"]    = "#2A3F5F"   # Soft light text (from light mode #2A3F5F)
            config.COLORS["secondary"]     = "#00C0A3"   # Keep same – good contrast on dark
            config.COLORS["accent"]        = "#FF6F61"   # Keep same – bright accent
            config.COLORS["text"]          = "#FFFFFF"   # Bright white for main text
            config.COLORS["card"]          = "#1E1E1E"   # Dark card background (soft contrast)
            config.COLORS["chart1"]        = "#00C0A3"   # Same – stands out on dark
            config.COLORS["chart2"]        = "#FF6F61"   # Same – bright red works well
            config.COLORS["highlight"]     = "#9B6EF3"   # Softer version of #6C5CE7 for dark
            config.COLORS["table_header"]  = "#2C2C2C"   # Dark header with slight elevation
            config.COLORS["positive"]      = "#03DAC6"   # Material-style teal (greenish)
            config.COLORS["neutral"]       = "#888888"   # Neutral gray for muted UI
            config.COLORS["top_bar"]       = "#23272A"   # <-- New dark mode top bar color
            config.COLORS["top_bar_icons"] = "#fbd307"   # <-- New dark mode user info color
        else:
            config.COLORS["background"]    = "#F5F7FA"
            config.COLORS["primary"]       = "#3B82F6"
            config.COLORS["main_frame"]    = "#2A3F5F"
            config.COLORS["secondary"]     = "#00C0A3"
            config.COLORS["accent"]        = "#FF6F61"
            config.COLORS["text"]          = "#2A3F5F"
            config.COLORS["card"]          = "#FFFFFF"
            config.COLORS["chart1"]        = "#00C0A3"
            config.COLORS["chart2"]        = "#FF6F61"
            config.COLORS["highlight"]     = "#6C5CE7"
            config.COLORS["table_header"]  = "#2A3F5F"
            config.COLORS["positive"]      = "#00C0A3"
            config.COLORS["neutral"]       = "#A0AEC0"
            config.COLORS["top_bar"]       = "#dbb40f"   # <-- Original light mode top bar color
            config.COLORS["top_bar_icons"] = "#000000"   # <-- Original light mode user info color
        self.main_menu()

    #Function to update the time 
    # def update_time(self, time_label):
    #     time_label.config(text=datetime.now().strftime('%B %d, %Y %I:%M %p'))
    #     self.root.after(1000, self.update_time, time_label)
    
    def handle_logout(self):
        if self.user_id:
            self.employees_collection.update_one(
                {"_id": self.user_id},
                {"$set": {
                    "logged_in": False,
                    "last_number_of_msgs": self.last_number_of_msgs
                }})
        config.report_log(self.logs_collection, self.user_name, None, f"{self.user_name} {self.t("logout from the application")}", None)
        self.login_window.open_login_window()

    def on_app_exit(self):
        if self.user_id:
            self.employees_collection.update_one(
                {"_id": self.user_id},
                {"$set": {
                    "logged_in": False,
                    "last_number_of_msgs": self.last_number_of_msgs
                }})
        config.report_log(self.logs_collection, self.user_name, None, f"{self.user_name} {self.t("Exit the application")}", None)
        self.root.quit()

        
    def export_to_excel(self, data, headers=None, title="Report", filename="report.xlsx", report_folder="reports",
                    startdate=None, enddate=None, footerline_out_of_table=None, source= None):
        """
        Enhanced Excel export function with date range display and comprehensive error handling
        
        Args:
            data: Data to export (list of dicts or lists)
            headers: Column headers (list)
            title: Report title (string)
            filename: Output filename (string)
            report_folder: Folder name on desktop (string)
            startdate: Start date for report (optional)
            enddate: End date for report (optional)
            footerline_out_of_table: Footer text (optional)
        
        Returns:
            str: Path to generated file if successful, None otherwise
        """
        try:
            # Create workbook and worksheet
            wb = openpyxl.Workbook()
            ws = wb.active
            
            # Set up output paths
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            report_path = os.path.join(desktop, report_folder)
            os.makedirs(report_path, exist_ok=True)
            file_path = os.path.join(report_path, filename)
            
            # Add title at the top
            if title:
                ws.append([title])
                ws.append([])  # Empty row for spacing
            
            # Add date range if provided
            if startdate or enddate:
                date_text = ""
                if startdate:
                    # Handle both string and datetime objects
                    if isinstance(startdate, datetime):
                        startdate = startdate.strftime("%Y-%m-%d")
                    date_text += f"From: {startdate} "
                if enddate:
                    if isinstance(enddate, datetime):
                        enddate = enddate.strftime("%Y-%m-%d")
                    date_text += f"To: {enddate}"
                
                ws.append([date_text])
                ws.append([])  # Empty row for spacing
            
            # Auto-detect headers if not provided
            if headers is None:
                if data and isinstance(data[0], dict):
                    headers = list(data[0].keys())
                elif data and isinstance(data[0], (list, tuple)):
                    headers = [f"Column {i+1}" for i in range(len(data[0]))]
            
            # Add headers if available
            if headers:
                ws.append(headers)
            
            # Process data rows
            for i, row in enumerate(data, 1):
                try:
                    if isinstance(row, dict):
                        # Handle dictionary rows
                        row_data = []
                        for header in headers:
                            val = row.get(header, "")
                            # Convert datetime objects to strings
                            if isinstance(val, datetime):
                                val = val.strftime("%Y-%m-%d %H:%M:%S")
                            row_data.append(str(val))
                    else:
                        # Handle list/tuple rows
                        row_data = []
                        for item in row:
                            if isinstance(item, datetime):
                                item = item.strftime("%Y-%m-%d %H:%M:%S")
                            row_data.append(str(item))
                    
                    ws.append(row_data)
                    
                except Exception as e:
                    print(f"Error processing row {i}: {str(e)}")
                    continue
            
            # Add footer if provided (with spacing)
            if footerline_out_of_table:
                ws.append([])  # Empty row for spacing
                if isinstance(footerline_out_of_table, (list, tuple)):
                    for line in footerline_out_of_table:
                        ws.append([str(line)])
                else:
                    ws.append([str(footerline_out_of_table)])
            
            # Auto-adjust column widths
            for col in ws.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = (max_length + 2) * 1.2
                ws.column_dimensions[column].width = adjusted_width
            
            # Save and open the file
            wb.save(file_path)

            config.report_log(self.logs_collection, self.user_name, None, f"{self.t('Generated Excel')} {source} {self.t('report')}", None)

            # Open the file if supported by OS
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # Mac/Linux
                subprocess.run(['open', file_path], check=False)
            # 10. Show success message (in Arabic)
            messagebox.showinfo("نجاح", f"تم حفظ الملف بنجاح في:\n{file_path}")                
            return file_path
        
        except Exception as e:
            error_msg = f"Failed to export Excel file: {str(e)}"
            print(error_msg)
            messagebox.showerror("Export Error", error_msg)
            return None

    def export_to_pdf(self, data, headers=None, title="Report", filename="report.pdf", report_folder="reports",
                    page_size=letter, font_size=12, startdate=None, enddate=None, footerline_out_of_table=None, source= None):
        """
        Enhanced PDF export function with PyInstaller-compatible font handlingz
        """
        def get_font_path():
            """Get the correct font path for both development and EXE"""
            try:
                if getattr(sys, 'frozen', False):  # Running in EXE
                    base_path = sys._MEIPASS
                else:  # Running in development
                    base_path = os.path.dirname(__file__)
                
                font_path = os.path.join(base_path, "Static", "Fonts", "Amiri-Regular.ttf")
                if os.path.exists(font_path):
                    return font_path
                return None
            except Exception as e:
                print(f"Font path error: {e}")
                return None

        def load_arabic_fonts():
            """Load Arabic fonts with fallback handling"""
            try:
                font_path = get_font_path()
                if font_path:
                    pdfmetrics.registerFont(TTFont('Arabic', font_path))
                    pdfmetrics.registerFont(TTFont('Arabic-Bold', font_path))
                    return True
            except Exception as e:
                print(f"Font loading error: {e}")
            
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
            # Load fonts
            arabic_font_loaded = load_arabic_fonts()
            font_name = 'Arabic' if arabic_font_loaded else 'Helvetica'
            print(f"Using font: {font_name}")  # Debug output
            
            # Create output directory
            desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
            report_path = os.path.join(desktop, report_folder)
            os.makedirs(report_path, exist_ok=True)
            pdf_path = os.path.join(report_path, filename)

            # Prepare PDF document
            doc = SimpleDocTemplate(pdf_path, pagesize=page_size)
            elements = []
            styles = getSampleStyleSheet()

            # Configure styles
            title_style = styles['Title']
            title_style.fontName = f'{font_name}-Bold'
            title_style.fontSize = font_size + 4
            title_style.alignment = 2  # Right align for Arabic

            date_style = styles['Normal']
            date_style.fontName = font_name
            date_style.fontSize = font_size - 2
            date_style.alignment = 0  # Left align

            # Add date range if provided
            if startdate or enddate:
                date_text = ""
                if startdate:
                    date_text += f"From: {startdate} "
                if enddate:
                    date_text += f"To: {enddate}"
                elements.append(Paragraph(format_arabic(date_text), date_style))
                elements.append(Spacer(1, 10))

            # Add title
            elements.append(Paragraph(format_arabic(title), title_style))
            elements.append(Spacer(1, 20))

            # Prepare table data
            table_data = []
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

            # Create and style table
            table = Table(table_data, repeatRows=1)
            # Center the entire table on the page
            table.hAlign = 'CENTER'

            style = TableStyle([
                # Header styling
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4F81BD')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,0), 'CENTER'),  # Center header text
                ('FONTNAME', (0,0), (-1,0), f'{font_name}-Bold'),
                ('FONTSIZE', (0,0), (-1,0), font_size),
                ('BOTTOMPADDING', (0,0), (-1,0), 12),
                
                # Body styling
                ('ALIGN', (0,1), (-1,-1), 'CENTER'),  # Center all body cells
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),  # Vertical center
                ('FONTNAME', (0,1), (-1,-1), font_name),
                ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#DCE6F1')),
                ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ])
            table.setStyle(style)
            elements.append(table)

            # Add footer if provided
            if footerline_out_of_table:
                footer_style = styles['Normal']
                footer_style.fontName = font_name
                footer_style.alignment = 2  # Center alignment
                footer_style.fontSize = font_size + 1
                
                # Increase vertical space before footer (changed from 20 to 30)
                elements.append(Spacer(1, 30))  # Increased space before footer
                
                if isinstance(footerline_out_of_table, list):
                    for i, line in enumerate(footerline_out_of_table):
                        elements.append(Paragraph(format_arabic(line), footer_style))
                        # Add space after each line except the last one
                        if i < len(footerline_out_of_table) - 1:
                            elements.append(Spacer(1, 15))  # Space between footer lines
                else:
                    elements.append(Paragraph(format_arabic(footerline_out_of_table), footer_style))

            # Generate PDF
            doc.build(elements)
            config.report_log(self.logs_collection, self.user_name, None, f"{self.t('Generated PDF')} {source} {self.t('report')}", None)
            # Try to open/print
            try:
                if os.name == 'nt':
                    os.startfile(pdf_path, "print")
                elif os.name == 'posix':
                    subprocess.run(['lp', pdf_path], check=False)
            except Exception as e:
                messagebox.showerror(self.t("Print Error"), f"{self.t('Failed to print PDF:')}\n{e}")

            messagebox.showinfo("نجاح", f"تم حفظ الملف بنجاح في:\n{pdf_path}")
            return pdf_path
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تصدير الملف:\n{str(e)}")
            return None


    def trash(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # make the top bar with change language button
        self.topbar.topbar(show_back_button=True)
        
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


def get_type(var):
    return type(var).__name__

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