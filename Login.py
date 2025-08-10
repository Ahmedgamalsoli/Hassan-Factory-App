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
class LoginWindow:
    def __init__(self, root, app):
        self.root = root
        self.app = app  # save reference to SalesSystemApp

    def open_login_window(self):
        for widget in self.app.root.winfo_children():
            widget.destroy()

        # Load and set the background image
        image_path = os.path.join(BASE_DIR, "Static", "images", "Login.png")  # Path to your JPG image
        bg_image = Image.open(image_path)
        self.app.bg_photo = ImageTk.PhotoImage(bg_image)  # Convert to a format Tkinter can use
        bg_label = tk.Label(self.app.root, image=self.app.bg_photo)
        bg_label.place(relwidth=1, relheight=1)  # Cover the entire window
        
        # Login Frame
        login_frame = tk.Frame(self.app.root, bg="white", bd=2, relief="ridge")
        login_frame.place(relx=0.515, rely=0.5, anchor="center", width=400, height=350)

        # Load Circular Logo
        logo_path = os.path.join(BASE_DIR, "Static", "images", "Logo.jpg")  # Change this to your logo path
        self.app.logo_image = self.create_circular_image(logo_path)
        if self.app.logo_image:
            self.logo_label = tk.Label(login_frame, image=self.app.logo_image, bg="white")
            self.logo_label.place(x=150, y=10)
            self.animate_image_slide_in(-750)

        # Title
        title = tk.Label(login_frame, text=self.app.t("Login"), font=("Arial", 18, "bold"), bg="white")
        title.place(x=150, y=120)

        # Username
        username_label = tk.Label(login_frame, text=self.app.t("Username:"), font=("Arial", 12), bg="white")
        username_label.place(x=50, y=160)
        username_entry = tk.Entry(login_frame, font=("Arial", 12), bg="#f0f0f0")
        username_entry.place(x=150, y=160, width=200)

        # Password
        password_label = tk.Label(login_frame, text=self.app.t("Password:"), font=("Arial", 12), bg="white")
        password_label.place(x=50, y=190)
        password_entry = tk.Entry(login_frame, font=("Arial", 12), bg="#f0f0f0", show="*")
        password_entry.place(x=150, y=190, width=200)

        username_entry.bind("<Return>", lambda event: validate_login()) # Bind Enter key to trigger add_todo from name_entry
        password_entry.bind("<Return>", lambda event: validate_login()) # Bind Enter key to trigger add_todo from name_entry
        
        # Login Button
        def validate_login():
            username = username_entry.get()  # Assuming `username_entry` is the input field for the username
            password = password_entry.get()  # Assuming `password_entry` is the input field for the password
            self.app.user_name = username
            
            if not username or not password:
                self.app.silent_popup(self.app.t("Error"), self.app.t("Both fields are required."),self.app.play_Error)
                return

            try:
                user = self.app.employees_collection.find_one({"Name": username, "Password": password})
                # print(user)
                if user:
                    self.app.user_role = user.get("Role", "Unknown")
                    self.app.user_id = user.get("_id", None)
                    
                    self.app.employees_collection.update_one({"_id": self.app.user_id}, {"$set": {"logged_in": True}})

                    self.app.last_number_of_msgs = user.get("last_number_of_msgs", 0)
                    config.report_log(self.app.logs_collection, self.app.user_name, None, f"{self.app.user_name} {self.app.t("login to the application")}", None)
                    # messagebox.showinfo("Success", f"Login successful! Role: {self.user_role}")
                    self.app.silent_popup(self.app.t("Success"), f"{self.app.t("Login successful! Role:")} {self.app.user_role}",self.app.play_success)
                    # open_main_menu(self.app.user_role)
                    self.show_logo_transition(self.app.user_role)
                else:
                    self.app.silent_popup(self.app.t("Error"), self.app.t("Invalid username or password."), self.app.play_Error)

            except Exception as e:
                self.app.silent_popup(self.app.t("Database Error"), f"{self.app.t("An error occurred:")} {e}", self.app.play_Error)


        login_button = tk.Button(login_frame, text=self.app.t("Login"), font=("Arial", 12), bg="lightblue", command=validate_login)
        login_button.place(x=150, y=270, width=100)

        # Exit Button
        exit_button = tk.Button(login_frame, text=self.app.t("Exit"), font=("Arial", 12), bg="lightgray", command=self.app.root.quit)
        exit_button.place(x=270, y=270, width=80)
        def open_main_menu(role):
            if role:
                self.app.main_menu()
            else:
                self.app.silent_popup(self.app.t("Unknown role"), self.app.t("Access denied."), self.app.play_Error)
    def animate_image_slide_in(self, x):
        if x < 20:
            self.logo_label.place(x=x)
            self.root.after(10, lambda: self.animate_image_slide_in(x + 15))
        else:
            self.logo_label.place(x=100)

    def show_logo_transition(self, role):
        for widget in self.app.root.winfo_children():
            widget.destroy()

        self.app.root.configure(bg="white")

        logo_path = os.path.join(BASE_DIR, "Static", "images", "Logo.jpg")
        self.logo_original = Image.open(logo_path)

        self.logo_frame = tk.Frame(self.app.root, bg="white")
        self.logo_frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=300)

        self.logo_size = 150  # Starting size
        self.logo_direction = 1  # Slide direction (1 = down, -1 = up)
        self.logo_y = 0         # Initial Y offset

        # Prepare the first image
        self.update_logo_image(self.logo_size)

        # Start the animation
        self.animate_logo_slide_and_grow(role, steps=0)

    def update_logo_image(self, size):
        resized = self.logo_original.resize((size, size))
        self.logo_photo = ImageTk.PhotoImage(resized)

        # Check if the logo_label exists and is still a valid widget
        if hasattr(self, 'logo_label') and self.logo_label.winfo_exists():
            self.logo_label.config(image=self.logo_photo)
        else:
            self.logo_label = tk.Label(self.logo_frame, image=self.logo_photo, bg="white")
            self.logo_label.pack()

        self.logo_label.image = self.logo_photo  # Prevent GC

    def animate_logo_slide_and_grow(self, role, steps):
        # Make logo grow for the first 15 steps
        if steps < 15:
            self.logo_size += 5
            self.update_logo_image(self.logo_size)

        # Slide up and down between -20 and +20 px
        self.logo_y += self.logo_direction * 2
        if abs(self.logo_y) >= 20:
            self.logo_direction *= -1
        self.logo_frame.place_configure(rely=0.5 + self.logo_y / 300.0)  # Slight vertical shift

        # Continue animation
        if steps < 75:
            self.app.root.after(30, lambda: self.animate_logo_slide_and_grow(role, steps + 1))
        else:
            if role:
                self.app.main_menu()
            else:
                self.app.silent_popup(self.app.t("Unknown role"), self.app.t("Access denied."), self.app.play_Error)
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
    
