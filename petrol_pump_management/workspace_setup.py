import frappe
import json
from frappe.utils import now_datetime


def execute():
    """Create workspace with all links using Frappe API.
    Run via: bench --site <site> execute petrol_pump_management.workspace_setup
    """
    ws_name = "Petrol Pump Management"

    # Step 1: Clean up ALL existing workspaces for this module
    for old_name in frappe.get_all("Workspace",
        filters={"module": "PP Management"},
        pluck="name"
    ):
        frappe.delete_doc("Workspace", old_name, force=True, ignore_missing=True)

    # Also delete any customization
    frappe.db.sql("DELETE FROM `tabCustom Workspace` WHERE reference_name = %s", ws_name)
    frappe.db.commit()

    # Step 2: Build card config - each card has a name, icon, and links
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

    # Step 3: Create workspace using Frappe's build_links_table_from_card
    doc = frappe.get_doc({
        "doctype": "Workspace",
        "label": ws_name,
        "title": ws_name,
        "module": "PP Management",
        "icon": "octicon octicon-fuel",
        "indicator_color": "orange",
        "public": 1,
        "is_hidden": 0,
        "content": json.dumps([
            {"type": "header", "data": {"text": ws_name, "level": "h2"}},
        ]),
        "type": "Workspace",
    })
    doc.flags.with_module = True
    doc.insert(ignore_permissions=True)

    # Step 4: Build links table using Frappe's own method
    card_json = []
    for card in cards_config:
        card_json.append({
            "label": card["label"],
            "icon": card["icon"],
            "links": json.dumps(card["links"]),
            "link_count": len(card["links"]),
            "hidden": 0,
            "description": "",
        })

    doc.build_links_table_from_card(card_json)
    doc.save(ignore_permissions=True)
    frappe.db.commit()

    # Step 5: Force public=1 (Frappe sometimes resets this)
    frappe.db.sql(
        "UPDATE `tabWorkspace` SET public=1, is_hidden=0 WHERE name=%s", ws_name
    )
    frappe.db.commit()

    # Step 6: Rebuild content JSON to match the actual links
    card_names = [c["label"] for c in cards_config]
    content = json.dumps(
        [{"type": "header", "data": {"text": ws_name, "level": "h2"}}]
        + [{"type": "card", "data": {"card_name": cn, "col": 4}} for cn in card_names]
    )
    frappe.db.sql(
        "UPDATE `tabWorkspace` SET content=%s WHERE name=%s",
        (content, ws_name),
    )
    frappe.db.commit()
    frappe.clear_cache()

    link_count = len(frappe.get_all("Workspace Link", filters={"parent": ws_name}))
    print(f"Workspace '{ws_name}' created with {link_count} links in {len(card_names)} cards!")
