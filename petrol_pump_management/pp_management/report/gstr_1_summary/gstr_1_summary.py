import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "customer", "fieldtype": "Data", "label": "Customer / Party", "width": 200},
        {"fieldname": "gst_number", "fieldtype": "Data", "label": "GSTIN", "width": 150},
        {"fieldname": "invoice_count", "fieldtype": "Int", "label": "Invoice Count", "width": 100},
        {"fieldname": "taxable_value", "fieldtype": "Currency", "label": "Taxable Value", "width": 150},
        {"fieldname": "cgst", "fieldtype": "Currency", "label": "CGST", "width": 120},
        {"fieldname": "sgst", "fieldtype": "Currency", "label": "SGST", "width": 120},
        {"fieldname": "total", "fieldtype": "Currency", "label": "Total", "width": 150},
    ]
    conditions = "fs.docstatus = 1"
    if filters.get("from_date"):
        conditions += f" AND fs.sale_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND fs.sale_date <= '{filters['to_date']}'"

    rows = frappe.db.sql(f"""
        SELECT fs.customer, IFNULL(c.gst_number, '') as gst_number,
               COUNT(*) as invoice_count, SUM(fs.amount) as taxable_value
        FROM `tabFuel Sale` fs
        LEFT JOIN `tabPP Customer` c ON fs.customer = c.name
        WHERE {conditions} AND fs.payment_mode = 'Credit'
        GROUP BY fs.customer
        ORDER BY fs.customer
    """, as_dict=True)

    data = []
    for row in rows:
        cgst = (row.taxable_value or 0) * 0.06
        sgst = (row.taxable_value or 0) * 0.06
        data.append({
            "customer": row.customer,
            "gst_number": row.gst_number,
            "invoice_count": row.invoice_count,
            "taxable_value": row.taxable_value,
            "cgst": cgst,
            "sgst": sgst,
            "total": row.taxable_value + cgst + sgst,
        })

    # Grand total row
    if data:
        total_taxable = sum(d["taxable_value"] for d in data)
        total_cgst = sum(d["cgst"] for d in data)
        total_sgst = sum(d["sgst"] for d in data)
        data.append({
            "customer": "<b>Grand Total</b>",
            "gst_number": "",
            "invoice_count": sum(d["invoice_count"] for d in data),
            "taxable_value": total_taxable,
            "cgst": total_cgst,
            "sgst": total_sgst,
            "total": total_taxable + total_cgst + total_sgst,
        })

    return columns, data
