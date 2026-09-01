import frappe
from frappe import _

def execute(filters=None):
    columns = [{"fieldname":"decantation_datetime","fieldtype":"Datetime","label":"DateTime","width":160},{"fieldname":"tanker_no","fieldtype":"Data","label":"Tanker","width":120},{"fieldname":"tank","fieldtype":"Data","label":"Tank","width":100},{"fieldname":"density","fieldtype":"Currency","label":"Density","width":100},{"fieldname":"invoiced_qty","fieldtype":"Currency","label":"Invoiced","width":120},{"fieldname":"received_qty","fieldtype":"Currency","label":"Received","width":120},{"fieldname":"variation_pct","fieldtype":"Percent","label":"Variation %","width":100}]
    conditions = "1=1"
    if filters.get("from_date"):
        conditions += f" AND t.from_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND t.to_date >= '{filters['to_date']}'"
    data = frappe.db.sql(f"""
        SELECT decantation_datetime, tanker_no, tank, density, invoiced_qty, received_qty, variation_pct
        FROM `tabStock Purchase Decantation` t
        WHERE {conditions}
        ORDER BY 1 DESC
    """, as_dict=True)
    return columns, data
