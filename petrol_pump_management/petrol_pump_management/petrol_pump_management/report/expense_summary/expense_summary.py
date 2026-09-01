import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "expense_date", "fieldtype": "Date", "label": "Date", "width": 120},
        {"fieldname": "expense_type", "fieldtype": "Data", "label": "Expense Type", "width": 150},
        {"fieldname": "amount", "fieldtype": "Currency", "label": "Amount", "width": 120},
        {"fieldname": "payment_method", "fieldtype": "Data", "label": "Payment Method", "width": 120},
        {"fieldname": "description", "fieldtype": "Data", "label": "Description", "width": 200},
        {"fieldname": "status", "fieldtype": "Data", "label": "Status", "width": 100},
    ]
    conditions = "ee.docstatus = 1"
    if filters.get("from_date"):
        conditions += f" AND ee.expense_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND ee.expense_date <= '{filters['to_date']}'"
    data = frappe.db.sql(f"""
        SELECT ee.expense_date, ee.expense_type, ee.amount,
               ee.payment_method, ee.description, ee.status
        FROM `tabExpense Entry` ee
        WHERE {conditions}
        ORDER BY ee.expense_date DESC
    """, as_dict=True)
    return columns, data
