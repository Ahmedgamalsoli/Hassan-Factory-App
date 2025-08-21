# ======================
# Used imports
# ======================
import json

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

from bson import ObjectId
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

# Determine the base directory
if getattr(sys, "frozen", False):
    # Running as an executable
    BASE_DIR = sys._MEIPASS
else:
    # Running as a script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class DataBase:
    def __init__(self, root, app):
        self.root = root
        self.app = app  # save reference to SalesSystemApp

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
            messagebox.showerror(self.AuxiliaryClass.t("No Internet Connection"), str(e))

        self.db = client["Hassan"]   

        self.app.customers_collection             = self.db['Customers']
        self.app.employees_collection             = self.db['Employees']
        self.app.employees_appointments_collection= self.db['Employee_appointimets']
        self.app.employee_withdrawls_collection   = self.db['Employee_withdrawls']
        self.app.employee_salary_collection       = self.db['Employee_Salary']
        self.app.products_collection              = self.db['Products']
        self.app.sales_collection                 = self.db['Sales']
        self.app.suppliers_collection             = self.db['Suppliers']
        self.app.materials_collection             = self.db['Materials']
        self.app.purchases_collection             = self.db['Purchases']
        self.app.shipping_collection              = self.db['Shipping']
        self.app.orders_collection                = self.db['Orders']
        self.app.expenses_collection              = self.db['Expenses']
        self.app.daily_shifts_collection          = self.db['Daily_shifts']
        self.app.accounts_collection              = self.db['Accounts']
        self.app.transactions_collection          = self.db['Transactions']
        self.app.big_deals_collection             = self.db['Big_deals']
        self.app.TEX_Calculations_collection      = self.db['TEX_Calculations']
        self.app.production_collection            = self.db['Production']
        self.app.customer_payments                = self.db["Customer_Payments"]
        self.app.supplier_payments                = self.db["Supplier_Payments"]
        self.app.general_exp_rev_collection       = self.db["general_exp_rev"]
        self.app.messages_collection              = self.db["Messages"]
        self.app.logs_collection                  = self.db["Logs"]
    def download_db_json_file(self, output_folder="mongodb_exports"):
        """
        Export all collections in the connected MongoDB database to JSON files.
        Each collection will be saved as <collection_name>.json in the output_folder.
        """
        try:
            if not hasattr(self, "db"):
                print("❌ Database is not connected. Please run Connect_DB() first.")
                return

            # Create output folder if not exists
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Custom serializer for JSON
            def custom_serializer(obj):
                if isinstance(obj, datetime):
                    return obj.isoformat()  # Convert datetime to ISO string
                return str(obj)  # Fallback for ObjectId or other types

            # Loop over all collections
            for coll_name in self.db.list_collection_names():
                collection = self.db[coll_name]
                data = list(collection.find())

                file_path = os.path.join(output_folder, f"{coll_name}.json")
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False, default=custom_serializer)

                print(f"✅ Exported {coll_name} to {file_path}")

            print("🎉 All collections exported successfully!")

        except Exception as e:
            print(f"❌ Error exporting database: {e}")