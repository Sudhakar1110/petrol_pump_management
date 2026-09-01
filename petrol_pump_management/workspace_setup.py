"""Create workspace with all links using pure SQL.
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
    now = str(frappe.utils.now_datetime())

    card_names = [c["label"] for c in cards]
    content = json.dumps([
        {"type": "card", "data": {"card_name": cn, "col": 4}}
        for cn in card_names
    ])

    # Insert workspace via pure SQL
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

    # Insert all links via pure SQL
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
