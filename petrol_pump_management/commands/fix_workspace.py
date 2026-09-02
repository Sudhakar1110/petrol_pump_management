import click
import frappe
import json


@click.command("fix-workspace")
@click.pass_context
def fix_workspace(ctx):
    """Fix Petrol Pump Management workspace - delete stale entries and create fresh with all links.

    Usage: bench --site <site-name> fix-workspace
    """
    site = ctx.obj.site if ctx.obj else None
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

    # Also clean up any partial matches
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

    # Step 2: Create workspace
    print("\n[2/3] Creating workspace with all links...")

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

    print(f"  Workspace '{ws.name}' created!")

    # Step 3: Verify
    print("\n[3/3] Verifying...")
    count = frappe.db.count("Workspace Link", {"parent": ws_name})
    exists = frappe.db.exists("Workspace", ws_name)
    print(f"  Workspace exists: {exists}")
    print(f"  Links count: {count}")

    # Print each link
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
    print("  Clear browser cache and refresh the page.")
    print("=" * 60)

    frappe.destroy()
