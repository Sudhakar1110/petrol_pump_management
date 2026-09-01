import frappe
import json
from frappe.utils import now_datetime


def execute():
    """Create workspace with all links.
    Run via: bench --site <site> execute petrol_pump_management.workspace_setup
    """
    ws_name = "Petrol Pump Management"
    now = str(now_datetime())

    # Step 1: Clean up ALL existing workspaces for this module
    existing = frappe.get_all("Workspace", filters={"module": "PP Management"}, pluck="name")
    for old_name in existing:
        frappe.delete_doc("Workspace", old_name, force=True, ignore_missing=True)

    # Also delete customizations
    frappe.db.sql("DELETE FROM `tabCustom Workspace` WHERE reference_name = %s", ws_name)
    frappe.db.commit()

    # Step 2: Get the actual column names from tabWorkspace
    ws_cols = set(r[0] for r in frappe.db.sql("SHOW COLUMNS FROM `tabWorkspace`"))

    # Step 3: Build content JSON
    card_names = ["Configuration", "Operations", "Credit & Sales", "Finance & HR", "Reports"]
    content = json.dumps([
        {"type": "header", "data": {"text": ws_name, "level": "h2"}},
    ] + [
        {"type": "card", "data": {"card_name": cn, "col": 4}} for cn in card_names
    ])

    # Step 4: Insert workspace using only columns that exist
    ws_data = {}
    ws_map = {
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
    for k, v in ws_map.items():
        if k in ws_cols:
            ws_data[k] = v

    cols_str = ", ".join([f"`{k}`" for k in ws_data])
    phs_str = ", ".join(["%s"] * len(ws_data))
    frappe.db.sql(f"INSERT INTO `tabWorkspace` ({cols_str}) VALUES ({phs_str})", list(ws_data.values()))
    frappe.db.commit()

    # Step 5: Get Workspace Link columns
    link_cols = set(r[0] for r in frappe.db.sql("SHOW COLUMNS FROM `tabWorkspace Link`"))

    # Step 6: Insert links - CRITICAL: 'type' field = Card Break or Link
    #         'link_type' field = DocType or Report
    links = [
        # Card Break, link_type, link_to, label, hidden, is_query_report, icon
        ("Card Break", None, None, "Configuration", 0, 0, "octicon octicon-gear"),
        ("Link", "DocType", "Station Configuration", "Station Configuration", 0, 0, None),
        ("Link", "DocType", "Tank Master", "Tank Master", 0, 0, None),
        ("Link", "DocType", "Nozzle Master", "Nozzle Master", 0, 0, None),
        ("Link", "DocType", "Fuel Price Master", "Fuel Price Master", 0, 0, None),
        ("Link", "DocType", "Employee Master", "Employee Master", 0, 0, None),
        ("Link", "DocType", "Tank Dip Chart", "Tank Dip Chart", 0, 0, None),

        ("Card Break", None, None, "Operations", 0, 0, "octicon octicon-gear"),
        ("Link", "DocType", "Shift", "Shift", 0, 0, None),
        ("Link", "DocType", "Shift Nozzle Allotment", "Shift Nozzle Allotment", 0, 0, None),
        ("Link", "DocType", "Fuel Sale", "Fuel Sale", 0, 0, None),
        ("Link", "DocType", "Meter Reading", "Meter Reading", 0, 0, None),
        ("Link", "DocType", "Daily Stock Register", "Daily Stock Register", 0, 0, None),
        ("Link", "DocType", "Stock Purchase Decantation", "Stock Purchase Decantation", 0, 0, None),
        ("Link", "DocType", "Trip Voucher", "Trip Voucher", 0, 0, None),
        ("Link", "DocType", "PP Supplier Master", "PP Supplier Master", 0, 0, None),

        ("Card Break", None, None, "Credit & Sales", 0, 0, "octicon octicon-credit-card"),
        ("Link", "DocType", "PP Customer", "PP Customer", 0, 0, None),
        ("Link", "DocType", "Vehicle Master", "Vehicle Master", 0, 0, None),
        ("Link", "DocType", "Credit Sale Invoice", "Credit Sale Invoice", 0, 0, None),
        ("Link", "DocType", "Payment Receipt", "Payment Receipt", 0, 0, None),
        ("Link", "DocType", "Credit Limit Ledger", "Credit Limit Ledger", 0, 0, None),
        ("Link", "DocType", "ANPR Scan Log", "ANPR Scan Log", 0, 0, None),

        ("Card Break", None, None, "Finance & HR", 0, 0, "octicon octicon-dollar"),
        ("Link", "DocType", "Expense Entry", "Expense Entry", 0, 0, None),
        ("Link", "DocType", "Attendance Register", "Attendance Register", 0, 0, None),
        ("Link", "DocType", "Advance Amount", "Advance Amount", 0, 0, None),
        ("Link", "DocType", "Bank Deposit", "Bank Deposit", 0, 0, None),
        ("Link", "DocType", "Day Settlement", "Day Settlement", 0, 0, None),

        ("Card Break", None, None, "Reports", 0, 0, "octicon octicon-graph"),
        ("Link", "Report", "Daily Sales Summary", "Daily Sales Summary", 0, 1, None),
        ("Link", "Report", "Shift Settlement Report", "Shift Settlement Report", 0, 1, None),
        ("Link", "Report", "Stock Variation Report", "Stock Variation Report", 0, 1, None),
        ("Link", "Report", "Credit Customer Ageing", "Credit Customer Ageing", 0, 1, None),
        ("Link", "Report", "GST VAT Summary", "GST VAT Summary", 0, 1, None),
    ]

    for idx, (ltype, link_type, link_to, label, hidden, is_qr, icon) in enumerate(links):
        # Build link values - only use columns that actually exist
        row = {
            "name": f"{ws_name}-{idx + 1}",
            "parent": ws_name,
            "parenttype": "Workspace",
            "parentfield": "links",
            "idx": idx + 1,
            "type": ltype,              # "Card Break" or "Link"
            "label": label,
            "hidden": hidden,
            "docstatus": 0,
            "owner": "Administrator",
            "modified_by": "Administrator",
            "modified": now,
            "creation": now,
        }
        # Only add link_type/link_to/icon for actual links
        if ltype == "Link":
            row["link_type"] = link_type
            row["link_to"] = link_to
            row["is_query_report"] = is_qr
        elif icon:
            row["icon"] = icon

        safe_row = {k: v for k, v in row.items() if v is not None and k in link_cols}
        lc = ", ".join([f"`{k}`" for k in safe_row])
        lp = ", ".join(["%s"] * len(safe_row))
        frappe.db.sql(f"INSERT INTO `tabWorkspace Link` ({lc}) VALUES ({lp})", list(safe_row.values()))

    frappe.db.commit()

    # Step 7: Verify
    count = frappe.db.count("Workspace Link", {"parent": ws_name})
    frappe.clear_cache()
    print(f"Workspace '{ws_name}' created successfully with {count} links!")
