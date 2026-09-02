import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "date", "fieldtype": "Date", "label": "Date", "width": 120},
        {"fieldname": "bank_account", "fieldtype": "Data", "label": "Bank Account", "width": 180},
        {"fieldname": "book_balance", "fieldtype": "Currency", "label": "Book Balance", "width": 150},
        {"fieldname": "bank_balance", "fieldtype": "Currency", "label": "Bank Balance", "width": 150},
        {"fieldname": "difference", "fieldtype": "Currency", "label": "Difference", "width": 150},
        {"fieldname": "status", "fieldtype": "Data", "label": "Status", "width": 100},
    ]
    conditions = "1=1"
    if filters.get("from_date"):
        conditions += f" AND reconciliation_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND reconciliation_date <= '{filters['to_date']}'"

    data = frappe.db.sql(f"""
        SELECT reconciliation_date as date, bank_account, book_balance,
               bank_balance, difference, status
        FROM `tabBank Reconciliation Entry`
        WHERE {conditions}
        ORDER BY reconciliation_date DESC
    """, as_dict=True)

    return columns, data
