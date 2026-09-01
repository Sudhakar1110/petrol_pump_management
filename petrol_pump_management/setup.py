import frappe
import os
import json


def after_install():
    """Setup after app installation."""
    create_roles()
    import_fixtures()
    frappe.db.commit()
    _create_workspace()


def after_migrate():
    """Ensure workspace exists after migration."""
    _create_workspace()


def _create_workspace():
    """Create workspace with links using pure SQL for both parent and children."""
    ws_name = "Petrol Pump Management"

    # Skip if already done
    if frappe.db.exists("Workspace", ws_name):
        count = frappe.db.count("Workspace Link", {"parent": ws_name})
        if count > 0:
            return

    # Clean up
    frappe.db.sql("DELETE FROM `tabWorkspace Link` WHERE parent LIKE '%%Petrol Pump%%'")
    frappe.db.sql("DELETE FROM `tabWorkspace` WHERE module = 'PP Management'")
    frappe.db.commit()

    now = str(frappe.utils.now_datetime())
    cards = _get_cards_config()

    card_names = [c["label"] for c in cards]
    content = json.dumps([
        {"type": "card", "data": {"card_name": cn, "col": 4}}
        for cn in card_names
    ])

    # Step 1: Insert workspace via pure SQL
    frappe.db.sql("""
        INSERT INTO `tabWorkspace`
        (name, label, title, module, icon, indicator_color,
         public, is_hidden, content, standard, docstatus,
         owner, modified_by, modified, creation)
        VALUES (%s, %s, %s, %s, %s, %s,
                1, 0, %s, 1, 0,
                'Administrator', 'Administrator', %s, %s)
    """, (ws_name, ws_name, ws_name, "PP Management",
          "octicon octicon-fuel", "orange", content, now, now))

    # Step 2: Insert ALL links via pure SQL
    idx = 1
    for card in cards:
        frappe.db.sql("""
            INSERT INTO `tabWorkspace Link`
            (name, parent, parenttype, parentfield, idx,
             type, label, icon, link_count, hidden, docstatus,
             owner, modified_by, modified, creation)
            VALUES (%s, %s, 'Workspace', 'links', %s,
                    'Card Break', %s, %s, %s, 0, 0,
                    'Administrator', 'Administrator', %s, %s)
        """, (f"{ws_name}-{idx}", ws_name, idx,
              card["label"], card.get("icon", ""), len(card["links"]), now, now))
        idx += 1

        for link_type, link_to in card["links"]:
            is_qr = 1 if link_type == "Report" else 0
            frappe.db.sql("""
                INSERT INTO `tabWorkspace Link`
                (name, parent, parenttype, parentfield, idx,
                 type, label, link_type, link_to, is_query_report,
                 hidden, docstatus,
                 owner, modified_by, modified, creation)
                VALUES (%s, %s, 'Workspace', 'links', %s,
                        'Link', %s, %s, %s, %s,
                        0, 0,
                        'Administrator', 'Administrator', %s, %s)
            """, (f"{ws_name}-{idx}", ws_name, idx,
                  link_to, link_type, link_to, is_qr, now, now))
            idx += 1

    frappe.db.commit()
    frappe.clear_cache()

    count = frappe.db.count("Workspace Link", {"parent": ws_name})
    print(f"Workspace '{ws_name}' created with {count} link entries!")


def _get_cards_config():
    return [
        {"label": "Configuration", "icon": "octicon octicon-gear", "links": [
            ("DocType", "Station Configuration"),
            ("DocType", "Tank Master"),
            ("DocType", "Nozzle Master"),
            ("DocType", "Fuel Price Master"),
            ("DocType", "Employee Master"),
            ("DocType", "Tank Dip Chart"),
        ]},
        {"label": "Operations", "icon": "octicon octicon-gear", "links": [
            ("DocType", "Shift"),
            ("DocType", "Shift Nozzle Allotment"),
            ("DocType", "Fuel Sale"),
            ("DocType", "Meter Reading"),
            ("DocType", "Daily Stock Register"),
            ("DocType", "Stock Purchase Decantation"),
            ("DocType", "Trip Voucher"),
            ("DocType", "PP Supplier Master"),
        ]},
        {"label": "Credit & Sales", "icon": "octicon octicon-credit-card", "links": [
            ("DocType", "PP Customer"),
            ("DocType", "Vehicle Master"),
            ("DocType", "Credit Sale Invoice"),
            ("DocType", "Payment Receipt"),
            ("DocType", "Credit Limit Ledger"),
            ("DocType", "ANPR Scan Log"),
        ]},
        {"label": "Finance & HR", "icon": "octicon octicon-dollar", "links": [
            ("DocType", "Expense Entry"),
            ("DocType", "Attendance Register"),
            ("DocType", "Advance Amount"),
            ("DocType", "Bank Deposit"),
            ("DocType", "Day Settlement"),
        ]},
        {"label": "Reports", "icon": "octicon octicon-graph", "links": [
            ("Report", "Daily Sales Summary"),
            ("Report", "Shift Settlement Report"),
            ("Report", "Stock Variation Report"),
            ("Report", "Credit Customer Ageing"),
            ("Report", "GST VAT Summary"),
        ]},
    ]


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
