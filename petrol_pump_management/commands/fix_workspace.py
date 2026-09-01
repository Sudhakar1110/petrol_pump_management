import click
import frappe
import os
import json


@click.command("fix-workspace")
def fix_workspace():
    """Fix Petrol Pump Management workspace - clean stale entries and rebuild from JSON.

    Usage: bench --site <site-name> fix-workspace
    """
    frappe.init()
    frappe.connect()

    print("=" * 60)
    print("  Fixing Petrol Pump Management Workspace")
    print("=" * 60)

    # Step 1: Delete ALL existing workspaces for this module
    print("\n[1/4] Cleaning up all existing workspace entries...")
    all_ws = frappe.db.get_all(
        "Workspace",
        filters={"module": "PP Management"},
        pluck="name",
    )
    for name in all_ws:
        frappe.db.sql("DELETE FROM `tabWorkspace Link` WHERE parent = %s", name)
        frappe.db.sql("DELETE FROM `tabWorkspace` WHERE name = %s", name)
        print(f"  Deleted workspace: {name}")

    # Also check for any workspace with "petrol" or "pp" in the name
    other_ws = frappe.db.sql(
        "SELECT name FROM `tabWorkspace` WHERE name LIKE %s OR name LIKE %s",
        ("%Petrol%", "%PP Management%"),
        as_dict=True,
    )
    for ws in other_ws:
        frappe.db.sql("DELETE FROM `tabWorkspace Link` WHERE parent = %s", ws.name)
        frappe.db.sql("DELETE FROM `tabWorkspace` WHERE name = %s", ws.name)
        print(f"  Deleted stale workspace: {ws.name}")

    frappe.db.commit()
    print("  ✓ All stale entries cleaned")

    # Step 2: Read workspace JSON definition
    print("\n[2/4] Reading workspace JSON definition...")
    ws_json_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "pp_management", "workspace", "petrol_pump_management",
        "petrol_pump_management.json"
    )

    if not os.path.exists(ws_json_path):
        print(f"  ✗ ERROR: Workspace JSON not found at: {ws_json_path}")
        frappe.destroy()
        return

    with open(ws_json_path, "r") as f:
        ws_data = json.load(f)

    links = ws_data.pop("links", [])
    print(f"  ✓ Found workspace definition with {len(links)} links")

    # Step 3: Create workspace document
    print("\n[3/4] Creating workspace document...")
    ws = frappe.get_doc(ws_data)
    ws.flags.with_module = True
    ws.flags.ignore_links = True
    ws.flags.ignore_validate = True

    for link in links:
        ws.append("links", link)

    ws.insert(ignore_permissions=True)
    frappe.db.commit()
    frappe.clear_cache()
    print(f"  ✓ Workspace '{ws.name}' created successfully")

    # Step 4: Verify
    print("\n[4/4] Verifying workspace...")
    count = frappe.db.count("Workspace Link", {"parent": ws.name})
    ws_exists = frappe.db.exists("Workspace", ws.name)
    print(f"  Workspace exists: {ws_exists}")
    print(f"  Links count: {count}")

    if count > 0:
        print(f"\n  ✓ SUCCESS! Workspace '{ws.name}' created with {count} links!")
    else:
        print(f"\n  ✗ FAILED! Workspace has 0 links")

    print("\n" + "=" * 60)
    print("  Done! Clear your browser cache and refresh the page.")
    print("=" * 60)

    frappe.destroy()
