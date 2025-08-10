from datetime import datetime

import cloudinary
import db
from reportlab.lib.pagesizes import letter,A7,A6,A5,A4,A3,A2,A1

COLORS = {
    "background": "#F5F7FA",       # Light grey background
    "primary": "#3B82F6",           # Dark blue for headers
    "main_frame": "#2A3F5F",           # Dark blue for headers
    "secondary": "#00C0A3",         # Teal for primary actions
    "accent": "#FF6F61",            # Coral for highlights
    "text": "#2A3F5F",              # Dark blue text
    "card": "#FFFFFF",              # White card backgrounds
    "chart1": "#00C0A3",            # Teal for Sales
    "chart2": "#FF6F61",            # Coral for Purchases
    "highlight": "#6C5CE7",         # Purple for interactive elements
    "table_header": "#FFFFFF",      # Dark blue table headers
    "positive": "#00C0A3",          # Teal for positive metrics
    "neutral": "#A0AEC0",            # Grey for secondary elements
    "top_bar": "#dbb40f",        # Dark blue for top bar
    "top_bar_icons": "#000000",  # White for top bar icons
}

PAGE_SIZES = {
    "A1": A1,
    "A2": A2,
    "A3": A3,
    "A4": A4,
    "A5": A5,
    "A6": A6,
    "A7": A7,
}

PRIMARY_KEYS = {
    "Employees": "Id",
    "Products": "product_code",
    "Materials": "material_code",
    "Customers": "Code",
    "Suppliers": "Code",
    # "Employee_appointimets": "employee_code",
    "Sales": "Receipt_Number",
    "Purchases": "Receipt_Number",
    "Customer_Payments": "Operation_Number",
    "Supplier_Payments": "Operation_Number",
    # "Production": "timestamp",
    # "Employee_Salary": "timestamp",
    # "Employee_withdrawls": "timestamp",
    "general_exp_rev": "code",
}

LOCKED_FIELDS = {
    "root": [ "Operation_Number","Code","employee_code", "material_code", "product_code", "Receipt_Number", "Operation_Number"],
    "Customer_info": ["code"],
    "supplier_info": ["code"],
    "Items": ["material_code","product_code"]
}

ZEROED_FIELDS = {
    "Sales_grade", "Growth_grade", "Frequency_grade", "Credit", "Debit", "Balance", "Sales"
}

PRIMARY_KEY_STARTERS = {
    "Customers": "CU",
    "Suppliers": "SU",
    "Products": "PR",
    "Employees": "EMP",
    "Sales": "INV",
    "Materials": "MAT",
    "Purchases": "INV",
    "Customer_Payments": "PM",
    "Supplier_Payments": "PM",
    # "Production": "PRD",
    # "Employee_Salary": "SAL",
    # "Employee_withdrawls": "WD",
    "general_exp_rev": "GEN",
}

search_field_mapping = {
    # Customer_info
    'customer_code': ('Customer_info', 'code'),
    'customer_name': ('Customer_info', 'name'),
    'customer_phone1': ('Customer_info', 'phone1'),
    'customer_phone2': ('Customer_info', 'phone2'),
    'customer_address': ('Customer_info', 'address'),
    
    # Financials
    'Net_total': ('Financials', 'Net_total'),
    'Previous_balance': ('Financials', 'Previous_balance'),
    'Total_balance': ('Financials', 'Total_balance'),
    'Payed_cash': ('Financials', 'Payed_cash'),
    'Remaining_balance': ('Financials', 'Remaining_balance'),
    'Payment_method': ('Financials', 'Payment_method'),
    'transport_fees' : ('Financials', 'transport_fees'),

    # Supplier_info
    'supplier_code': ('supplier_info', 'code'),
    'supplier_name': ('supplier_info', 'name'),
    'supplier_phone1': ('supplier_info', 'phone1'),
    'supplier_phone2': ('supplier_info', 'phone2'),
    'supplier_address': ('supplier_info', 'address'),
    
    #Items
    'Product_code': ('Items', 'Product_code'),
    'product_name': ('Items', 'product_name'),
    'material_code': ('Items', 'material_code'),
    'material_name': ('Items', 'material_name'),
    'Unit': ('Items', 'Unit'),
    'QTY': ('Items', 'QTY'),
    'numbering': ('Items', 'numbering'),
    'Total_QTY': ('Items', 'Total_QTY'),
    'Unit_price': ('Items', 'Unit_price'),
    'Discount_Type': ('Items', 'Discount_Type'),
    'Discount_Value': ('Items', 'Discount_Value'),
    'Final_Price': ('Items', 'Final_Price'),
}

