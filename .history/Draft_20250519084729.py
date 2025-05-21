import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Modern color palette
COLORS = {
    "background": "#F5F7FA",       # Light grey background
    "primary": "#2A3F5F",           # Dark blue for headers
    "secondary": "#00C0A3",         # Teal for primary actions
    "accent": "#FF6F61",            # Coral for highlights
    "text": "#2A3F5F",              # Dark blue text
    "card": "#FFFFFF",              # White card backgrounds
    "chart1": "#00C0A3",            # Teal for Sales
    "chart2": "#FF6F61",            # Coral for Purchases
    "highlight": "#6C5CE7",         # Purple for interactive elements
    "table_header": "#2A3F5F",      # Dark blue table headers
    "positive": "#00C0A3",          # Teal for positive metrics
    "neutral": "#A0AEC0"            # Grey for secondary elements
}

class ModernBusinessApp:
    def __init__(self, root, user_role="admin"):
        self.root = root
        self.user_role = user_role
        self.root.state("zoomed")
        self.root.configure(bg=COLORS["background"])
        self.current_window = None
        self.custom_font = ("Segoe UI", 12)
        self.title_font = ("Segoe UI", 16, "bold")
        self.setup_styles()
        self.main_menu()

    def setup_styles(self):
        # Configure ttk styles
        style = ttk.Style()
        style.theme_create("modern", parent="alt", settings={
            "TFrame": {"configure": {"background": COLORS["background"]}},
            "TLabel": {
                "configure": {
                    "background": COLORS["background"],
                    "foreground": COLORS["text"],
                    "font": self.custom_font
                }
            },
            "TButton": {
                "configure": {
                    "anchor": "center",
                    "relief": "flat",
                    "background": COLORS["primary"],
                    "foreground": COLORS["text"],
                    "font": self.custom_font,
                    "padding": 10
                },
                "map": {
                    "background": [
                        ("active", COLORS["highlight"]),
                        ("disabled", "#95a5a6")
                    ]
                }
            }
        })
        style.theme_use("modern")

    def main_menu(self):
        self.clear_window()
        self.create_topbar()
        self.create_main_layout()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_topbar(self):
        topbar = tk.Frame(self.root, bg=COLORS["card"], height=60)
        topbar.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(topbar, 
                            text="Business Management System",
                            font=self.title_font,
                            bg=COLORS["card"],
                            fg=COLORS["text"])
        title_label.pack(side=tk.LEFT, padx=30)

        user_label = tk.Label(topbar, 
                            text=f"User: {self.user_role.upper()}",
                            font=("Segoe UI", 12),
                            bg=COLORS["card"],
                            fg=COLORS["text"])
        user_label.pack(side=tk.RIGHT, padx=30)

    def create_main_layout(self):
        main_container = tk.Frame(self.root, bg=COLORS["background"])
        main_container.pack(fill=tk.BOTH, expand=True)

        # Visualization frames
        left_viz_frame = self.create_card_frame(main_container)
        left_viz_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
        
        right_viz_frame = self.create_card_frame(main_container)
        right_viz_frame.grid(row=0, column=2, sticky="nsew", padx=20, pady=10)

        # Button frame
        button_frame = self.create_card_frame(main_container, padding=20)
        button_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)

        # Grid configuration
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=2)
        main_container.grid_columnconfigure(2, weight=1)
        main_container.grid_rowconfigure(0, weight=1)

        # Create components
        self.create_left_visualization(left_viz_frame)
        self.create_right_visualization(right_viz_frame)
        self.create_main_buttons(button_frame)

    def create_card_frame(self, parent, padding=0):
        frame = tk.Frame(parent, bg=COLORS["card"], bd=0,
                        highlightbackground=COLORS["primary"],
                        highlightthickness=2)
        if padding:
            frame.grid_propagate(False)
            frame.config(width=400, height=600)
        return frame

    def create_main_buttons(self, parent):
        buttons = [
            {"text": "New Sales Invoice", "image": "Sales.png",
            "command": lambda: self.trash(self.user_role)},
            {"text": "New Purchase Invoice", "image": "Purchase.png", 
            "command": lambda: self.trash(self.user_role)},
            {"text": "Production Order", "image": "Production Order.png", 
            "command": lambda: self.trash(self.user_role)},
            {"text": "Employee Interactions", "image": "Employees.png", 
            "command": lambda: self.trash(self.user_role)},
            {"text": "Treasury", "image": "Treasury.png", 
            "command": lambda: self.trash(self.user_role)},
            {"text": "Database", "image": "Database.png", 
            "command": lambda: self.trash(self.user_role)},
            # {"text": "Analytics", "image": "Analytics.png", 
            # "command": lambda: self.trash(self.user_role)},
        ]

        columns_per_row = 3
        button_size = 100

        try:
            for index, btn_info in enumerate(buttons):
                row = index // columns_per_row
                column = index % columns_per_row

                btn_frame = tk.Frame(parent, bg=COLORS["card"])
                btn_frame.grid(row=row, column=column, padx=15, pady=15)

                # Load and process image
                img_path = os.path.join(BASE_DIR, "Static", "images", btn_info["image"])
                img = Image.open(img_path).resize((button_size, button_size), Image.LANCZOS)
                photo_img = ImageTk.PhotoImage(img)

                # Create modern button
                btn = tk.Button(btn_frame,
                            image=photo_img,
                            text=btn_info["text"],
                            compound=tk.TOP,
                            bg=COLORS["card"],
                            fg=COLORS["text"],
                            activebackground=COLORS["highlight"],
                            font=("Segoe UI", 10),
                            borderwidth=0,
                            command=btn_info["command"])
                btn.image = photo_img
                btn.pack()

                # Hover effect
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS["primary"]))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLORS["card"]))
                
        except Exception as e:
            print(f"Button error: {e}")
    def trash(self,user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # make the top bar with change language button
        self.create_topbar

    def create_left_visualization(self, parent):
        try:
            data = {
                'customers': self.get_customer_count(),
                'suppliers': self.get_supplier_count(),
                'sales': self.get_sales_count(),
                'purchases': self.get_purchase_count()
            }

            plt.style.use('dark_background')  # Modern dark theme
            fig = plt.Figure(figsize=(6, 8), dpi=70, facecolor=COLORS["card"])
            fig.subplots_adjust(hspace=0.4)

            # Bar Chart
        ax1 = fig.add_subplot(211)
        bars = ax1.bar(['Customers', 'Suppliers'], 
                      [data['customers'], data['suppliers']], 
                      color=[COLORS["chart1"], COLORS["chart2"]])
            ax1.set_facecolor(COLORS["card"])
            ax1.tick_params(colors=COLORS["text"], labelsize=10)
            
            # Add value labels
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height}',
                        ha='center', va='bottom',
                        color=COLORS["text"], fontsize=10)

            # Summary Table
            ax2 = fig.add_subplot(212)
            ax2.axis('off')
            table_data = [
                ['Metric', 'Value'],
                ['Customers', data['customers']],
                ['Suppliers', data['suppliers']],
                ['Sales', data['sales']],
                ['Purchases', data['purchases']]
            ]
            
            table = ax2.table(cellText=table_data,
                            loc='center',
                            cellLoc='center',
                            colWidths=[0.4, 0.4])
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.set_zorder(100)

            # Style table
            for (row, col), cell in table.get_celld().items():
                cell.set_facecolor(COLORS["card"])
                cell.set_text_props(color=COLORS["text"])
                if row == 0:
                    cell.set_facecolor(COLORS["primary"])
                    cell.set_text_props(weight='bold')

            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas.draw()
            canvas.get_tk_widget().config(bg=COLORS["card"])
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            print(f"Visualization error: {e}")

    def create_right_visualization(self, parent):
        try:
            data = {
                'sales': self.get_sales_count(),
                'purchases': self.get_purchase_count(),
                'top_client': self.get_top_client()
            }

            plt.style.use('dark_background')  # Modern dark theme
            fig = plt.Figure(figsize=(6, 8), dpi=70, facecolor=COLORS["card"])
            fig.subplots_adjust(hspace=0.4)

            # Pie Chart
            ax1 = fig.add_subplot(211)
            wedges, texts, autotexts = ax1.pie(
                [data['sales'], data['purchases']],
                labels=['Sales', 'Purchases'],
                autopct='%1.1f%%',
                colors=[COLORS["secondary"], COLORS["accent"]],
                startangle=90,
                textprops={'color': COLORS["text"], 'fontsize': 10}
            )
            ax1.set_title("Sales vs Purchases Ratio", 
                        color=COLORS["text"], 
                        fontsize=12)

            # Top Client
            ax2 = fig.add_subplot(212)
            if data['top_client']:
                bars = ax2.bar(data['top_client'][0], data['top_client'][1],
                            color=COLORS["primary"])
                ax2.set_title("Top Performing Client", 
                            color=COLORS["text"], 
                            fontsize=12)
                ax2.set_facecolor(COLORS["card"])
                ax2.tick_params(colors=COLORS["text"], labelsize=10)
                
                # Add value label
                for bar in bars:
                    height = bar.get_height()
                    ax2.text(bar.get_x() + bar.get_width()/2., height,
                            f'${height:,.2f}',
                            ha='center', va='bottom',
                            color=COLORS["text"], fontsize=10)

            canvas = FigureCanvasTkAgg(fig, master=parent)
            canvas.draw()
            canvas.get_tk_widget().config(bg=COLORS["card"])
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            print(f"Visualization error: {e}")

    # ... (Keep existing database methods and placeholder methods) ...
    # Add database query methods (implement with your actual DB connection)
    def get_customer_count(self):
        # Example: return self.db.execute("SELECT COUNT(*) FROM Customers").fetchone()[0]
        return 42

    def get_supplier_count(self):
        return 15

    def get_sales_count(self):
        return 175

    def get_purchase_count(self):
        return 89

    def get_top_client(self):
        return ("Maggie Corp", 175000) 
    

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernBusinessApp(root)
    root.mainloop()