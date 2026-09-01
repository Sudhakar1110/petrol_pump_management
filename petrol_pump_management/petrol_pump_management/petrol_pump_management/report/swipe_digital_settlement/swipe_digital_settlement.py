import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "sale_date", "fieldtype": "Date", "label": "Date", "width": 120},
        {"fieldname": "payment_mode", "fieldtype": "Data", "label": "Payment Mode", "width": 120},
        {"fieldname": "total_sales", "fieldtype": "Currency", "label": "Total Sales", "width": 140},
        {"fieldname": "sale_count", "fieldtype": "Int", "label": "Transactions", "width": 100},
        {"fieldname": "avg_amount", "fieldtype": "Currency", "label": "Avg Amount", "width": 120},
    ]
    conditions = "fs.docstatus = 1 AND fs.payment_mode IN ('Card', 'UPI', 'Petro-card')"
    if filters.get("from_date"):
        conditions += f" AND fs.sale_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND fs.sale_date <= '{filters['to_date']}'"
    data = frappe.db.sql(f"""
        SELECT fs.sale_date, fs.payment_mode,
               SUM(fs.amount) as total_sales,
               COUNT(fs.name) as sale_count,
               AVG(fs.amount) as avg_amount
        FROM `tabFuel Sale` fs
        WHERE {conditions}
        GROUP BY fs.sale_date, fs.payment_mode
        ORDER BY fs.sale_date DESC, fs.payment_mode
    """, as_dict=True)
    return columns, data