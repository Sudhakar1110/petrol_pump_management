import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "hsn_code", "fieldtype": "Data", "label": "HSN Code", "width": 120},
        {"fieldname": "fuel_type", "fieldtype": "Data", "label": "Product Description", "width": 180},
        {"fieldname": "uom", "fieldtype": "Data", "label": "UOM", "width": 80},
        {"fieldname": "qty", "fieldtype": "Float", "label": "Quantity", "width": 120},
        {"fieldname": "taxable_value", "fieldtype": "Currency", "label": "Taxable Value", "width": 150},
        {"fieldname": "cgst", "fieldtype": "Currency", "label": "CGST", "width": 120},
        {"fieldname": "sgst", "fieldtype": "Currency", "label": "SGST", "width": 120},
        {"fieldname": "total", "fieldtype": "Currency", "label": "Total", "width": 150},
    ]
    conditions = "docstatus = 1"
    if filters.get("from_date"):
        conditions += f" AND sale_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND sale_date <= '{filters['to_date']}'"

    # HSN codes for common fuel types
    hsn_map = {
        "Petrol": "27101200",
        "Diesel": "27101920",
        "Premium": "27101200",
        "CNG": "27111100",
        "LPG": "27111900",
    }

    rows = frappe.db.sql(f"""
        SELECT fuel_type, SUM(qty_litres) as qty, SUM(amount) as taxable_value
        FROM `tabFuel Sale`
        WHERE {conditions}
        GROUP BY fuel_type
        ORDER BY fuel_type
    """, as_dict=True)

    data = []
    for row in rows:
        ft = row.fuel_type or "Other"
        hsn = hsn_map.get(ft, "27101990")
        cgst = (row.taxable_value or 0) * 0.06
        sgst = (row.taxable_value or 0) * 0.06
        data.append({
            "hsn_code": hsn,
            "fuel_type": ft,
            "uom": "Litre",
            "qty": row.qty,
            "taxable_value": row.taxable_value,
            "cgst": cgst,
            "sgst": sgst,
            "total": row.taxable_value + cgst + sgst,
        })

    return columns, data
