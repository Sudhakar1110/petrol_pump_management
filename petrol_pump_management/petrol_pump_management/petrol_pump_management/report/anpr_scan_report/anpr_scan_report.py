import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "scan_datetime", "fieldtype": "Datetime", "label": "Scan Time", "width": 160},
        {"fieldname": "captured_plate", "fieldtype": "Data", "label": "Plate", "width": 120},
        {"fieldname": "camera_id", "fieldtype": "Data", "label": "Camera", "width": 100},
        {"fieldname": "matched_vehicle", "fieldtype": "Data", "label": "Vehicle", "width": 120},
        {"fieldname": "matched_customer_name", "fieldtype": "Data", "label": "Customer", "width": 150},
        {"fieldname": "confidence_score", "fieldtype": "Percent", "label": "Confidence", "width": 100},
        {"fieldname": "action_taken", "fieldtype": "Data", "label": "Action", "width": 120},
    ]
    conditions = "1=1"
    if filters.get("from_date"):
        conditions += f" AND scan_datetime >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND scan_datetime <= '{filters['to_date']} 23:59:59'"
    data = frappe.db.sql(f"""
        SELECT scan_datetime, captured_plate, camera_id,
               matched_vehicle, matched_customer_name,
               confidence_score, action_taken
        FROM `tabANPR Scan Log`
        WHERE {conditions}
        ORDER BY scan_datetime DESC
    """, as_dict=True)
    return columns, data