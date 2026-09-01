import frappe
from frappe import _

def execute(filters=None):
    columns = [{"fieldname":"sale_date","fieldtype":"Date","label":"Date","width":120},{"fieldname":"nozzle","fieldtype":"Data","label":"Nozzle","width":120},{"fieldname":"fuel_type","fieldtype":"Data","label":"Fuel Type","width":120},{"fieldname":"payment_mode","fieldtype":"Data","label":"Payment Mode","width":120},{"fieldname":"qty_litres","fieldtype":"Float","label":"Qty (L)","width":100},{"fieldname":"rate","fieldtype":"Currency","label":"Rate","width":100},{"fieldname":"amount","fieldtype":"Currency","label":"Amount","width":120}]
    conditions = "1=1"
    if filters.get("from_date"):
        conditions += f" AND t.from_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND t.to_date >= '{filters['to_date']}'"
    data = frappe.db.sql(f"""
        SELECT sale_date, nozzle, fuel_type, payment_mode, qty_litres, rate, amount
        FROM `tabFuel Sale` t
        WHERE {conditions}
        ORDER BY 1 DESC
    """, as_dict=True)
    return columns, data
