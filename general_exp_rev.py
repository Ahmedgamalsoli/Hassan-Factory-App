# ======================
# Used imports
# ======================

import tkinter as tk
import config
import os
import sys
import matplotlib
import matplotlib.pyplot as plt


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
class GeneralExpRev:
    def __init__(self, root, app):
        self.root = root
        self.app = app  # save reference to SalesSystemApp

    def general_exp_rev(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        self.app.topbar.topbar(show_back_button=True)
        
        # Create main container frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create paned window for resizable split
        paned_window = tk.PanedWindow(main_frame, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=4)
        paned_window.pack(fill=tk.BOTH, expand=True)
        
        # Expense Frame (left side)
        expense_frame = tk.LabelFrame(paned_window, text=self.app.AuxiliaryClass.t("Expenses"), font=("Arial", 12, "bold"), padx=10, pady=10)
        # Revenue Frame (right side)
        revenue_frame = tk.LabelFrame(paned_window, text=self.app.AuxiliaryClass.t("Revenues"), font=("Arial", 12, "bold"), padx=10, pady=10)
        
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
        
        tk.Label(expense_frame, text=self.app.AuxiliaryClass.t("Amount Paid:"), font=("Arial", 10)).grid(row=0, column=0, sticky='e', pady=5)
        self.app.expense_amount = tk.DoubleVar()
        expense_entry = tk.Entry(expense_frame, textvariable=self.app.expense_amount)
        expense_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        tk.Label(expense_frame, text=self.app.AuxiliaryClass.t("Payment Method:"), font=("Arial", 10)).grid(row=1, column=0, sticky='e', pady=5)
        self.app.expense_payment = tk.StringVar()
        expense_payment_cb = ttk.Combobox(expense_frame, textvariable=self.app.expense_payment, 
                                        values=payment_methods, state="readonly")
        expense_payment_cb.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        expense_payment_cb.current(0)  # Default to Cash
        
        tk.Label(expense_frame, text=self.app.AuxiliaryClass.t("Description:"), font=("Arial", 10)).grid(row=2, column=0, sticky='e', pady=5)
        self.app.expense_desc = tk.StringVar()
        expense_desc_entry = tk.Entry(expense_frame, textvariable=self.app.expense_desc)
        expense_desc_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        
        expense_submit = tk.Button(expense_frame, 
                            text=self.app.AuxiliaryClass.t("💾 Record Expense"), 
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
        
        tk.Label(revenue_frame, text=self.app.AuxiliaryClass.t("Amount Received:"), font=("Arial", 10)).grid(row=0, column=0, sticky='e', pady=5)
        self.app.revenue_amount = tk.DoubleVar()
        revenue_entry = tk.Entry(revenue_frame, textvariable=self.app.revenue_amount)
        revenue_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        
        tk.Label(revenue_frame, text=self.app.AuxiliaryClass.t("Payment Method:"), font=("Arial", 10)).grid(row=1, column=0, sticky='e', pady=5)
        self.app.revenue_payment = tk.StringVar()
        revenue_payment_cb = ttk.Combobox(revenue_frame, textvariable=self.app.revenue_payment, 
                                        values=payment_methods, state="readonly")
        revenue_payment_cb.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        revenue_payment_cb.current(0)  # Default to Cash
        
        tk.Label(revenue_frame, text=self.app.AuxiliaryClass.t("Description:"), font=("Arial", 10)).grid(row=2, column=0, sticky='e', pady=5)
        self.app.revenue_desc = tk.StringVar()
        revenue_desc_entry = tk.Entry(revenue_frame, textvariable=self.app.revenue_desc)
        revenue_desc_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        
        revenue_submit = tk.Button(revenue_frame, 
                            text=self.app.AuxiliaryClass.t("💾 Record Revenue"), 
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
            amount = self.app.expense_amount.get()
            payment = self.app.expense_payment.get()
            desc = self.app.expense_desc.get()
        else:  # Revenue
            amount = self.app.revenue_amount.get()
            payment = self.app.revenue_payment.get()
            desc = self.app.revenue_desc.get()
        
        if amount <= 0:
            messagebox.showerror(self.app.AuxiliaryClass.t("Error"), self.app.AuxiliaryClass.t("Amount must be greater than zero"))
            return
            
        if not payment:
            messagebox.showerror(self.app.AuxiliaryClass.t("Error"), self.app.AuxiliaryClass.t("Please select a payment method"))
            return
        code = config.get_next_code(self.app.general_exp_rev_collection)    
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
            collection = self.app.general_exp_rev_collection
            collection.insert_one(transaction)
            messagebox.showinfo(self.app.AuxiliaryClass.t("Success"), f"{self.app.AuxiliaryClass.t(transaction_type)} {self.app.AuxiliaryClass.t("recorded successfully!")}")
            config.report_log(self.app.logs_collection, self.app.user_name, None, f"{self.app.AuxiliaryClass.t(f"Recorded {transaction_type} of")} {amount} {self.app.AuxiliaryClass.t(f"in {self.app.general_exp_rev_collection.name} Database")}", None)

            # Clear fields
            if transaction_type == "Expense":
                self.app.expense_amount.set(0)
                self.app.expense_payment.set("cash")
                self.app.expense_desc.set("")
            else:
                self.app.revenue_amount.set(0)
                self.app.revenue_payment.set("cash")
                self.app.revenue_desc.set("")
                
        except Exception as e:
            messagebox.showerror(self.app.AuxiliaryClass.t("Database Error"), f"{self.app.AuxiliaryClass.t("Failed to save transaction:")} {str(e)}")