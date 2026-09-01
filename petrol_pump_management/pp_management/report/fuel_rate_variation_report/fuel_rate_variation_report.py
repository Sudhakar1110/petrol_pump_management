import frappe
from frappe import _

def execute(filters=None):
    columns = [{"fieldname":"effective_from","fieldtype":"Datetime","label":"Effective From","width":160},{"fieldname":"fuel_type","fieldtype":"Data","label":"Fuel Type","width":120},{"fieldname":"previous_rate","fieldtype":"Currency","label":"Previous Rate","width":120},{"fieldname":"rate_per_litre","fieldtype":"Currency","label":"New Rate","width":120},{"fieldname":"revised_by","fieldtype":"Data","label":"Revised By","width":150}]
    conditions = "1=1"

    data = frappe.db.sql(f"""
        SELECT effective_from, fuel_type, previous_rate, rate_per_litre, revised_by
        FROM `tabFuel Price Master` t
        WHERE {conditions}
        ORDER BY 1 DESC
    """, as_dict=True)
    return columns, data
