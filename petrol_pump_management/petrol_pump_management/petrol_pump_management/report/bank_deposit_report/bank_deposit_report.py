import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "deposit_date", "fieldtype": "Date", "label": "Deposit Date", "width": 120},
        {"fieldname": "amount", "fieldtype": "Currency", "label": "Amount", "width": 120},
        {"fieldname": "bank_name", "fieldtype": "Data", "label": "Bank", "width": 150},
        {"fieldname": "deposit_slip_no", "fieldtype": "Data", "label": "Slip No", "width": 120},
        {"fieldname": "status", "fieldtype": "Data", "label": "Status", "width": 100},
    ]
    conditions = "bd.docstatus = 1"
    if filters.get("from_date"):
        conditions += f" AND bd.deposit_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND bd.deposit_date <= '{filters['to_date']}'"
    data = frappe.db.sql(f"""
        SELECT bd.deposit_date, bd.amount, bd.bank_name,
               bd.deposit_slip_no, bd.status
        FROM `tabBank Deposit` bd
        WHERE {conditions}
        ORDER BY bd.deposit_date DESC
    """, as_dict=True)
    return columns, data
