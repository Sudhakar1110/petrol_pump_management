import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "decantation_datetime", "fieldtype": "Datetime", "label": "Date/Time", "width": 160},
        {"fieldname": "tanker_no", "fieldtype": "Data", "label": "Tanker", "width": 120},
        {"fieldname": "tank_no", "fieldtype": "Data", "label": "Tank", "width": 100},
        {"fieldname": "fuel_type", "fieldtype": "Data", "label": "Fuel Type", "width": 120},
        {"fieldname": "density", "fieldtype": "Currency", "label": "Density", "width": 100},
        {"fieldname": "invoiced_qty", "fieldtype": "Currency", "label": "Invoiced Qty", "width": 120},
        {"fieldname": "received_qty", "fieldtype": "Currency", "label": "Received Qty", "width": 120},
        {"fieldname": "variation_pct", "fieldtype": "Percent", "label": "Variation %", "width": 100},
    ]
    conditions = "spd.docstatus = 1"
    if filters.get("from_date"):
        conditions += f" AND spd.decantation_datetime >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND spd.decantation_datetime <= '{filters['to_date']} 23:59:59'"
    data = frappe.db.sql(f"""
        SELECT spd.decantation_datetime, spd.tanker_no, tm.tank_no, tm.fuel_type,
               spd.density, spd.invoiced_qty, spd.received_qty, spd.variation_pct
        FROM `tabStock Purchase Decantation` spd
        LEFT JOIN `tabTank Master` tm ON spd.tank = tm.name
        WHERE {conditions}
        ORDER BY spd.decantation_datetime DESC
    """, as_dict=True)
    return columns, data