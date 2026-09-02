import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "description", "fieldtype": "Data", "label": "Description", "width": 300},
        {"fieldname": "taxable_value", "fieldtype": "Currency", "label": "Taxable Value", "width": 150},
        {"fieldname": "cgst", "fieldtype": "Currency", "label": "CGST (6%)", "width": 120},
        {"fieldname": "sgst", "fieldtype": "Currency", "label": "SGST (6%)", "width": 120},
        {"fieldname": "total_tax", "fieldtype": "Currency", "label": "Total Tax", "width": 150},
    ]
    conditions = "docstatus = 1"
    if filters.get("from_date"):
        conditions += f" AND sale_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND sale_date <= '{filters['to_date']}'"

    total = frappe.db.sql(f"""
        SELECT SUM(amount) as total_taxable
        FROM `tabFuel Sale`
        WHERE {conditions}
    """, as_dict=True)

    total_taxable = total[0].total_taxable or 0
    cgst = total_taxable * 0.06
    sgst = total_taxable * 0.06

    data = [
        {"description": "3.1(a) Outward taxable supplies (other than zero rated, nil rated and exempted)", "taxable_value": total_taxable, "cgst": cgst, "sgst": sgst, "total_tax": cgst + sgst},
        {"description": "3.1(b) Outward taxable supplies (zero rated)", "taxable_value": 0, "cgst": 0, "sgst": 0, "total_tax": 0},
        {"description": "3.1(c) Other outward supplies (nil rated, exempted)", "taxable_value": 0, "cgst": 0, "sgst": 0, "total_tax": 0},
        {"description": "3.2(a) Inward supplies liable to reverse charge", "taxable_value": 0, "cgst": 0, "sgst": 0, "total_tax": 0},
        {"description": "4. Eligible ITC - Total", "taxable_value": 0, "cgst": 0, "sgst": 0, "total_tax": 0},
        {"description": "<b>5. Tax Payable</b>", "taxable_value": total_taxable, "cgst": cgst, "sgst": sgst, "total_tax": cgst + sgst},
    ]

    return columns, data