field_mapping = {
    # Customer_info
    'customer_code': ('Customer_info', 'code'),
    'customer_name': ('Customer_info', 'name'),
    'customer_phone1': ('Customer_info', 'phone1'),
    'customer_phone2': ('Customer_info', 'phone2'),
    'customer_address': ('Customer_info', 'address'),
    
    # Financials
    'Net_total': ('Financials', 'Net_total'),
    'Previous_balance': ('Financials', 'Previous_balance'),
    'Total_balance': ('Financials', 'Total_balance'),
    'Payed_cash': ('Financials', 'Payed_cash'),
    'Remaining_balance': ('Financials', 'Remaining_balance'),
    'Payment_method': ('Financials', 'Payment_method'),
    
    # Supplier_info
    'supplier_code': ('supplier_info', 'code'),
    'supplier_name': ('supplier_info', 'name'),
    'supplier_phone1': ('supplier_info', 'phone1'),
    'supplier_phone2': ('supplier_info', 'phone2'),
    'supplier_address': ('supplier_info', 'address'),
}

MANDATORTY_FIELDS = { # list all mandatory fields (fields that can't be empty)
    "Name", "Phone_number1", "Code", "Company_address", "Name", "Password", "Role", "Phone_number", "Address", "Salary",
    "product_name","category","stock_quantity","Unit_Price","product_code","Units",
    "material_name","material_code", "employee_code", "employee_name"
}

def report_log(logs_collection, user_name, current_collection, msg, entry_doc=None, translation_func=None):
    if current_collection is not None:
        primary_key_field = PRIMARY_KEYS.get(current_collection.name, "_id")
        unique_id = entry_doc.get(primary_key_field, 'N/A') if entry_doc else 'N/A'
        action_text = f"{msg} {translation_func(current_collection.name)} {translation_func("Database with Unique Id")} {unique_id}"
    else:
        action_text = msg
    name = user_name if user_name else "Unknown"
    new_log = {
        "date": datetime.now(),
        "employee_name": name,
        "action": action_text
        # "action": f"Added new record to {collection_name} Database with unique Id {unique_id if unique_id else 'N/A'}",
    }
    logs_collection.insert_one(new_log)
    trim_logs_collection(logs_collection)

def get_next_code(payment_collection):
    last_entry = payment_collection.find_one(
        {"code": {"$regex": r"^GEN-?\d+"}},
        sort=[("code", -1)]
    )
    if last_entry and "code" in last_entry:
        last_num = int(last_entry["code"].split("-")[1])
        return f"GEN-{last_num+1:05d}"
    return "GEN-00001"

def get_next_operation_number(payment_collection):
    last_entry = payment_collection.find_one(
        {"Operation_Number": {"$regex": r"^PM-?\d+"}},
        sort=[("Operation_Number", -1)]
    )
    if last_entry and "Operation_Number" in last_entry:
        last_num = int(last_entry["Operation_Number"].split("-")[1])
        return f"PM-{last_num+1:05d}"
    return "PM-00001"

def upload_pdf_to_cloudinary(file_path_param):
    # import cloudinary.uploader
    try:
        response = cloudinary.uploader.upload(file_path_param, resource_type="raw")
        return response['secure_url']
    except Exception as e:
        print(f"[Cloudinary Upload Error]: {e}")
        return None

