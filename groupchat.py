# ======================
# Used imports
# ======================

import tkinter as tk
import os
import matplotlib
import matplotlib.pyplot as plt
import sys

from PIL import Image, ImageTk, ImageDraw  # Import Pillow classes
from datetime import datetime

matplotlib.use('TkAgg')  # Set the backend before importing pyplot

# Determine the base directory
if getattr(sys, "frozen", False):
    # Running as an executable
    BASE_DIR = sys._MEIPASS
else:
    # Running as a script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class GroupChat:
    def __init__(self, root, app):
        self.root = root
        self.app = app  # save reference to SalesSystemApp
    def update_groupchat_icon(self):
        if self.app.last_number_of_msgs == 0:
            user_doc = self.app.employees_collection.find_one({"Id": self.app.user_id})
            if user_doc:
                self.app.last_number_of_msgs = user_doc.get("last_number_of_msgs", 0)
            
            self.app.root.after(10000, self.update_groupchat_icon)
            self.app.is_group_chat_read = False
            return
        
        icon_path = os.path.join(BASE_DIR, "Static", "images", "groupchat.ico")
        img = Image.open(icon_path).resize((60, 60), Image.LANCZOS).convert("RGBA")
        draw = ImageDraw.Draw(img)
        
        unread_count = self.app.messages_collection.count_documents({}) - self.app.last_number_of_msgs
        if (unread_count > 0):
            draw.ellipse((40, 0, 60, 20), fill="red")
            draw.text((45, 2), str(unread_count), fill="white")
            self.app.is_group_chat_read = False

        icon_photo = ImageTk.PhotoImage(img)
        self.app.groupchat_main_btn.config(image=icon_photo)
        self.app.groupchat_main_btn.image = icon_photo  # Prevent garbage collection
        
        # self.last_number_of_msgs = self.messages_collection.count_documents({})
        self.root.after(10000, self.update_groupchat_icon)

    def open_group_chat_window(self):
        chat_win = tk.Toplevel(self.root)
        chat_win.title(self.app.t("Group Chat - Employee Notes"))
        chat_win.geometry("450x500")
        chat_win.resizable(False, False)

        # Set custom icon for the window (groupchat.ico)
        icon_path = os.path.join(BASE_DIR, "Static", "images", "groupchat.ico")
        if os.path.exists(icon_path):
            chat_win.iconbitmap(icon_path)

        # Group chat icon (draggable)
        icon_frame = tk.Frame(chat_win, width=200, height=120)
        icon_frame.place(x=10, y=10)

        icon_img_path = os.path.join(BASE_DIR, "Static", "images", "groupchat.ico")
        if os.path.exists(icon_img_path):
            icon_img = Image.open(icon_img_path).resize((50, 50), Image.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon_img)
            icon_label = tk.Label(icon_frame, image=icon_photo)
            icon_label.image = icon_photo
            icon_label.pack(pady=(5, 0))
        else:
            icon_label = tk.Label(icon_frame, text="👥", font=("Arial", 24))
            icon_label.pack()
        
        # Make icon draggable
        def start_drag(event):
            icon_frame._drag_start_x = event.x
            icon_frame._drag_start_y = event.y

        def do_drag(event):
            x = icon_frame.winfo_x() + event.x - icon_frame._drag_start_x
            y = icon_frame.winfo_y() + event.y - icon_frame._drag_start_y
            icon_frame.place(x=x, y=y)

        icon_label.bind("<Button-1>", start_drag)
        icon_label.bind("<B2-Motion>", do_drag)

        logged_in_users = list(self.app.employees_collection.find({"logged_in": True}))
        if logged_in_users:

            online_frame = tk.Frame(icon_frame)
            online_frame.pack(pady=(5, 0))  # Place under the icon

        for user in logged_in_users:
            name = user.get("Name", "Unknown")
            row = tk.Frame(online_frame)
            row.pack(anchor="w")
            dot_label = tk.Label(row, text="●", fg="green", font=("Arial", 12, "bold"))
            dot_label.pack(side=tk.LEFT)
            name_label = tk.Label(row, text=name, font=("Arial", 12))
            name_label.pack(side=tk.LEFT, padx=1)
        
        chat_frame = tk.Frame(chat_win)
        chat_frame.place(x=100, y=10, width=300, height=420)
        chat_display = tk.Text(chat_frame, state="disabled", wrap="word", font=("Arial", 12))
        chat_display.pack(fill="both", expand=True)
        
        # Entry area
        entry_frame = tk.Frame(chat_win)
        entry_frame.place(x=10, y=440, width=380, height=50)

        msg_var = tk.StringVar()
        msg_entry = tk.Entry(entry_frame, textvariable=msg_var, width=28)
        msg_entry.pack(side=tk.LEFT, padx=5)

        def load_messages():
            chat_display.config(state="normal")
            chat_display.delete(1.0, tk.END)
            for msg in self.app.messages_collection.find().sort("timestamp", 1):
                name = msg.get("name", self.app.t("Unknown"))
                text = msg.get("text", "")
                time = msg.get("timestamp", "").strftime("%Y-%m-%d %H:%M") if msg.get("timestamp") else ""
                chat_display.insert(tk.END, f"[{time}] {self.app.t(name)}: {text}\n")
            chat_display.config(state="disabled")
            chat_display.see(tk.END)
            self.app.last_number_of_msgs = self.app.messages_collection.count_documents({})
            self.app.is_group_chat_read = True

        def send_message():
            # name = name_var.get().strip() or "Unknown"
            name = self.app.user_name if self.app.user_name else "Unknown"
            text = msg_var.get().strip()
            if text:
                self.app.messages_collection.insert_one({
                    "name": name,
                    "text": text,
                    "timestamp": datetime.now()
                })
                msg_var.set("")
                load_messages()


        send_btn = tk.Button(entry_frame, text="Send", command=send_message, font=("Arial", 11), width=8, bg="#2196F3", fg="white")
        send_btn.pack(side=tk.LEFT, padx=5)

        # Make refresh button larger and more visible
        refresh_btn = tk.Button(entry_frame, text="Refresh", command=load_messages, font=("Arial", 11), width=8, bg="#21F35D", fg="white")
        refresh_btn.pack(side=tk.LEFT, padx=5)

        chat_display.config(state="normal")
        chat_display.insert("end", "Welcome! This is the group chat for employee notes.\n\n")
        chat_display.config(state="disabled")

        load_messages()