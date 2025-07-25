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
        self.app.logo_image = self.app.create_circular_image(logo_path)
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
