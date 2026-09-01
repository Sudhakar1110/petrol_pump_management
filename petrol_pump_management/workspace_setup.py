"""Create workspace with all links.
Run: bench --site <site> execute petrol_pump_management.workspace_setup
"""
import frappe
import json


def execute():
    """Create workspace with all card links using SQL insert + ORM append."""
    ws_name = "Petrol Pump Management"

    # Delete existing
    frappe.db.sql("DELETE FROM `tabWorkspace Link` WHERE parent LIKE '%%Petrol Pump%%'")
    frappe.db.sql("DELETE FROM `tabWorkspace` WHERE module = 'PP Management'")
    frappe.db.commit()

    cards = [
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

    card_names = [c["label"] for c in cards]
    content = json.dumps([
        {"type": "card", "data": {"card_name": cn, "col": 4}}
        for cn in card_names
    ])

    now = str(frappe.utils.now_datetime())

    # Step 1: Insert workspace via SQL
    frappe.db.sql("""
        INSERT INTO `tabWorkspace`
        (name, label, title, module, icon, indicator_color,
         public, is_hidden, content, docstatus,
         owner, modified_by, modified, creation)
        VALUES (%s, %s, %s, %s, %s, %s,
                1, 0, %s, 0,
                'Administrator', 'Administrator', %s, %s)
    """, (ws_name, ws_name, ws_name, "PP Management",
          "octicon octicon-fuel", "orange", content, now, now))
    frappe.db.commit()

    # Step 2: Load and add links via ORM
    doc = frappe.get_doc("Workspace", ws_name)
    for card in cards:
        doc.append("links", {
            "type": "Card Break",
            "label": card["label"],
            "icon": card.get("icon", ""),
            "link_count": len(card["links"]),
        })
        for link_type, link_to in card["links"]:
            doc.append("links", {
                "type": "Link",
                "link_type": link_type,
                "link_to": link_to,
                "label": link_to,
                "is_query_report": 1 if link_type == "Report" else 0,
            })

    doc.save(ignore_permissions=True)
    frappe.db.commit()
    frappe.clear_cache()

    count = frappe.db.count("Workspace Link", {"parent": ws_name})
    print(f"Workspace '{ws_name}' created with {count} links!")
