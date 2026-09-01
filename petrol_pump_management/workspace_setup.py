import frappe
import json


def execute():
    """Create workspace with all links. Run via:
    bench --site pp.bizaxl.local execute petrol_pump_management.workspace_setup
    """
    ws_name = "Petrol Pump Management"
    now = str(frappe.utils.now_datetime())

    # Delete old workspaces
    for old in ["PP Management", ws_name]:
        if frappe.db.exists("Workspace", old):
            frappe.delete_doc("Workspace", old, force=True, ignore_missing=True)
    frappe.db.commit()

    content = json.dumps([
        {"id": "c1", "type": "card", "data": {"card_name": "Configuration", "col": 4}},
        {"id": "c2", "type": "card", "data": {"card_name": "Operations", "col": 4}},
        {"id": "c3", "type": "card", "data": {"card_name": "Credit & Sales", "col": 4}},
        {"id": "c4", "type": "card", "data": {"card_name": "Finance & HR", "col": 4}},
        {"id": "c5", "type": "card", "data": {"card_name": "Reports", "col": 4}},
    ])

    # Get actual columns of tabWorkspace
    cols = [r[0] for r in frappe.db.sql("SHOW COLUMNS FROM `tabWorkspace`")]
    print("Workspace columns:", cols)

    # Build safe values dict with only columns that exist
    values = {
        "name": ws_name,
        "label": ws_name,
        "title": "Petrol Pump Management",
        "module": "PP Management",
        "icon": "fuel",
        "indicator_color": "green",
        "public": 1,
        "is_hidden": 0,
        "content": content,
        "docstatus": 0,
        "owner": "Administrator",
        "modified_by": "Administrator",
        "modified": now,
        "creation": now,
    }

    # Only include columns that actually exist
    safe_values = {k: v for k, v in values.items() if k in cols}

    col_names = ", ".join([f"`{k}`" for k in safe_values.keys()])
    placeholders = ", ".join(["%s"] * len(safe_values))

    frappe.db.sql(
        f"INSERT INTO `tabWorkspace` ({col_names}) VALUES ({placeholders})",
        list(safe_values.values())
    )
    frappe.db.commit()

    # Get actual columns of tabWorkspace Link
    link_cols = [r[0] for r in frappe.db.sql("SHOW COLUMNS FROM `tabWorkspace Link`")]
    print("Workspace Link columns:", link_cols)

    links_data = [
        ("Card Break", "", "Configuration", 0, 0),
        ("Link", "Station Configuration", "Station Configuration", 0, 0),
        ("Link", "Tank Master", "Tank Master", 0, 0),
        ("Link", "Nozzle Master", "Nozzle Master", 0, 0),
        ("Link", "Fuel Price Master", "Fuel Price Master", 0, 0),
        ("Link", "Employee Master", "Employee Master", 0, 0),
        ("Link", "Tank Dip Chart", "Tank Dip Chart", 0, 0),
        ("Card Break", "", "Operations", 0, 0),
        ("Link", "Shift", "Shift", 0, 0),
        ("Link", "Shift Nozzle Allotment", "Shift Nozzle Allotment", 0, 0),
        ("Link", "Fuel Sale", "Fuel Sale", 0, 0),
        ("Link", "Meter Reading", "Meter Reading", 0, 0),
        ("Link", "Daily Stock Register", "Daily Stock Register", 0, 0),
        ("Link", "Stock Purchase Decantation", "Stock Purchase Decantation", 0, 0),
        ("Link", "Trip Voucher", "Trip Voucher", 0, 0),
        ("Link", "PP Supplier Master", "PP Supplier Master", 0, 0),
        ("Card Break", "", "Credit & Sales", 0, 0),
        ("Link", "PP Customer", "PP Customer", 0, 0),
        ("Link", "Vehicle Master", "Vehicle Master", 0, 0),
        ("Link", "Credit Sale Invoice", "Credit Sale Invoice", 0, 0),
        ("Link", "Payment Receipt", "Payment Receipt", 0, 0),
        ("Link", "Credit Limit Ledger", "Credit Limit Ledger", 0, 0),
        ("Link", "ANPR Scan Log", "ANPR Scan Log", 0, 0),
        ("Card Break", "", "Finance & HR", 0, 0),
        ("Link", "Expense Entry", "Expense Entry", 0, 0),
        ("Link", "Attendance Register", "Attendance Register", 0, 0),
        ("Link", "Advance Amount", "Advance Amount", 0, 0),
        ("Link", "Bank Deposit", "Bank Deposit", 0, 0),
        ("Link", "Day Settlement", "Day Settlement", 0, 0),
        ("Card Break", "", "Reports", 0, 0),
        ("Link", "Daily Sales Summary", "Daily Sales Summary", 0, 1),
        ("Link", "Shift Settlement Report", "Shift Settlement Report", 0, 1),
        ("Link", "Stock Variation Report", "Stock Variation Report", 0, 1),
        ("Link", "Credit Customer Ageing", "Credit Customer Ageing", 0, 1),
        ("Link", "GST VAT Summary", "GST VAT Summary", 0, 1),
    ]

    for idx, (link_type, link_to, label, hidden, is_query_report) in enumerate(links_data):
        link_values = {
            "name": f"{ws_name}-{idx}",
            "parent": ws_name,
            "parenttype": "Workspace",
            "parentfield": "links",
            "idx": idx + 1,
            "link_type": link_type,
            "link_to": link_to,
            "label": label,
            "hidden": hidden,
            "is_query_report": is_query_report,
            "docstatus": 0,
            "owner": "Administrator",
            "modified_by": "Administrator",
            "modified": now,
            "creation": now,
        }

        safe_link = {k: v for k, v in link_values.items() if k in link_cols}
        lcol_names = ", ".join([f"`{k}`" for k in safe_link.keys()])
        lplaceholders = ", ".join(["%s"] * len(safe_link))

        frappe.db.sql(
            f"INSERT INTO `tabWorkspace Link` ({lcol_names}) VALUES ({lplaceholders})",
            list(safe_link.values())
        )

    frappe.db.commit()
    frappe.clear_cache()
    print("Workspace 'Petrol Pump Management' created with", len(links_data), "links!")
