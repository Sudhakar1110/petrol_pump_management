import frappe
import os
import json


def after_install():
    """Setup after app installation."""
    create_roles()
    import_fixtures()
    frappe.db.commit()


def after_migrate():
    """After migration - ensure workspace exists with all links."""
    _ensure_workspace()


def _ensure_workspace():
    """Import workspace from JSON file and ensure all links are present."""
    ws_name = "Petrol Pump Management"

    # If workspace already has links, skip
    count = frappe.db.count("Workspace Link", {"parent": ws_name})
    if count > 0:
        print(f"Petrol Pump Management workspace already has {count} links, skipping.")
        return

    # Import workspace from JSON file using Frappe's built-in importer
    try:
        from frappe.desk.page.setup_wizard.setup_wizard import setup_complete
    except ImportError:
        pass

    # Try to import workspace from the standard location
    ws_json_path = os.path.join(
        os.path.dirname(__file__), "pp_management", "workspace", "petrol_pump_management.json"
    )
    if os.path.exists(ws_json_path):
        with open(ws_json_path, "r") as f:
            ws_data = json.load(f)

        # Delete any existing broken workspace
        for name in frappe.db.get_all("Workspace", filters={"module": "PP Management"}, pluck="name"):
            frappe.db.sql("DELETE FROM `tabWorkspace Link` WHERE parent = %s", name)
            frappe.db.sql("DELETE FROM `tabWorkspace` WHERE name = %s", name)
        frappe.db.commit()

        # Create workspace with links
        ws = frappe.get_doc({
            "doctype": "Workspace",
            "label": ws_data["label"],
            "title": ws_data["title"],
            "module": ws_data["module"],
            "icon": ws_data.get("icon", "octicon octicon-file"),
            "indicator_color": ws_data.get("indicator_color", "blue"),
            "public": ws_data.get("public", 1),
            "is_hidden": ws_data.get("is_hidden", 0),
            "content": json.dumps(ws_data["content"]),
            "links": ws_data["links"],
        })
        ws.flags.with_module = True
        ws.flags.ignore_links = True
        ws.flags.ignore_validate = True
        ws.flags.ignore_permissions = True
        ws.flags.ignore_mandatory = True
        ws.insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.clear_cache()

        final_count = frappe.db.count("Workspace Link", {"parent": ws_name})
        print(f"Petrol Pump Management workspace imported with {final_count} links!")
    else:
        print(f"WARNING: Workspace JSON not found at {ws_json_path}")


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
