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
                "command": lambda: self.customer_interactions(self.user_role)},
                {"text": self.t("Make Payment"), "image": "supplier_payment-light.png", 
                "command": lambda: self.supplier_interactions(self.user_role)},
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
            tree.column(col, anchor="center")  # This centers the content

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
                            text=self.t("Export to Excel"), 
                            command=lambda: self.export_to_excel(self.raw_tree_data,headers=headers,filename= f"كشف_حساب_للعميل_{clean_filename(self.report_customer_name)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
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
                            text=self.t("Export to PDF and Print"),
                            command=lambda: self.export_to_pdf(self.raw_tree_data,headers=headers,filename= f"كشف_حساب_للعميل_{clean_filename(self.report_customer_name)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
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
            messagebox.showerror(self.t("Error"), self.t("All fields must be filled!"))
            return

        try:
            debit_val = float(debit)
        except ValueError:
            messagebox.showerror(self.t("Error"), self.t("Cash must be a valid number."))
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
        config.report_log(self.logs_collection, self.user_name, supplier_payment_collection, f"{self.t("Added new record to")}", doc, self.t)
        messagebox.showinfo(self.t("Success"), f"{self.t("Entry")} {operation_number} {self.t("added.")}")

    def add_customer_payment(self, tree):
        credit = self.cash_entry.get().strip()
        payment_method = self.payment_entry.get().strip()
        customer_code = self.customer_code_cb.get().strip()
        customer_name = self.customer_name_cb.get().strip()
        customer_payment_collection = config.get_collection_by_name("Customer_Payments")
        sales_collection = config.get_collection_by_name("Sales")
        
        if not credit or not payment_method or not customer_code or not customer_name:
            messagebox.showerror(self.t("Error"), self.t("All fields must be filled!"))
            return

        try:
            credit_val = float(credit)
        except ValueError:
            messagebox.showerror(self.t("Error"), self.t("Cash must be a valid number."))
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
        config.report_log(self.logs_collection, self.user_name, customer_payment_collection, f"{self.t("Added new record to")}", doc, self.t)
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
                messagebox.showerror(self.t("Database Error"), f"{self.t("Failed to process code:")} {selected_code}.\n{self.t("Error")}: {str(e)}")
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
        tk.Label(left_frame, text=self.t("Cash"), font=("Arial", 12)).pack(pady=10, anchor="w", padx=10)
        self.cash_entry = tk.Entry(left_frame, font=("Arial", 12))
        self.cash_entry.pack(pady=5, padx=10, fill="x")

        tk.Label(left_frame, text=self.t("Payment Method"), font=("Arial", 12)).pack(pady=10, anchor="w", padx=10)
        selected_method = tk.StringVar()
        self.payment_entry = ttk.Combobox(left_frame, textvariable=selected_method, values=['Cash', 'E_Wallet', 'Bank_account', 'Instapay'], state="readonly", width=18)
        self.payment_entry.pack(pady=5, padx=10, fill="x")
        self.payment_entry.set(self.t("Cash"))  

        add_btn = tk.Button(left_frame, text=self.t("Add Entry"), width=35, 
                            command=lambda: self.add_customer_payment(tree))
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

        self.customer_code_cb.bind("<<ComboboxSelected>>", lambda event: self.on_code_selected(
                                        event, self.customer_code_cb, self.customer_name_cb, 
                                        self.customer_collection, self.sales_collection, self.customer_payment_collection, 
                                        "Customer_info.code", tree))
        self.customer_name_cb.bind("<<ComboboxSelected>>", lambda event: self.on_name_selected(
                                        event, self.customer_code_cb, self.customer_name_cb, 
                                        self.customer_collection, self.sales_collection, self.customer_payment_collection, 
                                        "Customer_info.code", tree))
        
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
            tree.column(col, anchor="center")  # This centers the content

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
                            text=self.t("Export to Excel"), 
                            command=lambda: self.export_to_excel(self.raw_tree_data,headers=headers,filename= f"كشف_حساب_للعميل_{clean_filename(self.report_customer_name)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
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
                            text=self.t("Export to PDF and Print"),
                            command=lambda: self.export_to_pdf(self.raw_tree_data,headers=headers,filename= f"كشف_حساب_للعميل_{clean_filename(self.report_customer_name)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
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