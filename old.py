    # def display_table(self):
    #     self.image_refs.clear()
    #     collection_name = self.table_name.get()
    #     search_query = self.search_query.get()
        
    #     current_collection = self.get_collection_by_name(collection_name)

    #     for row in self.tree.get_children():
    #         self.tree.delete(row)
        
    #     try:
    #         # Fetch all documents
    #         if search_query:
    #             # Create a dynamic query based on the search term
    #             first_document = current_collection.find_one()
    #             if first_document:
    #                 search_fields = self.get_fields_by_name(collection_name)
    #                 or_conditions = [{"$expr": {"$regexMatch": {"input": {"$toString": f"${field}"}, "regex": search_query, "options": "i"}}} for field in search_fields]
    #                 data = list(current_collection.find({"$or": or_conditions}).sort("Id", 1))
    #             else:
    #                 data = [] # No documents to search in
    #         else:
    #             data = list(current_collection.find().sort("Id", 1))

    #         if data:
    #             columns = self.get_fields_by_name(collection_name)
    #             self.tree["columns"] = columns

    #             for col in columns:
    #                 self.tree.heading(col, text=col)
    #                 self.tree.column(col, width=152, anchor="center", stretch=False)

    #             self.tree.column("#0", width=152, anchor="center")
    #             self.tree.heading("#0", text="Image")

    #             for row_data in data:
    #                 values = []
    #                 for col in columns:
    #                     val = row_data.get(col, '')
    #                     if 'pic' in col.lower():
    #                         if isinstance(val, str) and val.startswith("http"):
    #                             print(val)  # Optional: print the URL
                            
    #                     if 'date' in col.lower() and isinstance(val, datetime):
    #                         val = val.strftime("%d-%m-%Y")
    #                     values.append(val)
                            
    #                 self.tree.insert("", "end", values=values)
    #         else:
    #             # Show placeholder column and row
    #             self.tree["columns"] = ("No Data",)
    #             self.tree.heading("No Data", text="No Data Available")
    #             self.tree.column("No Data", width=300, anchor="center", stretch=True)
    #             self.tree.insert("", "end", values=("This collection has no documents.",))
    #             return

    #     except Exception as e:
    #         messagebox.showerror(self.t("Error"), f"{self.t("Error displaying data:")}\n{e}")
    

    # def add_entry(self):
    #     collection_name = self.table_name.get()
    #     current_collection = self.get_collection_by_name(collection_name)

    #     new_entry = {}
    #     fields = self.get_fields_by_name(collection_name)
    
    #     try:
    #         latest_entry = current_collection.find_one(sort=[("Id", -1)])  # Sort by Id descending
    #         new_id = (latest_entry["Id"] + 1) if latest_entry else 1
    #     except Exception:
    #         new_id = 1

    #     new_entry["Id"] = new_id

    #     for field in fields:
    #         if field == "Id":
    #             continue
    #         if "date" in field.lower():
    #             dialog = tk.Toplevel(self.root)  # Create a Toplevel for date input
    #             dialog.transient(self.root)
    #             dialog.grab_set()
    #             dialog.title(f"Enter value for {field}")

    #             date_label = tk.Label(dialog, text=f"Enter {field}:")
    #             date_label.pack(padx=10, pady=5)

    #             date_entry = DateEntry(dialog, font=("Arial", 12), date_pattern='dd-MM-yyyy')
    #             date_entry.pack(padx=10, pady=5)

    #             selected_date = tk.StringVar()

    #             def on_ok():
    #                 selected_date_obj = date_entry.get_date()
    #                 selected_date_str = selected_date_obj.strftime('%d-%m-%Y')
    #                 selected_date.set(selected_date_str)
    #                 dialog.destroy()

    #             ok_button = tk.Button(dialog, text="OK", command=on_ok)
    #             ok_button.pack(pady=5)
    #             ok_button.bind("<Return>", lambda event: ok_button.invoke())

    #             # Center the date selection dialog
    #             screen_width = self.root.winfo_screenwidth()
    #             screen_height = self.root.winfo_screenheight()
    #             x_position = (screen_width // 2) - (dialog_width // 2)
    #             y_position = (screen_height // 2) - (dialog_height // 2)
    #             dialog.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")
    #             self.root.wait_window(dialog)

    #             value = selected_date.get()
    #             if value:
    #                 try:
    #                     value = datetime.strptime(value, '%d-%m-%Y').date()
    #                     value = datetime.combine(value, time.min) #Must do this to be comaptible with mongodb's Date type 
    #                 except Exception as e:
    #                     print(f"ValueError: {e}")
    #                     messagebox.showerror(self.t("Error"), f"{self.t("Invalid date format for")} {field}")
    #                     return
    #             else:
    #                 return  # User cancelled
    #         elif "pic" in field.lower():
    #             file_path = filedialog.askopenfilename(title=f"Select image for {field}",
    #                                                 filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    #             if not file_path:
    #                 return  # User cancelled
    #             try:
    #                 value = upload_file_to_cloudinary(file_path)
    #             except Exception as e:
    #                 messagebox.showerror(self.t("Upload Error"), f"{self.t("Failed to upload image:")} {e}")
    #                 return
    #         else:
    #             dialog = AlwaysOnTopInputDialog(self.root, f"{self.t("Enter value for")} {field}:")
    #             value = dialog.get_result()
    #             if value is None:
    #                 return

    #         new_entry[field] = value

    #     try:
    #         current_collection.insert_one(new_entry)
    #         self.display_table()
    #         messagebox.showinfo(self.t("Success"), self.t("Record added successfully"))
    #     except Exception as e:
    #         messagebox.showerror(self.t("Error"), f"{self.t("Error adding record:")} {e}")

    # def edit_entry(self):
    #     collection_name = self.table_name.get()
    #     current_collection = self.get_collection_by_name(collection_name)
        
    #     selected_item = self.tree.selection()
    #     if not selected_item:
    #         messagebox.showwarning(self.t("Warning"), self.t("Please select a record to edit"))
    #         return

    #     #TODO fix this ID no longer available in tree
    #     try:
    #         unique_id = self.tree.item(selected_item)['values'][2]  # Assuming this holds the custom unique ID
    #     except IndexError:
    #         messagebox.showerror(self.t("Error"), self.t("Unable to read selected row data."))
    #         return
        
    #     # Get the fields to edit (excluding _id)
    #     first_document = current_collection.find_one({"Id": unique_id})
    #     if not first_document:
    #         messagebox.showerror(self.t("Error"), self.t("Could not retrieve record for editing."))
    #         return

    #     fields = self.get_fields_by_name(collection_name)
    #     updated_values = {}

    #     for field in fields:
    #         if field == "Id":
    #             continue
    #         if "date" in field.lower():
    #             dialog = tk.Toplevel(self.root)  # Create a Toplevel for date input
    #             dialog.transient(self.root)
    #             dialog.grab_set()
    #             dialog.title(f"Enter value for {field}")

    #             date_label = tk.Label(dialog, text=f"Enter {field}:")
    #             date_label.pack(padx=10, pady=5)

    #             date_entry = DateEntry(dialog, font=("Arial", 12), date_pattern='dd-MM-yyyy')
    #             date_entry.pack(padx=10, pady=5)

    #             selected_date = tk.StringVar()

    #             def on_ok():
    #                 selected_date_obj = date_entry.get_date()
    #                 selected_date_str = selected_date_obj.strftime('%d-%m-%Y')
    #                 selected_date.set(selected_date_str)
    #                 dialog.destroy()

    #             ok_button = tk.Button(dialog, text="OK", command=on_ok)
    #             ok_button.pack(pady=5)
    #             ok_button.bind("<Return>", lambda event: ok_button.invoke())

    #             # Center the date selection dialog
    #             screen_width = self.root.winfo_screenwidth()
    #             screen_height = self.root.winfo_screenheight()
    #             x_position = (screen_width // 2) - (dialog_width // 2)
    #             y_position = (screen_height // 2) - (dialog_height // 2)
    #             dialog.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")
    #             self.root.wait_window(dialog)

    #             value = selected_date.get()
    #             if value:
    #                 try:
    #                     value = datetime.strptime(value, '%d-%m-%Y').date()
    #                     value = datetime.combine(value, time.min) #Must do this to be comaptible with mongodb's Date type 

    #                 except Exception as e:
    #                     print(f"ValueError: {e}")
    #                     messagebox.showerror(self.t("Error"), f"{self.t("Invalid date format for")} {field}")
    #                     return
    #             else:
    #                 return  # User cancelled

    #         else:
    #             dialog = AlwaysOnTopInputDialog(self.root, f"Enter value for {field}:")
    #             value = dialog.get_result()
    #             if value is None:
    #                 return

    #         updated_values[field] = value

    #     try:
    #         current_collection.update_one({"Id": unique_id}, {"$set": updated_values})
    #         self.display_table()
    #         messagebox.showinfo(self.t("Success"), self.t("Record updated successfully"))
    #     except Exception as e:
    #         messagebox.showerror(self.t("Error"), f"{self.t("Error updating record:")} {e}")

    # def delete_entry(self):
    #     collection_name = self.table_name.get()
    #     current_collection = self.get_collection_by_name(collection_name)

    #     selected_item = self.tree.selection()
    #     if not selected_item:
    #         messagebox.showwarning(self.t("Warning"), self.t("Please select a record to delete"))
    #         return

    #     try:
    #         unique_id = self.tree.item(selected_item)['values'][2]  # Assuming this holds the custom unique ID
    #     except IndexError:
    #         messagebox.showerror(self.t("Error"), self.t("Unable to read selected row data."))
    #         return

    #     if messagebox.askyesno(self.t("Confirm"), self.t("Are you sure you want to delete this record?")):
    #         try:
    #             delete_result = current_collection.delete_one({"Id": unique_id})
    #             if delete_result.deleted_count == 0:
    #                 messagebox.showwarning(self.t("Not Found"), self.t("No matching record found to delete."))
    #             else:
    #                 self.display_table()
    #                 messagebox.showinfo(self.t("Success"), self.t("Record deleted successfully"))
    #         except Exception as e:
    #             messagebox.showerror(self.t("Error"), f"{self.t("Error deleting record:")} {e}")
