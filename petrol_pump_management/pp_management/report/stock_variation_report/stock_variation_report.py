import frappe
from frappe import _

def execute(filters=None):
    columns = [{"fieldname":"date","fieldtype":"Date","label":"Date","width":120},{"fieldname":"tank","fieldtype":"Data","label":"Tank","width":100},{"fieldname":"opening_stock","fieldtype":"Currency","label":"Opening","width":120},{"fieldname":"purchase_qty","fieldtype":"Currency","label":"Purchase","width":120},{"fieldname":"sale_qty","fieldtype":"Currency","label":"Sale","width":120},{"fieldname":"closing_stock","fieldtype":"Currency","label":"Closing","width":120},{"fieldname":"variation","fieldtype":"Currency","label":"Variation","width":120}]
    conditions = "1=1"
    if filters.get("from_date"):
        conditions += f" AND t.from_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND t.to_date >= '{filters['to_date']}'"
    data = frappe.db.sql(f"""
        SELECT date, tank, opening_stock, purchase_qty, sale_qty, closing_stock, variation
        FROM `tabDaily Stock Register` t
        WHERE {conditions}
        ORDER BY 1 DESC
    """, as_dict=True)
    return columns, data
