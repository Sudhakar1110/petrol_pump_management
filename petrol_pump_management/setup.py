import frappe
import os
import json


def after_install():
    """Setup after app installation."""
    create_roles()
    import_fixtures()
    frappe.db.commit()


def after_migrate():
    """After migration - ensure workspace exists with all links using direct SQL."""
    _ensure_workspace()


def _ensure_workspace():
    """Create workspace with all links using direct SQL. Idempotent - skips if already done."""
    ws_name = "Petrol Pump Management"

    # Check if workspace already has links - if so, skip
    count = frappe.db.count("Workspace Link", {"parent": ws_name})
    if count > 0:
        return

    now = frappe.utils.now_datetime()

    # Delete any empty/broken workspace entries
    for name in frappe.db.get_all("Workspace", filters={"module": "PP Management"}, pluck="name"):
        frappe.db.sql("DELETE FROM `tabWorkspace Link` WHERE parent = %s", name)
        frappe.db.sql("DELETE FROM `tabWorkspace` WHERE name = %s", name)

    for row in frappe.db.sql(
        "SELECT name FROM `tabWorkspace` WHERE name LIKE %s OR name LIKE %s",
        ("%Petrol%", "%PP%"), as_dict=True,
    ):
        if row.name != ws_name:
            frappe.db.sql("DELETE FROM `tabWorkspace Link` WHERE parent = %s", row.name)
            frappe.db.sql("DELETE FROM `tabWorkspace` WHERE name = %s", row.name)

    frappe.db.commit()

    content = json.dumps([
        {"type": "header", "data": {"text": "Your Shortcuts", "level": 4, "col": 12}},
        {"type": "spacer", "data": {"col": 12}},
        {"type": "card", "data": {"card_name": "Configuration", "col": 4}},
        {"type": "spacer", "data": {"col": 12}},
        {"type": "card", "data": {"card_name": "Operations", "col": 4}},
        {"type": "spacer", "data": {"col": 12}},
        {"type": "card", "data": {"card_name": "Credit & Sales", "col": 4}},
        {"type": "spacer", "data": {"col": 12}},
        {"type": "card", "data": {"card_name": "Finance & HR", "col": 4}},
        {"type": "spacer", "data": {"col": 12}},
        {"type": "card", "data": {"card_name": "Reports", "col": 4}},
    ])

    frappe.db.sql("""
        INSERT INTO `tabWorkspace`
        (name, creation, modified, owner, modified_by, docstatus, idx,
         module, label, title, icon, indicator_color,
         public, is_hidden, content)
        VALUES (%s, %s, %s, %s, %s, 0, 0,
         %s, %s, %s, %s, %s,
         1, 0, %s)
    """, (
        ws_name, now, now, "Administrator", "Administrator",
        "PP Management", ws_name, ws_name,
        "octicon octicon-fuel", "orange",
        content,
    ))

    links_data = [
        ("Card Break", "Configuration", "", "", 0, 0, "octicon octicon-gear", 1),
        ("Link", "Station Configuration", "DocType", "Station Configuration", 0, 0, "", 2),
        ("Link", "Tank Master", "DocType", "Tank Master", 0, 0, "", 3),
        ("Link", "Nozzle Master", "DocType", "Nozzle Master", 0, 0, "", 4),
        ("Link", "Fuel Price Master", "DocType", "Fuel Price Master", 0, 0, "", 5),
        ("Link", "Employee Master", "DocType", "Employee Master", 0, 0, "", 6),
        ("Link", "Tank Dip Chart", "DocType", "Tank Dip Chart", 0, 0, "", 7),
        ("Card Break", "Operations", "", "", 0, 0, "octicon octicon-gear", 8),
        ("Link", "Shift", "DocType", "Shift", 0, 0, "", 9),
        ("Link", "Shift Nozzle Allotment", "DocType", "Shift Nozzle Allotment", 0, 0, "", 10),
        ("Link", "Fuel Sale", "DocType", "Fuel Sale", 0, 0, "", 11),
        ("Link", "Meter Reading", "DocType", "Meter Reading", 0, 0, "", 12),
        ("Link", "Daily Stock Register", "DocType", "Daily Stock Register", 0, 0, "", 13),
        ("Link", "Stock Purchase Decantation", "DocType", "Stock Purchase Decantation", 0, 0, "", 14),
        ("Link", "Trip Voucher", "DocType", "Trip Voucher", 0, 0, "", 15),
        ("Link", "PP Supplier Master", "DocType", "PP Supplier Master", 0, 0, "", 16),
        ("Card Break", "Credit & Sales", "", "", 0, 0, "octicon octicon-credit-card", 17),
        ("Link", "PP Customer", "DocType", "PP Customer", 0, 0, "", 18),
        ("Link", "Vehicle Master", "DocType", "Vehicle Master", 0, 0, "", 19),
        ("Link", "Credit Sale Invoice", "DocType", "Credit Sale Invoice", 0, 0, "", 20),
        ("Link", "Payment Receipt", "DocType", "Payment Receipt", 0, 0, "", 21),
        ("Link", "Credit Limit Ledger", "DocType", "Credit Limit Ledger", 0, 0, "", 22),
        ("Link", "ANPR Scan Log", "DocType", "ANPR Scan Log", 0, 0, "", 23),
        ("Card Break", "Finance & HR", "", "", 0, 0, "octicon octicon-dollar", 24),
        ("Link", "Expense Entry", "DocType", "Expense Entry", 0, 0, "", 25),
        ("Link", "Attendance Register", "DocType", "Attendance Register", 0, 0, "", 26),
        ("Link", "Advance Amount", "DocType", "Advance Amount", 0, 0, "", 27),
        ("Link", "Bank Deposit", "DocType", "Bank Deposit", 0, 0, "", 28),
        ("Link", "Day Settlement", "DocType", "Day Settlement", 0, 0, "", 29),
        ("Card Break", "Reports", "", "", 0, 0, "octicon octicon-graph", 30),
        ("Link", "Daily Sales Summary", "Report", "Daily Sales Summary", 0, 1, "", 31),
        ("Link", "Shift Settlement Report", "Report", "Shift Settlement Report", 0, 1, "", 32),
        ("Link", "Stock Variation Report", "Report", "Stock Variation Report", 0, 1, "", 33),
        ("Link", "Credit Customer Ageing", "Report", "Credit Customer Ageing", 0, 1, "", 34),
        ("Link", "GST VAT Summary", "Report", "GST VAT Summary", 0, 1, "", 35),
    ]

    for ltype, label, lt, lto, hidden, iqr, icon, idx in links_data:
        frappe.db.sql("""
            INSERT INTO `tabWorkspace Link`
            (name, creation, modified, owner, modified_by, parent, parentfield, parenttype,
             docstatus, idx, type, label, link_type, link_to, hidden, is_query_report,
             onboard, dependencies, link_count, icon)
            VALUES (%s, %s, %s, %s, %s, %s, 'links', 'Workspace',
             0, %s, %s, %s, %s, %s, %s, %s, 0, '', 0, %s)
        """, (
            frappe.utils.cstr(frappe.utils.random_string(8)),
            now, now, "Administrator", "Administrator",
            ws_name, idx,
            ltype, label, lt, lto, hidden, iqr, icon,
        ))

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
