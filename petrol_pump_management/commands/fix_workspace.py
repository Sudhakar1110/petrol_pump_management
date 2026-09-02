import sys
import click
import frappe
import json
import os
import frappe.utils


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
    """Fix Petrol Pump Management workspace with all card breaks and links.

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

    # Step 2: Create workspace with all links
    print("\n[2/3] Creating workspace with all links...")

    ws_data = _get_workspace_data()
    links_data = ws_data["links"]

    # Create workspace WITHOUT links
    ws = frappe.get_doc({
        "doctype": "Workspace",
        "label": ws_name,
        "title": ws_name,
        "module": "PP Management",
        "icon": "octicon octicon-fuel",
        "indicator_color": "orange",
        "public": 1,
        "is_hidden": 0,
        "content": ws_data["content"],
        "shortcuts": ws_data.get("shortcuts", []),
        "charts": [],
        "number_cards": [],
        "custom_blocks": [],
        "quick_lists": [],
        "roles": [],
        "for_user": "",
        "parent_page": "",
        "restrict_to_domain": "",
        "hide_custom": 0,
    })

    ws.flags.with_module = True
    ws.flags.ignore_links = True
    ws.flags.ignore_validate = True
    ws.flags.ignore_permissions = True
    ws.flags.ignore_mandatory = True
    ws.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"  Workspace '{ws.name}' created (without links yet)")

    # Insert links via raw SQL with sequential idx
    print(f"  Inserting {len(links_data)} links via SQL...")
    now = frappe.utils.now_datetime()

    for idx, link in enumerate(links_data, start=1):
        link_name = frappe.utils.cstr(frappe.utils.random_string(8))
        frappe.db.sql("""
            INSERT INTO `tabWorkspace Link`
            (name, creation, modified, owner, modified_by,
             parent, parentfield, parenttype, docstatus,
             idx, type, label, link_type, link_to,
             hidden, is_query_report, onboard, dependencies, link_count)
            VALUES (%s, %s, %s, %s, %s,
                    %s, 'links', 'Workspace', 0,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s)
        """, (
            link_name, now, now, "Administrator", "Administrator",
            ws_name, idx,
            link["type"], link["label"],
            link.get("link_type", ""), link.get("link_to", ""),
            link.get("hidden", 0), link.get("is_query_report", 0),
            link.get("onboard", 0), link.get("dependencies", ""),
            link.get("link_count", 0),
        ))

    frappe.db.commit()
    frappe.clear_cache()

    # Step 3: Verify
    print("\n[3/3] Verifying...")
    count = frappe.db.count("Workspace Link", {"parent": ws_name})
    print(f"  Links count: {count}")

    if count > 0:
        all_links = frappe.db.get_all(
            "Workspace Link",
            filters={"parent": ws_name},
            fields=["type", "label", "link_type", "link_to", "idx"],
            order_by="idx asc",
        )
        for link in all_links:
            if link.type == "Card Break":
                print(f"\n  [{link.label}]")
            else:
                print(f"    - {link.label}")

    print("\n" + "=" * 60)
    if count > 0:
        print(f"  SUCCESS! {count} links created.")
    else:
        print("  FAILED! 0 links. Check errors above.")
    print("  Clear browser cache (Ctrl+Shift+R) and refresh.")
    print("=" * 60)

    frappe.destroy()


def _get_workspace_data():
    """Return complete workspace data with all links."""
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
        {"type": "header", "data": {"text": "<span class=\"h4\"><b>Digital Payments</b></span>", "col": 12}},
        {"type": "card", "data": {"card_name": "Digital Payments", "col": 4}},
        {"type": "spacer", "data": {"col": 12}},
        {"type": "header", "data": {"text": "<span class=\"h4\"><b>Compliance & GST</b></span>", "col": 12}},
        {"type": "card", "data": {"card_name": "Compliance & GST", "col": 4}},
        {"type": "spacer", "data": {"col": 12}},
        {"type": "header", "data": {"text": "<span class=\"h4\"><b>Reports</b></span>", "col": 12}},
        {"type": "card", "data": {"card_name": "Reports", "col": 4}},
    ])

    shortcuts = [
        {"color": "Green", "label": "Station Configuration", "link_to": "Station Configuration", "type": "DocType"},
        {"color": "Green", "label": "Fuel Sale", "link_to": "Fuel Sale", "type": "DocType"},
        {"color": "Green", "label": "Shift", "link_to": "Shift", "type": "DocType"},
        {"color": "Green", "label": "PP Customer", "link_to": "PP Customer", "type": "DocType"},
    ]

    links = [
        # ── Configuration ──
        {"type": "Card Break", "label": "Configuration", "hidden": 0, "is_query_report": 0, "link_count": 0, "onboard": 0},
        {"type": "Link", "label": "Station Configuration", "link_type": "DocType", "link_to": "Station Configuration", "hidden": 0, "is_query_report": 0, "onboard": 1, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Tank Master", "link_type": "DocType", "link_to": "Tank Master", "hidden": 0, "is_query_report": 0, "onboard": 1, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Tank Dip Chart", "link_type": "DocType", "link_to": "Tank Dip Chart", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Nozzle Master", "link_type": "DocType", "link_to": "Nozzle Master", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Fuel Price Master", "link_type": "DocType", "link_to": "Fuel Price Master", "hidden": 0, "is_query_report": 0, "onboard": 1, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Employee Master", "link_type": "DocType", "link_to": "Employee Master", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Commission Rule", "link_type": "DocType", "link_to": "Commission Rule", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "PP Supplier Master", "link_type": "DocType", "link_to": "PP Supplier Master", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},

        # ── Operations ──
        {"type": "Card Break", "label": "Operations", "hidden": 0, "is_query_report": 0, "link_count": 0, "onboard": 0},
        {"type": "Link", "label": "Shift", "link_type": "DocType", "link_to": "Shift", "hidden": 0, "is_query_report": 0, "onboard": 1, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Shift Nozzle Allotment", "link_type": "DocType", "link_to": "Shift Nozzle Allotment", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Fuel Sale", "link_type": "DocType", "link_to": "Fuel Sale", "hidden": 0, "is_query_report": 0, "onboard": 1, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Meter Reading", "link_type": "DocType", "link_to": "Meter Reading", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Daily Stock Register", "link_type": "DocType", "link_to": "Daily Stock Register", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Stock Purchase Decantation", "link_type": "DocType", "link_to": "Stock Purchase Decantation", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Trip Voucher", "link_type": "DocType", "link_to": "Trip Voucher", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Lube Stock", "link_type": "DocType", "link_to": "Lube Stock", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Day Settlement", "link_type": "DocType", "link_to": "Day Settlement", "hidden": 0, "is_query_report": 0, "onboard": 1, "dependencies": "", "link_count": 0},

        # ── Credit & Sales ──
        {"type": "Card Break", "label": "Credit & Sales", "hidden": 0, "is_query_report": 0, "link_count": 0, "onboard": 0},
        {"type": "Link", "label": "PP Customer", "link_type": "DocType", "link_to": "PP Customer", "hidden": 0, "is_query_report": 0, "onboard": 1, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Vehicle Master", "link_type": "DocType", "link_to": "Vehicle Master", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Credit Sale Invoice", "link_type": "DocType", "link_to": "Credit Sale Invoice", "hidden": 0, "is_query_report": 0, "onboard": 1, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Credit Statement", "link_type": "DocType", "link_to": "Credit Statement", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Credit Limit Ledger", "link_type": "DocType", "link_to": "Credit Limit Ledger", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Payment Receipt", "link_type": "DocType", "link_to": "Payment Receipt", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Payment Receipt Invoice", "link_type": "DocType", "link_to": "Payment Receipt Invoice", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "ANPR Scan Log", "link_type": "DocType", "link_to": "ANPR Scan Log", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},

        # ── Finance & HR ──
        {"type": "Card Break", "label": "Finance & HR", "hidden": 0, "is_query_report": 0, "link_count": 0, "onboard": 0},
        {"type": "Link", "label": "Expense Entry", "link_type": "DocType", "link_to": "Expense Entry", "hidden": 0, "is_query_report": 0, "onboard": 1, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Attendance Register", "link_type": "DocType", "link_to": "Attendance Register", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Leave Application", "link_type": "DocType", "link_to": "Leave Application", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Overtime Log", "link_type": "DocType", "link_to": "Overtime Log", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Advance Amount", "link_type": "DocType", "link_to": "Advance Amount", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Bank Deposit", "link_type": "DocType", "link_to": "Bank Deposit", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Reward Points Ledger", "link_type": "DocType", "link_to": "Reward Points Ledger", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},

        # ── Digital Payments ──
        {"type": "Card Break", "label": "Digital Payments", "hidden": 0, "is_query_report": 0, "link_count": 0, "onboard": 0},
        {"type": "Link", "label": "Swipe Settlement", "link_type": "DocType", "link_to": "Swipe Settlement", "hidden": 0, "is_query_report": 0, "onboard": 1, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Petro Card Transaction", "link_type": "DocType", "link_to": "Petro Card Transaction", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},

        # ── Compliance & GST ──
        {"type": "Card Break", "label": "Compliance & GST", "hidden": 0, "is_query_report": 0, "link_count": 0, "onboard": 0},
        {"type": "Link", "label": "Bank Reconciliation Entry", "link_type": "DocType", "link_to": "Bank Reconciliation Entry", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Tally Export Log", "link_type": "DocType", "link_to": "Tally Export Log", "hidden": 0, "is_query_report": 0, "onboard": 0, "dependencies": "", "link_count": 0},

        # ── Reports ──
        {"type": "Card Break", "label": "Reports", "hidden": 0, "is_query_report": 0, "link_count": 0, "onboard": 0},
        {"type": "Link", "label": "Daily Sales Summary", "link_type": "Report", "link_to": "Daily Sales Summary", "hidden": 0, "is_query_report": 1, "onboard": 1, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Shift Settlement Report", "link_type": "Report", "link_to": "Shift Settlement Report", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Stock Variation Report", "link_type": "Report", "link_to": "Stock Variation Report", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Credit Customer Ageing", "link_type": "Report", "link_to": "Credit Customer Ageing", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "GSTR-1 Summary", "link_type": "Report", "link_to": "GSTR-1 Summary", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "GSTR-3B Summary", "link_type": "Report", "link_to": "GSTR-3B Summary", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "HSN Wise Summary", "link_type": "Report", "link_to": "HSN Wise Summary", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "GST VAT Summary", "link_type": "Report", "link_to": "GST VAT Summary", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Employee Commission Report", "link_type": "Report", "link_to": "Employee Commission Report", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Cash Flow Report", "link_type": "Report", "link_to": "Cash Flow Report", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "PP Day Book", "link_type": "Report", "link_to": "PP Day Book", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Bank Reconciliation Report", "link_type": "Report", "link_to": "Bank Reconciliation Report", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Tally Export Report", "link_type": "Report", "link_to": "Tally Export Report", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Profit Loss Statement", "link_type": "Report", "link_to": "Profit Loss Statement", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Expense Summary", "link_type": "Report", "link_to": "Expense Summary", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Swipe Digital Settlement", "link_type": "Report", "link_to": "Swipe Digital Settlement", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Vehicle Wise Consumption", "link_type": "Report", "link_to": "Vehicle Wise Consumption", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Bank Deposit Report", "link_type": "Report", "link_to": "Bank Deposit Report", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "ANPR Scan Report", "link_type": "Report", "link_to": "ANPR Scan Report", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Density Dip Variation", "link_type": "Report", "link_to": "Density Dip Variation", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Employee Attendance Payroll", "link_type": "Report", "link_to": "Employee Attendance Payroll", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0},
        {"type": "Link", "label": "Fuel Rate Variation Report", "link_type": "Report", "link_to": "Fuel Rate Variation Report", "hidden": 0, "is_query_report": 1, "onboard": 0, "dependencies": "", "link_count": 0},
    ]

    return {
        "content": content,
        "shortcuts": shortcuts,
        "links": links,
    }
