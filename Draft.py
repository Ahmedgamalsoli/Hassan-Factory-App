# import tkinter as tk
# from tkinter import ttk, font
# from PIL import Image, ImageTk
# import matplotlib
# matplotlib.use('TkAgg')
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import os

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# # Modern color palette
# COLORS = {
#     "background": "#F5F7FA",       # Light grey background
#     "primary": "#2A3F5F",           # Dark blue for headers
#     "secondary": "#00C0A3",         # Teal for primary actions
#     "accent": "#FF6F61",            # Coral for highlights
#     "text": "#2A3F5F",              # Dark blue text
#     "card": "#FFFFFF",              # White card backgrounds
#     "chart1": "#00C0A3",            # Teal for Sales
#     "chart2": "#FF6F61",            # Coral for Purchases
#     "highlight": "#6C5CE7",         # Purple for interactive elements
#     "table_header": "#2A3F5F",      # Dark blue table headers
#     "positive": "#00C0A3",          # Teal for positive metrics
#     "neutral": "#A0AEC0"            # Grey for secondary elements
# }

# class ModernBusinessApp:
#     def __init__(self, root, user_role="admin"):
#         self.root = root
#         self.user_role = user_role
#         self.root.state("zoomed")
#         self.root.configure(bg=COLORS["background"])
#         self.current_window = None
#         self.custom_font = ("Segoe UI", 12)
#         self.title_font = ("Segoe UI", 16, "bold")
#         self.setup_styles()
#         self.main_menu()

#     def setup_styles(self):
#         # Configure ttk styles
#         style = ttk.Style()
#         style.theme_create("modern", parent="alt", settings={
#             "TFrame": {"configure": {"background": COLORS["background"]}},
#             "TLabel": {
#                 "configure": {
#                     "background": COLORS["background"],
#                     "foreground": COLORS["text"],
#                     "font": self.custom_font
#                 }
#             },
#             "TButton": {
#                 "configure": {
#                     "anchor": "center",
#                     "relief": "flat",
#                     "background": COLORS["primary"],
#                     "foreground": COLORS["text"],
#                     "font": self.custom_font,
#                     "padding": 10
#                 },
#                 "map": {
#                     "background": [
#                         ("active", COLORS["highlight"]),
#                         ("disabled", "#95a5a6")
#                     ]
#                 }
#             }
#         })
#         style.theme_use("modern")

#     def main_menu(self):
#         self.clear_window()
#         self.create_topbar()
#         self.create_main_layout()

#     def clear_window(self):
#         for widget in self.root.winfo_children():
#             widget.destroy()

#     def create_topbar(self):
#         topbar = tk.Frame(self.root, bg=COLORS["card"], height=60)
#         topbar.pack(fill=tk.X, pady=(0, 20))
        
#         title_label = tk.Label(topbar, 
#                             text="Business Management System",
#                             font=self.title_font,
#                             bg=COLORS["card"],
#                             fg=COLORS["text"])
#         title_label.pack(side=tk.LEFT, padx=30)

#         user_label = tk.Label(topbar, 
#                             text=f"User: {self.user_role.upper()}",
#                             font=("Segoe UI", 12),
#                             bg=COLORS["card"],
#                             fg=COLORS["text"])
#         user_label.pack(side=tk.RIGHT, padx=30)

#     def create_main_layout(self):
#         main_container = tk.Frame(self.root, bg=COLORS["background"])
#         main_container.pack(fill=tk.BOTH, expand=True)

#         # Visualization frames
#         left_viz_frame = self.create_card_frame(main_container)
#         left_viz_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
        
#         right_viz_frame = self.create_card_frame(main_container)
#         right_viz_frame.grid(row=0, column=2, sticky="nsew", padx=20, pady=10)

#         # Button frame
#         button_frame = self.create_card_frame(main_container, padding=20)
#         button_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)

#         # Grid configuration
#         main_container.grid_columnconfigure(0, weight=1)
#         main_container.grid_columnconfigure(1, weight=2)
#         main_container.grid_columnconfigure(2, weight=1)
#         main_container.grid_rowconfigure(0, weight=1)

#         # Create components
#         self.create_left_visualization(left_viz_frame)
#         self.create_right_visualization(right_viz_frame)
#         self.create_main_buttons(button_frame)

#     def create_card_frame(self, parent, padding=0):
#         frame = tk.Frame(parent, bg=COLORS["card"], bd=0,
#                         highlightbackground=COLORS["primary"],
#                         highlightthickness=2)
#         if padding:
#             frame.grid_propagate(False)
#             frame.config(width=400, height=600)
#         return frame

