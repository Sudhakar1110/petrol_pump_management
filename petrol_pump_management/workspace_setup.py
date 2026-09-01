import frappe
import json


def execute():
    """Create workspace with all links.
    Run: bench --site <site> execute petrol_pump_management.workspace_setup
    """
    ws_name = "Petrol Pump Management"

    # Clean up ALL existing
    for old in frappe.db.get_all("Workspace", filters={"module": "PP Management"}, pluck="name"):
        frappe.delete_doc("Workspace", old, force=True, ignore_missing=True)
    frappe.db.commit()

    # Card configuration
    cards_config = [
        {"label": "Configuration", "icon": "octicon octicon-gear", "links": [
            {"link_type": "DocType", "link_to": "Station Configuration"},
            {"link_type": "DocType", "link_to": "Tank Master"},
            {"link_type": "DocType", "link_to": "Nozzle Master"},
            {"link_type": "DocType", "link_to": "Fuel Price Master"},
            {"link_type": "DocType", "link_to": "Employee Master"},
            {"link_type": "DocType", "link_to": "Tank Dip Chart"},
        ]},
        {"label": "Operations", "icon": "octicon octicon-gear", "links": [
            {"link_type": "DocType", "link_to": "Shift"},
            {"link_type": "DocType", "link_to": "Shift Nozzle Allotment"},
            {"link_type": "DocType", "link_to": "Fuel Sale"},
            {"link_type": "DocType", "link_to": "Meter Reading"},
            {"link_type": "DocType", "link_to": "Daily Stock Register"},
            {"link_type": "DocType", "link_to": "Stock Purchase Decantation"},
            {"link_type": "DocType", "link_to": "Trip Voucher"},
            {"link_type": "DocType", "link_to": "PP Supplier Master"},
        ]},
        {"label": "Credit & Sales", "icon": "octicon octicon-credit-card", "links": [
            {"link_type": "DocType", "link_to": "PP Customer"},
            {"link_type": "DocType", "link_to": "Vehicle Master"},
            {"link_type": "DocType", "link_to": "Credit Sale Invoice"},
            {"link_type": "DocType", "link_to": "Payment Receipt"},
            {"link_type": "DocType", "link_to": "Credit Limit Ledger"},
            {"link_type": "DocType", "link_to": "ANPR Scan Log"},
        ]},
        {"label": "Finance & HR", "icon": "octicon octicon-dollar", "links": [
            {"link_type": "DocType", "link_to": "Expense Entry"},
            {"link_type": "DocType", "link_to": "Attendance Register"},
            {"link_type": "DocType", "link_to": "Advance Amount"},
            {"link_type": "DocType", "link_to": "Bank Deposit"},
            {"link_type": "DocType", "link_to": "Day Settlement"},
        ]},
        {"label": "Reports", "icon": "octicon octicon-graph", "links": [
            {"link_type": "Report", "link_to": "Daily Sales Summary"},
            {"link_type": "Report", "link_to": "Shift Settlement Report"},
            {"link_type": "Report", "link_to": "Stock Variation Report"},
            {"link_type": "Report", "link_to": "Credit Customer Ageing"},
            {"link_type": "Report", "link_to": "GST VAT Summary"},
        ]},
    ]

    # Build content JSON
    card_names = [c["label"] for c in cards_config]
    content = json.dumps(
        [{"type": "header", "data": {"text": ws_name, "level": "h2"}}]
        + [{"type": "card", "data": {"card_name": cn, "col": 4}} for cn in card_names]
    )

    # Create workspace using Frappe ORM
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
        "type": "Workspace",
    })
    ws.flags.with_module = True
    ws.insert(ignore_permissions=True)

    # Add links using Frappe's own method
    for card in cards_config:
        links_json = json.dumps(card["links"])
        ws.append("links", {
            "type": "Card Break",
            "label": card["label"],
            "icon": card.get("icon", ""),
            "link_count": len(card["links"]),
        })
        for link in card["links"]:
            ws.append("links", {
                "type": "Link",
                "link_type": link["link_type"],
                "link_to": link["link_to"],
                "label": link["link_to"],
            })

    ws.save(ignore_permissions=True)
    frappe.db.commit()
    frappe.clear_cache()

    # Verify
    link_count = frappe.db.count("Workspace Link", {"parent": ws_name})
    ws_exists = frappe.db.exists("Workspace", ws_name)
    print(f"Workspace '{ws_name}': exists={ws_exists}, links={link_count}")
