import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "month", "fieldtype": "Data", "label": "Month", "width": 120},
        {"fieldname": "fuel_type", "fieldtype": "Data", "label": "Fuel Type", "width": 120},
        {"fieldname": "total_taxable", "fieldtype": "Currency", "label": "Total Taxable", "width": 140},
        {"fieldname": "cgst", "fieldtype": "Currency", "label": "CGST", "width": 120},
        {"fieldname": "sgst", "fieldtype": "Currency", "label": "SGST", "width": 120},
        {"fieldname": "total_with_tax", "fieldtype": "Currency", "label": "Total with Tax", "width": 140},
    ]
    conditions = "fs.docstatus = 1"
    if filters.get("from_date"):
        conditions += f" AND fs.sale_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND fs.sale_date <= '{filters['to_date']}'"
    data = frappe.db.sql(f"""
        SELECT DATE_FORMAT(fs.sale_date, '%%Y-%%m') as month,
               tm.fuel_type,
               SUM(fs.amount) as total_taxable,
               SUM(fs.amount * 0.09) as cgst,
               SUM(fs.amount * 0.09) as sgst,
               SUM(fs.amount * 1.18) as total_with_tax
        FROM `tabFuel Sale` fs
        LEFT JOIN `tabNozzle Master` nm ON fs.nozzle = nm.name
        LEFT JOIN `tabTank Master` tm ON nm.tank = tm.name
        WHERE {conditions}
        GROUP BY DATE_FORMAT(fs.sale_date, '%%Y-%%m'), tm.fuel_type
        ORDER BY month DESC, tm.fuel_type
    """, as_dict=True)
    return columns, data