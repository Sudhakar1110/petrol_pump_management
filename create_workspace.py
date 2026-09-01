"""
Run this after installing the app:
    bench --site your-site.local console
    exec(open('apps/petrol_pump_management/create_workspace.py').read())
"""
import frappe

# Delete old workspaces
for name in ["PP Management", "Petrol Pump Management"]:
    if frappe.db.exists("Workspace", name):
        frappe.delete_doc("Workspace", name, force=True, ignore_missing=True)

frappe.db.commit()

# Create workspace
links = [
    {"hidden": 0, "is_query_report": 0, "label": "Configuration", "link_count": 0, "onboard": 0, "type": "Card Break"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Station Configuration", "link_count": 0, "link_to": "Station Configuration", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Tank Master", "link_count": 0, "link_to": "Tank Master", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Nozzle Master", "link_count": 0, "link_to": "Nozzle Master", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Fuel Price Master", "link_count": 0, "link_to": "Fuel Price Master", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Employee Master", "link_count": 0, "link_to": "Employee Master", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Tank Dip Chart", "link_count": 0, "link_to": "Tank Dip Chart", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"hidden": 0, "is_query_report": 0, "label": "Operations", "link_count": 0, "onboard": 0, "type": "Card Break"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Shift", "link_count": 0, "link_to": "Shift", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Shift Nozzle Allotment", "link_count": 0, "link_to": "Shift Nozzle Allotment", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Fuel Sale", "link_count": 0, "link_to": "Fuel Sale", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Meter Reading", "link_count": 0, "link_to": "Meter Reading", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Daily Stock Register", "link_count": 0, "link_to": "Daily Stock Register", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Stock Purchase Decantation", "link_count": 0, "link_to": "Stock Purchase Decantation", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Trip Voucher", "link_count": 0, "link_to": "Trip Voucher", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "PP Supplier Master", "link_count": 0, "link_to": "PP Supplier Master", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"hidden": 0, "is_query_report": 0, "label": "Credit & Sales", "link_count": 0, "onboard": 0, "type": "Card Break"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "PP Customer", "link_count": 0, "link_to": "PP Customer", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Vehicle Master", "link_count": 0, "link_to": "Vehicle Master", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Credit Sale Invoice", "link_count": 0, "link_to": "Credit Sale Invoice", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Payment Receipt", "link_count": 0, "link_to": "Payment Receipt", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Credit Limit Ledger", "link_count": 0, "link_to": "Credit Limit Ledger", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "ANPR Scan Log", "link_count": 0, "link_to": "ANPR Scan Log", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"hidden": 0, "is_query_report": 0, "label": "Finance & HR", "link_count": 0, "onboard": 0, "type": "Card Break"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Expense Entry", "link_count": 0, "link_to": "Expense Entry", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Attendance Register", "link_count": 0, "link_to": "Attendance Register", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Advance Amount", "link_count": 0, "link_to": "Advance Amount", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Bank Deposit", "link_count": 0, "link_to": "Bank Deposit", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Day Settlement", "link_count": 0, "link_to": "Day Settlement", "link_type": "DocType", "onboard": 0, "type": "Link"},
    {"hidden": 0, "is_query_report": 0, "label": "Reports", "link_count": 0, "onboard": 0, "type": "Card Break"},
    {"hidden": 0, "is_query_report": 1, "label": "Daily Sales Summary", "link_count": 0, "link_to": "Daily Sales Summary", "link_type": "Report", "onboard": 0, "type": "Link"},
    {"hidden": 0, "is_query_report": 1, "label": "Shift Settlement Report", "link_count": 0, "link_to": "Shift Settlement Report", "link_type": "Report", "onboard": 0, "type": "Link"},
    {"hidden": 0, "is_query_report": 1, "label": "Stock Variation Report", "link_count": 0, "link_to": "Stock Variation Report", "link_type": "Report", "onboard": 0, "type": "Link"},
    {"hidden": 0, "is_query_report": 1, "label": "Credit Customer Ageing", "link_count": 0, "link_to": "Credit Customer Ageing", "link_type": "Report", "onboard": 0, "type": "Link"},
    {"hidden": 0, "is_query_report": 1, "label": "GST VAT Summary", "link_count": 0, "link_to": "GST VAT Summary", "link_type": "Report", "onboard": 0, "type": "Link"},
]

content = json.dumps([
    {"id": "c1", "type": "card", "data": {"card_name": "Configuration", "col": 4}},
    {"id": "c2", "type": "card", "data": {"card_name": "Operations", "col": 4}},
    {"id": "c3", "type": "card", "data": {"card_name": "Credit & Sales", "col": 4}},
    {"id": "c4", "type": "card", "data": {"card_name": "Finance & HR", "col": 4}},
    {"id": "c5", "type": "card", "data": {"card_name": "Reports", "col": 4}},
])

ws = frappe.get_doc({
    "doctype": "Workspace",
    "name": "Petrol Pump Management",
    "label": "Petrol Pump Management",
    "title": "Petrol Pump Management",
    "module": "PP Management",
    "app": "petrol_pump_management",
    "icon": "fuel",
    "indicator_color": "green",
    "public": 1,
    "standard": 1,
    "is_hidden": 0,
    "custom": 0,
    "category": "Module",
    "links": links,
    "content": content,
    "charts": [],
    "number_cards": [],
    "shortcuts": [],
    "roles": [],
    "sidebar_items": [],
    "custom_blocks": [],
})
ws.insert(ignore_permissions=True)
frappe.db.commit()
print("Workspace 'Petrol Pump Management' created successfully!")
