import sys
import click
import frappe
import json
import os


def get_site_from_args():
    """Extract site name from bench CLI arguments."""
    args = sys.argv
    for i, arg in enumerate(args):
        if arg == "--site" and i + 1 < len(args):
            return args[i + 1]
        if arg.startswith("--site="):
            return arg.split("=", 1)[1]
        if arg == "-s" and i + 1 < len(args):
            return args[i + 1]
    return None


@click.command("fix-workspace")
def fix_workspace():
    """Fix Petrol Pump Management workspace - delete stale entries and create fresh with all links.

    Usage: bench --site <site-name> fix-workspace
    """
    site = get_site_from_args()
    if not site:
        print("ERROR: No site specified. Usage: bench --site <site-name> fix-workspace")
        sys.exit(1)

    frappe.init(site=site)
    frappe.connect()

    print("=" * 60)
    print("  Fixing Petrol Pump Management Workspace")
    print("=" * 60)

    ws_name = "Petrol Pump Management"

    # Step 1: Delete ALL existing workspaces for this module
    print("\n[1/3] Cleaning up all existing workspace entries...")
    all_ws = frappe.db.get_all(
        "Workspace",
        filters={"module": "PP Management"},
        pluck="name",
    )
    for name in all_ws:
        frappe.db.sql("DELETE FROM `tabWorkspace Link` WHERE parent = %s", name)
        frappe.db.sql("DELETE FROM `tabWorkspace` WHERE name = %s", name)
        print(f"  Deleted: {name}")

    other_ws = frappe.db.sql(
        "SELECT name FROM `tabWorkspace` WHERE name LIKE %s OR name LIKE %s",
        ("%Petrol%", "%PP%"),
        as_dict=True,
    )
    for ws in other_ws:
        if ws.name != ws_name:
            frappe.db.sql("DELETE FROM `tabWorkspace Link` WHERE parent = %s", ws.name)
            frappe.db.sql("DELETE FROM `tabWorkspace` WHERE name = %s", ws.name)
            print(f"  Deleted stale: {ws.name}")

    frappe.db.commit()
    print("  Done!")

    # Step 2: Create workspace - load from JSON file (ERPNext format)
    print("\n[2/3] Creating workspace with all links...")

    # Try to load from the JSON file first
    ws_json_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "pp_management", "workspace", "petrol_pump_management.json"
    )

    if os.path.exists(ws_json_path):
        print(f"  Loading from JSON file: {ws_json_path}")
        with open(ws_json_path, "r") as f:
            ws_data = json.load(f)
    else:
        print(f"  JSON file not found, using hardcoded data")
        ws_data = _get_hardcoded_workspace_data()

    # Build workspace doc from JSON data
    ws = frappe.get_doc({
        "doctype": "Workspace",
        "label": ws_data["label"],
        "title": ws_data["title"],
        "module": ws_data["module"],
        "icon": ws_data.get("icon", "octicon octicon-file"),
        "indicator_color": ws_data.get("indicator_color", "blue"),
        "public": ws_data.get("public", 1),
        "is_hidden": ws_data.get("is_hidden", 0),
        "content": ws_data["content"],
        "links": ws_data["links"],
        "shortcuts": ws_data.get("shortcuts", []),
        "charts": ws_data.get("charts", []),
        "number_cards": ws_data.get("number_cards", []),
        "custom_blocks": ws_data.get("custom_blocks", []),
        "quick_lists": ws_data.get("quick_lists", []),
        "roles": ws_data.get("roles", []),
        "for_user": ws_data.get("for_user", ""),
        "parent_page": ws_data.get("parent_page", ""),
        "restrict_to_domain": ws_data.get("restrict_to_domain", ""),
        "hide_custom": ws_data.get("hide_custom", 0),
    })

    ws.flags.with_module = True
    ws.flags.ignore_links = True
    ws.flags.ignore_validate = True
    ws.flags.ignore_permissions = True
    ws.flags.ignore_mandatory = True
    ws.insert(ignore_permissions=True)
    frappe.db.commit()
    frappe.clear_cache()

    print(f"  Workspace '{ws.name}' created!")

    # Step 3: Verify
    print("\n[3/3] Verifying...")
    count = frappe.db.count("Workspace Link", {"parent": ws_name})
    exists = frappe.db.exists("Workspace", ws_name)
    print(f"  Workspace exists: {exists}")
    print(f"  Links count: {count}")

    if count > 0:
        all_links = frappe.db.get_all(
            "Workspace Link",
            filters={"parent": ws_name},
            fields=["type", "label", "link_type", "link_to"],
            order_by="idx asc",
        )
        for link in all_links:
            if link.type == "Card Break":
                print(f"\n  [{link.label}]")
            else:
                print(f"    - {link.label} ({link.link_type}: {link.link_to})")

    print("\n" + "=" * 60)
    if count > 0:
        print(f"  SUCCESS! {count} links created.")
    else:
        print("  FAILED! 0 links. Check errors above.")
    print("  Clear browser cache (Ctrl+Shift+R) and refresh.")
    print("=" * 60)

    frappe.destroy()


