from pymongo import MongoClient
from urllib.parse import quote_plus

raw_password = "HassanFactory@1@6@6"
encoded_password = quote_plus(raw_password)
uri = f"mongodb+srv://hassanfactory116:{encoded_password}@hassan.fkplsys.mongodb.net/"

client = MongoClient(uri,serverSelectionTimeoutMS=5000)        
db = client["Hassan"]   

customers_collection             = db['Customers']
employees_collection             = db['Employees']
employees_appointments_collection= db['Employee_appointimets']
employee_withdrawls_collection   = db['Employee_withdrawls']
employee_salary_collection       = db['Employee_Salary']
products_collection              = db['Products']
sales_collection                 = db['Sales']
suppliers_collection             = db['Suppliers']
materials_collection             = db['Materials']
purchases_collection             = db['Purchases']
shipping_collection              = db['Shipping']
orders_collection                = db['Orders']
expenses_collection              = db['Expenses']
daily_shifts_collection          = db['Daily_shifts']
accounts_collection              = db['Accounts']
transactions_collection          = db['Transactions']
big_deals_collection             = db['Big_deals']
TEX_Calculations_collection      = db['TEX_Calculations']
production_collection            = db['Production']
customer_payments                = db["Customer_Payments"]
supplier_payments                = db["Supplier_Payments"]
general_exp_rev_collection       = db["general_exp_rev"]
messages_collection              = db["Messages"]
logs_collection                  = db["Logs"]