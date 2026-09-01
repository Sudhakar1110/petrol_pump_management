import frappe
import json


@frappe.whitelist()
def get_fuel_rate(fuel_type):
    rate = frappe.get_all("Fuel Price Master", filters={"fuel_type": fuel_type, "is_active": 1}, limit=1, fields=["rate_per_litre"])
    return {"rate": rate[0].rate_per_litre if rate else 0}


@frappe.whitelist()
def get_customer_credit_balance(customer):
    doc = frappe.get_doc("PP Customer", customer)
    return {"customer": customer, "credit_limit": doc.credit_limit, "credit_points": doc.credit_points, "is_blocked": doc.is_blocked}


@frappe.whitelist(allow_guest=True)
def fix_workspace():
    """Fix Petrol Pump Management workspace.

    Open: /api/method/petrol_pump_management.api.fix_workspace
    """
    ws_name = "Petrol Pump Management"
    now = frappe.utils.now_datetime()
    results = []

    # Step 1: Delete ALL existing workspaces for this module
    all_ws = frappe.db.get_all(
        "Workspace", filters={"module": "PP Management"}, pluck="name",
    )
    for name in all_ws:
        frappe.db.sql("DELETE FROM `tabWorkspace Link` WHERE parent = %s", name)
        frappe.db.sql("DELETE FROM `tabWorkspace` WHERE name = %s", name)
        results.append(f"Deleted: {name}")

    for row in frappe.db.sql(
        "SELECT name FROM `tabWorkspace` WHERE name LIKE %s OR name LIKE %s",
        ("%Petrol%", "%PP%"), as_dict=True,
    ):
        if row.name != ws_name:
            frappe.db.sql("DELETE FROM `tabWorkspace Link` WHERE parent = %s", row.name)
            frappe.db.sql("DELETE FROM `tabWorkspace` WHERE name = %s", row.name)
            results.append(f"Deleted stale: {row.name}")

    frappe.db.commit()

    # Step 2: Create workspace via ORM (avoids column issues)
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

    # Create workspace via ORM (no raw SQL for parent - avoids column issues)
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
    })
    ws.flags.with_module = True
    ws.flags.ignore_links = True
    ws.flags.ignore_validate = True
    ws.flags.ignore_permissions = True
    ws.flags.ignore_mandatory = True
    ws.insert(ignore_permissions=True)
    frappe.db.commit()
    results.append(f"Workspace '{ws.name}' created via ORM.")

    # Step 3: Insert links via raw SQL (child table DOES have 'type' column)
    for ltype, label, link_type, link_to, hidden, is_query_report, icon, idx in links_data:
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
            ltype, label, link_type, link_to, hidden, is_query_report, icon,
        ))

    frappe.db.commit()

    # Step 4: Verify
    count = frappe.db.count("Workspace Link", {"parent": ws_name})
    results.append(f"Links count: {count}")
    frappe.clear_cache()

    return {
        "success": count > 0,
        "links_count": count,
        "message": "\n".join(results),
    }
