# ======================
# Used imports
# ======================

import tkinter as tk
import os
import sys
import matplotlib
import config

from PIL import Image, ImageTk
from datetime import datetime
matplotlib.use('TkAgg')  # Set the backend before importing pyplot

# Determine the base directory
if getattr(sys, "frozen", False):
    # Running as an executable
    BASE_DIR = sys._MEIPASS
else:
    # Running as a script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class topbar:
    def __init__(self, root, app):
        self.root = root
        self.app = app  # save reference to SalesSystemApp
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
        import config
        from calculator import open_calculator
        # Top Bar
        top_bar = tk.Frame(self.root, bg=config.COLORS["top_bar"], height=60)
        top_bar.pack(fill="x")
        # Exit icon
        try:    
            if self.app.light:
                self.app.exit_icon_path  = os.path.join(BASE_DIR, "Static", "images", "exit-dark.png")
            elif not self.app.light:
                self.app.exit_icon_path  = os.path.join(BASE_DIR, "Static", "images", "exit-light.png")
            exit_image = Image.open(self.app.exit_icon_path)
            exit_image = exit_image.resize((35, 35), Image.LANCZOS)
            self.app.exit_photo = ImageTk.PhotoImage(exit_image)
            exit_icon = tk.Label(top_bar, image=self.app.exit_photo, bg=config.COLORS["top_bar"])
            exit_icon.pack(side="right", padx=10)
            exit_icon.bind("<Button-1>", lambda e: self.app.on_app_exit())
        except Exception as e:
            self.app.silent_popup("Error", "Error loading exit icon: {e}", self.app.play_Error)

        # Logout icon
        try:
            # login_window_instance = LoginWindow()
            if self.app.light:
                self.app.logout_icon_path = os.path.join(BASE_DIR, "Static", "images", "logout-dark.png")
            elif not self.app.light:
                self.app.logout_icon_path = os.path.join(BASE_DIR, "Static", "images", "logout-light.png")
            logout_image = Image.open(self.app.logout_icon_path)
            logout_image = logout_image.resize((40, 40), Image.LANCZOS)
            self.app.logout_photo = ImageTk.PhotoImage(logout_image)
            logout_icon = tk.Button(top_bar, image=self.app.logout_photo, bg=config.COLORS["top_bar"], bd=0, command=self.app.handle_logout)
            logout_icon.pack(side="right", padx=10)
        except Exception as e:
            self.app.silent_popup("Error", "Error loading Logout icon: {e}", self.app.play_Error)
        # Minimize icon
        try:
            if self.app.light:
                self.app.minimize_icon_path = os.path.join(BASE_DIR, "Static", "images", "minus-dark.png")
            elif not self.app.light:
                self.app.minimize_icon_path = os.path.join(BASE_DIR, "Static", "images", "minus-light.png")
            minimze_image = Image.open(self.app.minimize_icon_path)
            minimze_image = minimze_image.resize((40, 40), Image.LANCZOS)
            self.app.minimize_photo = ImageTk.PhotoImage(minimze_image)
            minimize_icon = tk.Button(top_bar, image=self.app.minimize_photo, bg=config.COLORS["top_bar"], bd=0, command=self.root.iconify)
            minimize_icon.pack(side="right", padx=10)
        except Exception as e:
            self.app.silent_popup("Error", "Error loading Minimize icon: {e}", self.app.play_Error)


        if show_back_button:
            try:
                if self.app.light:
                    self.app.back_icon_path = os.path.join(BASE_DIR, "Static", "images", "left-arrow-dark.png")
                elif not self.app.light:
                    self.app.back_icon_path = os.path.join(BASE_DIR, "Static", "images", "left-arrow-light.png")
                back_image = Image.open(self.app.back_icon_path)
                back_image = back_image.resize((40, 40), Image.LANCZOS)
                self.app.back_photo = ImageTk.PhotoImage(back_image)
                if Back_to_Database_Window:
                    back_icon = tk.Button(top_bar, image=self.app.back_photo, bg=config.COLORS["top_bar"], bd=0, command=self.app.manage_database_window)
                elif Back_to_Employee_Window:
                    back_icon = tk.Button(top_bar, image=self.app.back_photo, bg=config.COLORS["top_bar"], bd=0, command=self.app.EmployeeWindow.manage_Employees_window)
                elif Back_to_Sales_Window:
                    back_icon = tk.Button(top_bar, image=self.app.back_photo, bg=config.COLORS["top_bar"], bd=0, command=self.app.SalesInvoice.manage_sales_invoices_window)
                elif Back_to_Purchases_Window:
                    back_icon = tk.Button(top_bar, image=self.app.back_photo, bg=config.COLORS["top_bar"], bd=0, command=self.app.PurchaseInvoice.manage_purchases_invoices_window)
                elif Back_to_Reports_Window:
                    back_icon = tk.Button(top_bar, image=self.app.back_photo, bg=config.COLORS["top_bar"], bd=0, command=self.app.manage_Reports_window)
                else:
                    back_icon = tk.Button(top_bar, image=self.app.back_photo, bg=config.COLORS["top_bar"], bd=0, command=self.app.main_menu)
                back_icon.pack(side="left", padx=10)
            except Exception as e:
                self.app.silent_popup("Error", "Error loading back icon: {e}", self.app.play_Error)
        else:
            lang_btn = tk.Button(top_bar, text=self.app.t("Change Language"), bg=config.COLORS["top_bar"], fg=config.COLORS["top_bar_icons"],
                                font=("Arial", 10, "bold"), bd=0, command=self.toggle_language)
            lang_btn.pack(side="left", padx=10)
            if self.app.light:
                lang_image = Image.open(self.app.dark_mode_img)
            elif not self.app.light:
                lang_image = Image.open(self.app.light_mode_img)
            lang_image = lang_image.resize((40, 40), Image.LANCZOS)
            self.app.lang_photo = ImageTk.PhotoImage(lang_image)
            lang_btn = tk.Button(top_bar, text=self.app.t("Change Language"),image=self.app.lang_photo, bg=config.COLORS["top_bar"], fg="black",
                                font=("Arial", 10, "bold"), bd=0, command=self.toggle_theme)
            lang_btn.pack(side="left", padx=10)

        # Left side: Language or Back button
        # tk.Button(top_bar, text="Open Calculator", command=open_calculator, font=("Arial", 14)).pack(side="left", padx=10)
        if self.app.light:
            self.app.calc_icon_path = os.path.join(BASE_DIR, "Static", "images", "calculator-dark.png")
        elif not self.app.light:
            self.app.calc_icon_path = os.path.join(BASE_DIR, "Static", "images", "calculator-light.png")
        calc_image = Image.open(self.app.calc_icon_path)
        calc_image = calc_image.resize((35, 35), Image.LANCZOS)
        self.app.calc_photo = ImageTk.PhotoImage(calc_image)
        calc_icon = tk.Label(top_bar, image=self.app.calc_photo, bg=config.COLORS["top_bar"])
        calc_icon.pack(side="left", padx=10)
        calc_icon.bind("<Button-1>", lambda event: open_calculator())
        
        # Time label
        time_label = tk.Label(top_bar, text=datetime.now().strftime('%B %d, %Y %I:%M %p'),
                            font=("Arial", 20, "bold"), fg=config.COLORS["top_bar_icons"], bg=config.COLORS["top_bar"])

        time_label.place(relx=0.5, rely=0.5, anchor="center")
        # self.update_time(time_label)
        #TODO
        # User info frame
        user_frame = tk.Frame(top_bar, bg=config.COLORS["top_bar"])
        user_frame.pack(side="right", padx=10)

        username_label = tk.Label(user_frame, text=self.app.user_name, font=("Arial", 20), fg=config.COLORS["top_bar_icons"], bg=config.COLORS["top_bar"])
        username_label.pack(side="left")

    # Function tot oggle from Arabic to English and Vicaverse
    def toggle_language(self):
        self.app.language = "English" if self.app.language == "Arabic" else "Arabic"
        self.app.main_menu()   
    def toggle_theme(self):
        if self.app.light:
            self.app.light = False
        elif not self.app.light:
            self.app.light = True
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
        self.app.main_menu()