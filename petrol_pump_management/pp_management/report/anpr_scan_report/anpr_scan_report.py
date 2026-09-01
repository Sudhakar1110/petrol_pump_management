import frappe
from frappe import _

def execute(filters=None):
    columns = [{"fieldname":"scan_datetime","fieldtype":"Datetime","label":"Scan Time","width":160},{"fieldname":"captured_plate","fieldtype":"Data","label":"Plate","width":120},{"fieldname":"camera_id","fieldtype":"Data","label":"Camera","width":100},{"fieldname":"matched_vehicle","fieldtype":"Data","label":"Vehicle","width":120},{"fieldname":"confidence_score","fieldtype":"Percent","label":"Confidence","width":100},{"fieldname":"action_taken","fieldtype":"Data","label":"Action","width":120}]
    conditions = "1=1"
    if filters.get("from_date"):
        conditions += f" AND t.from_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND t.to_date >= '{filters['to_date']}'"
    data = frappe.db.sql(f"""
        SELECT scan_datetime, captured_plate, camera_id, matched_vehicle, confidence_score, action_taken
        FROM `tabANPR Scan Log` t
        WHERE {conditions}
        ORDER BY 1 DESC
    """, as_dict=True)
    return columns, data
