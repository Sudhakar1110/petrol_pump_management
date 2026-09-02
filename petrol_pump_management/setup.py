import frappe
import os
import json


def after_install():
    """Setup after app installation."""
    create_roles()
    import_fixtures()
    frappe.db.commit()


def after_migrate():
    """After migration - ensure workspace exists with all links."""
    _ensure_workspace()


def _ensure_workspace():
    """Create workspace with all links. Always rebuilds to ensure card breaks and links are shown."""
    ws_name = "Petrol Pump Management"

    # Always delete and recreate to ensure clean state with all card breaks and links
    for name in frappe.db.get_all("Workspace", filters={"module": "PP Management"}, pluck="name"):
        frappe.db.sql("DELETE FROM `tabWorkspace Link` WHERE parent = %s", name)
        frappe.db.sql("DELETE FROM `tabWorkspace` WHERE name = %s", name)

    for row in frappe.db.sql(
        "SELECT name FROM `tabWorkspace` WHERE name LIKE %s OR name LIKE %s",
        ("%Petrol%", "%PP%"), as_dict=True,
    ):
        frappe.db.sql("DELETE FROM `tabWorkspace Link` WHERE parent = %s", row.name)
        frappe.db.sql("DELETE FROM `tabWorkspace` WHERE name = %s", row.name)

    frappe.db.commit()

    content = json.dumps([
        {"type": "header", "data": {"text": "Petrol Pump Management", "level": 4, "col": 12}},
        {"type": "spacer", "data": {"col": 12}},
        {"type": "header", "data": {"text": "Configuration", "level": 4, "col": 12}},
        {"type": "card", "data": {"card_name": "Configuration", "col": 4}},
        {"type": "spacer", "data": {"col": 12}},
        {"type": "header", "data": {"text": "Operations", "level": 4, "col": 12}},
        {"type": "card", "data": {"card_name": "Operations", "col": 4}},
        {"type": "spacer", "data": {"col": 12}},
        {"type": "header", "data": {"text": "Credit & Sales", "level": 4, "col": 12}},
        {"type": "card", "data": {"card_name": "Credit & Sales", "col": 4}},
        {"type": "spacer", "data": {"col": 12}},
        {"type": "header", "data": {"text": "Finance & HR", "level": 4, "col": 12}},
        {"type": "card", "data": {"card_name": "Finance & HR", "col": 4}},
        {"type": "spacer", "data": {"col": 12}},
        {"type": "header", "data": {"text": "Reports", "level": 4, "col": 12}},
        {"type": "card", "data": {"card_name": "Reports", "col": 4}},
    ])

    links = [
        # Configuration Card
        {"type": "Card Break", "label": "Configuration", "icon": "octicon octicon-gear", "link_count": 6, "hidden": 0, "is_query_report": 0, "onboard": 0, "idx": 1},
        {"type": "Link", "link_type": "DocType", "link_to": "Station Configuration", "label": "Station Configuration", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 2},
        {"type": "Link", "link_type": "DocType", "link_to": "Tank Master", "label": "Tank Master", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 3},
        {"type": "Link", "link_type": "DocType", "link_to": "Nozzle Master", "label": "Nozzle Master", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 4},
        {"type": "Link", "link_type": "DocType", "link_to": "Fuel Price Master", "label": "Fuel Price Master", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 5},
        {"type": "Link", "link_type": "DocType", "link_to": "Employee Master", "label": "Employee Master", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 6},
        {"type": "Link", "link_type": "DocType", "link_to": "Tank Dip Chart", "label": "Tank Dip Chart", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 7},

        # Operations Card
        {"type": "Card Break", "label": "Operations", "icon": "octicon octicon-gear", "link_count": 8, "hidden": 0, "is_query_report": 0, "onboard": 0, "idx": 8},
        {"type": "Link", "link_type": "DocType", "link_to": "Shift", "label": "Shift", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 9},
        {"type": "Link", "link_type": "DocType", "link_to": "Shift Nozzle Allotment", "label": "Shift Nozzle Allotment", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 10},
        {"type": "Link", "link_type": "DocType", "link_to": "Fuel Sale", "label": "Fuel Sale", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 11},
        {"type": "Link", "link_type": "DocType", "link_to": "Meter Reading", "label": "Meter Reading", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 12},
        {"type": "Link", "link_type": "DocType", "link_to": "Daily Stock Register", "label": "Daily Stock Register", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 13},
        {"type": "Link", "link_type": "DocType", "link_to": "Stock Purchase Decantation", "label": "Stock Purchase Decantation", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 14},
        {"type": "Link", "link_type": "DocType", "link_to": "Trip Voucher", "label": "Trip Voucher", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 15},
        {"type": "Link", "link_type": "DocType", "link_to": "PP Supplier Master", "label": "PP Supplier Master", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 16},

        # Credit & Sales Card
        {"type": "Card Break", "label": "Credit & Sales", "icon": "octicon octicon-credit-card", "link_count": 6, "hidden": 0, "is_query_report": 0, "onboard": 0, "idx": 17},
        {"type": "Link", "link_type": "DocType", "link_to": "PP Customer", "label": "PP Customer", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 18},
        {"type": "Link", "link_type": "DocType", "link_to": "Vehicle Master", "label": "Vehicle Master", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 19},
        {"type": "Link", "link_type": "DocType", "link_to": "Credit Sale Invoice", "label": "Credit Sale Invoice", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 20},
        {"type": "Link", "link_type": "DocType", "link_to": "Payment Receipt", "label": "Payment Receipt", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 21},
        {"type": "Link", "link_type": "DocType", "link_to": "Credit Limit Ledger", "label": "Credit Limit Ledger", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 22},
        {"type": "Link", "link_type": "DocType", "link_to": "ANPR Scan Log", "label": "ANPR Scan Log", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 23},

        # Finance & HR Card
        {"type": "Card Break", "label": "Finance & HR", "icon": "octicon octicon-dollar", "link_count": 5, "hidden": 0, "is_query_report": 0, "onboard": 0, "idx": 24},
        {"type": "Link", "link_type": "DocType", "link_to": "Expense Entry", "label": "Expense Entry", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 25},
        {"type": "Link", "link_type": "DocType", "link_to": "Attendance Register", "label": "Attendance Register", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 26},
        {"type": "Link", "link_type": "DocType", "link_to": "Advance Amount", "label": "Advance Amount", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 27},
        {"type": "Link", "link_type": "DocType", "link_to": "Bank Deposit", "label": "Bank Deposit", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 28},
        {"type": "Link", "link_type": "DocType", "link_to": "Day Settlement", "label": "Day Settlement", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 29},

        # Reports Card
        {"type": "Card Break", "label": "Reports", "icon": "octicon octicon-graph", "link_count": 5, "hidden": 0, "is_query_report": 0, "onboard": 0, "idx": 30},
        {"type": "Link", "link_type": "Report", "link_to": "Daily Sales Summary", "label": "Daily Sales Summary", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 31},
        {"type": "Link", "link_type": "Report", "link_to": "Shift Settlement Report", "label": "Shift Settlement Report", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 32},
        {"type": "Link", "link_type": "Report", "link_to": "Stock Variation Report", "label": "Stock Variation Report", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 33},
        {"type": "Link", "link_type": "Report", "link_to": "Credit Customer Ageing", "label": "Credit Customer Ageing", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 34},
        {"type": "Link", "link_type": "Report", "link_to": "GST VAT Summary", "label": "GST VAT Summary", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 35},
    ]

    # Create workspace with links via ORM (proper child table save)
    ws = frappe.get_doc({
        "doctype": "Workspace",
        "label": ws_name,
        "title": ws_name,
        "module": "PP Management",
        "icon": "octicon octicon-fuel",
        "indicator_color": "orange",
        "public": 1,
        "is_hidden": 0,
        "content": content,
        "links": links,
    })
    ws.flags.with_module = True
    ws.flags.ignore_validate = True
    ws.flags.ignore_permissions = True
    ws.flags.ignore_mandatory = True
    ws.insert(ignore_permissions=True)
    frappe.db.commit()
    frappe.clear_cache()

    final_count = frappe.db.count("Workspace Link", {"parent": ws_name})
    print(f"Petrol Pump Management workspace created with {final_count} links!")


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
        os.path.dirname(os.path.dirname(__file__)), "pp_management", "fixtures"
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
            name = doc_data.get("name")
            if name and frappe.db.exists(doctype, name):
                continue
            try:
                doc = frappe.new_doc(doctype)
                doc.update(doc_data)
                doc.insert(ignore_permissions=True)
            except Exception:
                pass
