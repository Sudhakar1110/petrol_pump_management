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
    """Fix Petrol Pump Management workspace from browser.

    Open this URL in your browser to fix the workspace:
    /api/method/petrol_pump_management.api.fix_workspace
    """
    ws_name = "Petrol Pump Management"
    results = []

    # Step 1: Delete ALL existing workspaces for this module
    all_ws = frappe.db.get_all(
        "Workspace",
        filters={"module": "PP Management"},
        pluck="name",
    )
    for name in all_ws:
        frappe.db.sql("DELETE FROM `tabWorkspace Link` WHERE parent = %s", name)
        frappe.db.sql("DELETE FROM `tabWorkspace` WHERE name = %s", name)
        results.append(f"Deleted workspace: {name}")

    # Also clean partial matches
    other_ws = frappe.db.sql(
        "SELECT name FROM `tabWorkspace` WHERE name LIKE %s OR name LIKE %s",
        ("%Petrol%", "%PP%"),
        as_dict=True,
    )
    for ws in other_ws:
        if ws.name != ws_name:
            frappe.db.sql("DELETE FROM `tabWorkspace Link` WHERE parent = %s", ws.name)
            frappe.db.sql("DELETE FROM `tabWorkspace` WHERE name = %s", ws.name)
            results.append(f"Deleted stale: {ws.name}")

    frappe.db.commit()

    # Step 2: Create workspace with all links
    links = [
        {"type": "Card Break", "label": "Configuration", "icon": "octicon octicon-gear", "link_count": 6, "hidden": 0, "is_query_report": 0, "onboard": 0, "idx": 1},
        {"type": "Link", "link_type": "DocType", "link_to": "Station Configuration", "label": "Station Configuration", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 2},
        {"type": "Link", "link_type": "DocType", "link_to": "Tank Master", "label": "Tank Master", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 3},
        {"type": "Link", "link_type": "DocType", "link_to": "Nozzle Master", "label": "Nozzle Master", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 4},
        {"type": "Link", "link_type": "DocType", "link_to": "Fuel Price Master", "label": "Fuel Price Master", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 5},
        {"type": "Link", "link_type": "DocType", "link_to": "Employee Master", "label": "Employee Master", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 6},
        {"type": "Link", "link_type": "DocType", "link_to": "Tank Dip Chart", "label": "Tank Dip Chart", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 7},

        {"type": "Card Break", "label": "Operations", "icon": "octicon octicon-gear", "link_count": 8, "hidden": 0, "is_query_report": 0, "onboard": 0, "idx": 8},
        {"type": "Link", "link_type": "DocType", "link_to": "Shift", "label": "Shift", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 9},
        {"type": "Link", "link_type": "DocType", "link_to": "Shift Nozzle Allotment", "label": "Shift Nozzle Allotment", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 10},
        {"type": "Link", "link_type": "DocType", "link_to": "Fuel Sale", "label": "Fuel Sale", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 11},
        {"type": "Link", "link_type": "DocType", "link_to": "Meter Reading", "label": "Meter Reading", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 12},
        {"type": "Link", "link_type": "DocType", "link_to": "Daily Stock Register", "label": "Daily Stock Register", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 13},
        {"type": "Link", "link_type": "DocType", "link_to": "Stock Purchase Decantation", "label": "Stock Purchase Decantation", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 14},
        {"type": "Link", "link_type": "DocType", "link_to": "Trip Voucher", "label": "Trip Voucher", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 15},
        {"type": "Link", "link_type": "DocType", "link_to": "PP Supplier Master", "label": "PP Supplier Master", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 16},

        {"type": "Card Break", "label": "Credit & Sales", "icon": "octicon octicon-credit-card", "link_count": 6, "hidden": 0, "is_query_report": 0, "onboard": 0, "idx": 17},
        {"type": "Link", "link_type": "DocType", "link_to": "PP Customer", "label": "PP Customer", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 18},
        {"type": "Link", "link_type": "DocType", "link_to": "Vehicle Master", "label": "Vehicle Master", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 19},
        {"type": "Link", "link_type": "DocType", "link_to": "Credit Sale Invoice", "label": "Credit Sale Invoice", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 20},
        {"type": "Link", "link_type": "DocType", "link_to": "Payment Receipt", "label": "Payment Receipt", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 21},
        {"type": "Link", "link_type": "DocType", "link_to": "Credit Limit Ledger", "label": "Credit Limit Ledger", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 22},
        {"type": "Link", "link_type": "DocType", "link_to": "ANPR Scan Log", "label": "ANPR Scan Log", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 23},

        {"type": "Card Break", "label": "Finance & HR", "icon": "octicon octicon-dollar", "link_count": 5, "hidden": 0, "is_query_report": 0, "onboard": 0, "idx": 24},
        {"type": "Link", "link_type": "DocType", "link_to": "Expense Entry", "label": "Expense Entry", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 25},
        {"type": "Link", "link_type": "DocType", "link_to": "Attendance Register", "label": "Attendance Register", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 26},
        {"type": "Link", "link_type": "DocType", "link_to": "Advance Amount", "label": "Advance Amount", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 27},
        {"type": "Link", "link_type": "DocType", "link_to": "Bank Deposit", "label": "Bank Deposit", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 28},
        {"type": "Link", "link_type": "DocType", "link_to": "Day Settlement", "label": "Day Settlement", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 29},

        {"type": "Card Break", "label": "Reports", "icon": "octicon octicon-graph", "link_count": 5, "hidden": 0, "is_query_report": 0, "onboard": 0, "idx": 30},
        {"type": "Link", "link_type": "Report", "link_to": "Daily Sales Summary", "label": "Daily Sales Summary", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 31},
        {"type": "Link", "link_type": "Report", "link_to": "Shift Settlement Report", "label": "Shift Settlement Report", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 32},
        {"type": "Link", "link_type": "Report", "link_to": "Stock Variation Report", "label": "Stock Variation Report", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 33},
        {"type": "Link", "link_type": "Report", "link_to": "Credit Customer Ageing", "label": "Credit Customer Ageing", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 34},
        {"type": "Link", "link_type": "Report", "link_to": "GST VAT Summary", "label": "GST VAT Summary", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0, "idx": 35},
    ]

    content = json.dumps([
        {"type": "header", "data": {"text": "Your Shortcuts", "level": 4, "col": 12}},
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
    ws.flags.ignore_links = True
    ws.flags.ignore_validate = True
    ws.flags.ignore_permissions = True
    ws.flags.ignore_mandatory = True
    ws.insert(ignore_permissions=True)
    frappe.db.commit()
    frappe.clear_cache()

    results.append(f"Workspace '{ws.name}' created!")

    # Verify
    count = frappe.db.count("Workspace Link", {"parent": ws_name})
    results.append(f"Links count: {count}")

    return {
        "success": count > 0,
        "links_count": count,
        "message": "\n".join(results),
    }
