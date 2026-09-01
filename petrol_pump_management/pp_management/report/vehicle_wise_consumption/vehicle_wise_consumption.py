import frappe
from frappe import _

def execute(filters=None):
    columns = [{"fieldname":"vehicle","fieldtype":"Data","label":"Vehicle","width":140},{"fieldname":"customer","fieldtype":"Data","label":"Customer","width":180},{"fieldname":"fuel_type","fieldtype":"Data","label":"Fuel Type","width":120},{"fieldname":"qty_litres","fieldtype":"Currency","label":"Qty (L)","width":120},{"fieldname":"amount","fieldtype":"Currency","label":"Amount","width":140}]
    conditions = "1=1"
    if filters.get("from_date"):
        conditions += f" AND t.from_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND t.to_date >= '{filters['to_date']}'"
    data = frappe.db.sql(f"""
        SELECT vehicle, customer, fuel_type, qty_litres, amount
        FROM `tabFuel Sale` t
        WHERE {conditions}
        ORDER BY 1 DESC
    """, as_dict=True)
    return columns, data
