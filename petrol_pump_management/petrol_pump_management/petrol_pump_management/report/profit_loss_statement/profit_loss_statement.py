import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "month", "fieldtype": "Data", "label": "Month", "width": 120},
        {"fieldname": "fuel_type", "fieldtype": "Data", "label": "Fuel Type", "width": 120},
        {"fieldname": "total_sales", "fieldtype": "Currency", "label": "Total Sales", "width": 140},
        {"fieldname": "total_purchase", "fieldtype": "Currency", "label": "Total Purchase", "width": 140},
        {"fieldname": "gross_margin", "fieldtype": "Currency", "label": "Gross Margin", "width": 120},
        {"fieldname": "margin_pct", "fieldtype": "Percent", "label": "Margin %", "width": 100},
    ]
    conditions = "fs.docstatus = 1"
    if filters.get("from_date"):
        conditions += f" AND fs.sale_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND fs.sale_date <= '{filters['to_date']}'"
    data = frappe.db.sql(f"""
        SELECT DATE_FORMAT(fs.sale_date, '%%Y-%%m') as month,
               tm.fuel_type,
               SUM(fs.amount) as total_sales,
               0 as total_purchase,
               SUM(fs.amount) as gross_margin,
               0 as margin_pct
        FROM `tabFuel Sale` fs
        LEFT JOIN `tabNozzle Master` nm ON fs.nozzle = nm.name
        LEFT JOIN `tabTank Master` tm ON nm.tank = tm.name
        WHERE {conditions}
        GROUP BY DATE_FORMAT(fs.sale_date, '%%Y-%%m'), tm.fuel_type
        ORDER BY month DESC
    """, as_dict=True)
    return columns, data