#     def create_main_buttons(self, parent):
#         buttons = [
#             {"text": "New Sales Invoice", "image": "Sales.png",
#             "command": lambda: self.trash(self.user_role)},
#             {"text": "New Purchase Invoice", "image": "Purchase.png", 
#             "command": lambda: self.trash(self.user_role)},
#             {"text": "Production Order", "image": "Production Order.png", 
#             "command": lambda: self.trash(self.user_role)},
#             {"text": "Employee Interactions", "image": "Employees.png", 
#             "command": lambda: self.trash(self.user_role)},
#             {"text": "Treasury", "image": "Treasury.png", 
#             "command": lambda: self.trash(self.user_role)},
#             {"text": "Database", "image": "Database.png", 
#             "command": lambda: self.trash(self.user_role)},
#             # {"text": "Analytics", "image": "Analytics.png", 
#             # "command": lambda: self.trash(self.user_role)},
#         ]

#         columns_per_row = 3
#         button_size = 100

#         try:
#             for index, btn_info in enumerate(buttons):
#                 row = index // columns_per_row
#                 column = index % columns_per_row

#                 btn_frame = tk.Frame(parent, bg=COLORS["card"])
#                 btn_frame.grid(row=row, column=column, padx=15, pady=15)

#                 # Load and process image
#                 img_path = os.path.join(BASE_DIR, "Static", "images", btn_info["image"])
#                 img = Image.open(img_path).resize((button_size, button_size), Image.LANCZOS)
#                 photo_img = ImageTk.PhotoImage(img)

#                 # Create modern button
#                 btn = tk.Button(btn_frame,
#                             image=photo_img,
#                             text=btn_info["text"],
#                             compound=tk.TOP,
#                             bg=COLORS["card"],
#                             fg=COLORS["text"],
#                             activebackground=COLORS["highlight"],
#                             font=("Segoe UI", 10),
#                             borderwidth=0,
#                             command=btn_info["command"])
#                 btn.image = photo_img
#                 btn.pack()

#                 # Hover effect
#                 btn.bind("<Enter>", lambda e, b=btn: b.config(bg=COLORS["primary"]))
#                 btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLORS["card"]))
                
#         except Exception as e:
#             print(f"Button error: {e}")
#     def trash(self,user_role):
#         # Clear current window
#         for widget in self.root.winfo_children():
#             widget.destroy()

#         # make the top bar with change language button
#         self.create_topbar

#     def create_left_visualization(self, parent):
#         try:
#             data = {
#                 'customers': self.get_customer_count(),
#                 'suppliers': self.get_supplier_count(),
#                 'sales': self.get_sales_count(),
#                 'purchases': self.get_purchase_count()
#             }

#             plt.style.use('dark_background')  # Modern dark theme
#             fig = plt.Figure(figsize=(6, 8), dpi=70, facecolor=COLORS["card"])
#             fig.subplots_adjust(hspace=0.4)

#             # Bar Chart
#             ax1 = fig.add_subplot(211)
#             bars = ax1.bar(['Customers', 'Suppliers'], 
#                         [data['customers'], data['suppliers']], 
#                         color=[COLORS["chart1"], COLORS["chart2"]])
#             ax1.set_facecolor(COLORS["card"])
#             ax1.tick_params(colors=COLORS["text"], labelsize=10)
            
#             # Add value labels
#             for bar in bars:
#                 height = bar.get_height()
#                 ax1.text(bar.get_x() + bar.get_width()/2., height,
#                         f'{height}',
#                         ha='center', va='bottom',
#                         color=COLORS["text"], fontsize=10)

#             # Summary Table
#             ax2 = fig.add_subplot(212)
#             ax2.axis('off')
#             table_data = [
#                 ['Metric', 'Value'],
#                 ['Customers', data['customers']],
#                 ['Suppliers', data['suppliers']],
#                 ['Sales', data['sales']],
#                 ['Purchases', data['purchases']]
#             ]
            
#             table = ax2.table(cellText=table_data,
#                             loc='center',
#                             cellLoc='center',
#                             colWidths=[0.4, 0.4])
#             table.auto_set_font_size(False)
#             table.set_fontsize(10)
#             table.set_zorder(100)

#             # Style table
#             for (row, col), cell in table.get_celld().items():
#                 cell.set_facecolor(COLORS["card"])
#                 cell.set_text_props(color=COLORS["text"])
#                 if row == 0:
#                     cell.set_facecolor(COLORS["primary"])
#                     cell.set_text_props(weight='bold')

#             canvas = FigureCanvasTkAgg(fig, master=parent)
#             canvas.draw()
#             canvas.get_tk_widget().config(bg=COLORS["card"])
#             canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

#         except Exception as e:
#             print(f"Visualization error: {e}")

#     def create_right_visualization(self, parent):
#         try:
#             data = {
#                 'sales': self.get_sales_count(),
#                 'purchases': self.get_purchase_count(),
#                 'top_client': self.get_top_client()
#             }