def _get_hardcoded_workspace_data():
    """Fallback workspace data if JSON file is not found."""
    content = json.dumps([
        {"type": "header", "data": {"text": "<span class=\"h4\"><b>Your Shortcuts</b></span>", "col": 12}},
        {"type": "shortcut", "data": {"shortcut_name": "Station Configuration", "col": 3}},
        {"type": "shortcut", "data": {"shortcut_name": "Fuel Sale", "col": 3}},
        {"type": "shortcut", "data": {"shortcut_name": "Shift", "col": 3}},
        {"type": "shortcut", "data": {"shortcut_name": "PP Customer", "col": 3}},
        {"type": "spacer", "data": {"col": 12}},
        {"type": "header", "data": {"text": "<span class=\"h4\"><b>Configuration</b></span>", "col": 12}},
        {"type": "card", "data": {"card_name": "Configuration", "col": 4}},
        {"type": "spacer", "data": {"col": 12}},
        {"type": "header", "data": {"text": "<span class=\"h4\"><b>Operations</b></span>", "col": 12}},
        {"type": "card", "data": {"card_name": "Operations", "col": 4}},
        {"type": "spacer", "data": {"col": 12}},
        {"type": "header", "data": {"text": "<span class=\"h4\"><b>Credit & Sales</b></span>", "col": 12}},
        {"type": "card", "data": {"card_name": "Credit & Sales", "col": 4}},
        {"type": "spacer", "data": {"col": 12}},
        {"type": "header", "data": {"text": "<span class=\"h4\"><b>Finance & HR</b></span>", "col": 12}},
        {"type": "card", "data": {"card_name": "Finance & HR", "col": 4}},
        {"type": "spacer", "data": {"col": 12}},
        {"type": "header", "data": {"text": "<span class=\"h4\"><b>Reports</b></span>", "col": 12}},
        {"type": "card", "data": {"card_name": "Reports", "col": 4}},
    ])

    links = [
        {"hidden": 0, "is_query_report": 0, "label": "Configuration", "link_count": 0, "onboard": 0, "type": "Card Break"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Station Configuration", "link_count": 0, "link_to": "Station Configuration", "link_type": "DocType", "onboard": 1, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Tank Master", "link_count": 0, "link_to": "Tank Master", "link_type": "DocType", "onboard": 1, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Nozzle Master", "link_count": 0, "link_to": "Nozzle Master", "link_type": "DocType", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Fuel Price Master", "link_count": 0, "link_to": "Fuel Price Master", "link_type": "DocType", "onboard": 1, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Employee Master", "link_count": 0, "link_to": "Employee Master", "link_type": "DocType", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Tank Dip Chart", "link_count": 0, "link_to": "Tank Dip Chart", "link_type": "DocType", "onboard": 0, "type": "Link"},

        {"hidden": 0, "is_query_report": 0, "label": "Operations", "link_count": 0, "onboard": 0, "type": "Card Break"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Shift", "link_count": 0, "link_to": "Shift", "link_type": "DocType", "onboard": 1, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Shift Nozzle Allotment", "link_count": 0, "link_to": "Shift Nozzle Allotment", "link_type": "DocType", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Fuel Sale", "link_count": 0, "link_to": "Fuel Sale", "link_type": "DocType", "onboard": 1, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Meter Reading", "link_count": 0, "link_to": "Meter Reading", "link_type": "DocType", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Daily Stock Register", "link_count": 0, "link_to": "Daily Stock Register", "link_type": "DocType", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Stock Purchase Decantation", "link_count": 0, "link_to": "Stock Purchase Decantation", "link_type": "DocType", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Trip Voucher", "link_count": 0, "link_to": "Trip Voucher", "link_type": "DocType", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "PP Supplier Master", "link_count": 0, "link_to": "PP Supplier Master", "link_type": "DocType", "onboard": 0, "type": "Link"},

        {"hidden": 0, "is_query_report": 0, "label": "Credit & Sales", "link_count": 0, "onboard": 0, "type": "Card Break"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "PP Customer", "link_count": 0, "link_to": "PP Customer", "link_type": "DocType", "onboard": 1, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Vehicle Master", "link_count": 0, "link_to": "Vehicle Master", "link_type": "DocType", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Credit Sale Invoice", "link_count": 0, "link_to": "Credit Sale Invoice", "link_type": "DocType", "onboard": 1, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Payment Receipt", "link_count": 0, "link_to": "Payment Receipt", "link_type": "DocType", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Credit Limit Ledger", "link_count": 0, "link_to": "Credit Limit Ledger", "link_type": "DocType", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "ANPR Scan Log", "link_count": 0, "link_to": "ANPR Scan Log", "link_type": "DocType", "onboard": 0, "type": "Link"},

        {"hidden": 0, "is_query_report": 0, "label": "Finance & HR", "link_count": 0, "onboard": 0, "type": "Card Break"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Expense Entry", "link_count": 0, "link_to": "Expense Entry", "link_type": "DocType", "onboard": 1, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Attendance Register", "link_count": 0, "link_to": "Attendance Register", "link_type": "DocType", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Advance Amount", "link_count": 0, "link_to": "Advance Amount", "link_type": "DocType", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Bank Deposit", "link_count": 0, "link_to": "Bank Deposit", "link_type": "DocType", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 0, "label": "Day Settlement", "link_count": 0, "link_to": "Day Settlement", "link_type": "DocType", "onboard": 1, "type": "Link"},

        {"hidden": 0, "is_query_report": 0, "label": "Reports", "link_count": 0, "onboard": 0, "type": "Card Break"},
        {"dependencies": "", "hidden": 0, "is_query_report": 1, "label": "Daily Sales Summary", "link_count": 0, "link_to": "Daily Sales Summary", "link_type": "Report", "onboard": 1, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 1, "label": "Shift Settlement Report", "link_count": 0, "link_to": "Shift Settlement Report", "link_type": "Report", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 1, "label": "Stock Variation Report", "link_count": 0, "link_to": "Stock Variation Report", "link_type": "Report", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 1, "label": "Credit Customer Ageing", "link_count": 0, "link_to": "Credit Customer Ageing", "link_type": "Report", "onboard": 0, "type": "Link"},
        {"dependencies": "", "hidden": 0, "is_query_report": 1, "label": "GST VAT Summary", "link_count": 0, "link_to": "GST VAT Summary", "link_type": "Report", "onboard": 0, "type": "Link"},
    ]

    shortcuts = [
        {"color": "Green", "label": "Station Configuration", "link_to": "Station Configuration", "type": "DocType"},
        {"color": "Green", "label": "Fuel Sale", "link_to": "Fuel Sale", "type": "DocType"},
        {"color": "Green", "label": "Shift", "link_to": "Shift", "type": "DocType"},
        {"color": "Green", "label": "PP Customer", "link_to": "PP Customer", "type": "DocType"},
    ]

    return {
        "label": ws_name,
        "title": ws_name,
        "module": "PP Management",
        "icon": "octicon octicon-fuel",
        "indicator_color": "orange",
        "public": 1,
        "is_hidden": 0,
        "content": content,
        "links": links,
        "shortcuts": shortcuts,
        "charts": [],
        "number_cards": [],
        "custom_blocks": [],
        "quick_lists": [],
        "roles": [],
        "for_user": "",
        "parent_page": "",
        "restrict_to_domain": "",
        "hide_custom": 0,
    }
