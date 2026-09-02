import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "date", "fieldtype": "Date", "label": "Export Date", "width": 120},
        {"fieldname": "export_type", "fieldtype": "Data", "label": "Type", "width": 120},
        {"fieldname": "period_from", "fieldtype": "Date", "label": "Period From", "width": 120},
        {"fieldname": "period_to", "fieldtype": "Date", "label": "Period To", "width": 120},
        {"fieldname": "records", "fieldtype": "Int", "label": "Records", "width": 100},
        {"fieldname": "status", "fieldtype": "Data", "label": "Status", "width": 120},
    ]
    conditions = "1=1"
    if filters.get("from_date"):
        conditions += f" AND export_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND export_date <= '{filters['to_date']}'"
    if filters.get("export_type") and filters.get("export_type") != "All":
        conditions += f" AND export_type = '{filters['export_type']}'"

    data = frappe.db.sql(f"""
        SELECT export_date as date, export_type, period_from, period_to,
               records_exported as records, export_status as status
        FROM `tabTally Export Log`
        WHERE {conditions}
        ORDER BY export_date DESC
    """, as_dict=True)

    return columns, data
