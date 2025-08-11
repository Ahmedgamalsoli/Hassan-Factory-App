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

import db


class CommonInteractions:
    def __init__(self, root, app):
        self.root = root
        self.app = app  # save reference to SalesSystemApp
        self.t = self.app.t


    def on_code_selected(self, event, code_cb, name_cb, collection, invoices_collection, payment_collection, field_path, tree):
        selected_code = code_cb.get().strip()
        
        start_date_raw = self.app.start_date_entry.get_date()  # These should be instance variables
        end_date_raw   = self.app.end_date_entry.get_date()
        start_date     = datetime.combine(start_date_raw, time.min)          # 00:00:00
        end_date       = datetime.combine(end_date_raw, time.max)              # 23:59:59.999999
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
                    self.app.report_customer_name = name_cb.get().strip()  # Store the selected name for later use
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
        self.app.report_customer_name = selected_name  # Store the selected name for later use
        if not selected_name:
            return

        start_date_raw = self.app.start_date_entry.get_date()  # These should be instance variables
        end_date_raw = self.app.end_date_entry.get_date()
        
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
            self.app.total_debit_entry.delete(0, tk.END)
            self.app.total_debit_entry.insert(0, str(total_debit))

            self.app.total_credit_entry.delete(0, tk.END)
            self.app.total_credit_entry.insert(0, str(total_credit))

            self.app.balance_entry.delete(0, tk.END)
            self.app.balance_entry.insert(0, str(balance))

            if tree:
                tree.delete(*tree.get_children())
                for row in sample_data:
                    tree.insert("", tk.END, values=row)
        else:
            #load total_debit/credit of the user selected
            if (payment_collection.name == "Customer_Payments"):
                doc = db.customers_collection.find_one({"Code": person_code}, {"Debit": 1, "Credit": 1, "Balance": 1})
            else:
                doc = db.suppliers_collection.find_one({"Code": person_code}, {"Debit": 1, "Credit": 1, "Balance": 1})

            tree.delete(*tree.get_children())
            
            if not doc:
                if tree:
                    for row in sample_data:
                        tree.insert("", tk.END, values=row)
            
            else:
                doc_debit = doc.get("Debit", 0)
                doc_credit = doc.get("Credit", 0)
                doc_balance = doc.get("Balance", 0)

                self.app.total_debit_entry.delete(0, tk.END)
                self.app.total_debit_entry.insert(0, str(doc_debit))

                self.app.total_credit_entry.delete(0, tk.END)
                self.app.total_credit_entry.insert(0, str(doc_credit))

                self.app.balance_entry.delete(0, tk.END)
                self.app.balance_entry.insert(0, str(doc_balance))

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
        self.app.raw_tree_data = sample_data