#             plt.style.use('dark_background')  # Modern dark theme
#             fig = plt.Figure(figsize=(6, 8), dpi=70, facecolor=COLORS["card"])
#             fig.subplots_adjust(hspace=0.4)

#             # Pie Chart
#             ax1 = fig.add_subplot(211)
#             wedges, texts, autotexts = ax1.pie(
#                 [data['sales'], data['purchases']],
#                 labels=['Sales', 'Purchases'],
#                 autopct='%1.1f%%',
#                 colors=[COLORS["secondary"], COLORS["accent"]],
#                 startangle=90,
#                 textprops={'color': COLORS["text"], 'fontsize': 10}
#             )
#             ax1.set_title("Sales vs Purchases Ratio", 
#                         color=COLORS["text"], 
#                         fontsize=12)

#             # Top Client
#             ax2 = fig.add_subplot(212)
#             if data['top_client']:
#                 bars = ax2.bar(data['top_client'][0], data['top_client'][1],
#                             color=COLORS["primary"])
#                 ax2.set_title("Top Performing Client", 
#                             color=COLORS["text"], 
#                             fontsize=12)
#                 ax2.set_facecolor(COLORS["card"])
#                 ax2.tick_params(colors=COLORS["text"], labelsize=10)
                
#                 # Add value label
#                 for bar in bars:
#                     height = bar.get_height()
#                     ax2.text(bar.get_x() + bar.get_width()/2., height,
#                             f'${height:,.2f}',
#                             ha='center', va='bottom',
#                             color=COLORS["text"], fontsize=10)

#             canvas = FigureCanvasTkAgg(fig, master=parent)
#             canvas.draw()
#             canvas.get_tk_widget().config(bg=COLORS["card"])
#             canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

#         except Exception as e:
#             print(f"Visualization error: {e}")

#     # ... (Keep existing database methods and placeholder methods) ...
#     # Add database query methods (implement with your actual DB connection)
#     def get_customer_count(self):
#         # Example: return self.db.execute("SELECT COUNT(*) FROM Customers").fetchone()[0]
#         return 42

#     def get_supplier_count(self):
#         return 15

#     def get_sales_count(self):
#         return 175

#     def get_purchase_count(self):
#         return 89

#     def get_top_client(self):
#         return ("Maggie Corp", 175000) 
    

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = ModernBusinessApp(root)
#     root.mainloop()


# #     # Add at the top with other imports
# # import matplotlib.pyplot as plt
# # from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# # # Modern Color Scheme
# # COLORS = {
# #     "background": "#F5F7FA",       # Light grey background
# #     "primary": "#2A3F5F",           # Dark blue for headers
# #     "secondary": "#00C0A3",         # Teal for primary actions
# #     "accent": "#FF6F61",            # Coral for highlights
# #     "text": "#2A3F5F",              # Dark blue text
# #     "card": "#FFFFFF",              # White card backgrounds
# #     "chart1": "#00C0A3",            # Teal for Sales
# #     "chart2": "#FF6F61",            # Coral for Purchases
# #     "highlight": "#6C5CE7",         # Purple for interactive elements
# #     "table_header": "#2A3F5F",      # Dark blue table headers
# #     "positive": "#00C0A3",          # Teal for positive metrics
# #     "neutral": "#A0AEC0"            # Grey for secondary elements
# # }

# # class SalesSystemApp:
# #     def __init__(self, root):
# #         # ... existing init code ...
        
# #         # Update style configuration
# #         self.root.configure(bg=COLORS["background"])
# #         style = ttk.Style()
# #         style.theme_use("clam")
        
# #         # Configure modern styles
# #         style.configure("Treeview", 
# #                        background=COLORS["card"],
# #                        foreground=COLORS["text"],
# #                        rowheight=30,
# #                        fieldbackground=COLORS["card"],
# #                        font=("Arial", 10),
# #                        bordercolor=COLORS["neutral"]])
# #         style.map('Treeview', 
# #                  background=[('selected', COLORS["highlight"])],
# #                  foreground=[('selected', 'white')])
        
# #         # Configure button styles
# #         style.configure("TButton",
# #                        background=COLORS["secondary"],
# #                        foreground=COLORS["text"],
# #                        font=("Arial", 12, "bold"),
# #                        padding=10,
# #                        borderwidth=0)
# #         style.map("TButton",
# #                  background=[('active', COLORS["highlight"])])

# #     def main_menu(self):
# #         # Clear current window
# #         for widget in self.root.winfo_children():
# #             widget.destroy()

# #         # Create modern top bar
# #         topbar = tk.Frame(self.root, bg=COLORS["primary"], height=60)
# #         topbar.pack(fill=tk.X, pady=(0, 20))
        
# #         # Title with modern styling
# #         title_label = tk.Label(topbar, 
# #                              text="مصنع حسن سليم للمنتجات البلاستيكية",
# #                              font=("Arial", 18, "bold"),
# #                              bg=COLORS["primary"],
# #                              fg="white")
# #         title_label.pack(side=tk.LEFT, padx=30)

