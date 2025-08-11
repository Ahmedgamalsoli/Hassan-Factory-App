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
class EmployeeWindow:
    def __init__(self, root, app):
        self.root = root
        self.app = app  # save reference to SalesSystemApp


    def manage_Employees_window(self):
                # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.configure(bg=config.COLORS["background"])
        # Create the top bar
        self.app.topbar.topbar(show_back_button=True)

        button_frame = tk.Frame(self.root, bg=config.COLORS["background"])
        button_frame.pack(pady=30)

        # Define buttons with images, text, and commands
        if self.app.light:
            buttons = [
                {"text": self.app.AuxiliaryClass.t("Employee hours"), "image": "emp_hour-dark.png", 
                "command": lambda: self.employee_hours_window(self.app.user_role)},
                {"text": self.app.AuxiliaryClass.t("Employee Withdrawals"), "image": "emp_with-dark.png", 
                "command": lambda: self.employee_withdrowls_window(self.app.user_role)},
                {"text": self.app.AuxiliaryClass.t("Employee Statistics"), "image": "emp_salary-dark.png", 
                "command": lambda: self.employee_statistics_window(self.app.user_role)},
            ]
        elif not self.app.light:
            buttons = [
                {"text": self.app.AuxiliaryClass.t("Employee hours"), "image": "emp_hour-light.png", 
                "command": lambda: self.employee_hours_window(self.app.user_role)},
                {"text": self.app.AuxiliaryClass.t("Employee Withdrawals"), "image": "emp_with-light.png", 
                "command": lambda: self.employee_withdrowls_window(self.app.user_role)},
                {"text": self.app.AuxiliaryClass.t("Employee Statistics"), "image": "emp_salary-light.png", 
                "command": lambda: self.employee_statistics_window(self.app.user_role)},
            ]
        images = []  # Keep references to prevent garbage collection
        columns_per_row = 3  # Number of buttons per row
        button_size = 120
        try:
            for index, btn_info in enumerate(buttons):
                # Default transparent image
                img_path = os.path.join(BASE_DIR, "Static", "images", btn_info["image"])
                original_img = Image.open(img_path).convert("RGBA")
                transparent_img = original_img.resize((button_size, button_size), Image.LANCZOS)
                photo_transparent = ImageTk.PhotoImage(transparent_img)

                # Image with background
                bg_color = (0,0,0,0)  # F5F7FA in RGBA
                bg_img = Image.new("RGBA", original_img.size, bg_color)
                composited_img = Image.alpha_composite(bg_img, original_img)
                resized_composited = composited_img.resize((button_size, button_size), Image.LANCZOS)
                photo_with_bg = ImageTk.PhotoImage(resized_composited)

                # Save both images
                images.append(photo_transparent)
                images.append(photo_with_bg)

                # Calculate grid position
                row = index // columns_per_row
                column = index % columns_per_row

                # Create sub-frame for each button
                sub_frame = tk.Frame(button_frame, bg=config.COLORS["background"])
                sub_frame.grid(row=row, column=column, padx=20, pady=20)

                # Image button
                btn = tk.Button(sub_frame, image=photo_transparent, bd=0,
                                text=btn_info["text"], 
                                font=("Arial", 15, "bold"),
                                compound=tk.TOP,
                                bg=config.COLORS["background"],
                                fg=config.COLORS["text"],
                                activebackground=config.COLORS["highlight"],
                                command=btn_info["command"])
                btn.image_transparent = photo_transparent
                btn.image_with_bg = photo_with_bg
                btn.pack()
                
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=config.COLORS["primary"]))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=config.COLORS["background"]))

                # # Text label
                # lbl = tk.Label(sub_frame, text=btn_info["text"], 
                #             font=("Arial", 15, "bold"), bg=config.COLORS["background"], fg="#003366")
                # lbl.pack(pady=5)

        except Exception as e:
            print(f"Error loading images: {e}")
            # Fallback to text buttons if images fail
            fallback_frame = tk.Frame(self.root, bg=config.COLORS["background"])
            fallback_frame.pack(pady=20)
            for btn_info in buttons:
                tk.Button(fallback_frame, text=btn_info["text"], 
                        command=btn_info["command"]).pack(side="left", padx=10)


    def employee_hours_window(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()
        

        self.app.topbar.topbar(show_back_button=True, Back_to_Employee_Window=True)
        
        # Database collections
        employees_col = self.app.AuxiliaryClass.get_collection_by_name("Employees")
        appointments_col = self.app.AuxiliaryClass.get_collection_by_name("Employee_appointments")

        # Create mappings
        self.app.employee_code_name = {}
        self.app.employee_name_code = {}
        for emp in employees_col.find():
            code = emp.get('Id', '')
            name = emp.get('Name', '')
            self.app.employee_code_name[code] = name
            self.app.employee_name_code[name] = code

        # Main frame
        # self.root.configure(bg="#f0f0f0")
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Selection frame
        selection_frame = tk.Frame(main_frame)
        selection_frame.pack(fill=tk.X, pady=10)

        # Employee name dropdown
        tk.Label(selection_frame, text=self.app.AuxiliaryClass.t("Employee Name:")).pack(side=tk.LEFT, padx=5)
        self.app.name_var = tk.StringVar()
        name_cb = ttk.Combobox(selection_frame, textvariable=self.app.name_var, width=25)
        name_cb.pack(side=tk.LEFT, padx=5)
        name_cb.bind('<<ComboboxSelected>>', self.update_employee_code)

        # Employee code dropdown
        tk.Label(selection_frame, text=self.app.AuxiliaryClass.t("Employee Code:")).pack(side=tk.LEFT, padx=5)
        self.app.code_var = tk.StringVar()
        code_cb = ttk.Combobox(selection_frame, textvariable=self.app.code_var, width=15)
        code_cb.pack(side=tk.LEFT, padx=5)
        code_cb.bind('<<ComboboxSelected>>', self.update_employee_name)

        # Update dropdown values
        name_cb['values'] = list(self.app.employee_name_code.keys())
        code_cb['values'] = list(self.app.employee_code_name.keys())

        # Check-in/out button
        tk.Button(selection_frame, text=self.app.AuxiliaryClass.t("Check In/Out"), command=lambda: self.toggle_check_in_out(employees_col, appointments_col)).pack(side=tk.RIGHT, padx=10)
        # tk.Button(selection_frame, text=self.app.AuxiliaryClass.t("Check In/Out"), command=lambda: self.toggle_check_in_out(employees_col, appointments_col)).pack(side=tk.RIGHT, padx=10)

        # Checked-in employees treeview
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ("Employee Name", "Check-in Time", "Duration")
        self.app.checkin_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        for col in columns:
            self.app.checkin_tree.heading(col, text=self.app.AuxiliaryClass.t(col))
            self.app.checkin_tree.column(col, width=150, anchor='center')
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.app.checkin_tree.yview)
        self.app.checkin_tree.configure(yscrollcommand=vsb.set)
        
        self.app.checkin_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # Load initial check-ins
        self.update_checkin_tree(appointments_col)

    def update_employee_code(self, event):
        name = self.app.name_var.get()
        if name in self.app.employee_name_code:
            self.app.code_var.set(self.app.employee_name_code[name])

    def update_employee_name(self, event):
        code = self.app.code_var.get()
        if code in self.app.employee_code_name:
            self.app.name_var.set(self.app.employee_code_name[code])

    def toggle_check_in_out(self, employees_col, appointments_col):
        code = self.app.code_var.get()
        name = self.app.name_var.get()
        
        if not code or not name:
            messagebox.showerror(self.app.AuxiliaryClass.t("Error"), self.app.AuxiliaryClass.t("Please select an employee"))
            return
        
        # Check existing appointment
        existing = appointments_col.find_one({
            'employee_code': code,
             '$or': [
                {'check_out': {'$exists': False}},
                {'check_out': None}
            ]
        })
        
        try:
            if existing:
                # Check out
                check_out_time = datetime.now()
                duration = check_out_time - existing['check_in']
                
                appointments_col.update_one(
                    {'_id': existing['_id']},
                    {'$set': {
                        'check_out': check_out_time,
                        'duration': duration.total_seconds() / 3600  # in hours
                    }}
                )
                config.report_log(self.app.logs_collection, self.app.user_name, None, f"{existing['employee_name']} {self.app.AuxiliaryClass.t("Checked out with Id")} {existing['employee_code']}", None,self.app.AuxiliaryClass.t)

            else:
                # Check in
                appointments_col.insert_one({
                    'employee_code': code,
                    'employee_name': name,
                    'check_in': datetime.now(),
                    'check_out': None,
                    'duration': None
                })
                config.report_log(self.app.logs_collection, self.app.user_name, None, f"{name} {self.app.AuxiliaryClass.t("Checked in with Id")} {code}", None,self.app.AuxiliaryClass.t)

            self.update_checkin_tree(appointments_col)
            messagebox.showinfo(self.app.AuxiliaryClass.t("Success"), f"{name} {self.app.AuxiliaryClass.t("checked")} {self.app.AuxiliaryClass.t('out') if existing else self.app.AuxiliaryClass.t('in')} {self.app.AuxiliaryClass.t("successfully")}")
            
        except PyMongoError as e:
            messagebox.showerror(self.app.AuxiliaryClass.t("Database Error"), str(e))

    def update_checkin_tree(self, appointments_col):
        # Clear existing data
        for item in self.app.checkin_tree.get_children():
            self.app.checkin_tree.delete(item)
        
        # Get active check-ins
        active_appointments = appointments_col.find({
            '$or': [
            {'check_out': {'$exists': False}},
            {'check_out': None}
        ]
        }).sort('check_in', -1)
        
        for appt in active_appointments:
            # Convert string to datetime object
            check_in_value = appt.get('check_in', '')
            formatted_time = "Invalid timestamp"
            
            try:
                if isinstance(check_in_value, datetime):
                    formatted_time = check_in_value.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    # Handle string representations
                    if '.' in check_in_value:  # Handle milliseconds
                        check_in_time = datetime.strptime(check_in_value, "%Y-%m-%d %H:%M:%S.%f")
                    else:
                        check_in_time = datetime.strptime(check_in_value, "%Y-%m-%d %H:%M:%S")
                    formatted_time = check_in_time.strftime("%Y-%m-%d %H:%M:%S")
                    
            except (ValueError, TypeError, AttributeError) as e:
                print(f"Timestamp error: {str(e)}")
            
            self.app.checkin_tree.insert('', 'end', values=(
                appt.get('employee_name', ''),
                formatted_time,
                self.app.AuxiliaryClass.t('Still checked in')
            ))

    def employee_withdrowls_window(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        self.app.topbar.topbar(show_back_button=True, Back_to_Employee_Window=True)

        # Database collections
        employees_col = self.app.AuxiliaryClass.get_collection_by_name("Employees")
        withdrawals_col = self.app.AuxiliaryClass.get_collection_by_name("Employee_withdrawls")
        # Create mappings
        self.app.employee_code_map = {}
        self.app.employee_name_map = {}
        for emp in employees_col.find():
            code = emp.get('Id', '')
            name = emp.get('Name', '')
            self.app.employee_code_map[code] = name
            self.app.employee_name_map[name] = code
        # Main frame with left alignment
        main_frame = tk.Frame(self.root, padx=40, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True, anchor='nw')

        # Configure grid layout
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=3)

        # Employee Selection Section
        tk.Label(main_frame, text=self.app.AuxiliaryClass.t("Employee Selection"), font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10, sticky='w')
        tk.Label(main_frame, text=self.app.AuxiliaryClass.t("Employee Selection"), font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10, sticky='w')
        
        # Employee Name Dropdown
        tk.Label(main_frame, text=self.app.AuxiliaryClass.t("Employee Name:"), font=('Helvetica', 12)).grid(row=1, column=0, pady=5, sticky='w')
        tk.Label(main_frame, text=self.app.AuxiliaryClass.t("Employee Name:"), font=('Helvetica', 12)).grid(row=1, column=0, pady=5, sticky='w')
        self.app.withdraw_name_var = tk.StringVar()
        name_cb = ttk.Combobox(main_frame, textvariable=self.app.withdraw_name_var, 
                            width=30, font=('Helvetica', 12))
        name_cb.grid(row=1, column=1, pady=5, padx=10, sticky='w')
        name_cb.bind('<<ComboboxSelected>>', self.update_withdraw_code)

        # Employee Code Dropdown
        tk.Label(main_frame, text=self.app.AuxiliaryClass.t("Employee Code:"), font=('Helvetica', 12)).grid(row=2, column=0, pady=5, sticky='w')
        tk.Label(main_frame, text=self.app.AuxiliaryClass.t("Employee Code:"), font=('Helvetica', 12)).grid(row=2, column=0, pady=5, sticky='w')
        self.app.withdraw_code_var = tk.StringVar()
        code_cb = ttk.Combobox(main_frame, textvariable=self.app.withdraw_code_var, 
                            width=30, font=('Helvetica', 12))
        code_cb.grid(row=2, column=1, pady=5, padx=10, sticky='w')
        code_cb.bind('<<ComboboxSelected>>', self.update_withdraw_name)

        # Salary Display
        tk.Label(main_frame, text=self.app.AuxiliaryClass.t("Salary:"), font=('Helvetica', 12)).grid(row=3, column=0, pady=5, sticky='w')
        tk.Label(main_frame, text=self.app.AuxiliaryClass.t("Salary:"), font=('Helvetica', 12)).grid(row=3, column=0, pady=5, sticky='w')
        self.app.salary_var = tk.StringVar()
        salary_entry = tk.Entry(main_frame, textvariable=self.app.salary_var, 
                            state='readonly', width=33, font=('Helvetica', 12))
        salary_entry.grid(row=3, column=1, pady=5, padx=10, sticky='w')

        # Withdrawal Details Section (updated row numbers)
        tk.Label(main_frame, text=self.app.AuxiliaryClass.t("Withdrawal Details"), font=('Helvetica', 14, 'bold')).grid(row=4, column=0, columnspan=2, pady=10, sticky='w')
        tk.Label(main_frame, text=self.app.AuxiliaryClass.t("Withdrawal Details"), font=('Helvetica', 14, 'bold')).grid(row=4, column=0, columnspan=2, pady=10, sticky='w')

        # Amount Entry
        tk.Label(main_frame, text=self.app.AuxiliaryClass.t("Withdrawal Amount:"), font=('Helvetica', 12)).grid(row=5, column=0, pady=5, sticky='w')
        tk.Label(main_frame, text=self.app.AuxiliaryClass.t("Withdrawal Amount:"), font=('Helvetica', 12)).grid(row=5, column=0, pady=5, sticky='w')
        self.app.amount_entry = tk.Entry(main_frame, width=33, font=('Helvetica', 12))
        self.app.amount_entry.grid(row=5, column=1, pady=5, padx=10, sticky='w')

        # Payment Method
        tk.Label(main_frame, text=self.app.AuxiliaryClass.t("Payment Method"), font=('Helvetica', 12)).grid(row=6, column=0, pady=5, sticky='w')
        tk.Label(main_frame, text=self.app.AuxiliaryClass.t("Payment Method"), font=('Helvetica', 12)).grid(row=6, column=0, pady=5, sticky='w')
        self.app.payment_method = ttk.Combobox(main_frame, 
                                        values=["Cash", "Instapay", "E_wallet", "Bank Account"],
                                        width=30, 
                                        font=('Helvetica', 12),
                                        state="readonly")
        self.app.payment_method.grid(row=6, column=1, pady=5, padx=10, sticky='w')

        # Previous Withdrawals
        tk.Label(main_frame, text=self.app.AuxiliaryClass.t("Previous Withdrawals:"), font=('Helvetica', 12)).grid(row=7, column=0, pady=5, sticky='w')
        tk.Label(main_frame, text=self.app.AuxiliaryClass.t("Previous Withdrawals:"), font=('Helvetica', 12)).grid(row=7, column=0, pady=5, sticky='w')
        self.app.prev_withdrawals = tk.Entry(main_frame, 
                                    state='readonly', 
                                    width=33, 
                                    font=('Helvetica', 12))
        self.app.prev_withdrawals.grid(row=7, column=1, pady=5, padx=10, sticky='w')

        # Save Button (updated row number)
        save_btn = tk.Button(main_frame, 
                            text=self.app.AuxiliaryClass.t("💾 Save Withdrawal"), 
                            font=('Helvetica', 12, 'bold'),
                            width=20,
                            command=lambda: self.save_withdrawal(withdrawals_col, employees_col),
                            bg='#2196F3', fg='white')
        save_btn.grid(row=8, column=0, columnspan=2, pady=20)

        # Update dropdown values
        name_cb['values'] = list(self.app.employee_name_map.keys())
        code_cb['values'] = list(self.app.employee_code_map.keys())

        # Bind selection updates
        self.app.withdraw_name_var.trace_add('write', self.update_previous_withdrawals)
        self.app.withdraw_code_var.trace_add('write', self.update_previous_withdrawals)

    def update_withdraw_code(self, event):
        name = self.app.withdraw_name_var.get()
        if name in self.app.employee_name_map:
            self.app.withdraw_code_var.set(self.app.employee_name_map[name])

    def update_withdraw_name(self, event):
        code = self.app.withdraw_code_var.get()
        if code in self.app.employee_code_map:
            self.app.withdraw_name_var.set(self.app.employee_code_map[code])

    def update_previous_withdrawals(self, *args):
        code = self.app.withdraw_code_var.get()
        name = self.app.withdraw_name_var.get()
        
        if not code and name in self.app.employee_name_map:
            code = self.app.employee_name_map[name]
        elif not name and code in self.app.employee_code_map:
            name = self.app.employee_code_map[code]
        
        if code:
            # Update previous withdrawals
            total = self.calculate_previous_withdrawals(code)
            self.app.prev_withdrawals.config(state='normal')
            self.app.prev_withdrawals.delete(0, tk.END)
            self.app.prev_withdrawals.insert(0, f"{total:.2f}")
            self.app.prev_withdrawals.config(state='readonly')
            
            # Update salary display
            employees_col = self.app.AuxiliaryClass.get_collection_by_name("Employees")
            code = int(code)
            emp = employees_col.find_one({'Id': code})
            if emp:
                salary = emp.get('Salary', 0)
                salary = float(salary)
                self.app.salary_var.set(f"{salary:.2f}")
            else:
                self.app.salary_var.set("0.00")

    def calculate_previous_withdrawals(self, employee_code):
        withdrawals_col = self.app.AuxiliaryClass.get_collection_by_name("Employee_withdrawls")
        total = 0
        for withdrawal in withdrawals_col.find({'employee_code': employee_code}):
            total += withdrawal.get('amount_withdrawls', 0)
        return total

    def save_withdrawal(self, withdrawals_col, employees_col):
        code = self.app.withdraw_code_var.get()
        name = self.app.withdraw_name_var.get()
        amount = self.app.amount_entry.get()
        method = self.app.payment_method.get()

        if not code or not name:
            messagebox.showerror(self.app.AuxiliaryClass.t("Error"), self.app.AuxiliaryClass.t("Please select an employee"))
            return
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(self.app.AuxiliaryClass.t("Error"), self.app.AuxiliaryClass.t("Invalid amount entered"))
            return

        if not method:
            messagebox.showerror(self.app.AuxiliaryClass.t("Error"), self.app.AuxiliaryClass.t("Please select payment method"))
            return

        try:
            # Calculate previous total before this withdrawal
            previous_total = self.calculate_previous_withdrawals(code)
            
            # Save withdrawal record with cumulative tracking
            withdrawal_data = {
                'employee_code': code,
                'employee_name': name,
                'previous_withdrawls': previous_total,  # Total before this withdrawal
                'amount_withdrawls': amount,
                # 'cumulative_total': previous_total + amount,  # New total after this withdrawal
                'payment_method': method,
                'timestamp': datetime.now()
            }
            withdrawals_col.insert_one(withdrawal_data)

            # Update employee's total withdrawals
            employees_col.update_one(
                {'employee_code': code},
                {'$set': {'previous_withdrawls': previous_total + amount}}
            )

            messagebox.showinfo(self.app.AuxiliaryClass.t("Success"), self.app.AuxiliaryClass.t("Withdrawal recorded successfully"))
            
            config.report_log(self.app.logs_collection, self.app.user_name, None, f"{self.app.AuxiliaryClass.t("Completed withdrawal in Employee_withdrawls Database for")} {withdrawal_data['employee_name']} {self.app.AuxiliaryClass.t("with Id")} {withdrawal_data['employee_code']}", None,self.app.AuxiliaryClass.t)

            self.app.amount_entry.delete(0, tk.END)
            self.app.payment_method.set('')
            self.update_previous_withdrawals()

        except PyMongoError as e:
            messagebox.showerror(self.app.AuxiliaryClass.t("Database Error"), f"{self.app.AuxiliaryClass.t("Failed to save withdrawal:")} {str(e)}")

    def employee_statistics_window(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.app.topbar.topbar(show_back_button=True, Back_to_Employee_Window=True)
        
        # Database connections
        employees_col = self.app.AuxiliaryClass.get_collection_by_name("Employees")
        
        # Employee mappings
        self.app.employee_code_map = {}
        self.app.employee_name_map = {}
        for emp in employees_col.find():
            code = int(emp.get('Id', ''))
            name = emp.get('Name', '')
            self.app.employee_code_map[code] = {
                'name': name,
                'salary': float(emp.get('Salary', 0))
            }
            self.app.employee_name_map[name] = {
                'code': code,
                'salary': float(emp.get('Salary', 0))
            }

        # Main container
        main_frame = ttk.Frame(self.root, padding=(20, 10))
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Employee Selection
        selection_frame = ttk.LabelFrame(main_frame, text=self.app.AuxiliaryClass.t("Employee Selection"), padding=10)
        selection_frame.grid(row=0, column=0, sticky='ew', pady=5)
        
        ttk.Label(selection_frame, text=self.app.AuxiliaryClass.t("Name:")).grid(row=0, column=0, padx=5, sticky='e')
        self.app.emp_name_var = tk.StringVar()
        self.app.name_cb = ttk.Combobox(selection_frame, textvariable=self.app.emp_name_var, width=25)
        self.app.name_cb.grid(row=0, column=1, padx=5, sticky='ew')
        self.app.name_cb.bind('<<ComboboxSelected>>', self.update_salary_name)
        # code_cb.grid(row=2, column=1, pady=5, padx=10, sticky='w')
        # code_cb.bind('<<ComboboxSelected>>', self.update_withdraw_name)
        ttk.Label(selection_frame, text=self.app.AuxiliaryClass.t("Code:")).grid(row=0, column=2, padx=(15,5), sticky='e')
        self.app.emp_code_var = tk.StringVar()
        self.app.code_cb = ttk.Combobox(selection_frame, textvariable=self.app.emp_code_var, width=10)
        self.app.code_cb.grid(row=0, column=3, padx=5, sticky='ew')
        self.app.code_cb.bind('<<ComboboxSelected>>', self.update_salary_code)

        # Date Selection
        date_frame = ttk.LabelFrame(main_frame, text=self.app.AuxiliaryClass.t("Month/Year Selection"), padding=10)
        date_frame.grid(row=1, column=0, sticky='ew', pady=5)
        
        ttk.Label(date_frame, text=self.app.AuxiliaryClass.t("Month:")).grid(row=0, column=0, padx=5, sticky='e')
        self.app.month_var = tk.StringVar()
        self.app.month_cb = ttk.Combobox(date_frame, textvariable=self.app.month_var, 
                                values=["January", "February", "March", "April", "May", "June",
                                        "July", "August", "September", "October", "November", "December"],
                                width=12)
        self.app.month_cb.grid(row=0, column=1, padx=5, sticky='w')
        
        ttk.Label(date_frame, text=self.app.AuxiliaryClass.t("Year:")).grid(row=0, column=2, padx=(15,5), sticky='e')
        self.app.year_var = tk.StringVar()
        self.app.year_cb = ttk.Combobox(date_frame, textvariable=self.app.year_var, 
                                values=[str(year) for year in range(2020, 2040)],
                                width=6)
        self.app.year_cb.grid(row=0, column=3, padx=5, sticky='w')

        ttk.Label(date_frame, text=self.app.AuxiliaryClass.t("From Date:")).grid(row=0, column=4, padx=5, sticky='e')
        self.app.from_date_var = tk.StringVar()
        self.app.to_date_var = tk.StringVar()
        # Replace the Entry widgets with:
        DateEntry(date_frame, textvariable=self.app.from_date_var, date_pattern='dd-mm-yyyy').grid(row=0, column=5)
        ttk.Label(date_frame, text=self.app.AuxiliaryClass.t("To Date:")).grid(row=0, column=6, padx=5, sticky='e')
        DateEntry(date_frame, textvariable=self.app.to_date_var, date_pattern='dd-mm-yyyy').grid(row=0, column=7)
        # Working Hours
        hours_frame = ttk.LabelFrame(main_frame, text=self.app.AuxiliaryClass.t("Working Hours"), padding=10)
        hours_frame.grid(row=2, column=0, sticky='ew', pady=5)
        
        ttk.Label(hours_frame, text=self.app.AuxiliaryClass.t("Start Time:")).grid(row=0, column=0, padx=5, sticky='e')
        self.app.start_time_var = tk.StringVar()
        ttk.Entry(hours_frame, textvariable=self.app.start_time_var, width=10).grid(row=0, column=1, padx=5, sticky='w')
        ttk.Label(hours_frame, text="(e.g., 9:00 AM)").grid(row=0, column=2, padx=5, sticky='w')
        
        ttk.Label(hours_frame, text=self.app.AuxiliaryClass.t("End Time:")).grid(row=0, column=3, padx=(15,5), sticky='e')
        self.app.end_time_var = tk.StringVar()
        ttk.Entry(hours_frame, textvariable=self.app.end_time_var, width=10).grid(row=0, column=4, padx=5, sticky='w')
        ttk.Label(hours_frame, text="(e.g., 5:00 PM)").grid(row=0, column=5, padx=5, sticky='w')

        # Attendance Table
        table_frame = ttk.Frame(main_frame)
        table_frame.grid(row=3, column=0, sticky='nsew', pady=10)
        
        columns = ("Date", "From", "To", "Duration", "Delay", "More", "Withdrawls")
        self.app.table = ttk.Treeview(table_frame, columns=columns, show='headings', selectmode='browse')
        self.app.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.app.table.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.app.table.configure(yscrollcommand=vsb.set)
        
        for col in columns:
            self.app.table.heading(col, text=self.app.AuxiliaryClass.t(col), anchor='center')
            self.app.table.column(col, width=100, anchor='center')

        # Totals Section
        totals_frame = ttk.Frame(main_frame)
        totals_frame.grid(row=4, column=0, sticky='ew', pady=5)
        
        ttk.Label(totals_frame, text=self.app.AuxiliaryClass.t("Total Withdrawls:")).grid(row=0, column=0, padx=5, sticky='e')
        self.app.total_withdrawls = ttk.Entry(totals_frame, width=12, state='readonly')
        self.app.total_withdrawls.grid(row=0, column=1, padx=5, sticky='w')
        
        ttk.Label(totals_frame, text=self.app.AuxiliaryClass.t("Delay Amount:")).grid(row=0, column=2, padx=(20,5), sticky='e')
        self.app.delay_amount = ttk.Entry(totals_frame, width=12)
        self.app.delay_amount.grid(row=0, column=3, padx=5, sticky='w')
        
        ttk.Label(totals_frame, text=self.app.AuxiliaryClass.t("Overtime Amount:")).grid(row=0, column=4, padx=(20,5), sticky='e')
        self.app.overtime_amount = ttk.Entry(totals_frame, width=12)
        self.app.overtime_amount.grid(row=0, column=5, padx=5, sticky='w')

        # Payment Section
        payment_frame = ttk.Frame(main_frame)
        payment_frame.grid(row=5, column=0, sticky='ew', pady=5)
        
        ttk.Label(payment_frame, text=self.app.AuxiliaryClass.t("Payment Method:")).grid(row=0, column=0, padx=5, sticky='e')
        self.app.payment_method = ttk.Combobox(payment_frame, 
                                        values=["Cash", "Instapay", "E_wallet", "Bank_account"],
                                        state="readonly",
                                        width=15)
        self.app.payment_method.grid(row=0, column=1, padx=5, sticky='w')
        
        ttk.Label(payment_frame, text=self.app.AuxiliaryClass.t("Base Salary:")).grid(row=0, column=2, padx=(20,5), sticky='e')
        self.app.salary = ttk.Entry(payment_frame, width=15, state='readonly')
        self.app.salary.grid(row=0, column=3, padx=5, sticky='w')
        
        ttk.Label(payment_frame, text=self.app.AuxiliaryClass.t("Net Salary:")).grid(row=0, column=4, padx=(20,5), sticky='e')
        self.app.net_salary = ttk.Entry(payment_frame, width=15, state='readonly')
        self.app.net_salary.grid(row=0, column=5, padx=5, sticky='w')

        # Save Button
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=6, column=0, pady=15)
        ttk.Button(btn_frame, text=self.app.AuxiliaryClass.t("Save Salary Record"), command=self.save_salary).pack()

        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        # Initialize data
        self.app.name_cb['values'] = list(self.app.employee_name_map.keys())
        self.app.code_cb['values'] = list(self.app.employee_code_map.keys())

        # Bind events
        # self.emp_name_var.trace_add('write', self.update_employee_info)
        # self.emp_code_var.trace_add('write', self.update_employee_info)
        self.app.from_date_var.trace_add('write', self.load_attendance_data)
        self.app.to_date_var.trace_add('write', self.load_attendance_data)
        self.app.delay_amount.bind('<KeyRelease>', self.calculate_net_salary)
        self.app.overtime_amount.bind('<KeyRelease>', self.calculate_net_salary)
        self.app.start_time_var.trace_add('write', self.load_attendance_data)
        self.app.end_time_var.trace_add('write', self.load_attendance_data)
    
    def update_salary_code(self, event):
        # Update name based on selected code
        code = self.app.emp_code_var.get()
        if code in self.app.employee_code_map:
            # Get corresponding name from code map
            new_name = self.app.employee_code_map[code]['name']
            if self.app.emp_name_var.get() != new_name:
                self.app.emp_name_var.set(new_name)
        self.load_attendance_data()

    def update_salary_name(self, event):
        # Update code based on selected name
        name = self.app.emp_name_var.get()
        if name in self.app.employee_name_map:
            # Get corresponding code from name map
            new_code = self.app.employee_name_map[name]['code']
            if self.app.emp_code_var.get() != new_code:
                self.app.emp_code_var.set(new_code)
        self.load_attendance_data()

    def update_employee_info(self, *args):
        code = self.app.emp_code_var.get()
        name = self.app.emp_name_var.get()
        
        if name in self.app.employee_name_map:
            new_code = self.app.employee_name_map[name]['code']
            if new_code != code:
                self.app.emp_code_var.set(new_code)
        
        if code in self.app.employee_code_map:
            new_name = self.app.employee_code_map[code]['name']
            if new_name != name:
                self.app.emp_name_var.set(new_name)
        
        self.load_attendance_data()

    def parse_time(self, time_str):
        try:
            return datetime.strptime(time_str, "%I:%M %p")
        except ValueError:
            return None

    def load_attendance_data(self, *args):
        self.app.table.delete(*self.app.table.get_children())
        
        # Get selected dates
        from_date_str = self.app.from_date_var.get()
        to_date_str = self.app.to_date_var.get()
        employee_code = self.app.emp_code_var.get()
        
        if not all([from_date_str, to_date_str, employee_code]):
            return
        
        # Parse dates (assuming format DD-MM-YYYY as in your image)
        try:
            from_date = datetime.strptime(from_date_str, "%d-%m-%Y")
            to_date = datetime.strptime(to_date_str, "%d-%m-%Y")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use DD-MM-YYYY")
            return
        
        # Get collections
        withdrawals_col = self.app.AuxiliaryClass.get_collection_by_name("Employee_withdrawls")
        hours_col = self.app.AuxiliaryClass.get_collection_by_name("Employee_appointimets")
        
        # Get data - include end date by adding 1 day to to_date
        withdrawals = list(withdrawals_col.find({
            'employee_code': employee_code,
            'timestamp': {'$gte': from_date, '$lte': to_date + timedelta(days=1)}
        }))
        
        attendance = list(hours_col.find({
            'employee_code': employee_code,
            'check_in': {'$gte': from_date, '$lte': to_date + timedelta(days=1)}
        }))
        
        # Get scheduled hours
        start_time = self.parse_time(self.app.start_time_var.get())
        end_time = self.parse_time(self.app.end_time_var.get())
        
        # Initialize withdrawals tracking
        daily_withdrawals = defaultdict(float)
        total_withdrawls = 0.0

        # Process all withdrawals first
        for w in withdrawals:
            w_date = w['timestamp'].date()
            amount = w.get('amount_withdrawls', 0.0)
            daily_withdrawals[w_date] += amount
            total_withdrawls += amount

        # Generate daily records
        current_date = from_date
        while current_date <= to_date:
            current_date_date = current_date.date()
            current_date_str = current_date.strftime("%Y-%m-%d")
            
            # Find attendance for this date
            daily_attendance = next((a for a in attendance 
                                if a['check_in'].date() == current_date_date), None)
            
            # Get withdrawal amount from pre-processed data
            withdrawal = daily_withdrawals.get(current_date_date, 0.0)
            
            # Initialize defaults
            from_time = "--"
            to_time = "--"
            duration = "--"
            delay = "--"
            overtime = "--"
            tags = []

            if daily_attendance:
                # Process attendance data
                check_in = daily_attendance.get('check_in')
                check_out = daily_attendance.get('check_out')
                
                from_time = check_in.strftime("%H:%M") if check_in else "--"
                to_time = check_out.strftime("%H:%M") if check_out else "--"
                
                if check_in and check_out:
                    # Calculate duration
                    duration_delta = check_out - check_in
                    hours = duration_delta.seconds // 3600
                    minutes = (duration_delta.seconds // 60) % 60
                    duration = f"{hours:02}:{minutes:02}"
                    
                    # Calculate time differences
                    if start_time:
                        scheduled_start = datetime.combine(current_date_date, start_time.time())
                        if check_in < scheduled_start:
                            delay_min = (scheduled_start - check_in).seconds // 60
                            delay = f"{delay_min} mins early"
                            tags.append('before_start')
                        elif check_in > scheduled_start:
                            delay_min = (check_in - scheduled_start).seconds // 60
                            delay = f"{delay_min} mins late"
                            tags.append('after_start')

                    if end_time and check_out:
                        scheduled_end = datetime.combine(current_date_date, end_time.time())
                        if check_out > scheduled_end:
                            overtime_min = (check_out - scheduled_end).seconds // 60
                            overtime = f"{overtime_min} mins overtime"
                            tags.append('after_end')
                        elif check_out < scheduled_end:
                            overtime_min = (scheduled_end - check_out).seconds // 60
                            overtime = f"{overtime_min} mins early"
                            tags.append('before_end')

            # Insert row with accumulated withdrawal
            self.app.table.insert('', 'end', values=(
                current_date_str,
                from_time,
                to_time,
                duration,
                delay,
                overtime,
                f"{withdrawal:.2f}"
            ), tags=tags)
            
            current_date += timedelta(days=1)
        
        # Update totals
        self.app.total_withdrawls.config(state='normal')
        self.app.total_withdrawls.delete(0, tk.END)
        self.app.total_withdrawls.insert(0, f"{total_withdrawls:.2f}")
        self.app.total_withdrawls.config(state='readonly')
        self.calculate_net_salary()

    def calculate_net_salary(self, event=None):
        try:
            base_salary = self.app.employee_code_map.get(int(self.app.emp_code_var.get()), {}).get('salary', 0)
            base_salary = float(base_salary)
            print(base_salary)
            total_withdrawls = float(self.app.total_withdrawls.get())
            delay_penalty = float(self.app.delay_amount.get() or 0)
            overtime_bonus = float(self.app.overtime_amount.get() or 0)

            net_salary = base_salary - total_withdrawls - delay_penalty + overtime_bonus
            
            self.app.net_salary.config(state='normal')
            self.app.net_salary.delete(0, tk.END)
            self.app.net_salary.insert(0, f"{net_salary:.2f}")
            self.app.net_salary.config(state='readonly')
            self.app.salary.config(state='normal')
            self.app.salary.delete(0, tk.END)
            self.app.salary.insert(0, f"{base_salary:.2f}")
            self.app.salary.config(state='readonly')
        except ValueError:
            pass

    def save_salary(self):
        try:
            salary_data = {
                'employee_code': self.app.emp_code_var.get(),
                'employee_name': self.app.emp_name_var.get(),
                'month_year': f"{self.app.month_var.get()} {self.app.year_var.get()}",
                'base_salary': self.app.employee_code_map.get(int(self.app.emp_code_var.get()), {}).get('salary', 0),
                'total_withdrawls': float(self.app.total_withdrawls.get()),
                'delay_penalty': float(self.app.delay_amount.get() or 0),
                'overtime_bonus': float(self.app.overtime_amount.get() or 0),
                'net_salary': float(self.app.net_salary.get()),
                'payment_method': self.app.payment_method.get(),
                'timestamp': datetime.now()
            }
            previous_total = self.calculate_previous_withdrawals(self.app.emp_code_var.get())
            # For string inputs like "$1000"
            try:
                withdrawal_amount = -abs(float(self.app.total_withdrawls.get().replace('$', '').strip()))
            except (ValueError, AttributeError):
                withdrawal_amount = 0.0
            withdrawal_data = {
                'employee_code': self.app.emp_code_var.get(),
                'employee_name': self.app.emp_name_var.get(),
                'previous_withdrawls': previous_total,  # Total before this withdrawal
                'amount_withdrawls': withdrawal_amount,
                # 'cumulative_total': previous_total + amount,  # New total after this withdrawal
                'payment_method': self.app.payment_method.get(),
                'timestamp': datetime.now()
            }
            
            
            # Input validation
            if not all([salary_data['employee_code'], salary_data['month_year']]):
                raise ValueError("Missing required fields")
            
            salary_col = self.app.AuxiliaryClass.get_collection_by_name("Employee_Salary")
            # Database collections
            withdrawals_col = self.app.AuxiliaryClass.get_collection_by_name("Employee_withdrawls")
            
            # Check for existing salary record
            existing = salary_col.find_one({
                "employee_code": salary_data["employee_code"],
                "month_year": salary_data["month_year"]
            })
            if not self.app.month_var.get() or not self.app.year_var.get():
                messagebox.showinfo(self.app.AuxiliaryClass.t("Warning"), self.app.AuxiliaryClass.t("Please select month and year")) 
                return           
            if existing:
                messagebox.showwarning(self.app.AuxiliaryClass.t("Warning"), 
                    self.app.AuxiliaryClass.t("Employee already took the salary in this month"))
                return

            if not self.app.payment_method.get():
                messagebox.showinfo(self.app.AuxiliaryClass.t("Warning"),self.app.AuxiliaryClass.t("Enter the payment Method"))
                return
            # Insert new record if not exists
            salary_col.insert_one(salary_data)
            withdrawals_col.insert_one(withdrawal_data)
            # self.save_withdrawal(withdrawals_col,employees_col)
            messagebox.showinfo(self.app.AuxiliaryClass.t("Success"), self.app.AuxiliaryClass.t("Salary record saved successfully"))
            config.report_log(self.app.logs_collection, self.app.user_name, None, f"{self.app.AuxiliaryClass.t("Paid salary for")} {salary_data['employee_name']} {self.app.AuxiliaryClass.t("with code")} {salary_data['employee_code']}", None,self.app.AuxiliaryClass.t)
            
        except Exception as e:
            messagebox.showerror(self.app.AuxiliaryClass.t("Error"), f"{self.app.AuxiliaryClass.t("Failed to save salary:")} {str(e)}")