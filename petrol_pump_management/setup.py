import frappe
import os
import json


def after_install():
    """Setup after app installation."""
    create_roles()
    import_fixtures()
    frappe.db.commit()
    create_workspace()


def after_migrate():
    """Create workspace after migration."""
    create_workspace()


def create_workspace():
    """Create workspace with all links using Frappe ORM."""
    ws_name = "Petrol Pump Management"

    # Check if workspace already has links
    if frappe.db.exists("Workspace", ws_name):
        link_count = frappe.db.count("Workspace Link", {"parent": ws_name})
        if link_count > 0:
            # Ensure public
            frappe.db.sql(
                "UPDATE `tabWorkspace` SET public=1, is_hidden=0 WHERE name=%s",
                ws_name,
            )
            frappe.db.commit()
            return
        # Has no links - delete and recreate
        frappe.delete_doc("Workspace", ws_name, force=True, ignore_missing=True)
        frappe.db.commit()

    # Clean up old workspaces under this module
    for old in frappe.db.get_all(
        "Workspace", filters={"module": "PP Management"}, pluck="name"
    ):
        try:
            frappe.delete_doc("Workspace", old, force=True, ignore_missing=True)
        except Exception:
            pass
    frappe.db.commit()

    # Card configuration
    cards_config = [
        {
            "label": "Configuration",
            "icon": "octicon octicon-gear",
            "links": [
                {"link_type": "DocType", "link_to": "Station Configuration"},
                {"link_type": "DocType", "link_to": "Tank Master"},
                {"link_type": "DocType", "link_to": "Nozzle Master"},
                {"link_type": "DocType", "link_to": "Fuel Price Master"},
                {"link_type": "DocType", "link_to": "Employee Master"},
                {"link_type": "DocType", "link_to": "Tank Dip Chart"},
            ],
        },
        {
            "label": "Operations",
            "icon": "octicon octicon-gear",
            "links": [
                {"link_type": "DocType", "link_to": "Shift"},
                {"link_type": "DocType", "link_to": "Shift Nozzle Allotment"},
                {"link_type": "DocType", "link_to": "Fuel Sale"},
                {"link_type": "DocType", "link_to": "Meter Reading"},
                {"link_type": "DocType", "link_to": "Daily Stock Register"},
                {"link_type": "DocType", "link_to": "Stock Purchase Decantation"},
                {"link_type": "DocType", "link_to": "Trip Voucher"},
                {"link_type": "DocType", "link_to": "PP Supplier Master"},
            ],
        },
        {
            "label": "Credit & Sales",
            "icon": "octicon octicon-credit-card",
            "links": [
                {"link_type": "DocType", "link_to": "PP Customer"},
                {"link_type": "DocType", "link_to": "Vehicle Master"},
                {"link_type": "DocType", "link_to": "Credit Sale Invoice"},
                {"link_type": "DocType", "link_to": "Payment Receipt"},
                {"link_type": "DocType", "link_to": "Credit Limit Ledger"},
                {"link_type": "DocType", "link_to": "ANPR Scan Log"},
            ],
        },
        {
            "label": "Finance & HR",
            "icon": "octicon octicon-dollar",
            "links": [
                {"link_type": "DocType", "link_to": "Expense Entry"},
                {"link_type": "DocType", "link_to": "Attendance Register"},
                {"link_type": "DocType", "link_to": "Advance Amount"},
                {"link_type": "DocType", "link_to": "Bank Deposit"},
                {"link_type": "DocType", "link_to": "Day Settlement"},
            ],
        },
        {
            "label": "Reports",
            "icon": "octicon octicon-graph",
            "links": [
                {"link_type": "Report", "link_to": "Daily Sales Summary"},
                {"link_type": "Report", "link_to": "Shift Settlement Report"},
                {"link_type": "Report", "link_to": "Stock Variation Report"},
                {"link_type": "Report", "link_to": "Credit Customer Ageing"},
                {"link_type": "Report", "link_to": "GST VAT Summary"},
            ],
        },
    ]

    # Build content JSON
    card_names = [c["label"] for c in cards_config]
    content = json.dumps(
        [{"type": "header", "data": {"text": ws_name, "level": "h2"}}]
        + [{"type": "card", "data": {"card_name": cn, "col": 4}} for cn in card_names]
    )

    # Create workspace using Frappe ORM
    ws = frappe.get_doc(
        {
            "doctype": "Workspace",
            "label": ws_name,
            "title": ws_name,
            "module": "PP Management",
            "icon": "octicon octicon-fuel",
            "indicator_color": "orange",
            "public": 1,
            "is_hidden": 0,
            "content": content,
            "type": "Workspace",
        }
    )
    ws.flags.with_module = True
    ws.insert(ignore_permissions=True)

    # Add links using Frappe's append method
    for card in cards_config:
        ws.append(
            "links",
            {
                "type": "Card Break",
                "label": card["label"],
                "icon": card.get("icon", ""),
                "link_count": len(card["links"]),
            },
        )
        for link in card["links"]:
            ws.append(
                "links",
                {
                    "type": "Link",
                    "link_type": link["link_type"],
                    "link_to": link["link_to"],
                    "label": link["link_to"],
                },
            )

    ws.save(ignore_permissions=True)
    frappe.db.commit()
    frappe.clear_cache()

    link_count = frappe.db.count("Workspace Link", {"parent": ws_name})
    frappe.msgprint(f"Workspace created with {link_count} links!")


def create_roles():
    """Create custom roles for petrol pump management."""
    roles = [
        {
            "role_name": "Station Manager",
            "desk_access": 1,
            "is_custom": 1,
            "description": "Station Manager / Dealer - Full access to all modules",
        },
        {
            "role_name": "Salesman DSM",
            "desk_access": 1,
            "is_custom": 1,
            "description": "Salesman / Direct Sales Man",
        },
        {
            "role_name": "Credit Accounts Officer",
            "desk_access": 1,
            "is_custom": 1,
            "description": "Credit & Accounts Officer",
        },
        {
            "role_name": "Compliance Officer",
            "desk_access": 1,
            "is_custom": 1,
            "description": "Compliance Officer (GST)",
        },
        {
            "role_name": "Recovery Officer",
            "desk_access": 1,
            "is_custom": 1,
            "description": "Recovery Officer - Credit recovery",
        },
        {
            "role_name": "Petrol Pump Auditor",
            "desk_access": 1,
            "is_custom": 1,
            "description": "Auditor / CA - Read-only access",
        },
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

            name = doc_data.get("name") or doc_data.get(
                doc_data.get("__key", "name")
            )
            if name and frappe.db.exists(doctype, name):
                continue

            try:
                doc = frappe.new_doc(doctype)
                doc.update(doc_data)
                doc.insert(ignore_permissions=True)
            except Exception:
                pass
