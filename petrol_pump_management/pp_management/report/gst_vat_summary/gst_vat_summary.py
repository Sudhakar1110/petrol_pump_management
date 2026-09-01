import frappe
from frappe import _

def execute(filters=None):
    columns = [{"fieldname":"sale_date","fieldtype":"Date","label":"Date","width":120},{"fieldname":"fuel_type","fieldtype":"Data","label":"Fuel Type","width":120},{"fieldname":"amount","fieldtype":"Currency","label":"Taxable Amount","width":140},{"fieldname":"cgst","fieldtype":"Currency","label":"CGST","width":120},{"fieldname":"sgst","fieldtype":"Currency","label":"SGST","width":120}]
    conditions = "1=1"
    if filters.get("from_date"):
        conditions += f" AND t.from_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND t.to_date >= '{filters['to_date']}'"
    data = frappe.db.sql(f"""
        SELECT sale_date, fuel_type, amount, cgst, sgst
        FROM `tabFuel Sale` t
        WHERE {conditions}
        ORDER BY 1 DESC
    """, as_dict=True)
    return columns, data
