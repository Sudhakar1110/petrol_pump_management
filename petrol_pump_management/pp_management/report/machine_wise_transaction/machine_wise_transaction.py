import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "machine_id", "fieldtype": "Data", "label": "Machine ID", "width": 120},
        {"fieldname": "date", "fieldtype": "Date", "label": "Date", "width": 100},
        {"fieldname": "total_transactions", "fieldtype": "Int", "label": "Transactions", "width": 100},
        {"fieldname": "total_amount", "fieldtype": "Currency", "label": "Total Amount", "width": 120},
        {"fieldname": "card_amount", "fieldtype": "Currency", "label": "Card", "width": 100},
        {"fieldname": "upi_amount", "fieldtype": "Currency", "label": "UPI", "width": 100},
        {"fieldname": "wallet_amount", "fieldtype": "Currency", "label": "Wallet", "width": 100},
        {"fieldname": "settlement_status", "fieldtype": "Data", "label": "Status", "width": 100},
    ]

    from_date = filters.get("from_date") if filters else None
    to_date = filters.get("to_date") if filters else None

    conditions = "WHERE docstatus = 1"
    params = []
    if from_date:
        conditions += " AND settlement_date >= %s"
        params.append(from_date)
    if to_date:
        conditions += " AND settlement_date <= %s"
        params.append(to_date)

    data = frappe.db.sql(f"""
        SELECT machine_id, settlement_date as date,
               COUNT(*) as total_transactions,
               SUM(total_collected) as total_amount,
               SUM(CASE WHEN payment_mode = 'Card' THEN total_collected ELSE 0 END) as card_amount,
               SUM(CASE WHEN payment_mode = 'UPI' THEN total_collected ELSE 0 END) as upi_amount,
               SUM(CASE WHEN payment_mode = 'E-Wallet' THEN total_collected ELSE 0 END) as wallet_amount,
               settlement_status
        FROM `tabSwipe Settlement`
        {conditions}
        GROUP BY machine_id, settlement_date, settlement_status
        ORDER BY settlement_date DESC, machine_id
    """, params, as_dict=True)

    return columns, data
