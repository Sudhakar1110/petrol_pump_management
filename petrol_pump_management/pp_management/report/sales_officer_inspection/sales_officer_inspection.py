import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "date", "fieldtype": "Date", "label": "Date", "width": 100},
        {"fieldname": "inspector", "fieldtype": "Data", "label": "Inspector", "width": 150},
        {"fieldname": "tank", "fieldtype": "Data", "label": "Tank", "width": 100},
        {"fieldname": "fuel_type", "fieldtype": "Data", "label": "Fuel Type", "width": 100},
        {"fieldname": "dip_reading", "fieldtype": "Float", "label": "Dip Reading (cm)", "width": 110},
        {"fieldname": "density", "fieldtype": "Float", "label": "Density", "width": 80},
        {"fieldname": "temperature", "fieldtype": "Float", "label": "Temp (C)", "width": 80},
        {"fieldname": "stock_at_dip", "fieldtype": "Float", "label": "Stock at Dip (L)", "width": 110},
        {"fieldname": "variation", "fieldtype": "Float", "label": "Variation (L)", "width": 100},
        {"fieldname": "remarks", "fieldtype": "Data", "label": "Remarks", "width": 150},
    ]

    from_date = filters.get("from_date") if filters else None
    to_date = filters.get("to_date") if filters else None
    inspector = filters.get("inspector") if filters else None

    conditions = "WHERE 1=1"
    params = []
    if from_date:
        conditions += " AND inspection_date >= %s"
        params.append(from_date)
    if to_date:
        conditions += " AND inspection_date <= %s"
        params.append(to_date)
    if inspector:
        conditions += " AND inspector = %s"
        params.append(inspector)

    data = frappe.db.sql(f"""
        SELECT inspection_date as date, em.employee_name as inspector,
               tank, fuel_type, dip_reading, density, temperature,
               stock_at_dip, variation, remarks
        FROM `tabStation Inspection` soi
        LEFT JOIN `tabEmployee Master` em ON soi.inspector = em.name
        {conditions}
        ORDER BY inspection_date DESC
    """, params, as_dict=True)

    return columns, data