def get_collection_by_name(collection_name):
    """Returns the appropriate MongoDB collection object based on the provided name.
    Args: collection_name (str): The name of the collection to access (e.g., "Employees", "Products").
    Returns: pymongo.collection.Collection or None: The corresponding MongoDB collection object,
                                                or None if the name is not recognized."""
    if collection_name == "Employees":
        return db.employees_collection
    if collection_name == "Employee_appointimets":
        return db.employees_appointments_collection
    if collection_name == "Employee_withdrawls":
        return db.employee_withdrawls_collection
    if collection_name == "Employee_Salary":
        return db.employee_salary_collection
    elif collection_name == "Products":
        return db.products_collection
    elif collection_name == "Sales":
        return db.sales_collection
    elif collection_name == "Customers":
        return db.customers_collection
    elif collection_name == "Suppliers":
        return db.suppliers_collection
    elif collection_name =="Materials":
        return db.materials_collection
    elif collection_name =="Purchases":
        return db.purchases_collection
    elif collection_name == "Shipping":
        return db.shipping_collection
    elif collection_name == "Orders":
        return db.orders_collection
    elif collection_name == "Expenses":
        return db.expenses_collection
    elif collection_name == "Daily_shifts":
        return db.daily_shifts_collection
    elif collection_name == "Accounts":
        return db.accounts_collection
    elif collection_name == "Transactions":
        return db.transactions_collection
    elif collection_name == "Big_deals":
        return db.big_deals_collection
    elif collection_name == "Production":
        return db.production_collection
    elif collection_name == "Customer_Payments":
        return db.customer_payments
    elif collection_name == "Supplier_Payments":
        return db.supplier_payments
    elif collection_name == "TEX_Calculations":
        return db.TEX_Calculations_collection
    elif collection_name == "general_exp_rev":
        return db.general_exp_rev_collection
    else:
        print(f"Warning: Collection name '{collection_name}' not recognized.")
        return None

