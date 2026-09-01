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
    """Create workspace using raw SQL for reliability."""

    # Delete old workspaces
    for old_name in ["PP Management", "Petrol Pump Management"]:
        if frappe.db.exists("Workspace", old_name):
            try:
                frappe.delete_doc("Workspace", old_name, force=True, ignore_missing=True)
            except Exception:
                pass
    frappe.db.commit()

    now = frappe.utils.now_datetime()
    now_str = str(now)

    links = [
        ("Card Break", "", "Configuration", "", 0, 0, 0),
        ("Link", "DocType", "Station Configuration", "Station Configuration", 0, 0, 0),
        ("Link", "DocType", "Tank Master", "Tank Master", 0, 0, 0),
        ("Link", "DocType", "Nozzle Master", "Nozzle Master", 0, 0, 0),
        ("Link", "DocType", "Fuel Price Master", "Fuel Price Master", 0, 0, 0),
        ("Link", "DocType", "Employee Master", "Employee Master", 0, 0, 0),
        ("Link", "DocType", "Tank Dip Chart", "Tank Dip Chart", 0, 0, 0),
        ("Card Break", "", "Operations", "", 0, 0, 0),
        ("Link", "DocType", "Shift", "Shift", 0, 0, 0),
        ("Link", "DocType", "Shift Nozzle Allotment", "Shift Nozzle Allotment", 0, 0, 0),
        ("Link", "DocType", "Fuel Sale", "Fuel Sale", 0, 0, 0),
        ("Link", "DocType", "Meter Reading", "Meter Reading", 0, 0, 0),
        ("Link", "DocType", "Daily Stock Register", "Daily Stock Register", 0, 0, 0),
        ("Link", "DocType", "Stock Purchase Decantation", "Stock Purchase Decantation", 0, 0, 0),
        ("Link", "DocType", "Trip Voucher", "Trip Voucher", 0, 0, 0),
        ("Link", "DocType", "PP Supplier Master", "PP Supplier Master", 0, 0, 0),
        ("Card Break", "", "Credit & Sales", "", 0, 0, 0),
        ("Link", "DocType", "PP Customer", "PP Customer", 0, 0, 0),
        ("Link", "DocType", "Vehicle Master", "Vehicle Master", 0, 0, 0),
        ("Link", "DocType", "Credit Sale Invoice", "Credit Sale Invoice", 0, 0, 0),
        ("Link", "DocType", "Payment Receipt", "Payment Receipt", 0, 0, 0),
        ("Link", "DocType", "Credit Limit Ledger", "Credit Limit Ledger", 0, 0, 0),
        ("Link", "DocType", "ANPR Scan Log", "ANPR Scan Log", 0, 0, 0),
        ("Card Break", "", "Finance & HR", "", 0, 0, 0),
        ("Link", "DocType", "Expense Entry", "Expense Entry", 0, 0, 0),
        ("Link", "DocType", "Attendance Register", "Attendance Register", 0, 0, 0),
        ("Link", "DocType", "Advance Amount", "Advance Amount", 0, 0, 0),
        ("Link", "DocType", "Bank Deposit", "Bank Deposit", 0, 0, 0),
        ("Link", "DocType", "Day Settlement", "Day Settlement", 0, 0, 0),
        ("Card Break", "", "Reports", "", 0, 0, 0),
        ("Link", "Report", "Daily Sales Summary", "Daily Sales Summary", 0, 1, 0),
        ("Link", "Report", "Shift Settlement Report", "Shift Settlement Report", 0, 1, 0),
        ("Link", "Report", "Stock Variation Report", "Stock Variation Report", 0, 1, 0),
        ("Link", "Report", "Credit Customer Ageing", "Credit Customer Ageing", 0, 1, 0),
        ("Link", "Report", "GST VAT Summary", "GST VAT Summary", 0, 1, 0),
    ]

    content = json.dumps([
        {"id": "c1", "type": "card", "data": {"card_name": "Configuration", "col": 4}},
        {"id": "c2", "type": "card", "data": {"card_name": "Operations", "col": 4}},
        {"id": "c3", "type": "card", "data": {"card_name": "Credit & Sales", "col": 4}},
        {"id": "c4", "type": "card", "data": {"card_name": "Finance & HR", "col": 4}},
        {"id": "c5", "type": "card", "data": {"card_name": "Reports", "col": 4}},
    ])

    ws_name = "Petrol Pump Management"

    # Insert workspace
    frappe.db.sql("""
        INSERT INTO `tabWorkspace`
        (name, label, title, module, app, icon, indicator_color, public, standard,
         is_hidden, custom, category, content, docstatus, owner, modified_by,
         modified, creation)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0, 'Administrator',
         'Administrator', %s, %s)
    """, (ws_name, ws_name, ws_name, "PP Management", "petrol_pump_management",
          "fuel", "green", 1, 1, 0, 0, "Module", content, now_str, now_str))

    # Insert links as child records
    for idx, (link_type, link_type_val, label, link_to, hidden, is_query_report, onboard) in enumerate(links):
        link_name = f"{ws_name}-{idx}"
        frappe.db.sql("""
            INSERT INTO `tabWorkspace Link`
            (name, parent, parenttype, parentfield, idx, link_type, link_to,
             label, hidden, is_query_report, onboard, dependencies, link_count)
            VALUES (%s, %s, 'Workspace', 'links', %s, %s, %s, %s, %s, %s, %s, '', 0)
        """, (link_name, ws_name, idx + 1, link_type, link_to, label, hidden, is_query_report, onboard))

    frappe.db.commit()
    frappe.clear_cache()


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