# #         # User info with modern styling
# #         user_label = tk.Label(topbar, 
# #                             text=f"User: {self.user_role.upper()}",
# #                             font=("Arial", 12),
# #                             bg=COLORS["primary"],
# #                             fg="white")
# #         user_label.pack(side=tk.RIGHT, padx=30)

# #         # Main container with modern layout
# #         main_container = tk.Frame(self.root, bg=COLORS["background"])
# #         main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# #         # Visualization frames
# #         viz_frame = tk.Frame(main_container, bg=COLORS["card"], 
# #                             relief="flat", borderwidth=2)
# #         viz_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# #         # Button frame with modern styling
# #         button_frame = tk.Frame(main_container, bg=COLORS["card"],
# #                                relief="flat", borderwidth=2)
# #         button_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

# #         # Configure grid weights
# #         main_container.grid_columnconfigure(0, weight=2)
# #         main_container.grid_columnconfigure(1, weight=3)
# #         main_container.grid_rowconfigure(0, weight=1)

# #         # Create visualizations
# #         self.create_dashboard_visualizations(viz_frame)

# #         # Modern buttons setup
# #         buttons = [
# #             {"text": self.t("New Sales Invoice"), "image": "Sales.png",
# #              "color": COLORS["secondary"], "command": lambda: self.new_sales_invoice(self.user_role)},
# #             {"text": self.t("New Purchase Invoice"), "image": "Purchase.png",
# #              "color": COLORS["accent"], "command": lambda: self.new_Purchase_invoice(self.user_role)},
# #             # ... rest of buttons ...
# #         ]

# #         # Create modern buttons grid
# #         for index, btn_info in enumerate(buttons):
# #             btn_frame = tk.Frame(button_frame, bg=COLORS["card"])
# #             btn_frame.grid(row=index, column=0, sticky="ew", pady=5)
            
# #             img = Image.open(os.path.join(BASE_DIR, "Static", "images", btn_info["image"]))
# #             img = img.resize((40, 40), Image.LANCZOS)
# #             photo_img = ImageTk.PhotoImage(img)
            
# #             btn = tk.Button(btn_frame,
# #                           image=photo_img,
# #                           text=btn_info["text"],
# #                           compound=tk.LEFT,
# #                           bg=COLORS["card"],
# #                           fg=COLORS["text"],
# #                           activebackground=COLORS["highlight"],
# #                           font=("Arial", 12),
# #                           borderwidth=0,
# #                           command=btn_info["command"])
# #             btn.image = photo_img
# #             btn.pack(fill=tk.X, expand=True)

# #     def create_dashboard_visualizations(self, parent):
# #         try:
# #             # Create figure with modern styling
# #             plt.style.use('seaborn-whitegrid')
# #             fig = plt.Figure(figsize=(10, 6), dpi=100, facecolor=COLORS["card"])
            
# #             # Add charts
# #             ax1 = fig.add_subplot(121)
# #             ax2 = fig.add_subplot(122)
            
# #             # Sales/Purchases pie chart
# #             sales_data = self.get_sales_count()
# #             purchase_data = self.get_purchase_count()
# #             ax1.pie([sales_data, purchase_data],
# #                     labels=[self.t("Sales"), self.t("Purchases")],
# #                     colors=[COLORS["chart1"], COLORS["chart2"]],
# #                     autopct='%1.1f%%',
# #                     textprops={'color': COLORS["text"], 'fontsize': 10})
# #             ax1.set_title(self.t("Sales vs Purchases Ratio"), color=COLORS["text"])
            
# #             # Customer/Supplier bar chart
# #             customer_data = self.get_customer_count()
# #             supplier_data = self.get_supplier_count()
# #             ax2.bar([self.t("Customers"), self.t("Suppliers")], 
# #                    [customer_data, supplier_data],
# #                    color=[COLORS["chart1"], COLORS["chart2"]])
# #             ax2.set_title(self.t("Customer & Supplier Count"), color=COLORS["text"])
# #             ax2.tick_params(colors=COLORS["text"], labelsize=10)
            
# #             # Embed in Tkinter
# #             canvas = FigureCanvasTkAgg(fig, master=parent)
# #             canvas.draw()
# #             canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# #         except Exception as e:
# #             print(f"Visualization error: {e}")

# #     # ... rest of your existing methods ...








# #         # Database Methods
# #     def get_customer_count(self):
# #         return self.customers.count_documents({})

# #     def get_supplier_count(self):
# #         return self.suppliers.count_documents({})

# #     def get_sales_count(self):
# #         return self.sales.count_documents({})

# #     def get_purchase_count(self):
# #         return self.purchases.count_documents({})