def get_fields_by_name(collection_name):
    """Returns the appropriate fields array based on the provided collection name.
    Args: collection_name (str): The name of the collection (e.g., "Employees", "Products").
    Returns: list: A list of field names for the corresponding collection, or an empty list if the name is not recognized.
    """
    if collection_name == "Employees":#DONE
        return ["Name", "Password", "Id", "Role", "Join_Date", "National_id_pic", "Phone_number", "Address", "Salary"]
    
    elif collection_name == "Products":
        return ["product_name", "category", "stock_quantity", "Specs", "Unit_Price", "product_code", "Units", "prod_pic"]
    
    # elif collection_name == "Sales_Header":
    #     return [self.t("Product_code"), self.t("product_name"), self.t("unit"),self.t("numbering"),self.t("QTY"),self.t("Discount Type"),self.t("Discount Value"),self.t("Total_QTY"),self.t("Unit_Price"),self.t("Total_Price")]
    
    # elif collection_name == "Materials_Header":
    #     return [self.t("Material_code"), self.t("Material_name"), self.t("unit"),self.t("numbering"),self.t("QTY"),self.t("Discount Type"),self.t("Discount Value"),self.t("Total_QTY"),self.t("Unit_Price"),self.t("Total_Price")]
    
    elif collection_name == "Sales_Header":
        return ["Product_code", "product_name", "unit","numbering","QTY","Discount_Type","Discount Value","Total_QTY","Unit_Price","Total_Price"]
    
    elif collection_name == "Materials":
        return ["material_name", "category","stock_quantity","specs","material_code","Units","material_pic","Unit_Price"]

    elif collection_name == "Materials_Header":
        return ["Material_code", "Material_name", "unit","numbering","QTY","Discount_Type","Discount Value","Total_QTY","Unit_Price","Total_Price"]
    
    elif collection_name == "Customers":
        return ["Name", "Phone_number1", "Phone_number2", "Code", "Last_purchase_date" , "Purchase_mgr_number", "Financial_mgr_number", "Purchase_mgr_name", 
                "Financial_mgr_name", "Email", "Company_address", "Extra_address", "Maps_link", "Bank_account",
                "Instapay", "E_wallet", "Accountant_name", "Accountant_number", "Sales_grade", "Growth_grade", "Frequency_grade", "Credit",
                "Debit", "Balance", "Sales"]
    
    elif collection_name == "Suppliers":
        return ["Name", "Phone_number1", "Phone_number2", "Code", "Last_purchase_date" , "Purchase_mgr_number", "Financial_mgr_number", "Purchase_mgr_name", 
                "Financial_mgr_name", "Email", "Company_address", "Extra_address", "Maps_link", "Bank_account",
                "Instapay", "E_wallet", "Accountant_name", "Accountant_number", "Sales_grade", "Growth_grade", "Frequency_grade", "Credit",
                "Debit", "Balance", "Sales"]
    
    elif collection_name == "Shipping":
        return ["order_id", "shipping_date", "tracking_number", "shipping_address"]
    
    elif collection_name == "Orders":
        return ["order_id", "order_date", "customer_id", "total_amount", "status"]
    
    elif collection_name == "Expenses":
        return ["expense_id", "expense_type", "amount", "date", "description"]
    
    # elif collection_name == "Employee_appointimets":
    elif collection_name == "Employee_appointimets":
        return ["employee_code", "employee_name", "check_in", "check_out", "duration"]
    
    elif collection_name == "Daily_shifts":
        return ["shift_id", "employee_id", "shift_date", "start_time", "end_time"]
    
    elif collection_name == "Accounts":
        return ["account_id", "account_name", "balance", "account_type"]
    
    elif collection_name == "Transactions":
        return ["transaction_id", "account_id", "transaction_date", "amount", "transaction_type"]
    
    elif collection_name == "Big_deals":
        return ["deal_id", "deal_date", "customer_id", "product_id", "deal_value"]
    
    elif collection_name == "Sales":
        return ["Receipt_Number", "Date", "customer_code", "customer_name", "customer_phone1","customer_phone2","customer_address",
                "Product_code","product_name","Unit", "QTY","numbering","Total_QTY", "Unit_price", "Discount_Type", "Discount_Value",
                "Final_Price","Net_total", "Previous_balance", "Total_balance", "Payed_cash", "Remaining_balance", "Payment_method", "PDF_Path"]
    
    elif collection_name == "Purchases":
        return ["Receipt_Number", "Date", "supplier_code", "supplier_name", "supplier_phone1","supplier_phone2","supplier_address",
                "material_code","material_name","Unit","QTY", "numbering","Total_QTY", "Unit_price", "Discount_Type", "Discount_Value",
                "Final_Price", "Net_total", "Previous_balance", "Total_balance", "Payed_cash", "Remaining_balance", "Payment_method", "PDF_Path"]
    
    elif collection_name == "Customer_Payments":
        return ["Operation_Number", "Time", "Credit", "Debit","Payment_method", "Customer_info"]

    elif collection_name == "Supplier_Payments":
        return ["Operation_Number", "Time", "Credit", "Debit","Payment_method", "supplier_info"]

    elif collection_name == "Production":
        return ["material_code", "material_qty", "product_code","product_qty", "timestamp", "waste"]

    elif collection_name == "TEX_Calculations":
        return ["calculation_id", "product_id", "calculation_date", "value"]
    
    elif collection_name == "Employee_Salary":
        return ["employee_code", "employee_name", "month_year", "base_salary","total_withdrawls" , "delay_penalty", "overtime_bonus", "net_salary", "payment_method", "timestamp"]
    
    elif collection_name == "Employee_withdrawls":
        return ["employee_code", "employee_name", "previous_withdrawls", "amount_withdrawls", "payment_method", "timestamp"]

    elif collection_name == "general_exp_rev":
        return ["code", "type", "amount", "payment_method", "description", "date"]
    
    else:
        print(f"Warning: Collection name '{collection_name}' not recognized.")
        return []

def trim_logs_collection(logs_collection, keep_last=30):
    """Keep only the last `keep_last` logs, delete older ones."""
    total_logs = logs_collection.count_documents({})
    if total_logs > keep_last:
        logs_to_keep = list(logs_collection.find().sort("date", -1).limit(keep_last))
        if logs_to_keep:
            last_id_to_keep = logs_to_keep[-1]["_id"]
            logs_collection.delete_many({"_id": {"$lt": last_id_to_keep}})