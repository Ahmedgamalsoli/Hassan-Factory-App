# ======================
# Used imports
# ======================
import tkinter as tk
import matplotlib
import os
import sys

from PIL import Image, ImageTk # Import Pillow classes


matplotlib.use('TkAgg')  # Set the backend before importing pyplot

# ======================
# Unused imports
# ======================
# from reportlab.lib.pagesizes import letter


# Determine the base directory
if getattr(sys, "frozen", False):
    # Running as an executable
    BASE_DIR = sys._MEIPASS
else:
    # Running as a script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class LoginWindow:
    def __init__(self, root, app):
        # self.root = root
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
        self.app.logo_image = self.app.create_circular_image(logo_path)
        if self.app.logo_image:
            logo_label = tk.Label(login_frame, image=self.app.logo_image, bg="white")
            logo_label.place(x=150, y=10)

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
            # Validate input
            if not username or not password:
                self.app.silent_popup(self.app.t("Error"), self.app.t("Both fields are required."),self.app.play_Error)
                return

            try:
                user = self.app.employees_collection.find_one({"Name": username, "Password": password})
                # print(user)
                if user:
                    self.app.user_role = user.get("Role", "Unknown")
                    # messagebox.showinfo("Success", f"Login successful! Role: {self.user_role}")
                    self.app.silent_popup(self.app.t("Success"), f"{self.app.t("Login successful! Role:")} {self.app.user_role}",self.app.play_success)
                    open_main_menu(self.app.user_role)
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