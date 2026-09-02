import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "date", "fieldtype": "Date", "label": "Date", "width": 100},
        {"fieldname": "purchase_id", "fieldtype": "Data", "label": "Purchase ID", "width": 150},
        {"fieldname": "tanker_no", "fieldtype": "Data", "label": "Tanker No", "width": 100},
        {"fieldname": "supplier", "fieldtype": "Data", "label": "Supplier", "width": 150},
        {"fieldname": "fuel_type", "fieldtype": "Data", "label": "Fuel Type", "width": 100},
        {"fieldname": "invoiced_qty", "fieldtype": "Float", "label": "Invoiced Qty (L)", "width": 120},
        {"fieldname": "received_qty", "fieldtype": "Float", "label": "Received Qty (L)", "width": 120},
        {"fieldname": "variation", "fieldtype": "Float", "label": "Variation (L)", "width": 100},
        {"fieldname": "match_status", "fieldtype": "Data", "label": "Status", "width": 100},
    ]

    from_date = filters.get("from_date") if filters else None
    to_date = filters.get("to_date") if filters else None

    conditions = "WHERE docstatus = 1"
    params = []
    if from_date:
        conditions += " AND decantation_datetime >= %s"
        params.append(from_date)
    if to_date:
        conditions += " AND decantation_datetime <= %s"
        params.append(to_date)

    data = frappe.db.sql(f"""
        SELECT DATE(decantation_datetime) as date, name as purchase_id,
               tanker_no, supplier, fuel_type, invoiced_qty, received_qty,
               variation_pct,
               CASE
                   WHEN ABS(invoiced_qty - received_qty) < 1 THEN 'Matched'
                   ELSE 'Unmatched'
               END as match_status
        FROM `tabStock Purchase Decantation`
        {conditions}
        ORDER BY decantation_datetime DESC
    """, params, as_dict=True)

    for row in data:
        row["variation"] = (row.get("invoiced_qty") or 0) - (row.get("received_qty") or 0)

    return columns, data
