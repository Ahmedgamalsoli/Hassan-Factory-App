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



    # def manage_old_database_window(self, db_name=None, table_name=None):
    #     # self.db_name.set(db_name if db_name else "")
    #     self.table_name.set(table_name if table_name else "")

    #     for widget in self.root.winfo_children():
    #         widget.destroy()

    #     # تحميل صورة الخلفية
    #     self.topbar.topbar(show_back_button=True)

    #     tk.Label(self.root, text="Select Table:", bg="#4a90e2", fg="white", font=("Arial", 12)).place(x=130, y=110)
    #     table_dropdown = ttk.Combobox(self.root, textvariable=self.table_name, values=["Employees", "Products", "Sales", "Customers","Suppliers","Shipping","Orders","Expenses","Employee_appointments","Daily_shifts","Accounts","Transactions","Big_deals","TEX_Calculations"])
    #     table_dropdown.place(x=250, y=110)
    #     table_dropdown.bind("<<ComboboxSelected>>", lambda e: self.display_table())

    #     tk.Label(self.root, text="Search:", bg="#4a90e2", fg="white", font=("Arial", 12)).place(x=140, y=150)
    #     search_entry = tk.Entry(self.root, textvariable=self.search_query)
    #     search_entry.place(x=250, y=150)
    #     tk.Button(self.root, text="Search", command=self.display_table).place(x=410, y=145)

    #     self.tree = ttk.Treeview(self.root, show="headings")
    #     self.tree.place(x=50, y=190)

    #     # # Create scrollbars inside frame
    #     # self.tree_xscroll = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
    #     # self.tree_yscroll = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)

    #     # # Attach scrollbars to tree
    #     # self.tree.configure(xscrollcommand=self.tree_xscroll.set, yscrollcommand=self.tree_yscroll.set)

    #     # # Place them manually
    #     # self.tree.place(x=0, y=0, width=780, height=230)  # little smaller so scrollbars fit
    #     # self.tree_xscroll.place(x=0, y=230, width=780, height=20)
    #     # self.tree_yscroll.place(x=780, y=0, width=20, height=230)


    #     tk.Button(self.root, text="Add Record", command=self.add_entry).place(width=120, height=40, x=100, y=550)
    #     tk.Button(self.root, text="Edit Record", command=self.edit_entry).place(width=120, height=40, x=250, y=550)
    #     tk.Button(self.root, text="Delete Record", command=self.delete_entry).place(width=120, height=40, x=400, y=550)

    #     self.display_table()


# ######################### Auxiliary classes #########################################################
# class AlwaysOnTopInputDialog(tk.Toplevel):
#     def __init__(self, parent, prompt):
#         super().__init__(parent)
#         self.transient(parent)
#         self.grab_set()

#         self.title("Input")

#         self.prompt_label = tk.Label(self, text=prompt)
#         self.prompt_label.pack(padx=10, pady=10)

#         self.input_widget = tk.Entry(self)
#         self.input_widget.pack(padx=10, pady=10)
#         self.input_widget.focus_set()

#         self.result = None

#         self.ok_button = tk.Button(self, text="OK", command=self.on_ok)
#         self.ok_button.pack(pady=5)
#         self.ok_button.bind("<Return>", lambda event: self.ok_button.invoke())

#         self.after(1, self.adjust_geometry)
#         self.center_dialog(parent)

#     def adjust_geometry(self):
#         self.geometry("300x150")

#     def center_dialog(self, parent):
#         screen_width = parent.winfo_screenwidth()
#         screen_height = parent.winfo_screenheight()
#         dialog_width = self.winfo_reqwidth()
#         dialog_height = self.winfo_reqheight()
#         x_position = (screen_width // 2) - (dialog_width // 2)
#         y_position = (screen_height // 2) - (dialog_height // 2)
#         self.geometry(f"{dialog_width}x{dialog_height}+{x_position}+{y_position}")

#     def on_ok(self):
#         if isinstance(self.input_widget, DateEntry):
#             self.result = self.input_widget.get_date()
#         else:
#             self.result = self.input_widget.get()
#         self.destroy()

#     def get_result(self):
#         self.wait_window(self)
#         return self.result



