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


translations = {
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

PAGE_SIZES = {
    "A1": A1,
    "A2": A2,
    "A3": A3,
    "A4": A4,
    "A5": A5,
    "A6": A6,
    "A7": A7,
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

LOCKED_FIELDS = {
    "root": [ "Operation_Number","Code","employee_code", "material_code", "product_code", "Receipt_Number", "Operation_Number"],
    "Customer_info": ["code"],
    "supplier_info": ["code"],
    "Items": ["material_code","product_code"]
}

ZEROED_FIELDS = {
    "Sales_grade", "Growth_grade", "Frequency_grade", "Credit", "Debit", "Balance", "Sales"
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

MANDATORTY_FIELDS = { # list all mandatory fields (fields that can't be empty)
    "Name", "Phone_number1", "Code", "Company_address", "Name", "Password", "Role", "Phone_number", "Address", "Salary",
    "product_name","category","stock_quantity","Unit_Price","product_code","Units",
    "material_name","material_code", "employee_code", "employee_name"
}

def report_log(logs_collection, user_name, current_collection, msg, entry_doc=None, translation_func=None):
    if current_collection is not None:
        primary_key_field = PRIMARY_KEYS.get(current_collection.name, "_id")
        unique_id = entry_doc.get(primary_key_field, 'N/A') if entry_doc else 'N/A'
        action_text = f"{msg} {translation_func(current_collection.name)} {translation_func("Database with Unique Id")} {unique_id}"
    else:
        action_text = msg
    name = user_name if user_name else "Unknown"
    new_log = {
        "date": datetime.now(),
        "employee_name": name,
        "action": action_text
        # "action": f"Added new record to {collection_name} Database with unique Id {unique_id if unique_id else 'N/A'}",
    }
    logs_collection.insert_one(new_log)
    trim_logs_collection(logs_collection)

def get_next_code(payment_collection):
    last_entry = payment_collection.find_one(
        {"code": {"$regex": r"^GEN-?\d+"}},
        sort=[("code", -1)]
    )
    if last_entry and "code" in last_entry:
        last_num = int(last_entry["code"].split("-")[1])
        return f"GEN-{last_num+1:05d}"
    return "GEN-00001"

def get_next_operation_number(payment_collection):
    last_entry = payment_collection.find_one(
        {"Operation_Number": {"$regex": r"^PM-?\d+"}},
        sort=[("Operation_Number", -1)]
    )
    if last_entry and "Operation_Number" in last_entry:
        last_num = int(last_entry["Operation_Number"].split("-")[1])
        return f"PM-{last_num+1:05d}"
    return "PM-00001"

def upload_pdf_to_cloudinary(file_path_param):
    # import cloudinary.uploader
    try:
        response = cloudinary.uploader.upload(file_path_param, resource_type="raw")
        return response['secure_url']
    except Exception as e:
        print(f"[Cloudinary Upload Error]: {e}")
        return None



def get_fields_by_name(collection_name):
    """Returns the appropriate fields array based on the provided collection name.
    Args: collection_name (str): The name of the collection (e.g., "Employees", "Products").
    Returns: list: A list of field names for the corresponding collection, or an empty list if the name is not recognized.
    """
    if collection_name == "Employees":#DONE
        return ["Name", "Password", "Id", "Role", "Join_Date", "National_id_pic", "Phone_number", "Address", "Salary"]
    
    elif collection_name == "Products":
        return ["product_name", "category", "stock_quantity", "Specs", "Unit_Price", "product_code", "Units", "prod_pic"]
    
    # elif collection_name == "Sales_Header":
    #     return [self.app.t("Product_code"), self.app.t("product_name"), self.app.t("unit"),self.app.t("numbering"),self.app.t("QTY"),self.app.t("Discount Type"),self.app.t("Discount Value"),self.app.t("Total_QTY"),self.app.t("Unit_Price"),self.app.t("Total_Price")]
    
    # elif collection_name == "Materials_Header":
    #     return [self.app.t("Material_code"), self.app.t("Material_name"), self.app.t("unit"),self.app.t("numbering"),self.app.t("QTY"),self.app.t("Discount Type"),self.app.t("Discount Value"),self.app.t("Total_QTY"),self.app.t("Unit_Price"),self.app.t("Total_Price")]
    
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
        return ["code", "type", "amount", "payment_method", "description", "date"]
    
    else:
        print(f"Warning: Collection name '{collection_name}' not recognized.")
        return []

def trim_logs_collection(logs_collection, keep_last=30):
    """Keep only the last `keep_last` logs, delete older ones."""
    total_logs = logs_collection.count_documents({})
    if total_logs > keep_last:
        logs_to_keep = list(logs_collection.find().sort("date", -1).limit(keep_last))
        if logs_to_keep:
            last_id_to_keep = logs_to_keep[-1]["_id"]
            logs_collection.delete_many({"_id": {"$lt": last_id_to_keep}})

# Determine the base directory
if getattr(sys, "frozen", False):
    # Running as an executable
    BASE_DIR = sys._MEIPASS
else:
    # Running as a script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class AuxiliaryClass:
    def __init__(self, root, app):
        self.root = root
        self.app = app  # save reference to SalesSystemApp
        # self.t = self.app.t
    def stop_sound(self):
        """Method to stop the sound playing."""
        self.app.stop_event.set()

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

    def play_Error(self):
        sound_path = os.path.join(BASE_DIR, 'Static', 'sounds', 'Error.mp3')
        if os.path.exists(sound_path):
            threading.Thread(target=playsound, args=(sound_path,), daemon=True).start()
            print("done")
        else:
            print("Sound file not found:", sound_path)


    def play_success(self):
        sound_path = os.path.join(BASE_DIR, 'Static', 'sounds', 'Success.mp3')

        def play_sound():
            if os.path.exists(sound_path):
                while not self.app.stop_event.is_set():  # Check if stop_event is set
                    playsound(sound_path)
                    break  # In this case, we'll play the sound only once.
            else:
                print("Sound file not found:", sound_path)

        # Create and start the thread to play sound
        self.app.stop_event.clear()  # Clear the stop event before starting the thread
        threading.Thread(target=play_sound, daemon=True).start()       

    def trash(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # make the top bar with change language button
        self.app.topbar.topbar(show_back_button=True)
        
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

            report_log(self.app.logs_collection, self.app.user_name, None, f"{self.t('Generated Excel')} {source} {self.t('report')}", None)

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
            report_log(self.app.logs_collection, self.app.user_name, None, f"{self.t('Generated PDF')} {source} {self.t('report')}", None)
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

    # To get the text button based on language
    def t(self, text):
        return translations.get(text, {}).get(self.app.language, text)

    # Function to toggle from Arabic to English and Vicaverse
    def toggle_language(self):
        self.app.language = "English" if self.app.language == "Arabic" else "Arabic"
        self.app.main_menu()   

    def toggle_theme(self):
        if self.app.light:
            self.app.light = False
        elif not self.app.light:
            self.app.light = True
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
        self.app.main_menu()

    def get_collection_by_name(self,collection_name):
        """Returns the appropriate MongoDB collection object based on the provided name.
        Args: collection_name (str): The name of the collection to access (e.g., "Employees", "Products").
        Returns: pymongo.collection.Collection or None: The corresponding MongoDB collection object,
                                                    or None if the name is not recognized."""
        if collection_name == "Employees":
            return self.app.employees_collection
        if collection_name == "Employee_appointimets":
            return self.app.employees_appointments_collection
        if collection_name == "Employee_withdrawls":
            return self.app.employee_withdrawls_collection
        if collection_name == "Employee_Salary":
            return self.app.employee_salary_collection
        elif collection_name == "Products":
            return self.app.products_collection
        elif collection_name == "Sales":
            return self.app.sales_collection
        elif collection_name == "Customers":
            return self.app.customers_collection
        elif collection_name == "Suppliers":
            return self.app.suppliers_collection
        elif collection_name =="Materials":
            return self.app.materials_collection
        elif collection_name =="Purchases":
            return self.app.purchases_collection
        elif collection_name == "Shipping":
            return self.app.shipping_collection
        elif collection_name == "Orders":
            return self.app.orders_collection
        elif collection_name == "Expenses":
            return self.app.expenses_collection
        elif collection_name == "Daily_shifts":
            return self.app.daily_shifts_collection
        elif collection_name == "Accounts":
            return self.app.accounts_collection
        elif collection_name == "Transactions":
            return self.app.transactions_collection
        elif collection_name == "Big_deals":
            return self.app.big_deals_collection
        elif collection_name == "Production":
            return self.app.production_collection
        elif collection_name == "Customer_Payments":
            return self.app.customer_payments
        elif collection_name == "Supplier_Payments":
            return self.app.supplier_payments
        elif collection_name == "TEX_Calculations":
            return self.app.TEX_Calculations_collection
        elif collection_name == "general_exp_rev":
            return self.app.general_exp_rev_collection
        else:
            print(f"Warning: Collection name '{collection_name}' not recognized.")
            return None