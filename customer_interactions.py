import config
from common_interactions import CommonInteractions
import tkinter as tk
from annotated_types import doc
import matplotlib.pyplot as plt

from tkinter import filedialog, ttk, messagebox
from datetime import datetime,time , time, timedelta, date
from tkcalendar import DateEntry  # Import DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class CustomerInteractions:
    def __init__(self, root, app):
        self.root = root
        self.app = app  # save reference to SalesSystemApp
        self.t = self.app.AuxiliaryClass.t
        self.CommonInteractions = CommonInteractions(self.root, self.app)

    def customer_interactions(self, user_role):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.app.topbar.topbar(show_back_button=True,Back_to_Database_Window=False)
        
        self.customer_collection         = self.app.AuxiliaryClass.get_collection_by_name("Customers")
        self.customer_payment_collection = self.app.AuxiliaryClass.get_collection_by_name("Customer_Payments")
        self.sales_collection            = self.app.AuxiliaryClass.get_collection_by_name("Sales")

        customer_codes = []
        customer_names = []

        for customer in self.customer_collection.find({}, {"Name": 1, "Code": 1, "_id": 0}):
            customer_codes.append(customer.get("Code"))
            customer_names.append(customer.get("Name"))
        
        main_frame = tk.Frame(self.root ,padx=20, pady=50)
        main_frame.pack(fill="both", expand=True)
        
        left_frame = tk.Frame(main_frame, width=330)
        left_frame.pack(side="left", fill="y")
        left_frame.pack_propagate(False)  # Prevent auto-resizing

        # Left half
        tk.Label(left_frame, text=self.t("Cash"), font=("Arial", 12)).pack(pady=10, anchor="w", padx=10)
        self.app.cash_entry = tk.Entry(left_frame, font=("Arial", 12))
        self.app.cash_entry.pack(pady=5, padx=10, fill="x")

        tk.Label(left_frame, text=self.t("Payment Method"), font=("Arial", 12)).pack(pady=10, anchor="w", padx=10)
        selected_method = tk.StringVar()
        self.app.payment_entry = ttk.Combobox(left_frame, textvariable=selected_method, values=['Cash', 'E_Wallet', 'Bank_account', 'Instapay'], state="readonly", width=18)
        self.app.payment_entry.pack(pady=5, padx=10, fill="x")
        self.app.payment_entry.set(self.t("Cash"))  

        add_btn = tk.Button(left_frame, text=self.t("Add Entry"), width=35, 
                            command=lambda: self.add_customer_payment(tree))
        add_btn.pack(pady=20 , padx=10)

        #Right part (table)
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="left", fill="both", expand=True)

        # ==== Drop-down Section ====
        tk.Label(right_frame, text=self.t("Customer Code")).grid(padx=(10,20), row=0, column=4)
        self.app.customer_code_cb = ttk.Combobox(right_frame, values=customer_codes)
        self.app.customer_code_cb.grid(padx=(10,20), row=1, column=4)

        tk.Label(right_frame, text=self.t("Customer Name")).grid(padx=(10,20), row=0, column=5)
        self.app.customer_name_cb = ttk.Combobox(right_frame, values=customer_names)
        self.app.customer_name_cb.grid(padx=(10,20), row=1, column=5)

        self.app.customer_code_cb.bind("<<ComboboxSelected>>", lambda event: self.CommonInteractions.on_code_selected(
                                        event, self.app.customer_code_cb, self.app.customer_name_cb, 
                                        self.customer_collection, self.sales_collection, self.customer_payment_collection, 
                                        "Customer_info.code", tree))
        self.app.customer_name_cb.bind("<<ComboboxSelected>>", lambda event: self.CommonInteractions.on_name_selected(
                                        event, self.app.customer_code_cb, self.app.customer_name_cb, 
                                        self.customer_collection, self.sales_collection, self.customer_payment_collection, 
                                        "Customer_info.code", tree))
        
        tk.Label(right_frame, text=self.t("Start Date")).grid(padx=(10,20), row=0, column=7)
        self.app.start_date_entry = DateEntry(right_frame, font=("Arial", 12), date_pattern='dd-MM-yyyy', width=14)
        self.app.start_date_entry.grid(padx=(10,20), row=1, column=7)
        self.app.start_date_entry.set_date(date(2022, 1, 1))

        tk.Label(right_frame, text=self.t("End Date")).grid(padx=(10,20), row=0, column=8)
        self.app.end_date_entry = DateEntry(right_frame, font=("Arial", 12), date_pattern='dd-MM-yyyy', width=14)
        self.app.end_date_entry.grid(padx=(10,20), row=1, column=8)
        # self.end_date_entry.set_date(date(2025, 7, 7))
        self.app.end_date_entry.set_date(date.today())
        
        search_btn = tk.Button(
            right_frame,
            text=self.t("Search"),
            font=("Arial", 11),
            width=12,
            command=lambda: self.CommonInteractions.on_code_selected(
                None,
                self.app.customer_code_cb,
                self.app.customer_name_cb,
                self.customer_collection,
                self.sales_collection,
                self.customer_payment_collection,
                "Customer_info.code",
                tree
            )
        )
        search_btn.grid(row=1, column=10, padx=(5, 0), pady=5)

        # ==== Table Section ====
        columns = ("date", "invoice_no", "debit", "credit", "Payment_method")
        tree_container = ttk.Frame(right_frame)
        tree_container.grid(row=3, column=3, columnspan=7, padx=10, pady=10, sticky="nsew")

        # Scrollbar (attached to the right side of the tree)
        scrollbar = ttk.Scrollbar(tree_container, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Treeview
        tree = ttk.Treeview(tree_container, columns=self.t(columns), show="headings", height=8, yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)

        # Configure scrollbar to control tree
        scrollbar.config(command=tree.yview)
        
        for col in columns:
            tree.heading(col, text=self.t(col))
            # tree.heading(col, text=col.capitalize())
            tree.column(col, width=150)
            tree.column(col, anchor="center")  # This centers the content

        # ==== Footer Totals ====
        tk.Label(right_frame, text=self.t("Total Debit")).grid(row=13, column=3, sticky="e")
        self.app.total_debit_entry = tk.Entry(right_frame)
        self.app.total_debit_entry.grid(row=13, column=4, sticky="w")

        tk.Label(right_frame, text=self.t("Total Credit")).grid(row=13, column=5, sticky="e")
        self.app.total_credit_entry = tk.Entry(right_frame)
        self.app.total_credit_entry.grid(row=13, column=6, sticky="w")

        tk.Label(right_frame, text=self.t("Balance")).grid(row=13, column=7, sticky="e")
        self.app.balance_entry = tk.Entry(right_frame)
        self.app.balance_entry.grid(row=13, column=8, sticky="w")

        if self.app.language == "Arabic":
            headers = ["التاريخ", "الوصف", 'المدين', 'الدائن',  "طريقة الدفع"]
        else:
            headers = ["date", "description", 'debit', 'credit',  "payment_method"]
        # 1. Get the selected customer name from the Combobox
    
        # 2. Clean the name for use in filenames (remove special characters)
        def clean_filename(text):
            # Replace spaces and special characters
            return (text.replace(" ", "_")
                        .replace("/", "-")
                        .replace("\\", "-")
                        .replace(":", "-")
                        .replace("*", "")
                        .replace("?", "")
                        .replace('"', "")
                        .replace("<", "")
                        .replace(">", "")
                        .replace("|", "")
                        .strip())

        report_folder = "حسابات مفصلة للعملاء"
        # Initial update with empty query
        self.CommonInteractions.update_totals(self.sales_collection, self.customer_payment_collection, tree=tree)
        tk.Button(right_frame,
                            text=self.t("Export to Excel"), 
                            command=lambda: self.app.export_to_excel(self.app.raw_tree_data,headers=headers,filename= f"كشف_حساب_للعميل_{clean_filename(self.app.report_customer_name)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                                                report_folder=report_folder,title=report_folder,
                                                                startdate=self.app.start_date_entry.get() if hasattr(self.app.start_date_entry, 'get') else str(self.app.start_date_entry),
                                                                enddate=self.app.end_date_entry.get() if hasattr(self.app.end_date_entry, 'get') else str(self.app.end_date_entry),
                                                                footerline_out_of_table=[
                                                                    f"إجمالي دائن: {str(self.app.total_credit_entry.get())}",
                                                                    f"إجمالي مدين: {str(self.app.total_debit_entry.get())}",
                                                                    f"الرصيد: {str(self.app.balance_entry.get())}"
                                                                ], source="Customer Interaction"
                                                                 ),bg="#21F35D", fg='white').grid(row=13, column=9, sticky="w")
        # Create a variable to hold the selected page size
        self.page_size_var = tk.StringVar(value="A4")  # Default value

        # Create the OptionMenu (drop-down list)
        page_sizes = ["A1", "A2", "A3", "A4", "A5", "A6", "A7"]
        page_size_menu = tk.OptionMenu(right_frame, self.page_size_var, *page_sizes)
        page_size_menu.grid(row=13, column=11, sticky="w", padx=5)  # Placed before the button
        tk.Button(right_frame, 
                            text=self.t("Export to PDF and Print"),
                            command=lambda: self.app.export_to_pdf(self.app.raw_tree_data,headers=headers,filename= f"كشف_حساب_للعميل_{clean_filename(self.app.report_customer_name)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                                                report_folder=report_folder,title=report_folder,
                                                                startdate=self.app.start_date_entry.get() if hasattr(self.app.start_date_entry, 'get') else str(self.app.start_date_entry),
                                                                enddate=self.app.end_date_entry.get() if hasattr(self.app.end_date_entry, 'get') else str(self.app.end_date_entry),
                                                                footerline_out_of_table=[
                                                                    f"إجمالي دائن: {str(self.app.total_credit_entry.get())}",
                                                                    f"إجمالي مدين: {str(self.app.total_debit_entry.get())}",
                                                                    f"الرصيد: {str(self.app.balance_entry.get())}"
                                                                ], source="Customer Interaction",page_size=config.PAGE_SIZES[self.page_size_var.get()]
                                                                ),bg="#2144F3", fg='white').grid(row=13, column=10, sticky="w", padx=10)
        

    def add_customer_payment(self, tree):
        credit = self.app.cash_entry.get().strip()
        payment_method = self.app.payment_entry.get().strip()
        customer_code = self.app.customer_code_cb.get().strip()
        customer_name = self.app.customer_name_cb.get().strip()
        customer_payment_collection = self.app.AuxiliaryClass.get_collection_by_name("Customer_Payments")
        sales_collection = self.app.AuxiliaryClass.get_collection_by_name("Sales")
        
        if not credit or not payment_method or not customer_code or not customer_name:
            messagebox.showerror(self.t("Error"), self.t("All fields must be filled!"))
            return

        try:
            credit_val = float(credit)
        except ValueError:
            messagebox.showerror(self.t("Error"), self.t("Cash must be a valid number."))
            return

        operation_number = config.get_next_operation_number(customer_payment_collection)
        # current_time = datetime.now().strftime("%d/%m/%Y %H:%M")
        current_time = datetime.now()

        doc = {
            "Operation_Number": operation_number,
            "Time": current_time,
            "Credit": credit_val,
            "Debit": 0.0,
            "Payment_method": payment_method,
            "Customer_info": {
                "code": customer_code,
                "name": customer_name
            }
        }
        
        formatted = current_time.strftime("%Y-%m-%d %H:%M")
        
        customer_payment_collection.insert_one(doc)
        tree.insert("", tk.END, values=(formatted, operation_number, 0.0, credit_val,payment_method))

        self.customer_collection.update_one(
            {"Code": customer_code},
            {
                "$inc": {
                    "Credit": credit_val,
                    "Balance": -credit_val
                }
            }
        )

        self.CommonInteractions.on_code_selected(
            event=None,
            code_cb=self.app.customer_code_cb,
            name_cb=self.app.customer_name_cb,
            collection=self.app.AuxiliaryClass.get_collection_by_name("Customers"),
            invoices_collection=sales_collection,
            payment_collection=customer_payment_collection,
            field_path="Customer_info.code",
            tree=tree
        )
        config.report_log(self.app.logs_collection, self.app.user_name, customer_payment_collection, f"{self.t("Added new record to")}", doc, self.t)
        messagebox.showinfo(self.t("Success"), f"{self.t("Entry")} {operation_number} {self.t("added.")}")