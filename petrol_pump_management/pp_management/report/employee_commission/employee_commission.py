import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "employee", "fieldtype": "Data", "label": "Employee", "width": 180},
        {"fieldname": "shifts_worked", "fieldtype": "Int", "label": "Shifts Worked", "width": 100},
        {"fieldname": "total_litres", "fieldtype": "Float", "label": "Total Litres", "width": 120},
        {"fieldname": "total_sale", "fieldtype": "Currency", "label": "Total Sale Amount", "width": 150},
        {"fieldname": "commission", "fieldtype": "Currency", "label": "Commission", "width": 120},
    ]
    conditions = "1=1"
    if filters.get("from_date"):
        conditions += f" AND s.shift_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND s.shift_date <= '{filters['to_date']}'"
    if filters.get("employee"):
        conditions += f" AND s.salesman = '{filters['employee']}'"

    data = frappe.db.sql(f"""
        SELECT s.salesman as employee,
               COUNT(DISTINCT s.name) as shifts_worked,
               IFNULL(SUM(fs.qty_litres), 0) as total_litres,
               IFNULL(SUM(fs.amount), 0) as total_sale
        FROM `tabShift` s
        LEFT JOIN `tabFuel Sale` fs ON fs.shift = s.name AND fs.docstatus = 1
        WHERE {conditions} AND s.docstatus = 1
        GROUP BY s.salesman
        ORDER BY s.salesman
    """, as_dict=True)

    # Simple commission: 0.50 per litre
    for row in data:
        row.commission = (row.total_litres or 0) * 0.50

    return columns, data
