import frappe
import os
import json


def after_install():
    """Setup after app installation."""
    create_roles()
    import_fixtures()
    create_workspace()
    frappe.db.commit()


def after_migrate():
    """Fix workspace after migrate."""
    fix_workspace()
    frappe.db.commit()


def create_workspace():
    """Create workspace programmatically."""
    # Delete old workspaces
    for old_name in ["PP Management", "Petrol Pump Management"]:
        if frappe.db.exists("Workspace", old_name):
            try:
                frappe.delete_doc("Workspace", old_name, force=True, ignore_missing=True)
            except Exception:
                pass
    frappe.db.commit()

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

    try:
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
    except Exception as e:
        print("Error creating workspace: " + str(e))


def fix_workspace():
    """Fix workspace visibility."""
    try:
        frappe.db.sql(
            "UPDATE `tabWorkspace` SET public=1, is_hidden=0 WHERE name=%s",
            ("Petrol Pump Management",)
        )
        frappe.clear_cache()
    except Exception:
        pass


def create_roles():
    """Create custom roles for petrol pump management."""
    roles = [
        {"role_name": "Station Manager", "desk_access": 1, "is_custom": 1,
         "description": "Station Manager / Dealer - Full access to all modules"},
        {"role_name": "Salesman DSM", "desk_access": 1, "is_custom": 1,
         "description": "Salesman / Direct Sales Man"},
        {"role_name": "Credit Accounts Officer", "desk_access": 1, "is_custom": 1,
         "description": "Credit & Accounts Officer"},
        {"role_name": "Compliance Officer", "desk_access": 1, "is_custom": 1,
         "description": "Compliance Officer (GST)"},
        {"role_name": "Recovery Officer", "desk_access": 1, "is_custom": 1,
         "description": "Recovery Officer - Credit recovery"},
        {"role_name": "Petrol Pump Auditor", "desk_access": 1, "is_custom": 1,
         "description": "Auditor / CA - Read-only access"},
    ]
    for role_data in roles:
        if not frappe.db.exists("Role", role_data["role_name"]):
            role = frappe.new_doc("Role")
            role.update(role_data)
            role.insert(ignore_permissions=True)


def import_fixtures():
    """Import fixture data from the fixtures directory."""
    fixtures_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "pp_management", "fixtures"
    )

    if not os.path.exists(fixtures_path):
        return

    for filename in sorted(os.listdir(fixtures_path)):
        if not filename.endswith(".json"):
            continue

        filepath = os.path.join(fixtures_path, filename)
        with open(filepath, "r") as f:
            docs = json.load(f)

        if not isinstance(docs, list):
            docs = [docs]

        for doc_data in docs:
            doctype = doc_data.pop("doctype", None)
            if not doctype:
                continue

            name = doc_data.get("name") or doc_data.get(doc_data.get("__key", "name"))
            if name and frappe.db.exists(doctype, name):
                continue

            try:
                doc = frappe.new_doc(doctype)
                doc.update(doc_data)
                doc.insert(ignore_permissions=True)
            except Exception:
                pass
