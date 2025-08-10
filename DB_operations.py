# ======================
# Used imports
# ======================

import tkinter as tk
import config
import os
import io
import sys
from pymongo.errors import PyMongoError
import cloudinary
import random
from tkinter import filedialog, ttk, messagebox
from PIL import Image, ImageTk # Import Pillow classes
from datetime import datetime,time , time, timedelta, date
from tkcalendar import DateEntry  # Import DateEntry
import urllib.request
import db

MANDATORTY_FIELDS = { # list all mandatory fields (fields that can't be empty)
    "Name", "Phone_number1", "Code", "Company_address", "Name", "Password", "Role", "Phone_number", "Address", "Salary",
    "product_name","category","stock_quantity","Unit_Price","product_code","Units",
    "material_name","material_code", "employee_code", "employee_name"
}

MANDATORY_DBS = {
    "Customers", "Employees", "Materials", "Products", "Suppliers" 
}


# Determine the base directory
if getattr(sys, "frozen", False):
    # Running as an executable
    BASE_DIR = sys._MEIPASS
else:
    # Running as a script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class DBOperations:
    def __init__(self, root, app):
        self.root = root
        self.app = app  # save reference to SalesSystemApp
        self.t = self.app.t

    def add_generic_entry(self, tree, current_collection, collection_name):
        fields = config.get_fields_by_name(collection_name)
        info_obj = {}
        items = []
        financials_obj = {}
        temp = None

        new_entry = {}
        if collection_name in ["general_exp_rev"]:
            code = config.get_next_code(current_collection)
            new_entry["code"] = code

        # Handle customer/supplier info
        if collection_name in ["Customer_Payments", "Supplier_Payments"]:
            prefix = "Customer" if collection_name == "Customer_Payments" else "supplier"
            
            operation_number = config.get_next_operation_number(current_collection)
            
            new_entry["Operation_Number"] = operation_number
            current_time = datetime.now()
            new_entry["Time"] = current_time

            # Get the code and name from entries
            code = self.entries.get(f"{prefix.lower()}_code", None)
            name = self.entries.get(f"{prefix.lower()}_name", None)
            
            if code:
                code_value = code.get()
            else:
                code_value = ""
                
            if name:
                name_value = name.get()
            else:
                name_value = ""

            # Create the nested info object
            info_object = {
                "code": code_value,
                "name": name_value
            }
            new_entry[f"{prefix}_info"] = info_object
        
        if collection_name in ["Sales","Purchases"]:
            prefix = "Customer" if collection_name == "Sales" else "supplier"
            
            code = self.entries.get(f"{prefix.lower()}_code")
            name = self.entries.get(f"{prefix.lower()}_name")
            phone1 = self.entries.get(f"{prefix.lower()}_phone1")
            phone2 = self.entries.get(f"{prefix.lower()}_phone2")
            address = self.entries.get(f"{prefix.lower()}_address")

            info_obj = {
                "code": code.get().strip() if code else "",
                "name": name.get().strip() if name else "",
                "phone1": phone1.get().strip() if phone1 else "",
                "phone2": phone2.get().strip() if phone2 else "",
                "address": address.get().strip() if address else "",
            }

            # --- Financials ---
            def safe_float(entry):
                try:
                    return float(entry.get().strip()) if entry and entry.get().strip() else 0.0
                except ValueError:
                    return 0.0

            def safe_str(entry):
                return entry.get().strip() if entry else ""

            net_total = safe_float(self.entries.get("Net_total"))
            prev_balance = safe_float(self.entries.get("Previous_balance"))
            total_balance = safe_float(self.entries.get("Total_balance"))
            payed_cash = safe_float(self.entries.get("Payed_cash"))
            remaining_balance = safe_float(self.entries.get("Remaining_balance"))
            payment_method = safe_str(self.entries.get("Payment_method"))

            financials_obj = {
                "Net_total": net_total,
                "Previous_balance": prev_balance,
                "Total_balance": total_balance,
                "Payed_cash": payed_cash,
                "Remaining_balance": remaining_balance,
                "Payment_method": payment_method
            }

            def split_entry(name):
                entry = self.entries.get(name)
                return entry.get().strip().split(",") if entry and entry.get().strip() else []
            
            var = None
            if prefix.lower() == "customer":
                Product_codes     = split_entry("Product_code")
                product_names     = split_entry("product_name")
                var=product_names
            else :
                material_codes     = split_entry("material_code")
                material_names     = split_entry("material_name")
                var=material_names
            
            Units             = split_entry("Unit")
            QTYs              = split_entry("QTY")
            Total_QTYs        = split_entry("Total_QTY")
            Unit_prices       = split_entry("Unit_price")
            numberings        = split_entry("numbering")
            Discount_Types    = split_entry("Discount_Type")
            Discount_Values   = split_entry("Discount_Value")
            Final_Prices      = split_entry("Final_Price")

            for i in range(len(var)):
                try:
                    item = {}
                    # Add product/material info depending on prefix
                    item = { 
                        "Unit": Units[i].strip(),
                        "QTY": float(QTYs[i].strip()),
                        "numbering": float(numberings[i].strip()),
                        "Total_QTY": float(Total_QTYs[i].strip()),
                        "Unit_price": float(Unit_prices[i].strip()),
                        "Discount_Type": Discount_Types[i].strip(),
                        "Discount_Value": float(Discount_Values[i].strip()),
                        "Final_Price": float(Final_Prices[i].strip())
                    }
                    
                    if prefix.lower() == "customer":
                        item["Product_code"] = Product_codes[i].strip()
                        item["product_name"] = product_names[i].strip()
                    else:
                        item["material_code"] = material_codes[i].strip()
                        item["material_name"] = material_names[i].strip()
                    

                    items.append(item)
                except (IndexError, ValueError) as e:
                    messagebox.showerror(self.t("Upload Error"), f"{self.t("All Data fields must be filled:")} {e}")
                    return
                
            # new_entry["Date"] = datetime.now().strftime("%d/%m/%Y %H:%M")
            temp = datetime.now()
            # value_date = datetime.strptime(temp, '%d-%m-%Y').date()
            # new_entry["Date"] = datetime.combine(value_date, time.min)


        for field, widget in self.entries.items():
            #add fields not added when using add entry here
            # if field in ["product_name","product_code"] and collection_name == "Products":
            # if (field in ["product_name","product_code","material_code","material_name"] and (collection_name == "Sales" or collection_name == "Purchases")):
            #     dummy=0
            
            if field == config.PRIMARY_KEYS.get(collection_name):
                prim_key_val = widget.get()
                is_unique = self.is_primary_key_unique(current_collection, collection_name, prim_key_val)

                if is_unique:
                    value = prim_key_val
                else:
                    messagebox.showerror(self.t("Data Error"), f"{prim_key_val} {self.t("is not unique in field")} {field}")
                    return
                
            elif field == "Date" and collection_name in ["Sales","Purchases"]:
                continue
            
            elif field in config.ZEROED_FIELDS:
                value = widget.get()
                if not value:
                    value = 0
            elif field in [
                "customer_code", "customer_name", "customer_phone1", "customer_phone2", "customer_address",
                "Net_total", "Previous_balance", "Total_balance", "Payed_cash", "Remaining_balance", "Payment_method",
                "Product_code", "product_name", "Unit", "QTY", "Total_QTY", "Unit_price", "numbering",
                "Discount_Type", "Discount_Value", "Final_Price",
                "supplier_code", "supplier_name", "Id",
                "supplier_phone1","supplier_phone2","supplier_address","material_code","material_name"
                ] and collection_name in ["Sales","Purchases","Customer_Payments", "Supplier_Payments"]:
                value = widget.get()
                
                if not str(value).strip():
                    messagebox.showerror(self.t("Validation Error"), f"{self.t("Field")} '{field}' {self.t("cannot be empty.")}")
                    return  # stop processing if any critical field is empty
                continue  # Skip these fields
            
            if "date" in field.lower() or "timestamp" in field.lower() or "check_out" in field.lower() or "check_in" in field.lower():
                value = widget.get()
                if value:
                    try:
                        value_date = datetime.strptime(value, '%d-%m-%Y').date()
                        value = datetime.combine(value_date, time.min)
                        # Add this only for Employee_withdrawls
                        if collection_name in ["Employee_withdrawls", "Employee_Salary", "Production"]:
                            random_hours   = random.randint(0, 23)
                            random_minutes = random.randint(0, 59)
                            random_seconds = random.randint(0, 59)
                            value += timedelta(hours=random_hours, minutes=random_minutes, seconds=random_seconds)

                    except Exception as e:
                        messagebox.showerror(self.t("Error"), f"{self.t("Invalid date format for")} {field}: {e}")
                        return
                else:
                    messagebox.showwarning(self.t("Warning"), f"{self.t("Please enter a value for")} {field}")
                    return
            elif "pic" in field.lower():
                local_image_path = getattr(widget, 'image_path', None)
                if not local_image_path:
                    messagebox.showerror(self.t("Invalid Input"), self.t("No img was selected"))
                    return
                try:
                    value = upload_file_to_cloudinary(local_image_path)
                except Exception as e:
                    messagebox.showerror(self.t("Upload Error"), f"{self.t("Failed to upload image:")} {e}")
                    return
            elif "pdf_path" in field.lower():
                local_pdf_path = getattr(widget, 'filepath', None)

                if not local_pdf_path:
                    messagebox.showerror(self.t("Invalid Input"), self.t("No PDF was selected."))
                    return

                try:
                    value = config.upload_pdf_to_cloudinary(local_pdf_path)

                    # ✅ Clear filepath attribute and display text after successful upload
                    if hasattr(widget, 'filepath'):
                        widget.filepath = None
                    widget.config(text="")  # Clear displayed filename or label
                except Exception as e:
                    messagebox.showerror(self.t("Upload Error"), f"{self.t("Failed to upload PDF:")} {e}")
                    return

            elif any(word in field.lower() for word in ["instapay","bank_account","e-wallet"]) or (current_collection.name == "Customers" and field=="Sales") :
                value = widget.get() 
                if value:
                    try: 
                        value = int(value)
                    except Exception as e:
                        messagebox.showerror(self.t("Error"), f"{field} {self.t("should be a number")}")
                        return
            elif any(word in field.lower() for word in ["stock_quantity", "salary", "credit", "debit", "balance", "Unit_Price", "duration", "net_total", "previous_balance", "payed_cash", "remaining_balance", "base_salary", "total_withdrawls", "delay_penalty", "overtime_bonus", "net_salary", "amount_withdrawls", "previous_withdrawls", "waste", "product_qty", "material_qty", "amount"]):
                value = widget.get() 
                if not value:
                    messagebox.showwarning(self.t("Warning"), f"{self.t("Please enter a value for")} {field}")
                    return
                try: 
                    value = float(value)
                except Exception as e:
                    messagebox.showerror(self.t("Error"), f"{field} {self.t("should be a floating number")}")
                    return
            else:
                value = widget.get()
                if not value and (field in config.MANDATORTY_FIELDS) :
                    messagebox.showwarning(self.t("Warning"), f"{self.t("Please enter a value for")} {self.t(field)}")
                    return
                if any(word in field.lower() for word in ["units"]):
                    # Parse comma-separated input to list
                    value = [item.strip() for item in value.split(',') if item.strip()]

            new_entry[field] = value

        try:
            # Generate unique Id
            if "Id" in fields:
                # Convert string IDs to integers and find the maximum
                existing_ids = [int(doc["Id"]) for doc in current_collection.find({}, {"Id": 1})]
                
                new_id = max(existing_ids, default=0) + 1
                new_entry["Id"] = new_id

            #TODO this line is never reached on adding
            if collection_name in ["Sales","Purchases"]:
                new_entry["Date"] = temp
                new_entry[f"{prefix}_info"] = info_obj
                new_entry["Items"] = items
                new_entry["Financials"] = financials_obj

            current_collection.insert_one(new_entry)
            config.report_log(db.logs_collection, self.app.user_name, current_collection, f"{self.t("Added new record to")}", new_entry, self.t)

            self.refresh_generic_table(tree, current_collection, collection_name, search_text="")
            messagebox.showinfo(self.t("Success"), self.t("Record added successfully"))

            # Clear form fields after successful addition
            for field, widget in self.entries.items():
                if "date" in field.lower():
                    widget.set_date(datetime.now())
                elif "pic" in field.lower():
                    widget.config(image='')
                    widget.image = None
                elif "pdf_path" in field.lower():
                    widget.config(text="")
                else:
                    widget.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror(self.t("Error"), f"{self.t("Error adding record:")} {e}")

    def on_tree_selection(self, event, tree, columns, collection_name, img_label):
        first_document = None
        current_collection = config.get_collection_by_name(collection_name)
        id_index = 0
        selected_item = tree.selection()
        if not selected_item:
            for field, entry in self.entries.items():
                if isinstance(entry, ttk.Combobox):
                    entry.set('')
                elif isinstance(entry, DateEntry):
                    entry.set_date(datetime.now())
                elif "pdf_path" in field.lower():
                    entry.config(text="")
                elif hasattr(entry, 'image') and img_label:
                    img_label.config(image='')
                    img_label.image = None
                else:
                    entry.delete(0, tk.END)
            
            if(img_label):
                img_label.config(image="")
                img_label.image = None
            return
        try:
            lower_columns = [col.lower() for col in columns]
            # if "id" in lower_columns:
            #     id_index = columns.index("Id")  # Dynamically get the index of "Id" #TODO need something different to loop on
            # elif any(('code' in col) or ('receipt_number' in col) for col in lower_columns):
            #     for idx, col in enumerate(lower_columns):
            #         if 'code' in col or 'receipt_number' in col:
            #             id_index = idx
            #             break


            # Find which column is used as identifier (id / code)
            if current_collection.name in ["Customer_Payments","Supplier_Payments", "Sales", "Purchases"]:
                id_index = 0
            elif current_collection.name in ["Production", "Employee_Salary", "Employee_withdrawls"]:
                id_index = columns.index("timestamp")

            elif current_collection.name in ["Employee_appointimets"]:
                id_index = columns.index("duration")
            elif "id" in [col.lower() for col in columns]:
                id_index = columns.index("Id")
            elif any('code' in col.lower() for col in columns):
                for idx, col in enumerate(columns):
                    if 'code' in col.lower():
                        id_index = idx
                        break
            else:
                messagebox.showerror(self.t("Error"), self.t("Unable to determine identifier column."))
                return

            if id_index is None:
                messagebox.showerror(self.t("Error"), self.t("Unable to determine identifier column."))
                return

            # unique_id = tree.item(selected_item)['values'][id_index]

            field_name = columns[id_index]
            if field_name == "timestamp":
                #change to datetime obj
                raw_unique_id = tree.item(selected_item)["values"][id_index]
                unique_id = datetime.strptime(raw_unique_id, "%Y-%m-%d %H:%M:%S.%f")
            elif field_name == "duration":
                unique_id = float(tree.item(selected_item)["values"][id_index])
            else:
                unique_id = tree.item(selected_item)["values"][id_index]

            first_document = current_collection.find_one({columns[id_index]: unique_id})

            if not first_document and isinstance(unique_id, str):
                try:
                    first_document = current_collection.find_one({columns[id_index]: int(unique_id)})
                except ValueError:
                    pass

            # If not found, and type is int, try converting to str
            elif not first_document and isinstance(unique_id, int):
                first_document = current_collection.find_one({columns[id_index]: str(unique_id)})

        except IndexError:
            return
        
        for field, entry in self.entries.items():
            if field in config.field_mapping: 
                parent, child = config.field_mapping[field]
                value = first_document.get(parent, {}).get(child, "")
            else:
                value = first_document.get(field, "")
            
            items = first_document.get("Items", [])
            
            if isinstance(entry, ttk.Combobox):
                if value == '':
                    value = first_document.get(child, "")
                entry.set(value)

            if isinstance(value, datetime):
                value = value.strftime('%d-%m-%Y')
                entry.delete(0, tk.END)
                entry.insert(0, value)
            elif field in ['product_name', 'Product_code', 'Unit', 'QTY', 'numbering',
                    'Total_QTY', 'Unit_price', 'Discount_Type', 'Discount_Value', 'Final_Price'] \
                    and collection_name == "Sales":

                if isinstance(items, list):
                    values = [str(item.get(field, '')) for item in items]
                    value = ', '.join(values)
                else:
                    value = ''
                entry.delete(0, tk.END)
                entry.insert(0, value)
            elif field in ['material_name', 'material_code', 'Unit', 'QTY', 'numbering',
                    'Total_QTY', 'Unit_price', 'Discount_Type', 'Discount_Value', 'Final_Price'] \
                    and collection_name == "Purchases":

                if isinstance(items, list):
                    values = [str(item.get(field, '')) for item in items]
                    value = ', '.join(values)
                else:
                    value = ''
                entry.delete(0, tk.END)
                entry.insert(0, value)
            elif field == "Units" and isinstance(value, list):
                value_str = ' , '.join(map(str, value))
                entry.delete(0, tk.END)
                entry.insert(0, value_str)
            # If it's a pic field, load preview
            elif "pic" in field.lower():
                if img_label and value:
                    load_image_preview_from_url(value, img_label)
            elif "pdf_path" in field.lower():
                empty = 0 #dummy code
            else:
                entry.delete(0, tk.END)
                entry.insert(0, value)


    def edit_generic_entry(self, tree, current_collection, collection_name):
        selected_item = tree.selection()

        if not selected_item:
            messagebox.showwarning(self.t("Warning"), self.t("Please select a record to edit"))
            return

        selected_data = tree.item(selected_item)["values"]
        if not selected_data:
            messagebox.showwarning(self.t("Warning"), self.t("No data found for selected record"))
            return

        columns = tree["columns"]  # This returns a tuple/list of column names
        try:
            lower_columns = [col.lower() for col in columns]
            if current_collection.name in ["Customer_Payments","Supplier_Payments","Sales", "Purchases"]:
                id_index = 0
            elif current_collection.name in ["Production", "Employee_Salary", "Employee_withdrawls"]:
                id_index = columns.index("timestamp")
            elif "id" in lower_columns:
                id_index = columns.index("Id")  # Dynamically get the index of "Id" #TODO need something different to loop on
            elif any('code' in col for col in lower_columns):
                for idx, col in enumerate(lower_columns):
                    if 'code' in col:
                        id_index = idx
                        break
        except ValueError:
            messagebox.showerror(self.t("Error"), self.t("'Id' field not found in table columns"))
            return

        field_name = columns[id_index]
        if field_name == "timestamp":
            #change to datetime obj
            raw_unique_id = tree.item(selected_item)["values"][id_index]
            unique_id = datetime.strptime(raw_unique_id, "%Y-%m-%d %H:%M:%S.%f")
        elif field_name == "duration":
            unique_id = float(tree.item(selected_item)["values"][id_index])
        else:
            unique_id = tree.item(selected_item)["values"][id_index]


        existing_record = current_collection.find_one({columns[id_index]: unique_id})

        if not existing_record:
            try:
                unique_id = str(unique_id)
                existing_record = current_collection.find_one({columns[id_index]: unique_id})
                existing_record.pop("_id", None)
            except ValueError:
                pass

        if not existing_record: #recheck existing record after potential update
            messagebox.showerror(self.t("Error"), self.t("Could not find record in database"))
            return
        
        updated_entry = {}
        prefix = ""
        # Handle special cases for Customer_Payments and Supplier_Payments
        if collection_name in ["Customer_Payments", "Supplier_Payments"]:
            prefix = "Customer" if collection_name == "Customer_Payments" else "supplier"
            info_object = existing_record.get(f"{prefix}_info", {})
            
            # Update info object if code/name fields were modified
            code_field = f"{prefix.lower()}_code"
            name_field = f"{prefix.lower()}_name"

            if code_field in self.entries:
                code_value = self.entries[code_field].get()
                if code_value:
                    info_object["code"] = code_value
            
            if name_field in self.entries:
                name_value = self.entries[name_field].get()
                if name_value:
                    info_object["name"] = name_value
            
            updated_entry[f"{prefix}_info"] = info_object

        if collection_name in ['Sales','Purchases']:
            prefix = "Customer" if collection_name == "Sales" else "supplier"

            financials_obj = existing_record.get("Financials",{})
            info_obj = existing_record.get(f"{prefix}_info",{})
            items = existing_record.get("Items",{})
            big_obj = {
                "Financials": financials_obj,
                f"{prefix}_info": info_obj,
                "Items": items
            }

            for field, widget in self.entries.items():  
                if field in ["Product_code","material_code"] and isinstance(items,list):
                    item_codes = None
                    if field == "Product_code":
                        item_codes = self.entries["Product_code"].get()
                    else: 
                        item_codes = self.entries["material_code"].get()

                    split_item_codes = item_codes.split(',')
                    num_items = len(split_item_codes)
                    idx = 0
                    
                    while num_items > idx:
                        item = items[idx] if idx < len(items) else {}
                        for key in item.keys():
                            value = self.entries[key].get() #check out this line
                            if isinstance(value, str):
                                split_values = value.split(',')
                                if idx < len(split_values):
                                    if key in ["QTY", "numbering", "Total_QTY", "Unit_price", "Discount_Value", "Final_Price"]:
                                        item[key] = float(split_values[idx].strip())
                                    else: 
                                        item[key] = split_values[idx].strip()
                                else:
                                    item[key] = ''
                            else:
                                if key in ["QTY", "numbering", "Total_QTY", "Unit_price", "Discount_Value", "Final_Price"]:
                                    item[key] = float(value)  # or handle non-string cases differently
                                else:
                                    item[key] = value
                                    
                        if(len(items) < num_items):
                            items.append(item)
                        else:
                            items[idx] = item
                        idx += 1

                    big_obj["Items"] = items
   
                elif field in ["product_name", "Unit", "QTY", "Total_QTY", "Unit_price", "numbering",
                                "Discount_Type", "Discount_Value", "Final_Price", "material_name"]:
                    continue

                elif field in config.field_mapping:
                    parent, child = config.field_mapping[field]
                    value = widget.get()
                    parent, child = config.field_mapping[field]
                    if parent in big_obj:
                        if child in ["QTY", "numbering", "Total_QTY", "Unit_price", "Discount_Value", "Final_Price", "Net_total", "Previous_balance", "Total_balance", "Payed_cash", "Remaining_balance"]:
                            big_obj[parent][child] = float(value)
                        else:
                            big_obj[parent][child] = value

            updated_entry["Financials"]    = big_obj["Financials"]
            updated_entry[f"{prefix}_info"] = big_obj[f"{prefix}_info"]
            updated_entry["Items"]         = big_obj["Items"]

        for field, widget in self.entries.items():
            if collection_name in ['Sales', 'Purchases'] and field in ["customer_code", "customer_name", "customer_phone1", 
                "customer_phone2", "customer_address", "Net_total", "Previous_balance", "Total_balance", "Payed_cash",
                "Remaining_balance", "Payment_method", "Product_code", "product_name", "Unit", "QTY", "Total_QTY", 
                "Unit_price", "numbering", "Discount_Type", "Discount_Value", "Final_Price", "supplier_code", "supplier_name", "Id"
                "supplier_phone1","supplier_phone2","supplier_address","material_code","material_name"]  :
                continue
            elif collection_name in ['Customer_Payments', 'Supplier_Payments'] and field in ["customer_code", "customer_name","supplier_code", "supplier_name"]:
                continue
            elif field in ["Id", "Date"]:
                continue  # Skip Id and special fields (handled above)

            existing_value = existing_record.get(field, None)

            if "date" in field.lower() or "timestamp" in field.lower() or "check_out" in field.lower() or "check_in" in field.lower():
                value = widget.get()
                if value and collection_name != "Sales":
                    try:
                        value_date = datetime.strptime(value, '%d-%m-%Y').date()
                        value = datetime.combine(value_date, time.min)
                    except Exception as e:
                        messagebox.showerror(self.t("Error"), f"{self.t("Invalid date format for")} {field}: {e}")
                        return
                else:
                    value = existing_value  # Keep old date if no new input

            elif "pic" in field.lower():
                local_image_path = getattr(widget, 'image_path', None)

                if local_image_path:
                    try:
                        value = upload_file_to_cloudinary(local_image_path)
                    except Exception as e:
                        messagebox.showerror(self.t("Upload Error"), f"{self.t("Failed to upload image:")} {e}")
                        return
                else:
                    value = existing_value  # Keep old image URL if no new selection
            
            elif "pdf_path" in field.lower():
                local_pdf_path = getattr(widget, 'filepath', None)

                if local_pdf_path:
                    try:
                        value = config.upload_pdf_to_cloudinary(local_pdf_path)
                    except Exception as e:
                        messagebox.showerror(self.t("Upload Error"), f"{self.t("Failed to upload PDF:")} {e}")
                        return
                else:
                    value = existing_value  # Keep old PDF URL if no new selection
            elif any(word in field.lower() for word in ["instapay","bank_account","e-wallet"]) or (current_collection.name == "Customers" and field=="Sales") :
                value = widget.get() 
                if not value:
                    value = existing_value  # Keep old text if no new input

                try: 
                    if value:
                        value = int(value)
                except Exception as e:
                    messagebox.showerror(self.t("Error"), f"{field} {self.t("should be a number")}")
                    return

            elif any(word in field.lower() for word in ["stock_quantity", "salary", "credit", "debit", "balance", "Unit_Price", "duration", "net_total", "previous_balance", "payed_cash", "remaining_balance", "base_salary", "total_withdrawls", "delay_penalty", "overtime_bonus", "net_salary", "amount_withdrawls", "previous_withdrawls", "waste", "product_qty", "material_qty", "amount"]):
                value = widget.get()
                if not value:
                    value = existing_value  # Keep old text if no new input
                try: 
                    if value:
                        value = float(value)
                except Exception as e:
                    messagebox.showerror(self.t("Error"), f"{field} {self.t("should be a floating number")}")
                    return
            else:
                try:
                    value = widget.get()
                except Exception:
                    value = None  # For non-entry widgets (just in case)

                if not value:
                    value = existing_value  # Keep old text if no new input
                else:
                    if "units" in field.lower():
                        value = [item.strip() for item in value.split(',') if item.strip()]

            updated_entry[field] = value

        try:
            self.revert_locked_fields(existing_record, updated_entry)

            identifier_field = columns[id_index]
            result = current_collection.update_one({identifier_field: unique_id}, {"$set": updated_entry})
            
            if result.modified_count > 0:
                config.report_log(db.logs_collection, self.app.user_name, current_collection, f"{self.t("Updated a record in")}", existing_record, self.t)
                messagebox.showinfo(self.t("Success"), self.t("Record updated successfully"))
            else:
                messagebox.showinfo(self.t("Info"), self.t("No changes were made (record was identical)"))

            # Refresh table
            self.refresh_generic_table(tree, current_collection, collection_name, search_text="")

            # Clear form fields after update
            for field, widget in self.entries.items():
                if "date" in field.lower():
                    widget.set_date(datetime.now())
                elif "pdf_path" in field.lower():
                    widget.config(text="")
                elif "pic" in field.lower():
                    widget.config(image='')
                    widget.image = None
                    widget.image_path = None
                else:
                    widget.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror(self.t("Error"), f"{self.t("Error updating record:")} {e}")
    
    def revert_locked_fields(self, existing, updated):
        for key, locked_fields in config.LOCKED_FIELDS.items():
            if key == "root":
                for field in locked_fields:
                    if field in updated:
                        updated[field] = existing.get(field)
                # break

            elif key == "Items":
                # Handle list of objects
                existing_items = existing.get("Items", [])
                updated_items = updated.get("Items", [])

                for idx, item in enumerate(updated_items):
                    if idx < len(existing_items):
                        for field in locked_fields:
                            if field in item:
                                if field in ["QTY", "numbering", "Total_QTY", "Unit_price", "Discount_Value", "Final_Price"]:
                                    item[field] = float(existing_items[idx].get(field))
                                else: 
                                    item[field] = existing_items[idx].get(field)
                    updated_items[idx] = item
                if len(updated_items) > 0:
                    updated["Items"] = updated_items
                # updated["Items"] = updated_items

            elif key in ["Customer_info", "supplier_info"]:
                # Handle normal nested dicts like Financials, Customer_info, etc.
                nested_existing = existing.get(key, {})
                nested_updated = updated.get(key, {})
                for field in locked_fields:
                    if field in nested_updated:
                        nested_updated[field] = nested_existing.get(field)
                if len(nested_updated) > 0:
                    updated[key] = nested_updated
    
    def delete_generic_entry(self, tree, current_collection):   
        selected_item = tree.selection()
        id_index = None
        field_name = None

        if not selected_item:
            messagebox.showwarning(self.t("Warning"), self.t("Please select a record to delete"))
            return
        columns = tree["columns"]  # Tuple/list of column names
        try:
            #TODO check this part of code, nolonger necessary?
            # lower_columns = [col.lower() for col in columns]
            # original_columns = [self.get_original_key(col) for col in columns]
            
            # # Find which column is used as identifier (id / code)
            # primary_key_field = PRIMARY_KEYS.get(current_collection.name)
            
            # Find which column is used as identifier (id / code)
            if current_collection.name in ["Customer_Payments","Supplier_Payments", "Sales", "Purchases"]:
                id_index = 0
            elif current_collection.name in ["Production", "Employee_Salary", "Employee_withdrawls"]:
                id_index = columns.index("timestamp")

            elif current_collection.name in ["Employee_appointimets"]:
                id_index = columns.index("duration")
            elif "id" in [col.lower() for col in columns]:
                id_index = columns.index("Id")
            elif any('code' in col.lower() for col in columns):
                for idx, col in enumerate(columns):
                    if 'code' in col.lower():
                        id_index = idx
                        break
            else:
                messagebox.showerror(self.t("Error"), self.t("Unable to determine identifier column."))
                return

            if id_index is None:
                messagebox.showerror(self.t("Error"), self.t("Unable to determine identifier column."))
                return
            
            raw_unique_id = None
            unique_id = None
            
            field_name = columns[id_index]
            if field_name == "timestamp":
                #change to datetime obj
                raw_unique_id = tree.item(selected_item)["values"][id_index]
                unique_id = datetime.strptime(raw_unique_id, "%Y-%m-%d %H:%M:%S.%f")
            elif field_name == "duration":
                unique_id = float(tree.item(selected_item)["values"][id_index])
            else:
                unique_id = tree.item(selected_item)["values"][id_index]

        except (IndexError, ValueError):
            if field_name == "timestamp":
                try:
                    unique_id = datetime.strptime(raw_unique_id, "%Y-%m-%d %H:%M:%S")
                except:
                    messagebox.showerror(self.t("Error"), self.t("Unable to read selected row data."))
                    return
            else:
                messagebox.showerror(self.t("Error"), self.t("Unable to read selected row data."))
                return

        if not messagebox.askyesno(self.t("Confirm"), self.t("Are you sure you want to delete this record?")):
            return

        try:
            # ARRAY_FIELDS = ['units']  # Fields you want to treat as arrays (custom handling)

            query = {field_name: unique_id}
            document = current_collection.find_one(query)
            
            if not document:
                try:
                    query = {field_name: str(unique_id)}
                    document = current_collection.find_one(query)
                except ValueError:
                    pass

            if not document:
                messagebox.showwarning(self.t("Not Found"), self.t("No matching record found to delete."))
                return

            # Step 2: Check if document contains any ARRAY_FIELDS (like 'units')
            handled = False
            values = tree.item(selected_item)["values"]
            
            prefix = None
            item_code = None
            unit_value = None
            
            if("Units" in columns):
                index = columns.index('Units')
                unit_value = values[index]

            if("Product_code" in columns or "material_code" in columns) and current_collection.name in ["Sales","Purchases"]:
                prefix = "Product" if current_collection.name == "Sales" else "material"
                idx1 = columns.index(f'{prefix}_code')
                idx2 = columns.index('Unit')
                item_code = values[idx1]
                unit_value = values[idx2]

            # for array_field in ARRAY_FIELDS:
            units_list = document.get('Units', None)
            items_list = document.get('Items', None)
            print(f"units_list: {isinstance(units_list, list)} , unique_id {unique_id}")
            if isinstance(units_list, list):
                # Found Units array and unique_id is inside → handle it
                if len(units_list) > 1:
                    handled = True
                    update_result = current_collection.update_one(
                        {"_id": document["_id"]},
                        {"$pull": {'Units': unit_value}}
                    )
                    if update_result.modified_count > 0:
                        config.report_log(db.logs_collection, self.app.user_name, current_collection, f"{self.t("Deleted a record from")}", document, self.t)
                        self.deselect_entry(tree)
                        self.refresh_generic_table(tree, current_collection, current_collection.name, search_text="")
                        messagebox.showinfo(self.t("Success"), f"{self.t("Unit")} '{unique_id}' {self.t("removed from record.")}")
                    else:
                        messagebox.showwarning(self.t("Warning"), self.t("No changes were made to the document."))

            if isinstance(items_list,list):
                if len(items_list) > 1 and current_collection.name in ['Sales','Purchases']:
                    update_result = current_collection.update_one(
                        {"_id": document["_id"]},
                        {
                            "$pull": {
                                "Items": {
                                    "$and": [
                                        {f"{prefix}_code": item_code},
                                        {"Unit": str(unit_value)}
                                    ]
                                }
                            }
                        }
                    )                  
                    if update_result.modified_count > 0:
                        config.report_log(db.logs_collection, self.app.user_name, current_collection, f"{self.t("Deleted a record from")}", document, self.t)
                        self.deselect_entry(tree)
                        self.refresh_generic_table(tree, current_collection, current_collection.name, search_text="")
                        messagebox.showinfo(self.t("Success"), f"{self.t("Unit")} '{unique_id}' {self.t("removed from record.")}")
                    else:
                        messagebox.showwarning(self.t("Warning"), self.t("No changes were made to the document."))

                else:
                    delete_result = current_collection.delete_one({"_id": document["_id"]})
                    if delete_result.deleted_count > 0:
                        config.report_log(db.logs_collection, self.app.user_name, current_collection, f"{self.t("Deleted a record from")}", document, self.t)
                        self.deselect_entry(tree)
                        self.refresh_generic_table(tree, current_collection, current_collection.name, search_text="")
                        messagebox.showinfo(self.t("Success"), self.t("Record deleted successfully."))
                    else:
                        messagebox.showwarning(self.t("Warning"), self.t("No matching record found to delete."))
                return  # After handling Units logic, exit

            # Step 3: If no ARRAY_FIELDS handling triggered → do standard delete
            if not handled:
                delete_result = current_collection.delete_one(query)
                if delete_result.deleted_count > 0:
                    config.report_log(db.logs_collection, self.app.user_name, current_collection, f"{self.t("Deleted a record from")}", document, self.t)
                    self.deselect_entry(tree)
                    self.refresh_generic_table(tree, current_collection, current_collection.name, search_text="")
                    messagebox.showinfo(self.t("Success"), self.t("Record deleted successfully."))
                else:
                    messagebox.showwarning(self.t("Warning"), self.t("No matching record found to delete."))

        except Exception as e:
            messagebox.showerror(self.t("Error"), f"{self.t("Error deleting record:")} {e}")         

    def display_general_table(self, current_collection, collection_name):
        
        if self.app.language == "Arabic":
            alignment = "e"
            label_col = 1
            entry_col = 0
        else:
            alignment = "w"
            label_col = 0
            entry_col = 1
        
        img_label= None
        columns = config.get_fields_by_name(collection_name)
        
        normal_fields = [label for label in columns if label != "Id" and "pic" not in label.lower()]
        pic_fields = [label for label in columns if "pic" in label.lower()]
        ordered_fields = normal_fields + pic_fields

        main_frame = tk.Frame(self.root, padx=20, pady=50)
        main_frame.pack(fill="both", expand=True)

        # ==== 1. Create scrollable form frame ====
        form_container = tk.Frame(main_frame)
        form_container.pack(side="left", fill="y", padx=10, pady=10)

        canvas = tk.Canvas(form_container, width=350)   # Set width for form
        scrollbar = tk.Scrollbar(form_container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.pack(side="left", fill="y", expand=False)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Frame inside canvas (holds labels + entries)
        form_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=form_frame, anchor='nw')

        # Ensure scrollregion resizes automatically
        def on_frame_config(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        form_frame.bind("<Configure>", on_frame_config)

        # Optional — enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        # Enable scrolling when mouse hovers inside form_frame
        def enable_scrolling(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
                
        def disable_scrolling(event):
            canvas.unbind_all("<MouseWheel>")

        # Bind mouse hovering for scroll enable/disable
        form_container.bind("<Enter>", enable_scrolling)
        form_container.bind("<Leave>", disable_scrolling)

        if 'Customer_info' in ordered_fields:
            ordered_fields.remove('Customer_info')
            if 'customer_code' not in ordered_fields:
                ordered_fields.append('customer_code')
            if 'customer_name' not in ordered_fields:
                ordered_fields.append('customer_name')
        if 'supplier_info' in ordered_fields:
            ordered_fields.remove('supplier_info')
            if 'supplier_code' not in ordered_fields:
                ordered_fields.append('supplier_code')
            if 'supplier_name' not in ordered_fields:
                ordered_fields.append('supplier_name')

        self.entries = {}
        row_index = 0

        for label in ordered_fields:
            if label in ["Id", "Operation_Number", "Customer_info", "supplier_info", "Time"]:
                continue
            elif label in ["code"] and collection_name == "general_exp_rev":
                continue
            
            #anchor="e" → aligns text to the right within the label ... "w" alternative
            # justify="right" → right-justifies multi-line text
            # sticky="e" → aligns the label to the right of the grid cell
            if label in MANDATORTY_FIELDS and collection_name in MANDATORY_DBS:
                if self.app.language == "English":
                    tk.Label(form_frame, text=f"{self.t(label)}⭐", font=("Arial", 12), anchor=alignment).grid(row=row_index, column=label_col, sticky=alignment, pady=5, padx=2)
                else:
                    tk.Label(form_frame, text=f"⭐{self.t(label)}", font=("Arial", 12), anchor=alignment).grid(row=row_index, column=label_col, sticky=alignment, pady=5, padx=2)
            else:
                tk.Label(form_frame, text=f"{self.t(label)}", font=("Arial", 12), anchor=alignment).grid(row=row_index, column=label_col, sticky=alignment, pady=5, padx=2)

            if "date" in label.lower() or "timestamp" in label.lower() or "check_out" in label.lower() or "check_in" in label.lower():
                entry = DateEntry(form_frame, font=("Arial", 12), date_pattern='dd-MM-yyyy', width=18)
                entry.grid(row=row_index, column=entry_col, pady=5)
                self.entries[label] = entry
                row_index += 1

            elif "payment_method" in label.lower():
                selected_method = tk.StringVar()
                dropdown = ttk.Combobox(form_frame, textvariable=selected_method, values=['Cash', 'E_Wallet', 'Bank_account', 'Instapay'], state="readonly", width=27)
                dropdown.grid(row=row_index, column=entry_col, pady=5)
                dropdown.set("Cash")
                self.entries[label] = dropdown
                row_index += 1

            elif "pic" in label.lower():
                frame = tk.Frame(form_frame)
                frame.grid(row=row_index, column=entry_col, pady=5)
                
                # Image Label in a *new row* below the current field
                img_label = tk.Label(form_frame)
                img_label.grid(row=row_index + 1, column=0, columnspan=3, pady=5)

                def browse_file(e=entry, img_lbl=img_label):  # Pass the current entry as argument
                    filepath = filedialog.askopenfilename(
                        title="Select a file",
                        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All files", "*.*")]
                    )
                    if filepath:
                        load_image_preview(filepath, img_lbl)

                browse_btn = tk.Button(frame, text=self.t("Browse"),width=25, command=lambda e=entry: browse_file(e))
                browse_btn.pack(side="left", padx=5)
                self.entries[label] = img_label

            elif "pdf_path" in label.lower():
                frame = tk.Frame(form_frame)
                frame.grid(row=row_index, column=entry_col, pady=5)

                file_label = tk.Label(form_frame, text="No file selected", anchor="w")
                file_label.grid(row=row_index + 1, column=0, columnspan=3, pady=5)

                def browse_file(lbl=file_label):
                    filepath = filedialog.askopenfilename(
                        title="Select a file",
                        filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
                    )
                    if filepath:
                        filename = filepath.split("/")[-1]
                        lbl.config(text=f"Selected: {filename}")
                        lbl.filepath = filepath

                browse_btn = tk.Button(frame, text=self.t("Browse"), width=25, command=browse_file)
                browse_btn.pack(side="left", padx=5)

                self.entries[label] = file_label
                row_index += 2  # Skip a row for the file label

            else:
                entry = tk.Entry(form_frame, font=("Arial", 12), width=20)
                entry.grid(row=row_index, column=entry_col, pady=5)
                self.entries[label] = entry
                if label in config.ZEROED_FIELDS:
                    entry.insert(0, "0")
                elif label == config.PRIMARY_KEYS.get(collection_name):
                    prim_key_val = self.get_next_prim_key(current_collection, collection_name)
                    entry.insert(0,prim_key_val)
                row_index += 1


        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True)

        search_frame = tk.Frame(right_frame)
        search_frame.pack(fill="x", pady=(0, 10))

        self.selected_field = tk.StringVar()
        

        if self.app.language =="Arabic":
            self.selected_field.set(self.t(ordered_fields[0]))
            translated_columns = [self.t(col) for col in ordered_fields]
        else: 
            self.selected_field.set((ordered_fields[0]))
            translated_columns = ordered_fields
        
        field_dropdown = ttk.Combobox(search_frame, textvariable=self.selected_field, values=translated_columns, width=20)
        field_dropdown.pack(side="left", padx=(0, 5))

        local_search_query = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=local_search_query)
        search_entry.pack(side="left", padx=(0, 5))

        table_frame = tk.Frame(right_frame)
        table_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(table_frame, columns=ordered_fields, show="headings")
        for col in ordered_fields:
            tree.heading(col, text=self.t(col))
            tree.column(col, anchor="center", stretch=True)
        tree.pack(fill="both", expand=True)
        tree.bind("<<TreeviewSelect>>", lambda event: self.on_tree_selection(event, tree, columns, collection_name, img_label)) #Bind tree selection to an event handler

        horizontal_scrollbar = ttk.Scrollbar(tree, orient="horizontal", command=tree.xview)
        horizontal_scrollbar.pack(side="bottom", fill="x")
        tree.configure(xscrollcommand=horizontal_scrollbar.set)

        vertical_scrollbar = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
        vertical_scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=vertical_scrollbar.set)

        # Search button now refreshes table, doesn't rebuild everything!
        tk.Button(
            search_frame,
            text=self.t("Search"),
            width=14,
            command=lambda: self.refresh_generic_table(tree, current_collection, collection_name, local_search_query.get())
        ).pack(side="left")
        
        # Bottom buttons
        self.root.configure(bg="#f0f0f0")  # Set background color for the root window
        button_frame = tk.LabelFrame(self.root, text="Actions", padx=10, pady=10, font=("Arial", 12, 'bold'))
        button_frame.pack(pady=10)

        btn_add = tk.Button(button_frame, text=self.t("Add Entry"), font=("Arial", 12), width=15, command=lambda: self.add_generic_entry(tree, current_collection,collection_name))
        btn_edit = tk.Button(button_frame, text=self.t("Update Entry"), font=("Arial", 12), width=15, command=lambda: self.edit_generic_entry(tree, current_collection,collection_name))
        btn_delete = tk.Button(button_frame, text=self.t("Delete Entry"), font=("Arial", 12), width=15, command=lambda: self.delete_generic_entry(tree, current_collection))
        btn_deselect = tk.Button(button_frame, text=self.t("Deselect Entry"), font=("Arial", 12), width=15, command=lambda:self.deselect_entry(tree))

        btn_add.grid(row=0, column=0, padx=10)
        btn_edit.grid(row=0, column=1, padx=10)
        btn_delete.grid(row=0, column=2, padx=10)
        btn_deselect.grid(row=0, column=3, padx=10)

        # Load initial table content
        self.refresh_generic_table(tree, current_collection, collection_name, search_text="")
        # self.root.configure(bg=config.COLORS["background"])


    def refresh_generic_table(self, tree, current_collection, collection_name, search_text):
        try:
            # Clear existing rows
            for row in tree.get_children():
                tree.delete(row)

            if search_text:
                # raw_selected_field = self.selected_field.get()
                if self.app.language == "Arabic":
                    raw_selected_field = self.show_original()
                else: 
                    raw_selected_field = self.selected_field.get()
                
                mogno_selected_field = self.get_mongo_field_path(raw_selected_field)
                first_document = current_collection.find_one()
                
                if first_document:
                    search_fields = config.get_fields_by_name(collection_name)
                    
                    if "Items." in mogno_selected_field:
                        field_inside_items = mogno_selected_field.split(".")[1]
                        query = { "Items": { "$elemMatch": {} } }
                        
                        if field_inside_items in ['Net_total','Previous_balance','Total_balance','Payed_cash','Remaining_balance','Unit','QTY','numbering','Total_QTY','Unit_price','Discount_Value','Final_Price']:
                            query["Items"]["$elemMatch"][field_inside_items] = float(search_text)
                        else: 
                            query["Items"]["$elemMatch"][field_inside_items] = {
                                "$regex": search_text,
                                "$options": "i"
                            }
                        
                        try:
                            data = list(current_collection.find(query).sort("Id", 1))
                        except PyMongoError as e:
                            print(f"An error occurred: {e}")
                    else:
                        or_conditions = [{"$expr": {"$regexMatch": {"input": {"$toString": f"${mogno_selected_field}"}, "regex": search_text, "options": "i"}}} for field in search_fields]
                        data = list(current_collection.find({"$or": or_conditions}).sort("Id", 1))
                else:
                    data = []
            else:
                data = list(current_collection.find().sort("Id", 1))


            if data:
                columns = config.get_fields_by_name(collection_name)
                if '_id' in columns:
                    columns.remove('_id')
                if 'Customer_info' in columns:
                    columns.remove('Customer_info')
                    if 'customer_code' not in columns:
                        columns.append('customer_code')
                    if 'customer_name' not in columns:
                        columns.append('customer_name')
                if 'supplier_info' in columns:
                    columns.remove('supplier_info')
                    if 'supplier_code' not in columns:
                        columns.append('supplier_code')
                    if 'supplier_name' not in columns:
                        columns.append('supplier_name')
                        
                tree["columns"] = columns

                for col in columns:
                    tree.heading(col, text=self.t(col))
                    tree.column(col, width=152, anchor="center", stretch=False)

                
                for row_data in data:
                    units = row_data.get('Units', [])
                    items = row_data.get('Items', {})
                    
                    if(collection_name == "Customer_Payments"):
                        customer_info = row_data.get('Customer_info', {})
                        row_data['customer_code'] = customer_info.get('code', '')
                        row_data['customer_name'] = customer_info.get('name', '')
                    
                    elif(collection_name == "Supplier_Payments"):
                        customer_info = row_data.get('supplier_info', {})
                        row_data['supplier_code'] = customer_info.get('code', '')
                        row_data['supplier_name'] = customer_info.get('name', '')
                    
                    elif(collection_name in ["Sales", "Purchases"] ):
                        prefix = "Customer" if collection_name == "Sales" else "supplier"
                        info_obj = row_data.get(f'{prefix}_info', {})
                        financials = row_data.get('Financials', {})
                        
                        #start extracting Data from these objects
                        # cust_info
                        row_data[f'{prefix.lower()}_code']    = info_obj.get('code', '')
                        row_data[f'{prefix.lower()}_name']    = info_obj.get('name', '')
                        row_data[f'{prefix.lower()}_phone1']  = info_obj.get('phone1', '')
                        row_data[f'{prefix.lower()}_phone2']  = info_obj.get('phone2', '')
                        row_data[f'{prefix.lower()}_address'] = info_obj.get('address', '')
                        #financials
                        row_data['Net_total'] = financials.get('Net_total', '')
                        row_data['Previous_balance'] = financials.get('Previous_balance', '')
                        row_data['Total_balance'] = financials.get('Total_balance', '')
                        row_data['Payed_cash'] = financials.get('Payed_cash', '')
                        row_data['Remaining_balance'] = financials.get('Remaining_balance', '')
                        row_data['Payment_method'] = financials.get('Payment_method', '')

                    # If Units is a non-empty list
                    if isinstance(units, list) and len(units) > 0:
                        for unit_value in units:
                            values = []

                            for col in columns:
                                value = row_data.get(col, '')
                                
                                if col == 'Units':
                                    value = unit_value  # Set current unit value
                                
                                elif isinstance(value, datetime):
                                    value = value.strftime('%d-%m-%Y')
                                
                                values.append(value)
                            
                            tree.insert("", "end", values=values)
                    elif isinstance(items, list) and len(items) > 0 and collection_name in ["Sales", "Purchases"]:
                        prefix = "Customer" if collection_name == "Sales" else "supplier"
                        keys = []
                        if prefix == "Customer":
                            keys = ['Product_code', 'product_name', 'Unit', 'QTY', 'numbering', \
                                    'Total_QTY', 'Unit_price', 'Discount_Type', 'Discount_Value', 'Final_Price'] 
                        else:
                            keys = ['material_code', 'material_name', 'Unit', 'QTY', 'numbering', \
                                    'Total_QTY', 'Unit_price', 'Discount_Type', 'Discount_Value', 'Final_Price'] 
                        for item in items:
                            values = []
    
                            for key in keys:
                                row_data[key] = item.get(key, '')

                            for col in columns:
                                value = row_data.get(col,'')
                                
                                values.append(value)

                            tree.insert("", "end", values=values)
                    else:
                        # Fallback to insert normally if Units is not a list or is empty
                        values = []
                        for col in columns:
                            value = row_data.get(col, '')
                            if isinstance(value, datetime) and col != "timestamp":
                                value = value.strftime('%d-%m-%Y')
                            values.append(value)
                        
                        tree.insert("", "end", values=values)
            else:
                tree["columns"] = ("No Data",)
                tree.heading("No Data", text="No Data Available")
                tree.column("No Data", width=300, anchor="center", stretch=True)
                tree.insert("", "end", values=("This collection has no documents.",))

        except Exception as e:
            messagebox.showerror(self.t("Error"), f"{self.t("Error displaying data:")}\n{e}")    

    def show_original(self):
        """Print the English key for the selected translated value."""
        selected_translated = self.selected_field.get()
        original_key = self.app.reverse_translations.get(selected_translated, "Unknown")
        return original_key
    
    def get_original_key(self, translated_label):
        """Return the original field key from a translated label."""
        return self.app.reverse_translations.get(translated_label, translated_label)

    def get_next_prim_key(self, collection, collection_name):
        primary_key_field = config.PRIMARY_KEYS.get(collection_name)
        prefix = config.PRIMARY_KEY_STARTERS.get(collection_name)

        # Find the last document sorted by primary key descending
        last_entry = collection.find_one(
            {primary_key_field: {"$regex": rf"^{prefix}-?\d+"}},
            sort=[(primary_key_field, -1)]
        )

        if last_entry and primary_key_field in last_entry:
            raw_value = last_entry[primary_key_field]
            number_part = ''.join(filter(str.isdigit, raw_value))
            next_number = int(number_part) + 1 if number_part else 1
        else:
            next_number = 1

        padded_number = f"{next_number:05d}" if prefix in ["PM", "GEN", "INV", "PR"] else f"{next_number:03d}"

        return f"{prefix}-{padded_number}"

    def deselect_entry(self,tree):
        tree.selection_remove(tree.selection())
        # Clear form fields
        for field, widget in self.entries.items():
            if "date" in field.lower():
                widget.set_date(datetime.now())
            elif "pdf_path" in field.lower():
                widget.config(text="")
            elif "pic" in field.lower():
                widget.config(image='')
                widget.image = None
            else:
                widget.delete(0, tk.END)

    def get_mongo_field_path(self, key):
        if key in config.search_field_mapping:
            parts = config.search_field_mapping[key]
            return ".".join(parts)
        return key  # fallback: return as-is if not nested
    


    def is_primary_key_unique(self, collection, collection_name, new_prim_key):
        primary_key_field = config.PRIMARY_KEYS.get(collection_name)

        existing = collection.find_one({primary_key_field: new_prim_key})
        return existing is None

