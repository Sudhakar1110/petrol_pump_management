import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "date", "fieldtype": "Date", "label": "Date", "width": 120},
        {"fieldname": "tank_no", "fieldtype": "Data", "label": "Tank", "width": 100},
        {"fieldname": "fuel_type", "fieldtype": "Data", "label": "Fuel Type", "width": 120},
        {"fieldname": "opening_stock", "fieldtype": "Currency", "label": "Opening Stock", "width": 120},
        {"fieldname": "purchase_qty", "fieldtype": "Currency", "label": "Purchase", "width": 120},
        {"fieldname": "sale_qty", "fieldtype": "Currency", "label": "Sale", "width": 120},
        {"fieldname": "closing_stock", "fieldtype": "Currency", "label": "Closing Stock", "width": 120},
        {"fieldname": "dip_closing_stock", "fieldtype": "Currency", "label": "Dip Stock", "width": 120},
        {"fieldname": "variation", "fieldtype": "Currency", "label": "Variation", "width": 120},
    ]
    
    conditions = "1=1"
    if filters.get("from_date"):
        conditions += f" AND dsr.date >= '{filters.from_date}'"
    if filters.get("to_date"):
        conditions += f" AND dsr.date <= '{filters.to_date}'"
    if filters.get("tank"):
        conditions += f" AND dsr.tank = '{filters.tank}'"
    
    data = frappe.db.sql(f"""
        SELECT dsr.date, tm.tank_no, tm.fuel_type,
               dsr.opening_stock, dsr.purchase_qty, dsr.sale_qty,
               dsr.closing_stock, dsr.dip_closing_stock, dsr.variation
        FROM `tabDaily Stock Register` dsr
        LEFT JOIN `tabTank Master` tm ON dsr.tank = tm.name
        WHERE {conditions}
        ORDER BY dsr.date DESC, tm.tank_no
    """, as_dict=True)
    
    return columns, data
