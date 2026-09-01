import frappe
import os
import json


def after_install():
    """Setup after app installation."""
    create_roles()
    import_fixtures()
    frappe.db.commit()
    # Create workspace
    try:
        _create_workspace()
    except Exception as e:
        frappe.log_error(f"Workspace setup in after_install failed: {e}", "PP Workspace")


def after_migrate():
    """Create workspace after migration."""
    try:
        _create_workspace()
    except Exception as e:
        frappe.log_error(f"Workspace setup in after_migrate failed: {e}", "PP Workspace")


def _create_workspace():
    """Create workspace with all links using raw SQL."""
    ws_name = "Petrol Pump Management"

    # Check if workspace already has links
    existing_links = frappe.db.count("Workspace Link", {"parent": ws_name})
    if existing_links > 0:
        # Already set up, just ensure public
        frappe.db.sql("UPDATE `tabWorkspace` SET public=1, is_hidden=0 WHERE name=%s", ws_name)
        frappe.db.commit()
        return

    now = str(frappe.utils.now_datetime())

    # Delete old workspaces
    for old in frappe.db.get_all("Workspace", filters={"module": "PP Management"}, pluck="name"):
        frappe.db.sql("DELETE FROM `tabWorkspace Link` WHERE parent=%s", old)
        frappe.db.sql("DELETE FROM `tabWorkspace` WHERE name=%s", old)
    frappe.db.commit()

    # Get column names
    ws_cols = set(r[0] for r in frappe.db.sql("SHOW COLUMNS FROM `tabWorkspace`"))
    link_cols = set(r[0] for r in frappe.db.sql("SHOW COLUMNS FROM `tabWorkspace Link`"))

    # Content JSON
    card_names = ["Configuration", "Operations", "Credit & Sales", "Finance & HR", "Reports"]
    content = json.dumps([
        {"type": "header", "data": {"text": ws_name, "level": "h2"}},
    ] + [
        {"type": "card", "data": {"card_name": cn, "col": 4}} for cn in card_names
    ])

    # Insert workspace
    ws_data = {}
    ws_map = {
        "name": ws_name, "label": ws_name, "title": ws_name,
        "module": "PP Management", "icon": "octicon octicon-fuel",
        "indicator_color": "orange", "public": 1, "is_hidden": 0,
        "content": content, "type": "Workspace", "docstatus": 0,
        "owner": "Administrator", "modified_by": "Administrator",
        "modified": now, "creation": now,
    }
    for k, v in ws_map.items():
        if k in ws_cols:
            ws_data[k] = v
    cols_str = ", ".join([f"`{k}`" for k in ws_data])
    phs_str = ", ".join(["%s"] * len(ws_data))
    frappe.db.sql(f"INSERT INTO `tabWorkspace` ({cols_str}) VALUES ({phs_str})", list(ws_data.values()))
    frappe.db.commit()

    # Links data: (type, link_type, link_to, label, hidden, is_query_report, icon)
    links = [
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
        row = {
            "name": f"{ws_name}-{idx + 1}",
            "parent": ws_name,
            "parenttype": "Workspace",
            "parentfield": "links",
            "idx": idx + 1,
            "type": ltype,
            "label": label,
            "hidden": hidden,
            "docstatus": 0,
            "owner": "Administrator",
            "modified_by": "Administrator",
            "modified": now,
            "creation": now,
        }
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
    frappe.clear_cache()


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
        os.path.dirname(os.path.dirname(__file__)),
        "pp_management", "fixtures"
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

            name = doc_data.get("name") or doc_data.get(doc_data.get("__key", "name"))
            if name and frappe.db.exists(doctype, name):
                continue

            try:
                doc = frappe.new_doc(doctype)
                doc.update(doc_data)
                doc.insert(ignore_permissions=True)
            except Exception:
                pass