def upload_file_to_cloudinary(file_path_param):
    # import cloudinary.uploader
    try:
        response = cloudinary.uploader.upload(file_path_param, resource_type="image")
        return response['secure_url']
    except Exception as e:
        print(f"[Cloudinary Upload Error]: {e}")
        return None
    
def load_image_preview_from_url(image_url, label, max_size=(300, 300)):
    """Load image from a URL and display it in a Tkinter Label.
    Args:image_url (str): The image URL to load.
         label (tk.Label): The Tkinter Label to display the image in.
         image_refs (list): A list to store image references (to avoid garbage collection).
         max_size (tuple): Max size of the image (width, height)"""
    try:
        with urllib.request.urlopen(image_url) as response:
            image_data = Image.open(io.BytesIO(response.read()))
            image_data.thumbnail(max_size)  # Resize image
            image_obj = ImageTk.PhotoImage(image_data)

            label.config(image=image_obj)
            label.image = image_obj  # Also attach to label itself (extra safety)
    except Exception as e:
        print(f"Error loading image from URL: {e}")
        label.config(image="")
        label.image = None

def load_image_preview(filepath, img_label):
    try:
        img = Image.open(filepath)
        img.thumbnail((300, 300))  # Make it bigger (adjust size as you wish)
        img_tk = ImageTk.PhotoImage(img)
        
        img_label.config(image=img_tk)
        img_label.image = img_tk
        img_label.image_path = filepath   # <== DID YOU ADD THIS LINE? 👈👈👈
    except Exception as e:
        print(f"Error loading image preview: {e}")
