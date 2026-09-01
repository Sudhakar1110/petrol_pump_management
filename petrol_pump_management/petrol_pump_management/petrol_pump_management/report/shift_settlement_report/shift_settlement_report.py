import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "shift_date", "fieldtype": "Date", "label": "Date", "width": 120},
        {"fieldname": "salesman_name", "fieldtype": "Data", "label": "Salesman", "width": 150},
        {"fieldname": "opening_cash", "fieldtype": "Currency", "label": "Opening Cash", "width": 120},
        {"fieldname": "closing_cash", "fieldtype": "Currency", "label": "Closing Cash", "width": 120},
        {"fieldname": "total_sale_amount", "fieldtype": "Currency", "label": "Total Sale", "width": 120},
        {"fieldname": "cash_collected", "fieldtype": "Currency", "label": "Cash Collected", "width": 120},
        {"fieldname": "card_upi_amount", "fieldtype": "Currency", "label": "Card/UPI", "width": 120},
        {"fieldname": "credit_amount", "fieldtype": "Currency", "label": "Credit", "width": 120},
        {"fieldname": "cash_shortage", "fieldtype": "Currency", "label": "Shortage", "width": 120},
        {"fieldname": "status", "fieldtype": "Data", "label": "Status", "width": 100},
    ]
    
    conditions = "s.docstatus = 1"
    if filters.get("from_date"):
        conditions += f" AND s.shift_date >= '{filters.from_date}'"
    if filters.get("to_date"):
        conditions += f" AND s.shift_date <= '{filters.to_date}'"
    
    data = frappe.db.sql(f"""
        SELECT s.shift_date,
               em.employee_name as salesman_name,
               s.opening_cash,
               s.closing_cash,
               s.total_sale_amount,
               s.cash_collected,
               s.card_upi_amount,
               s.credit_amount,
               s.cash_shortage,
               s.status
        FROM `tabShift` s
        LEFT JOIN `tabEmployee Master` em ON s.salesman = em.name
        WHERE {conditions}
        ORDER BY s.shift_date DESC
    """, as_dict=True)
    
    return columns, data
