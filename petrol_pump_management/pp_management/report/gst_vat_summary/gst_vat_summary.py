import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"fieldname":"sale_date","fieldtype":"Date","label":"Date","width":120},
        {"fieldname":"fuel_type","fieldtype":"Data","label":"Fuel Type","width":120},
        {"fieldname":"amount","fieldtype":"Currency","label":"Taxable Amount","width":140},
        {"fieldname":"cgst","fieldtype":"Currency","label":"CGST (6%)","width":120},
        {"fieldname":"sgst","fieldtype":"Currency","label":"SGST (6%)","width":120},
        {"fieldname":"total","fieldtype":"Currency","label":"Total","width":140},
    ]
    conditions = "1=1"
    if filters.get("from_date"):
        conditions += f" AND t.sale_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND t.sale_date <= '{filters['to_date']}'"
    rows = frappe.db.sql(f"""
        SELECT sale_date, fuel_type, amount
        FROM `tabFuel Sale` t
        WHERE {conditions} AND t.docstatus = 1
        ORDER BY 1 DESC
    """, as_dict=True)
    data = []
    for row in rows:
        cgst = row.amount * 0.06
        sgst = row.amount * 0.06
        data.append({
            "sale_date": row.sale_date,
            "fuel_type": row.fuel_type,
            "amount": row.amount,
            "cgst": cgst,
            "sgst": sgst,
            "total": row.amount + cgst + sgst,
        })
    return columns, data
