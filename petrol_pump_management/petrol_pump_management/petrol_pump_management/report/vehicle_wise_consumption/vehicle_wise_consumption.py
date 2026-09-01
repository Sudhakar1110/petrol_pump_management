import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "vehicle_number", "fieldtype": "Data", "label": "Vehicle", "width": 140},
        {"fieldname": "customer_name", "fieldtype": "Data", "label": "Customer", "width": 180},
        {"fieldname": "fuel_type", "fieldtype": "Data", "label": "Fuel Type", "width": 120},
        {"fieldname": "total_qty", "fieldtype": "Currency", "label": "Total Qty (L)", "width": 120},
        {"fieldname": "total_amount", "fieldtype": "Currency", "label": "Total Amount", "width": 140},
        {"fieldname": "sale_count", "fieldtype": "Int", "label": "Sales Count", "width": 100},
    ]
    conditions = "fs.docstatus = 1 AND fs.vehicle IS NOT NULL"
    if filters.get("from_date"):
        conditions += f" AND fs.sale_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND fs.sale_date <= '{filters['to_date']}'"
    data = frappe.db.sql(f"""
        SELECT vm.vehicle_number, pp.full_name as customer_name, tm.fuel_type,
               SUM(fs.qty_litres) as total_qty,
               SUM(fs.amount) as total_amount,
               COUNT(fs.name) as sale_count
        FROM `tabFuel Sale` fs
        LEFT JOIN `tabVehicle Master` vm ON fs.vehicle = vm.name
        LEFT JOIN `tabPP Customer` pp ON vm.customer = pp.name
        LEFT JOIN `tabNozzle Master` nm ON fs.nozzle = nm.name
        LEFT JOIN `tabTank Master` tm ON nm.tank = tm.name
        WHERE {conditions}
        GROUP BY fs.vehicle
        ORDER BY total_amount DESC
    """, as_dict=True)
    return columns, data