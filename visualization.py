# ======================
# Used imports
# ======================

import tkinter as tk
import io
import re
import config
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
class Visualization:
    def __init__(self, root, app):
        self.root = root
        self.app = app  # save reference to SalesSystemApp


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
            fig = plt.Figure(figsize=(6, 10), dpi=70, facecolor=config.COLORS["card"])
            # fig.subplots_adjust(hspace=0.4)
            fig.subplots_adjust(hspace=0.4, left=0.15, right=0.85)
            # fig.patch.set_facecolor('#FFFFFF')  # White background

            # Bar Chart
            ax1 = fig.add_subplot(211)
            try:
                arabic_title0 = self.app.AuxiliaryClass.t("Customers")
                reshaped_text0 = arabic_reshaper.reshape(arabic_title0)
                bidi_text0 = get_display(reshaped_text0)
                arabic_title1 = self.app.AuxiliaryClass.t("Suppliers")
                reshaped_text1 = arabic_reshaper.reshape(arabic_title1)
                bidi_text1 = get_display(reshaped_text1)
                bars = ax1.bar([bidi_text0, bidi_text1], 
                            [data['customers'], data['suppliers']], 
                            color=['#2E86C1', '#17A589'])
                arabic_title2 = self.app.AuxiliaryClass.t("Customer & Supplier Overview")
                reshaped_text2 = arabic_reshaper.reshape(arabic_title2)
                bidi_text2 = get_display(reshaped_text2)                
                arabic_title3 = self.app.AuxiliaryClass.t("Count")
                reshaped_text3 = arabic_reshaper.reshape(arabic_title3)
                bidi_text3 = get_display(reshaped_text3)                
                ax1.set_title(bidi_text2, fontsize=20,color=config.COLORS["text"], fontname="Arial")
                ax1.set_facecolor(config.COLORS["text"])
                ax1.tick_params(colors=config.COLORS["text"], labelsize=13,)
                ax1.set_ylabel("xx",text=bidi_text3,color=config.COLORS["text"], fontsize=18, fontname="Arial")
                for label in ax1.get_xticklabels():
                    label.set_fontsize(15)         # Change to your desired size
                    label.set_fontname("Arial")    # Use a font that supports Arabic
                    label.set_color(config.COLORS["text"])
                    label.set_weight("bold") 
                # Add simple data labels
                for bar in bars:
                    height = bar.get_height()
                    ax1.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}',
                            ha='center', va='bottom',
                            color=config.COLORS["text"], fontsize=10)
                    
            except Exception as bar_error:
                print(f"Bar chart error: {bar_error}")

            # Summary Table
            ax2 = fig.add_subplot(212)
            ax2.axis('off')
            arabic_title4 = self.app.AuxiliaryClass.t("Metric")
            reshaped_text4 = arabic_reshaper.reshape(arabic_title4)
            bidi_text4 = get_display(reshaped_text4) 

            arabic_title5 = self.app.AuxiliaryClass.t("Value")
            reshaped_text5 = arabic_reshaper.reshape(arabic_title5)
            bidi_text5 = get_display(reshaped_text5) 

            arabic_title6 = self.app.AuxiliaryClass.t("Customers number")
            reshaped_text6 = arabic_reshaper.reshape(arabic_title6)
            bidi_text6 = get_display(reshaped_text6) 

            arabic_title7 = self.app.AuxiliaryClass.t("Suppliers number")
            reshaped_text7 = arabic_reshaper.reshape(arabic_title7)
            bidi_text7 = get_display(reshaped_text7) 

            arabic_title8 = self.app.AuxiliaryClass.t("Number of Sales")
            reshaped_text8 = arabic_reshaper.reshape(arabic_title8)
            bidi_text8 = get_display(reshaped_text8) 

            arabic_title9 = self.app.AuxiliaryClass.t("Number of Purchases")
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
            if self.app.language == "Arabic":
                table.set_fontsize(15)
            else:
                table.set_fontsize(13)
            # table.set_fontname("Arial")
            table.set_zorder(100)
            table.scale(1, 2)  # Less aggressive scaling

            for (row, col), cell in table.get_celld().items():
                cell.set_facecolor(config.COLORS["card"])
                cell.set_text_props(fontname="Arial")
                # cell.set_facecolor("black") # background content
                cell.set_text_props(color=config.COLORS["text"])
                # cell.set_text_props(color="black") #text in header
                if row == 0:
                    cell.set_facecolor(config.COLORS["main_frame"])
                    cell.set_text_props(weight='bold',color="white")

            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas.draw()
            canvas.get_tk_widget().config(bg=config.COLORS["card"])
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
            fig.patch.set_facecolor(config.COLORS["card"])  
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
                        colors=[config.COLORS["main_frame"]],
                        startangle=90,
                        wedgeprops={'width': 1}
                    )
                else:
                    arabic_title1 = self.app.AuxiliaryClass.t("Sales")
                    reshaped_text1 = arabic_reshaper.reshape(arabic_title1)
                    bidi_text1 = get_display(reshaped_text1)
                    arabic_title2 = self.app.AuxiliaryClass.t("Purchases")
                    reshaped_text2 = arabic_reshaper.reshape(arabic_title2)
                    bidi_text2 = get_display(reshaped_text2)
                    ax1.pie(
                        [sales, purchases],
                        labels=[bidi_text1, bidi_text2],
                        autopct='%1.1f%%',
                        colors=['#28B463', '#E74C3C'],
                        textprops={'color': config.COLORS["text"], 'fontsize': 16, 'fontname': 'Arial'},
                        wedgeprops={'width': 1}
                    )
                ax1.axis('equal')  # Ensures the pie is drawn as a circle
                # Before setting the title:
                arabic_title = self.app.AuxiliaryClass.t("Sales vs Purchases")
                reshaped_text = arabic_reshaper.reshape(arabic_title)
                bidi_text = get_display(reshaped_text)
                ax1.set_title(bidi_text, fontsize=20, color=config.COLORS["text"], fontname="Arial")  # Use a font that supports Arabic
                # ax1.set_title(self.app.AuxiliaryClass.t("المبيعات مقابل المشتريات"), fontsize=14, color=config.COLORS["text"])
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
                        label.set_color(config.COLORS["text"])   
                        label.set_weight("bold")  # Font size
                    arabic_title3 = self.app.AuxiliaryClass.t("Top Client")
                    reshaped_text3 = arabic_reshaper.reshape(arabic_title3)
                    bidi_text3 = get_display(reshaped_text3)
                    ax2.set_title(bidi_text3, fontsize=20,color=config.COLORS["text"],fontname="Arial")  # Use a font that supports Arabic
                    ax2.set_facecolor(config.COLORS["text"])
                    ax2.tick_params(colors=config.COLORS["text"])
                    arabic_title4 = self.app.AuxiliaryClass.t("Amount")
                    reshaped_text4 = arabic_reshaper.reshape(arabic_title4)
                    bidi_text4 = get_display(reshaped_text4)
                    ax2.set_ylabel(bidi_text4,fontsize=18,color=config.COLORS["text"],fontname="Arial")
                    # Add value label
                    for rect in bar:
                        height = rect.get_height()
                        ax2.text(rect.get_x() + rect.get_width()/2., height,
                                f'${height:.2f}',
                                ha='center', va='bottom',
                                color=config.COLORS["text"], fontsize=10)
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
        frame = tk.Frame(parent, bg=config.COLORS["card"], bd=0,
                        highlightbackground=config.COLORS["main_frame"],
                        highlightthickness=3)
        if padding:
            frame.grid_propagate(False)
            frame.config(width=400, height=600)
        return frame

    # Database query methods
    def get_customer_count(self):
        try:
            return self.app.customers_collection.count_documents({})
        except PyMongoError as e:
            print(f"Database error: {e}")
            return 0

    def get_supplier_count(self):
        try:
            return self.app.suppliers_collection.count_documents({})
        except PyMongoError as e:
            print(f"Database error: {e}")
            return 0

    def get_sales_count(self):
        try:
            return self.app.sales_collection.count_documents({})
        except PyMongoError as e:
            print(f"Database error: {e}")
            return 0

    def get_purchase_count(self):
        try:
            return self.app.purchases_collection.count_documents({})
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
            result = list(self.app.customers_collection.aggregate(pipeline))
            # print(1)
            if result:
                print(f"{result[0]["Name"]} ,{result[0]["Debit"]}")
                return (result[0]["Name"], result[0]["Debit"])  # 🔑 Fix here
            return ("No clients found", 0)
            
        except PyMongoError as e:
            print(f"Database error: {e}")
            return ("Error", 0)
        

    