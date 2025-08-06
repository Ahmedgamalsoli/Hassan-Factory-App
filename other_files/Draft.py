def new_Purchase_invoice(self, user_role, add_or_update):
        # Clear current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Initialize product mappings
        self.material_map = {}
        self.name_to_code = {}
        
        # Create top bar
        self.topbar(show_back_button=True,Back_to_Purchases_Window=True)

        # MongoDB collections
        suppliers_col = self.get_collection_by_name("Suppliers")
        purchases_col = self.get_collection_by_name("Purchases")
        materials_col = self.get_collection_by_name("Materials")

        # Main form frame with responsive sizing
        form_frame = tk.Frame(self.root)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Configure columns - 10 columns with equal weight
        for i in range(10):
            form_frame.columnconfigure(i, weight=1)

        # ===== INVOICE SELECTION FOR UPDATE MODE =====
        current_row = 0
        self.selected_invoice_id = None
        
        if add_or_update == "update":
            # Create invoice selection frame
            invoice_frame = tk.Frame(form_frame, bd=1, relief=tk.SOLID, padx=5, pady=5)
            invoice_frame.grid(row=current_row, column=0, columnspan=12, sticky='ew', pady=5)
            current_row += 1
            
            # Configure invoice frame columns
            for i in range(12):
                invoice_frame.columnconfigure(i, weight=1 if i % 2 == 1 else 0)
            
            # Fetch invoice numbers
            invoice_numbers = [str(doc["Receipt_Number"]) for doc in purchases_col.find({}, {"Receipt_Number": 1})]
            
            # Invoice selection
            tk.Label(invoice_frame, text=self.t("Select Invoice"), 
                    font=("Arial", 10, "bold")).grid(row=0, column=0, sticky='w')
            self.invoice_var = tk.StringVar()
            invoice_cb = ttk.Combobox(invoice_frame, textvariable=self.invoice_var, values=invoice_numbers)
            invoice_cb.grid(row=0, column=1, padx=5, sticky='ew', columnspan=3)
            
            # Load button
            load_btn = tk.Button(invoice_frame, text=self.t("Load Invoice"), 
                                command=lambda: self.load_invoice_data(purchases_col),
                                bg='#2196F3', fg='white')
            load_btn.grid(row=0, column=4, padx=5, sticky='ew')
            
            # Delete button
            delete_btn = tk.Button(invoice_frame, text=self.t("Delete Invoice"), 
                                command=lambda: self.delete_invoice(purchases_col, suppliers_col),
                                bg='red', fg='white')
            delete_btn.grid(row=0, column=5, padx=5, sticky='ew')

        # ===== Supplier SECTION =====
        # Create Supplier frame
        supplier_frame = tk.Frame(form_frame, bd=1, relief=tk.SOLID, padx=5, pady=5)
        supplier_frame.grid(row=current_row, column=0, columnspan=12, sticky='ew', pady=5)
        current_row += 1
        
        # Configure Supplier frame columns
        for i in range(12):
            supplier_frame.columnconfigure(i, weight=1 if i % 2 == 1 else 0)        

        # Create bidirectional supplier mappings
        self.supplier_code_map = {}  # name -> code
        self.code_name_map = {}      # code -> name
        self.supplier_balance_map = {}  # name -> balance

        # Populate supplier data
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
        tk.Label(supplier_frame, text=self.t("Supplier Name"), 
                font=("Arial", 10, "bold")).grid(row=0, column=0, sticky='w')
        self.supplier_name_var = tk.StringVar()
        self.supplier_name_cb = ttk.Combobox(supplier_frame, 
                                            textvariable=self.supplier_name_var, 
                                            values=sorted(all_suppliers))
        self.supplier_name_cb.grid(row=0, column=1, padx=5, sticky='ew')

        # Supplier Code Combobox
        tk.Label(supplier_frame, text=self.t("Supplier Code"), 
                font=("Arial", 10, "bold")).grid(row=0, column=2, sticky='w')
        self.supplier_code_var = tk.StringVar()
        self.supplier_code_cb = ttk.Combobox(supplier_frame, 
                                            textvariable=self.supplier_code_var, 
                                            values=sorted(all_codes))
        self.supplier_code_cb.grid(row=0, column=3, padx=5, sticky='ew')

        # Balance and Payment Fields
        tk.Label(supplier_frame, text=self.t("Previous Balance"), 
                font=("Arial", 10, "bold")).grid(row=0, column=4, sticky='e')
        self.previous_balance_var = tk.StringVar()
        self.previous_balance_entry = tk.Entry(supplier_frame, 
                                            textvariable=self.previous_balance_var, 
                                            state='readonly')
        self.previous_balance_entry.grid(row=0, column=5, sticky='ew', padx=5)

        tk.Label(supplier_frame, text=self.t("Paid Money"), 
                font=("Arial", 10, "bold")).grid(row=0, column=6, sticky='e')
        self.payed_cash_var = tk.DoubleVar()
        self.payed_cash_entry = tk.Entry(supplier_frame, 
                                        textvariable=self.payed_cash_var)
        self.payed_cash_entry.grid(row=0, column=7, sticky='ew', padx=5)

        # Payment Method Dropdown
        tk.Label(supplier_frame, text=self.t("Payment Method"), 
                font=("Arial", 10, "bold")).grid(row=0, column=8, sticky='e')
        self.payment_method_var = tk.StringVar()
        payment_methods = ['Cash', 'E_Wallet', 'Bank_account', 'Instapay']
        payment_cb = ttk.Combobox(supplier_frame, 
                                textvariable=self.payment_method_var, 
                                values=payment_methods, 
                                state='readonly')
        payment_cb.grid(row=0, column=9, sticky='ew', padx=5)
        payment_cb.current(0)  # Set default to Cash

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

        # Load material data
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
            messagebox.showerror("Database Error", f"Failed to load materials: {str(e)}")
            return

        # ===== ITEMS GRID SECTION =====
        # Make items grid expandable
        form_frame.grid_rowconfigure(current_row + 1, weight=1)
        
        # Invoice Items Grid - Responsive Configuration
        columns = self.get_fields_by_name("Materials_Header")
        num_columns = len(columns)
        
        # Create header frame with uniform columns
        header_frame = tk.Frame(form_frame, bg='#f0f0f0')
        header_frame.grid(row=2, column=0, columnspan=10, sticky='ew', pady=(20, 0))
        
        # Configure header columns with uniform weights
        for col_idx in range(num_columns):
            header_frame.columnconfigure(col_idx, weight=1, uniform='cols')
            tk.Label(header_frame, text=self.t(columns[col_idx]), relief='ridge', 
                    bg='#f0f0f0', anchor='w', padx=5).grid(row=0, column=col_idx, sticky='ew')

        # Scrollable Canvas with responsive sizing
        canvas_container = tk.Frame(form_frame)
        canvas_container.grid(row=3, column=0, columnspan=10, sticky='nsew')
        canvas_container.grid_rowconfigure(0, weight=1)
        canvas_container.grid_columnconfigure(0, weight=1)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(canvas_container, highlightthickness=0)
        scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
        
        # Create a frame inside the canvas for the rows
        self.rows_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.rows_frame, anchor="nw", tags="inner_frame")
        
        # Grid layout for canvas and scrollbar
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configure scroll region
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        # Configure canvas width
        def configure_canvas(event):
            canvas_width = event.width
            canvas.itemconfig("inner_frame", width=canvas_width)
        
        # Bind events
        self.rows_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_canvas)

        # Set initial width
        canvas.update_idletasks()
        canvas_width = canvas.winfo_width()
        if canvas_width > 1:
            canvas.itemconfig("inner_frame", width=canvas_width)

        self.entries = []

        # Modified create_row function with responsive widgets
        def create_row(parent, row_number, bg_color):
            row_frame = tk.Frame(parent, bg=bg_color)
            row_frame.pack(fill=tk.X)  # Use pack with fill to ensure full width
            
            # Configure columns with uniform weights (same as header)
            for col_idx in range(num_columns):
                row_frame.columnconfigure(col_idx, weight=1, uniform='cols')
            
            row_entries = []
            for col_idx, col in enumerate(columns):
                if col == "Material_code":
                    var = tk.StringVar()
                    cb = ttk.Combobox(row_frame, textvariable=var, values=material_codes)
                    cb.bind('<<ComboboxSelected>>', lambda e, r=row_number: self.update_material_info(r, "code"))
                    cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_combobox_change_purchase(e, r, "code"))
                    cb.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                    row_entries.append(cb)
                elif col == "Material_name":
                    var = tk.StringVar()
                    cb = ttk.Combobox(row_frame, textvariable=var, values=material_names)
                    cb.bind('<<ComboboxSelected>>', lambda e, r=row_number: self.update_material_info(r, "name"))
                    cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_combobox_change_purchase(e, r, "name"))
                    cb.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                    row_entries.append(cb)
                elif col == "unit":
                    var = tk.StringVar()
                    cb = ttk.Combobox(row_frame, textvariable=var, values=[])
                    cb.bind('<KeyRelease>', lambda e, r=row_number: self.handle_unit_change(e, r))
                    cb.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                    row_entries.append(cb)
                elif col == "Discount Type":
                    var = tk.StringVar()
                    cb = ttk.Combobox(row_frame, textvariable=var, 
                                    values=["Percentage", "Value"], 
                                    state="readonly")
                    cb.current(0)
                    cb.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                    row_entries.append(cb)
                elif col == "Discount Value":
                    var = tk.StringVar()
                    entry = tk.Entry(row_frame, textvariable=var)
                    entry.bind('<KeyRelease>', lambda e, r=row_number: self.calculate_totals(r))
                    entry.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                    row_entries.append(entry)
                elif col in ["Unit_Price", "Total_QTY", "Total_Price"]:
                    entry = tk.Entry(row_frame, relief='flat', state='readonly')
                    entry.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                    row_entries.append(entry)
                else:
                    entry = tk.Entry(row_frame, relief='sunken')
                    entry.bind('<KeyRelease>', lambda e, r=row_number: self.calculate_totals(r))
                    entry.grid(row=0, column=col_idx, sticky='ew', padx=1, pady=1)
                    row_entries.append(entry)
            
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
        button_frame.grid(row=4, column=0, columnspan=10, pady=10, sticky='ew')
        
        # Configure button frame columns
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        add_btn = tk.Button(button_frame, text=self.t("➕ Add 3 More Rows"), 
                        command=add_three_rows, bg='#4CAF50', fg='white')
        add_btn.grid(row=0, column=0, padx=5, sticky='w')
        if add_or_update == "add":
            save_btn = tk.Button(button_frame, text=self.t("💾 Save Invoice"), 
                                command=lambda: self.save_invoice_purchase(purchases_col, suppliers_col, materials_col),
                                bg='#2196F3', fg='white')
            save_btn.grid(row=0, column=1, padx=5, sticky='e')
        else:
            self.update = True
            update_btn = tk.Button(button_frame, text=self.t("🔄 Update Invoice"), 
                                command=lambda: self.save_invoice_purchase(purchases_col, suppliers_col, materials_col),
                                bg='#FF9800', fg='white')
            update_btn.grid(row=0, column=1, padx=5, sticky='e')