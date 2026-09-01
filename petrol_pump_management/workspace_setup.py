import frappe
import json
from frappe.utils import now_datetime


def execute():
    """Create workspace with all links. Run via:
    bench --site <site> execute petrol_pump_management.workspace_setup
    """
    ws_name = "Petrol Pump Management"
    now = str(now_datetime())

    # Delete old workspaces
    for old in ["PP Management", ws_name]:
        if frappe.db.exists("Workspace", old):
            frappe.delete_doc("Workspace", old, force=True, ignore_missing=True)
    frappe.db.commit()

    # Get actual columns
    ws_cols = [r[0] for r in frappe.db.sql("SHOW COLUMNS FROM `tabWorkspace`")]
    link_cols = [r[0] for r in frappe.db.sql("SHOW COLUMNS FROM `tabWorkspace Link`")]

    # Build content JSON - cards layout referencing the card names
    card_names = ["Configuration", "Operations", "Credit & Sales", "Finance & HR", "Reports"]
    content = json.dumps([
        {"id": "shortcuts_section", "type": "header", "data": {"text": "Shortcuts", "level": "h2"}},
    ] + [
        {"id": f"card_{i}", "type": "card", "data": {"card_name": name, "col": 4}}
        for i, name in enumerate(card_names)
    ])

    # Build workspace record
    ws_values = {
        "name": ws_name,
        "label": ws_name,
        "title": ws_name,
        "module": "PP Management",
        "icon": "octicon octicon-fuel",
        "indicator_color": "orange",
        "public": 1,
        "is_hidden": 0,
        "content": content,
        "type": "Workspace",
        "docstatus": 0,
        "owner": "Administrator",
        "modified_by": "Administrator",
        "modified": now,
        "creation": now,
    }
    safe_ws = {k: v for k, v in ws_values.items() if k in ws_cols}
    ws_col_names = ", ".join([f"`{k}`" for k in safe_ws.keys()])
    ws_placeholders = ", ".join(["%s"] * len(safe_ws))
    frappe.db.sql(
        f"INSERT INTO `tabWorkspace` ({ws_col_names}) VALUES ({ws_placeholders})",
        list(safe_ws.values()),
    )
    frappe.db.commit()

    # Links data: (type, link_type, link_to, label, hidden, is_query_report)
    # CRITICAL: "type" = Card Break or Link
    #           "link_type" = DocType or Report (only for type="Link")
    links_data = [
        # --- Configuration ---
        ("Card Break", None, None, "Configuration", 0, 0),
        ("Link", "DocType", "Station Configuration", "Station Configuration", 0, 0),
        ("Link", "DocType", "Tank Master", "Tank Master", 0, 0),
        ("Link", "DocType", "Nozzle Master", "Nozzle Master", 0, 0),
        ("Link", "DocType", "Fuel Price Master", "Fuel Price Master", 0, 0),
        ("Link", "DocType", "Employee Master", "Employee Master", 0, 0),
        ("Link", "DocType", "Tank Dip Chart", "Tank Dip Chart", 0, 0),
        # --- Operations ---
        ("Card Break", None, None, "Operations", 0, 0),
        ("Link", "DocType", "Shift", "Shift", 0, 0),
        ("Link", "DocType", "Shift Nozzle Allotment", "Shift Nozzle Allotment", 0, 0),
        ("Link", "DocType", "Fuel Sale", "Fuel Sale", 0, 0),
        ("Link", "DocType", "Meter Reading", "Meter Reading", 0, 0),
        ("Link", "DocType", "Daily Stock Register", "Daily Stock Register", 0, 0),
        ("Link", "DocType", "Stock Purchase Decantation", "Stock Purchase Decantation", 0, 0),
        ("Link", "DocType", "Trip Voucher", "Trip Voucher", 0, 0),
        ("Link", "DocType", "PP Supplier Master", "PP Supplier Master", 0, 0),
        # --- Credit & Sales ---
        ("Card Break", None, None, "Credit & Sales", 0, 0),
        ("Link", "DocType", "PP Customer", "PP Customer", 0, 0),
        ("Link", "DocType", "Vehicle Master", "Vehicle Master", 0, 0),
        ("Link", "DocType", "Credit Sale Invoice", "Credit Sale Invoice", 0, 0),
        ("Link", "DocType", "Payment Receipt", "Payment Receipt", 0, 0),
        ("Link", "DocType", "Credit Limit Ledger", "Credit Limit Ledger", 0, 0),
        ("Link", "DocType", "ANPR Scan Log", "ANPR Scan Log", 0, 0),
        # --- Finance & HR ---
        ("Card Break", None, None, "Finance & HR", 0, 0),
        ("Link", "DocType", "Expense Entry", "Expense Entry", 0, 0),
        ("Link", "DocType", "Attendance Register", "Attendance Register", 0, 0),
        ("Link", "DocType", "Advance Amount", "Advance Amount", 0, 0),
        ("Link", "DocType", "Bank Deposit", "Bank Deposit", 0, 0),
        ("Link", "DocType", "Day Settlement", "Day Settlement", 0, 0),
        # --- Reports ---
        ("Card Break", None, None, "Reports", 0, 0),
        ("Link", "Report", "Daily Sales Summary", "Daily Sales Summary", 0, 1),
        ("Link", "Report", "Shift Settlement Report", "Shift Settlement Report", 0, 1),
        ("Link", "Report", "Stock Variation Report", "Stock Variation Report", 0, 1),
        ("Link", "Report", "Credit Customer Ageing", "Credit Customer Ageing", 0, 1),
        ("Link", "Report", "GST VAT Summary", "GST VAT Summary", 0, 1),
    ]

    for idx, (link_type, ltype, link_to, label, hidden, is_qr) in enumerate(links_data):
        link_values = {
            "name": f"{ws_name}-{idx + 1}",
            "parent": ws_name,
            "parenttype": "Workspace",
            "parentfield": "links",
            "idx": idx + 1,
            "type": link_type,           # "Card Break" or "Link"
            "label": label,
            "link_type": ltype,          # "DocType" or "Report" (None for Card Break)
            "link_to": link_to,          # DocType/Report name (None for Card Break)
            "hidden": hidden,
            "is_query_report": is_qr,
            "docstatus": 0,
            "owner": "Administrator",
            "modified_by": "Administrator",
            "modified": now,
            "creation": now,
        }
        safe_link = {k: v for k, v in link_values.items() if v is not None and k in link_cols}
        lcol_names = ", ".join([f"`{k}`" for k in safe_link.keys()])
        lplaceholders = ", ".join(["%s"] * len(safe_link))
        frappe.db.sql(
            f"INSERT INTO `tabWorkspace Link` ({lcol_names}) VALUES ({lplaceholders})",
            list(safe_link.values()),
        )

    frappe.db.commit()
    frappe.clear_cache()
    print(f"Workspace '{ws_name}' created with {len(links_data)} link entries!")
    print("Card sections:", card_names)
