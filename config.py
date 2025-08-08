from datetime import datetime


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

def report_log(logs_collection, user_name, current_collection, msg, entry_doc=None):
    if current_collection is not None:
        primary_key_field = PRIMARY_KEYS.get(current_collection.name, "_id")
        unique_id = entry_doc.get(primary_key_field, 'N/A') if entry_doc else 'N/A'
        action_text = f"{msg} {current_collection.name} Database with Unique Id {unique_id}"
    else:
        action_text = msg

    new_log = {
        "date": datetime.now(),
        "employee_name": user_name,
        "action": action_text
        # "action": f"Added new record to {collection_name} Database with unique Id {unique_id if unique_id else 'N/A'}",
    }
    logs_collection.insert_one(new_log)
    trim_logs_collection(logs_collection)

def trim_logs_collection(logs_collection, keep_last=30):
    """Keep only the last `keep_last` logs, delete older ones."""
    total_logs = logs_collection.count_documents({})
    if total_logs > keep_last:
        logs_to_keep = list(logs_collection.find().sort("date", -1).limit(keep_last))
        if logs_to_keep:
            last_id_to_keep = logs_to_keep[-1]["_id"]
            logs_collection.delete_many({"_id": {"$lt": last_id_to_keep}})