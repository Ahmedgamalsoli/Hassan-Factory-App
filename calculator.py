# ======================
# Used imports
# ======================

import tkinter as tk
import os
import matplotlib
import matplotlib.pyplot as plt
import sys

matplotlib.use('TkAgg')  # Set the backend before importing pyplot

# ======================
# Files Imports
# ======================
# from calculator import CalculatorPopup
# from Login import LoginWindow
# from AuxiliaryClass import AlwaysOnTopInputDialog

# Determine the base directory
if getattr(sys, "frozen", False):
    # Running as an executable
    BASE_DIR = sys._MEIPASS
else:
    # Running as a script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def open_calculator():
    calc_win = tk.Toplevel()
    calc_win.title("Calculator")
    calc_win.configure(bg="#2e2e2e")
    calc_win.resizable(False, False)

    # Set window icon (shows in title bar and taskbar)
    icon_path = os.path.join(BASE_DIR, "Static", "images", "calculator-1.ico")
    if os.path.exists(icon_path):
        try:
            calc_win.iconbitmap(icon_path)
        except Exception as e:
            print(f"Calculator icon error: {e}")

    # ...rest of your calculator code...

    entry = tk.Entry(calc_win, width=18, font=('Helvetica', 28), bd=0, bg="#1e1e1e", fg="white", justify='right')
    entry.grid(row=0, column=0, columnspan=4, pady=(10, 20), padx=10, ipady=20)

    # Button styles
    btn_config = {
        "font": ('Helvetica', 18),
        "bd": 0,
        "width": 5,
        "height": 2,
        "bg": "#3c3f41",
        "fg": "white",
        "activebackground": "#505354",
        "activeforeground": "white"
    }

    special_btn_config = {
        "=": {"bg": "#4caf50", "activebackground": "#45a049"},
        "C": {"bg": "#f44336", "activebackground": "#e53935"},
        "÷": {"bg": "#ff9800"},
        "x": {"bg": "#ff9800"},
        "-": {"bg": "#ff9800"},
        "+": {"bg": "#ff9800"},
        "()": {"bg": "#ff9800"},
        "%": {"bg": "#ff9800"},
    }

    def calculate(expression):
        """Safely evaluate a mathematical expression with percentage support"""
        try:
            # Replace symbols with Python operators
            expression = expression.replace('x', '*').replace('÷', '/')
            
            # Handle percentages by replacing them with their decimal equivalents
            # This needs to handle cases where % follows a number in an expression
            tokens = []
            current_token = ''
            
            for char in expression:
                if char.isdigit() or char == '.':
                    current_token += char
                else:
                    if current_token:
                        tokens.append(current_token)
                        current_token = ''
                    tokens.append(char)
            
            if current_token:
                tokens.append(current_token)
            
            # Process the tokens to handle percentages
            processed_tokens = []
            i = 0
            while i < len(tokens):
                token = tokens[i]
                if token == '%':
                    if i > 0 and tokens[i-1].replace('.', '').isdigit():
                        # Convert the previous number to percentage (divide by 100)
                        num = float(tokens[i-1]) / 100
                        processed_tokens[-1] = str(num)
                    else:
                        processed_tokens.append(token)
                else:
                    processed_tokens.append(token)
                i += 1
            
            # Rebuild the expression
            processed_expr = ''.join(processed_tokens)
            
            # Evaluate the expression
            return str(eval(processed_expr))
        except:
            return "Error"

    def on_click(value):
        current = entry.get()
        
        if value == '=':
            try:
                result = calculate(current)
                entry.delete(0, tk.END)
                entry.insert(tk.END, result)
            except:
                entry.delete(0, tk.END)
                entry.insert(tk.END, "Error")
        elif value == 'C':
            entry.delete(0, tk.END)
        elif value == '()':
            if '(' not in current:
                entry.insert(tk.END, '(')
            elif ')' not in current[current.index('('):]:
                entry.insert(tk.END, ')')
            else:
                entry.insert(tk.END, 'x(')
        elif value == '+/-':
            if current.startswith('-'):
                entry.delete(0)
            else:
                entry.insert(0, '-')
        elif value == '%':
            entry.insert(tk.END, '%')
        else:
            entry.insert(tk.END, value)

    buttons = [
        'C'  , '()', '%', '÷',
        '7'  , '8' , '9', 'x',
        '4'  , '5' , '6', '-',
        '1'  , '2' , '3', '+',
        '+/-', '0' , '.', '='
    ]

    row, col = 1, 0
    for btn in buttons:
        style = btn_config.copy()
        if btn in special_btn_config:
            style.update(special_btn_config[btn])

        pady_val = 5
        if row == 5:
            pady_val = 20  

        tk.Button(calc_win, text=btn, command=lambda b=btn: on_click(b), **style).grid(
            row=row, column=col, padx=5, pady=pady_val
        )

        col += 1
        if col >3:
            col = 0
            row += 1