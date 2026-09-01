"""Create workspace with all links.
Run: bench --site <site> execute petrol_pump_management.workspace_setup
"""
import frappe
import json


def execute():
    ws_name = "Petrol Pump Management"

    # Clean up
    frappe.db.sql("DELETE FROM `tabWorkspace Link` WHERE parent LIKE '%%Petrol Pump%%'")
    frappe.db.sql("DELETE FROM `tabWorkspace` WHERE module = 'PP Management'")
    frappe.db.commit()

    from petrol_pump_management.setup import _get_cards_config
    cards = _get_cards_config()
    card_names = [c["label"] for c in cards]
    content = json.dumps([
        {"type": "card", "data": {"card_name": cn, "col": 4}}
        for cn in card_names
    ])

    # Bypass restrictions
    old_in_install = frappe.flags.in_install
    old_in_migrate = frappe.flags.in_migrate
    frappe.flags.in_install = False
    frappe.flags.in_migrate = False

    try:
        doc = frappe.get_doc({
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
        doc.flags.with_module = True
        doc.flags.ignore_links = True

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

        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        frappe.clear_cache()
    finally:
        frappe.flags.in_install = old_in_install
        frappe.flags.in_migrate = old_in_migrate

    count = frappe.db.count("Workspace Link", {"parent": ws_name})
    print(f"Workspace '{ws_name}' created with {count} links!")