# #     def get_top_client(self):
# #         try:
# #             pipeline = [
# #                 {"$group": {
# #                     "_id": "$Customer",  # Field name from your sales documents
# #                     "total_sales": {"$sum": "$Total_Prices"}  # Amount field
# #                 }},
# #                 {"$sort": {"total_sales": -1}},
# #                 {"$limit": 1}
# #             ]
# #             result = list(self.sales.aggregate(pipeline))
            
# #             if result:
# #                 return (str(result[0]["_id"]), float(result[0]["total_sales"]))
# #             return ("No clients", 0.0)
            
# #         except PyMongoError as e:
# #             print(f"Database error: {e}")
# #             return ("Error", 0.0)

# #     # Updated Visualization with Type Fixes
# #     def create_right_visualization(self, parent):
# #         try:
# #             data = {
# #                 'sales': self.get_sales_count(),
# #                 'purchases': self.get_purchase_count(),
# #                 'top_client': self.get_top_client()
# #             }

# #             fig = plt.Figure(figsize=(6, 8), dpi=60)
# #             fig.subplots_adjust(hspace=0.5)

# #             # Top Client Chart Fix
# #             ax2 = fig.add_subplot(212)
# #             if data['top_client'] and data['top_client'][1] > 0:
# #                 name, value = data['top_client']
                
# #                 # Explicit type conversion and width specification
# #                 ax2.bar(
# #                     x=[str(name)],
# #                     height=[float(value)],
# #                     width=0.6,  # Explicit numeric width
# #                     color='#8E44AD',
# #                     edgecolor='black'
# #                 )
                
# #                 ax2.set_title("Top Performing Client")
# #                 ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.2f}'))
                
# #             else:
# #                 ax2.text(0.5, 0.5, 'No client data available', ha='center', va='center')
# #                 ax2.axis('off')