#######################################unused#######################################
    # Modify your show_visualizations method:
    # def show_visualizations(self,user_role):
    #     # Clear current window
    #     for widget in self.root.winfo_children():
    #         widget.destroy()
    #     print(1)
    #     # Create the top bar
    #     self.topbar.topbar(show_back_button=True)
    #     print(1)
    #     try:
    #         print(1)
    #         # Create new window
    #         # vis_window = tk.Toplevel(self.root)
    #         # vis_window.title("Business Analytics")
    #         # vis_window.state("zoomed")  # Maximized window
    #         print(1)
    #         # Create main container
    #         main_frame = tk.Frame(self.root, bg="white")
    #         main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    #         print(1)
    #         # Get data from database
    #         data = {
    #             'customers': self.get_customer_count(),
    #             'suppliers': self.get_supplier_count(),
    #             'sales': self.get_sales_count(),
    #             'purchases': self.get_purchase_count(),
    #             'top_client': self.get_top_client()
    #         }
    #         print(1)
    #         # Create figure
    #         fig = plt.Figure(figsize=(16, 10), dpi=100)
    #         fig.suptitle("Business Performance Dashboard", fontsize=16, y=0.95)
    #         print(1)
    #         # Create subplots
    #         ax1 = fig.add_subplot(221)
    #         ax2 = fig.add_subplot(222)
    #         ax3 = fig.add_subplot(223)
    #         ax4 = fig.add_subplot(224)
    #         print(1)
    #         # Chart 1: Customers vs Suppliers
    #         ax1.bar(['Customers', 'Suppliers'], 
    #                 [data['customers'], data['suppliers']], 
    #                 color=['#1f77b4', '#ff7f0e'])
    #         ax1.set_title(self.t("Customer & Supplier Count"), pad=15,font="Arial")
    #         ax1.set_ylabel("Count")
    #         print(1)
    #         # Chart 2: Sales/Purchases Ratio
    #         ax2.pie([data['sales'], data['purchases']],
    #                 labels=['Sales', 'Purchases'],
    #                 autopct='%1.1f%%',
    #                 colors=['#2ca02c', '#d62728'],
    #                 startangle=90)
    #         ax2.set_title("Sales vs Purchases Ratio", pad=15)
    #         print(1)
    #         # Chart 3: Top Client
    #         if data['top_client']:
    #             ax3.bar(data['top_client'][0], data['top_client'][1],
    #                     color='#9467bd')
    #             ax3.set_title("Top Performing Client", pad=15)
    #             ax3.set_ylabel("Sales Amount")
    #         print(1)
    #         # Chart 4: Summary Table
    #         table_data = [
    #             ['Metric', 'Value'],
    #             ['Total Customers', data['customers']],
    #             ['Total Suppliers', data['suppliers']],
    #             ['Total Sales', data['sales']],
    #             ['Total Purchases', data['purchases']]
    #         ]
    #         ax4.axis('off')
    #         table = ax4.table(cellText=table_data, 
    #                         loc='center', 
    #                         cellLoc='center',
    #                         colWidths=[0.4, 0.4])
    #         table.auto_set_font_size(False)
    #         table.set_fontsize(12)

    #         # Embed in Tkinter
    #         canvas = FigureCanvasTkAgg(fig, master=main_frame)
    #         canvas.draw()
    #         canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


    #     except Exception as e:
    #         print(f"Error generating visualizations: {e}")
    #         tk.messagebox.showerror(self.t("Error"), f"{self.t("Failed to load reports:")} {str(e)}")      


    # def create_main_buttons(self, parent,buttons):
    #     # buttons = [
    #     #     {"text": "New Sales Invoice", "image": "Sales.png",
    #     #     "command": lambda: self.AuxiliaryClass.trash(self.user_role)},
    #     #     {"text": "New Purchase Invoice", "image": "Purchase.png", 
    #     #     "command": lambda: self.AuxiliaryClass.trash(self.user_role)},
    #     #     {"text": "Production Order", "image": "Production Order.png", 
    #     #     "command": lambda: self.AuxiliaryClass.trash(self.user_role)},
    #     #     {"text": "Employee Interactions", "image": "Employees.png", 
    #     #     "command": lambda: self.AuxiliaryClass.trash(self.user_role)},
    #     #     {"text": "Treasury", "image": "Treasury.png", 
    #     #     "command": lambda: self.AuxiliaryClass.trash(self.user_role)},
    #     #     {"text": "Database", "image": "Database.png", 
    #     #     "command": lambda: self.AuxiliaryClass.trash(self.user_role)},
    #     #     # {"text": "Analytics", "image": "Analytics.png", 
    #     #     # "command": lambda: self.AuxiliaryClass.trash(self.user_role)},
    #     # ]

    #     columns_per_row = 3
    #     button_size = 100

    #     try:
    #         for index, btn_info in enumerate(buttons):
    #             row = index // columns_per_row
    #             column = index % columns_per_row

    #             btn_frame = tk.Frame(parent, bg=config.COLORS["card"])
    #             btn_frame.grid(row=row, column=column, padx=15, pady=15)

    #             # button_frame = tk.Frame(parent, bg=config.COLORS["card"])
    #             # button_frame.pack(pady=30)
                
    #             # Load and process image
    #             img_path = os.path.join(BASE_DIR, "Static", "images", btn_info["image"])
    #             img = Image.open(img_path).resize((button_size, button_size), Image.LANCZOS)
    #             photo_img = ImageTk.PhotoImage(img)

    #             # Create modern button
    #             btn = tk.Button(btn_frame,
    #                         image=photo_img,
    #                         text=btn_info["text"],
    #                         compound=tk.TOP,
    #                         bg=config.COLORS["card"],
    #                         fg=config.COLORS["text"],
    #                         activebackground=config.COLORS["highlight"],
    #                         font=("Segoe UI", 10),
    #                         borderwidth=0,
    #                         command=btn_info["command"])
    #             btn.image = photo_img
    #             btn.pack()

    #             # Hover effect
    #             btn.bind("<Enter>", lambda e, b=btn: b.config(bg=config.COLORS["primary"]))
    #             btn.bind("<Leave>", lambda e, b=btn: b.config(bg=config.COLORS["card"]))
                
    #     except Exception as e:
    #         print(f"Button error: {e}")


    #Function to update the time 
    # def update_time(self, time_label):
    #     time_label.config(text=datetime.now().strftime('%B %d, %Y %I:%M %p'))
    #     self.root.after(1000, self.update_time, time_label)


    # def on_canvas_press(self, event):
    #     self.tree.scan_mark(event.x, event.y)

    # def on_canvas_drag(self, event):
    #     self.tree.scan_dragto(event.x, event.y, gain=1)

    # # Update scroll region dynamically
    # def update_scroll_region(self, event=None):
    #     self.tree.configure(scrollregion=self.tree.bbox("all"))

    # def check_access_and_open(self, role):
    #     allowed_roles = ["admin","developer"]  # Define roles that can access this
    #     if role in allowed_roles:
    #         # self.manage_old_database_window(db_name, table_name)
    #         self.manage_database_window()
    #     else:
    #         messagebox.showwarning(self.t("Access Denied"), self.t("You do not have permission to access this page."))