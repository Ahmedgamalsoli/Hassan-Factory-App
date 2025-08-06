# ======================
# Used imports
# ======================

import tkinter as tk
import os
import sys
import matplotlib

from tkinter import ttk
from PIL import Image, ImageTk

matplotlib.use('TkAgg')  # Set the backend before importing pyplot


# Determine the base directory
if getattr(sys, "frozen", False):
    # Running as an executable
    BASE_DIR = sys._MEIPASS
else:
    # Running as a script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
class chatbot:
    def __init__(self, root, app):
        self.root = root
        self.app = app  # save reference to SalesSystemApp
    def open_chatbot(self):
        chatbot_win = tk.Toplevel(self.root)
        chatbot_win.title("مساعد التطبيق")
        chatbot_win.title(self.app.t("Application Assistant"))
        chatbot_win.geometry("400x500")
        chatbot_win.resizable(False, False)
    
        # Set custom icon for the window (feather.ico)
        icon_path = os.path.join(BASE_DIR, "Static", "images", "chatbot_icon.ico")
        if os.path.exists(icon_path):
            chatbot_win.iconbitmap(icon_path)
    
        # Chatbot icon (draggable)
        icon_frame = tk.Frame(chatbot_win, width=60, height=60)
        icon_frame.place(x=10, y=10)
        icon_img_path = os.path.join(BASE_DIR, "Static", "images", "chatbot_icon.ico")
        if os.path.exists(icon_img_path):
            icon_img = Image.open(icon_img_path).resize((60, 60), Image.LANCZOS)
            icon_photo = ImageTk.PhotoImage(icon_img)
            icon_label = tk.Label(icon_frame, image=icon_photo)
            icon_label.image = icon_photo
            icon_label.pack()
        else:
            icon_label = tk.Label(icon_frame, text="🤖", font=("Arial", 32))
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
        icon_label.bind("<B1-Motion>", do_drag)
    
        # Chat area
        chat_frame = tk.Frame(chatbot_win)
        chat_frame.place(x=80, y=10, width=310, height=420)
        chat_text = tk.Text(chat_frame, state="disabled", wrap="word", font=("Arial", 12))
        chat_text.pack(fill="both", expand=True)
    
        # Entry and send button (hidden, not used)
        entry_frame = tk.Frame(chatbot_win)
        entry_frame.place(x=10, y=440, width=380, height=50)
    
        # ...inside open_chatbot...
                # Fixed questions and replies
        questions = [
            "كيف أضيف فاتورة مبيعات؟",
            "كيف أبحث عن عميل؟",
            "كيف أعدل بيانات منتج؟",
            "كيف أغير اللغة؟",
            "كيف أضيف موظف جديد؟",
            "كيف أبحث عن فاتورة مبيعات؟",
            "كيف أعدل فاتورة مبيعات؟",
            "كيف أضيف فاتورة مشتريات؟",
            "كيف أبحث عن مورد؟",
            "كيف أعدل بيانات مورد؟",
            "كيف أضيف منتج جديد؟",
            "كيف أبحث عن منتج؟",
            "كيف أعدل بيانات موظف؟",
            "كيف أضيف مصروف عام؟",
            "كيف أضيف إيراد عام؟",
            "كيف أبحث في قاعدة البيانات؟",
            "كيف أستخدم التقارير؟",
            "كيف أغير كلمة المرور؟",
            "كيف أعمل نسخة احتياطية للبيانات؟",
            "كيف أسترجع نسخة احتياطية؟",
            "كيف أضيف وردية يومية؟",
            "كيف أضيف أمر إنتاج؟",
            "كيف أبحث عن سجل موظف؟",
            "كيف أبحث عن سجل مورد؟",
            "كيف أبحث عن سجل منتج؟",
            "كيف أبحث عن سجل فاتورة؟",
            "مساعدة"
        ]
        replies = {
            "كيف أضيف فاتورة مبيعات؟": "من القائمة الرئيسية، اختر 'فاتورة مبيعات' ثم اضغط على 'فاتورة مبيعات جديدة'.",
            "كيف أبحث عن عميل؟": "استخدم مربع البحث في نافذة العملاء أو قاعدة البيانات.",
            "كيف أعدل بيانات منتج؟": "اذهب إلى قاعدة البيانات، اختر 'المنتجات' ثم اضغط على 'تعديل سجل'.",
            "كيف أغير اللغة؟": "اضغط على زر تغيير اللغة في الشريط العلوي.",
            "كيف أضيف موظف جديد؟": "من قاعدة البيانات، اختر 'الموظفين' ثم اضغط على 'إضافة سجل'.",
            "كيف أبحث عن فاتورة مبيعات؟": "من نافذة الفواتير، استخدم مربع البحث أو اختر رقم الفاتورة من القائمة.",
            "كيف أعدل فاتورة مبيعات؟": "من نافذة الفواتير، اختر الفاتورة ثم اضغط على 'تعديل'.",
            "كيف أضيف فاتورة مشتريات؟": "من القائمة الرئيسية، اختر 'فاتورة مشتريات' ثم اضغط على 'فاتورة مشتريات جديدة'.",
            "كيف أبحث عن مورد؟": "استخدم مربع البحث في نافذة الموردين أو قاعدة البيانات.",
            "كيف أعدل بيانات مورد؟": "اذهب إلى قاعدة البيانات، اختر 'الموردين' ثم اضغط على 'تعديل سجل'.",
            "كيف أضيف منتج جديد؟": "من قاعدة البيانات، اختر 'المنتجات' ثم اضغط على 'إضافة سجل'.",
            "كيف أبحث عن منتج؟": "استخدم مربع البحث في نافذة المنتجات أو قاعدة البيانات.",
            "كيف أعدل بيانات موظف؟": "اذهب إلى قاعدة البيانات، اختر 'الموظفين' ثم اضغط على 'تعديل سجل'.",
            "كيف أضيف مصروف عام؟": "من القائمة الرئيسية، اختر 'ايرادات و مصروفات عامة' ثم اضغط على 'تسجيل مصروف'.",
            "كيف أضيف إيراد عام؟": "من القائمة الرئيسية، اختر 'ايرادات و مصروفات عامة' ثم اضغط على 'تسجيل إيراد'.",
            "كيف أبحث في قاعدة البيانات؟": "استخدم مربع البحث في نافذة قاعدة البيانات وحدد الجدول المطلوب.",
            "كيف أستخدم التقارير؟": "من القائمة الرئيسية، اختر 'التقارير' ثم حدد التقرير المطلوب.",
            "كيف أغير كلمة المرور؟": "من نافذة المستخدمين، اختر اسمك ثم اضغط على 'تغيير كلمة المرور'.",
            "كيف أعمل نسخة احتياطية للبيانات؟": "من الإعدادات، اختر 'نسخة احتياطية' واتبع التعليمات.",
            "كيف أسترجع نسخة احتياطية؟": "من الإعدادات، اختر 'استرجاع نسخة احتياطية' واتبع التعليمات.",
            "كيف أضيف وردية يومية؟": "من قاعدة البيانات، اختر 'الورديات اليومية' ثم اضغط على 'إضافة وردية'.",
            "كيف أضيف أمر إنتاج؟": "من القائمة الرئيسية، اختر 'أمر إنتاج' ثم أدخل البيانات المطلوبة.",
            "كيف أبحث عن سجل موظف؟": "استخدم مربع البحث في نافذة الموظفين أو قاعدة البيانات.",
            "كيف أبحث عن سجل مورد؟": "استخدم مربع البحث في نافذة الموردين أو قاعدة البيانات.",
            "كيف أبحث عن سجل منتج؟": "استخدم مربع البحث في نافذة المنتجات أو قاعدة البيانات.",
            "كيف أبحث عن سجل فاتورة؟": "استخدم مربع البحث في نافذة الفواتير أو قاعدة البيانات.",
            "مساعدة": "اسألني عن إضافة أو تعديل أو بحث أو تقارير أو إعدادات أو أي وظيفة أخرى في التطبيق.",
        }
        # ...rest of open_chatbot...
    
        # Dropdown for questions
        selected_question = tk.StringVar()
        question_dropdown = ttk.Combobox(entry_frame, textvariable=selected_question, values=questions, font=("Arial", 14), state="readonly")
        question_dropdown.pack(fill="x", padx=8, pady=8)
    
        def on_select(event=None):
            q = selected_question.get()
            if not q:
                return
            chat_text.config(state="normal")
            chat_text.insert("end", f"أنت: {q}\n")
            reply = replies.get(q, "عذراً، لم أفهم سؤالك. جرب كلمة 'مساعدة'.")
            chat_text.insert("end", f"المساعد: {reply}\n\n")
            chat_text.config(state="disabled")
            chat_text.see("end")
    
        question_dropdown.bind("<<ComboboxSelected>>", on_select)
    
        # Optionally, show a welcome/help message
        chat_text.config(state="normal")
        chat_text.insert("end", "مرحباً! اختر سؤالاً من الأسئلة الشائعة بالأسفل.\n\n")
        chat_text.config(state="disabled")
    def create_chatbot_button(self):
        import config
        """Create and animate the chatbot GIF button in the main menu"""
        chatbot_icon_path = os.path.join(BASE_DIR, "Static", "images", "chatbot.gif")
        
        # Initialize animation variables
        self.app.gif_frames = []
        self.app.current_gif_frame = 0  # Initialize frame counter
        
        try:
            with Image.open(chatbot_icon_path) as gif:
                # Get total frames (some GIFs report 0 for n_frames)
                total_frames = gif.n_frames if hasattr(gif, 'n_frames') else 0
                
                if total_frames > 0:
                    for frame in range(total_frames):
                        gif.seek(frame)
                        resized_frame = gif.copy().resize((60, 60), Image.LANCZOS)
                        self.app.gif_frames.append(ImageTk.PhotoImage(resized_frame))
                else:
                    # Handle single-frame GIFs or invalid frame counts
                    resized_frame = gif.copy().resize((60, 60), Image.LANCZOS)
                    self.app.gif_frames.append(ImageTk.PhotoImage(resized_frame))
                    
        except Exception as e:
            print(f"Error loading GIF: {e}")
            # Fallback to blank image
            blank_img = Image.new('RGBA', (60, 60), (0, 0, 0, 0))
            self.app.gif_frames = [ImageTk.PhotoImage(blank_img)]
        
        # Create the button
        self.app.chatbot_main_btn = tk.Label(
            self.root,
            image=self.app.gif_frames[0],
            bg=config.COLORS["card"],
            cursor="hand2"
        )
        # Initial placement (bottom-left, 1% from left, 95% from top)
        self.app.chatbot_main_btn.place(relx=0.01, rely=0.97, anchor='sw')

        def start_drag(event):
            widget = event.widget
            # Store initial cursor position (window-relative)
            widget._drag_start_x = event.x_root - widget.winfo_rootx()
            widget._drag_start_y = event.y_root - widget.winfo_rooty()

        def do_drag(event):
            widget = event.widget
            if hasattr(widget, '_drag_start_x'):
                # Calculate new position in window coordinates
                new_x = event.x_root - widget._drag_start_x
                new_y = event.y_root - widget._drag_start_y
                
                # Convert to relative (0.0-1.0) coordinates
                relx = new_x / widget.winfo_toplevel().winfo_width()
                rely = new_y / widget.winfo_toplevel().winfo_height()
                
                # Constrain to window bounds
                relx = max(0.0, min(relx, 0.99))  # 1% margin
                rely = max(0.0, min(rely, 0.99))
                
                # Update position
                widget.place(relx=relx, rely=rely, anchor='nw')  # Anchor NW for smooth dragging

        def on_drag_end(event):
            self.open_chatbot()  # Your original functionality

        # Bind events
        self.app.chatbot_main_btn.bind("<Button-1>", start_drag)
        self.app.chatbot_main_btn.bind("<B1-Motion>", do_drag)
        self.app.chatbot_main_btn.bind("<ButtonRelease-1>", on_drag_end)
        
        # Start animation if we have multiple frames
        if len(self.app.gif_frames) > 1:
            self.animate_gif()

    def animate_gif(self):
        """Handle GIF animation"""
        if not hasattr(self.app, 'chatbot_main_btn') or not self.app.chatbot_main_btn.winfo_exists():
            return  # Stop if button doesn't exist
        
        self.app.current_gif_frame = (self.app.current_gif_frame + 1) % len(self.app.gif_frames)
        self.app.chatbot_main_btn.config(image=self.app.gif_frames[self.app.current_gif_frame])
        self.root.after(100, self.animate_gif)  # Continue animation