# #             canvas = FigureCanvasTkAgg(fig, master=parent)
# #             canvas.draw()
# #             canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# #         except Exception as e:
# #             print(f"Visualization error: {e}")
    def new_Purchase_invoice(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Initialize product mappings
        self.material_map = {}
        self.name_to_code = {}
        
        # Create top bar
        self.topbar(show_back_button=True)

        # MongoDB collections
        suppliers_col = self.get_collection_by_name("Suppliers")
        purchases_col = self.get_collection_by_name("Purchases")
        materials_col = self.get_collection_by_name("Materials")

        # Main form frame
        form_frame = tk.Frame(self.root, padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Supplier Selection Frame
        Supplier_frame = tk.Frame(form_frame, bd=1, relief=tk.SOLID, padx=5, pady=5)
        Supplier_frame.grid(row=0, column=0, columnspan=2, sticky='w', pady=5)

        # Create bidirectional Supplier mappings
        self.supplier_code_map = {}  # name -> code
        self.code_name_map = {}      # code -> name
        self.supplier_balance_map = {}  # name -> balance

        # Populate Supplier data
        all_suppliers = []
        all_codes = []
        for supp in suppliers_col.find():
            name = supp.get('Name', '')
            code = str(supp.get('Code', ''))
            balance = supp.get('Balance', 0)
            
            self.supplier_code_map[name] = code
            self.code_name_map[code] = name
            self.supplier_balance_map[name] = balance
            all_suppliers.append(name)
            all_codes.append(code)

        # Supplier Name Combobox
        tk.Label(Supplier_frame, text=self.t("Supplier Name"), font=("Arial", 12, "bold")).grid(row=0, column=0, sticky='w')
        self.supplier_name_var = tk.StringVar()
        self.supplier_name_cb = ttk.Combobox(Supplier_frame, textvariable=self.supplier_name_var, values=sorted(all_suppliers))
        self.supplier_name_cb.grid(row=0, column=1, padx=5, sticky='ew')

        # Supplier Code Combobox
        tk.Label(Supplier_frame, text=self.t("Supplier Code"), font=("Arial", 12, "bold")).grid(row=0, column=2, sticky='w')
        self.supplier_code_var = tk.StringVar()
        self.supplier_code_cb = ttk.Combobox(Supplier_frame, textvariable=self.supplier_code_var, values=sorted(all_codes))
        self.supplier_code_cb.grid(row=0, column=3, padx=5, sticky='ew')

        # Balance and Payment Fields
        tk.Label(Supplier_frame, text=self.t("Previous Balance"), font=("Arial", 12, "bold")).grid(row=0, column=4, sticky='e', padx=(20, 0))
        self.previous_balance_var = tk.StringVar()
        self.previous_balance_entry = tk.Entry(Supplier_frame, textvariable=self.previous_balance_var, 
                                            width=15, state='readonly')
        self.previous_balance_entry.grid(row=0, column=5, sticky='e')

        tk.Label(Supplier_frame, text=self.t("Paid Money"), font=("Arial", 12, "bold")).grid(row=0, column=6, sticky='e', padx=(20, 0))
        self.payed_cash_var = tk.DoubleVar()
        self.payed_cash_entry = tk.Entry(Supplier_frame, textvariable=self.payed_cash_var, width=15)
        self.payed_cash_entry.grid(row=0, column=7, sticky='e')

        # Payment Method Dropdown
        tk.Label(Supplier_frame, text=self.t("Payment Method"), font=("Arial", 12, "bold")).grid(row=0, column=8, sticky='e', padx=(20, 0))
        self.payment_method_var = tk.StringVar()
        payment_methods = ['Cash', 'E_Wallet', 'Bank_account', 'Instapay']
        payment_cb = ttk.Combobox(Supplier_frame, textvariable=self.payment_method_var, 
                                values=payment_methods, state='readonly', width=12)
        payment_cb.grid(row=0, column=9, sticky='ew', padx=(5, 10))
        payment_cb.current(0)  # Set default to Cash

        # Configure column weights
        Supplier_frame.columnconfigure(1, weight=1)
        Supplier_frame.columnconfigure(3, weight=1)
        Supplier_frame.columnconfigure(5, weight=0)
        Supplier_frame.columnconfigure(7, weight=0)
        Supplier_frame.columnconfigure(9, weight=0)

        # Synchronization functions
        def sync_from_name(event=None):
            name = self.supplier_name_var.get()
            code = self.supplier_code_map.get(name, '')
            self.supplier_code_var.set(code)
            self.previous_balance_var.set(str(self.supplier_balance_map.get(name, 0)))

        def sync_from_code(event=None):
            code = self.supplier_code_var.get()
            name = self.code_name_map.get(code, '')
            self.supplier_name_var.set(name)
            self.previous_balance_var.set(str(self.supplier_balance_map.get(name, 0)))

        # Event bindings
        self.supplier_name_cb.bind('<<ComboboxSelected>>', sync_from_name)
        self.supplier_code_cb.bind('<<ComboboxSelected>>', sync_from_code)
        
        self.supplier_name_cb.bind('<KeyRelease>', lambda e: [
            self.filter_combobox(e, all_suppliers, self.supplier_name_cb),
            sync_from_name()
        ])
        
        self.supplier_code_cb.bind('<KeyRelease>', lambda e: [
            self.filter_combobox(e, all_codes, self.supplier_code_cb),
            sync_from_code()
        ])

        # Load product data
        try:
            materials = list(materials_col.find())
            all_units = set()
            material_names = []
            material_codes = []

            for m in materials:
                code = str(m.get('material_code', '')).strip()
                name = m.get('material_name', '').strip()
                units_list = m.get('Units', [])

                # Process units
                unit_names = []
                for unit in units_list:
                    if isinstance(unit, dict):
                        unit_name = str(unit.get('unit_name', '')).strip()
                    elif isinstance(unit, str):
                        unit_name = unit.strip()
                    else:
                        continue
                    
                    if unit_name:
                        unit_names.append(unit_name)
                        all_units.add(unit_name)

                # Handle price conversion
                try:
                    price_str = str(m.get('Unit_Price', '0')).strip('kgm ')
                    price = float(price_str) if price_str else 0.0
                except ValueError:
                    price = 0.0

                # Update mappings
                self.material_map[code] = {
                    'name': name,
                    'units': unit_names,
                    'price': price
                }
                self.name_to_code[name] = code
                material_names.append(name)
                material_codes.append(code)

            self.product_codes = sorted(list(set(material_codes)))
            self.product_names = sorted(list(set(material_names)))
            all_units = sorted(list(all_units))

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to load products: {str(e)}")
            return

        # Invoice Items Grid
        columns = self.get_fields_by_name("Materials_Header")
        col_width = 23

        header_row = tk.Frame(form_frame, bg='#f0f0f0')
        header_row.grid(row=2, column=0, columnspan=len(columns), sticky='nsew', pady=(20, 0))
        for col_idx, col in enumerate(columns):
            tk.Label(header_row, text=self.t(col), width=col_width, relief='ridge',
                    bg='#f0f0f0', anchor='w').grid(row=0, column=col_idx, sticky='ew')
            header_row.columnconfigure(col_idx, weight=1)

        # Scrollable Canvas
        canvas = tk.Canvas(form_frame, highlightthickness=0)
        scrollbar = tk.Scrollbar(form_frame, orient="vertical", command=canvas.yview)
        self.rows_frame = tk.Frame(canvas)
        
        self.rows_frame.bind("<Configure>", lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.rows_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.grid(row=3, column=0, columnspan=len(columns), sticky="nsew")
        scrollbar.grid(row=3, column=len(columns), sticky="ns")
        
        form_frame.grid_rowconfigure(3, weight=1)
        for i in range(len(columns)):
            form_frame.columnconfigure(i, weight=1)

        self.entries = []

        # Modified create_row function with discount fields
        def create_row(parent, row_number, bg_color):
            row_frame = tk.Frame(parent, bg=bg_color)
            row_frame.grid(row=row_number, column=0, sticky='ew')
            
            row_entries = []
            for col_idx, col in enumerate(columns):
                if col == "Material_code":
                    var = tk.StringVar()
                    cb = ttk.Combobox(row_frame, textvariable=var, values=material_codes, width=col_width-2)
                    cb.bind('<<ComboboxSelected>>', lambda e, r=row_number: self.update_material_info(r, "code"))
                    cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_combobox_change_purchase(e, r, "code"))
                    cb.grid(row=0, column=col_idx, sticky='ew')
                    row_entries.append(cb)
                elif col == "Material_name":
                    var = tk.StringVar()
                    cb = ttk.Combobox(row_frame, textvariable=var, values=material_names, width=col_width-2)
                    cb.bind('<<ComboboxSelected>>', lambda e, r=row_number: self.update_material_info(r, "name"))
                    cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_combobox_change_purchase(e, r, "name"))
                    cb.grid(row=0, column=col_idx, sticky='ew')
                    row_entries.append(cb)
                elif col == "unit":
                    var = tk.StringVar()
                    cb = ttk.Combobox(row_frame, textvariable=var, values=[], width=col_width-2)
                    cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_unit_change(e, r))
                    cb.grid(row=0, column=col_idx, sticky='ew')
                    row_entries.append(cb)
                elif col == "Discount Type":
                    var = tk.StringVar()
                    cb = ttk.Combobox(row_frame, textvariable=var, 
                                    values=["Percentage", "Value"], 
                                    state="readonly",
                                    width=col_width-2)
                    cb.current(0)  # Default to Percentage
                    cb.grid(row=0, column=col_idx, sticky='ew')
                    row_entries.append(cb)
                elif col == "Discount Value":
                    var = tk.StringVar()
                    entry = tk.Entry(row_frame, textvariable=var, width=col_width+1)
                    entry.bind('<KeyRelease>', lambda e, r=row_number: self.calculate_totals(r))
                    entry.grid(row=0, column=col_idx, sticky='ew')
                    row_entries.append(entry)
                elif col in ["Unit_Price", "Total_QTY", "Total_Price"]:
                    entry = tk.Entry(row_frame, width=col_width+1, relief='flat', state='readonly')
                    entry.grid(row=0, column=col_idx, sticky='ew')
                    row_entries.append(entry)
                else:
                    entry = tk.Entry(row_frame, width=col_width+1, relief='sunken')
                    entry.bind('<KeyRelease>', lambda e, r=row_number: self.calculate_totals(r))
                    entry.grid(row=0, column=col_idx, sticky='ew')
                    row_entries.append(entry)
                
                row_frame.columnconfigure(col_idx, weight=1)
            
            return row_entries

        def add_three_rows():
            current_row_count = len(self.entries)
            for i in range(3):
                bg_color = 'white' if (current_row_count + i) % 2 == 0 else '#f0f0f0'
                row_entries = create_row(self.rows_frame, current_row_count + i, bg_color)
                self.entries.append(row_entries)

        add_three_rows()

        # Buttons Frame
        button_frame = tk.Frame(form_frame)
        button_frame.grid(row=4, column=0, columnspan=len(columns), pady=10, sticky='ew')
        
        tk.Button(button_frame, text=self.t("➕ Add 3 More Rows"), command=add_three_rows,
                bg='#4CAF50', fg='white').grid(row=0, column=0, padx=5, sticky='w')
        tk.Button(button_frame, text=self.t("💾 Save Invoice"), 
                command=lambda: self.save_invoice_purchase(purchases_col, suppliers_col,materials_col),
                bg='#2196F3', fg='white').grid(row=0, column=1, padx=5, sticky='e')
        
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)




        ########################################################################################################################
        def employee_statistics_window(self, user_role):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.topbar(show_back_button=True, Back_to_Employee_Window=True)
        
        # Database connections
        employees_col = self.get_collection_by_name("Employees")
        # Employee mappings
        self.employee_code_map = {}
        self.employee_name_map = {}
        for emp in employees_col.find():
            code = emp.get('Id', '')
            name = emp.get('Name', '')
            self.employee_code_map[code] = {
                'name': name,
                'salary': float(emp.get('Salary', 0))
            }
            self.employee_name_map[name] = {
                'code': code,
                'salary': float(emp.get('Salary', 0))
            }

        # Main GUI components
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Employee Selection
        selection_frame = tk.Frame(main_frame)
        selection_frame.pack(fill=tk.X, pady=5)
        
        self.emp_name_var = tk.StringVar()
        self.emp_code_var = tk.StringVar()
        
        ttk.Label(selection_frame, text="Employee Name:").pack(side=tk.LEFT)
        self.name_cb = ttk.Combobox(selection_frame, textvariable=self.emp_name_var, width=25)
        self.name_cb.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(selection_frame, text="Employee Code:").pack(side=tk.LEFT, padx=10)
        self.code_cb = ttk.Combobox(selection_frame, textvariable=self.emp_code_var, width=15)
        self.code_cb.pack(side=tk.LEFT)
        print("hamada")
        # Date Selection
        date_frame = tk.Frame(main_frame)
        date_frame.pack(fill=tk.X, pady=5)
        ttk.Label(date_frame, text="Month/Year:").pack(side=tk.LEFT)
        
        self.month_var = tk.StringVar()
        self.year_var = tk.StringVar()
        
        self.month_cb = ttk.Combobox(date_frame, textvariable=self.month_var, 
                                values=["January", "February", "March", "April", "May", "June",
                                        "July", "August", "September", "October", "November", "December"])
        self.month_cb.pack(side=tk.LEFT, padx=5)
        
        self.year_cb = ttk.Combobox(date_frame, textvariable=self.year_var, 
                                values=[str(year) for year in range(2020, 2031)])
        self.year_cb.pack(side=tk.LEFT)
        
        # Working Hours
        hours_frame = tk.Frame(main_frame)
        hours_frame.pack(fill=tk.X, pady=5)
        
        self.start_time_var = tk.StringVar()
        self.end_time_var = tk.StringVar()
        
        ttk.Label(hours_frame, text="Start Time:").pack(side=tk.LEFT)
        ttk.Entry(hours_frame, textvariable=self.start_time_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Label(hours_frame, text="(e.g., 9:00 AM)").pack(side=tk.LEFT)
        
        ttk.Label(hours_frame, text="End Time:").pack(side=tk.LEFT, padx=10)
        ttk.Entry(hours_frame, textvariable=self.end_time_var, width=10).pack(side=tk.LEFT)
        ttk.Label(hours_frame, text="(e.g., 5:00 PM)").pack(side=tk.LEFT)
        
        # Attendance Table
        columns = ("Date", "From", "To", "Duration", "Delay", "More", "Withdrawls")
        self.table = ttk.Treeview(main_frame, columns=columns, show='headings', selectmode='browse')
        
        for col in columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=100, anchor='center')
        
        self.scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=self.scrollbar.set)
        
        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Calculation Fields
        totals_frame = tk.Frame(main_frame)
        totals_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(totals_frame, text="Total Withdrawls:").pack(side=tk.LEFT)
        self.total_withdrawls = ttk.Entry(totals_frame, width=10, state='readonly')
        self.total_withdrawls.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(totals_frame, text="Delay Amount:").pack(side=tk.LEFT, padx=10)
        self.delay_amount = ttk.Entry(totals_frame, width=10)
        self.delay_amount.pack(side=tk.LEFT)
        
        ttk.Label(totals_frame, text="Overtime Amount:").pack(side=tk.LEFT, padx=10)
        self.overtime_amount = ttk.Entry(totals_frame, width=10)
        self.overtime_amount.pack(side=tk.LEFT)
        
        # Payment and Salary
        payment_frame = tk.Frame(main_frame)
        payment_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(payment_frame, text="Payment Method:").pack(side=tk.LEFT)
        self.payment_method = ttk.Combobox(payment_frame, 
                                        values=["Cash", "Instapay", "E_wallet", "Bank_account"],
                                        state="readonly",
                                        width=15)
        self.payment_method.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(payment_frame, text="Salary:").pack(side=tk.LEFT, padx=10)
        self.salary = ttk.Entry(payment_frame, width=15, state='readonly')
        self.salary.pack(side=tk.LEFT)
        ttk.Label(payment_frame, text="Net Salary:").pack(side=tk.LEFT, padx=10)
        self.net_salary = ttk.Entry(payment_frame, width=15, state='readonly')
        self.net_salary.pack(side=tk.LEFT)
        
        # Save Button
        ttk.Button(main_frame, text="Take Salary", command=self.save_salary).pack(pady=10)
        
        # Initialize data
        self.name_cb['values'] = list(self.employee_name_map.keys())
        self.code_cb['values'] = list(self.employee_code_map.keys())
        
        # Bind events
        self.emp_name_var.trace_add('write', self.update_employee_info)
        self.emp_code_var.trace_add('write', self.update_employee_info)
        self.month_var.trace_add('write', self.load_attendance_data)
        self.year_var.trace_add('write', self.load_attendance_data)
        self.delay_amount.bind('<KeyRelease>', self.calculate_net_salary)
        self.overtime_amount.bind('<KeyRelease>', self.calculate_net_salary)
        self.start_time_var.trace_add('write', self.load_attendance_data)
        self.end_time_var.trace_add('write', self.load_attendance_data)