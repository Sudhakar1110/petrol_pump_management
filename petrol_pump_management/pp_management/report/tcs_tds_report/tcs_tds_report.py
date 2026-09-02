import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "entry_type", "fieldtype": "Data", "label": "Type", "width": 60},
        {"fieldname": "date", "fieldtype": "Date", "label": "Date", "width": 100},
        {"fieldname": "party_name", "fieldtype": "Data", "label": "Party", "width": 150},
        {"fieldname": "pan", "fieldtype": "Data", "label": "PAN", "width": 100},
        {"fieldname": "gross_amount", "fieldtype": "Currency", "label": "Gross Amount", "width": 120},
        {"fieldname": "tax_rate", "fieldtype": "Float", "label": "Tax Rate %", "width": 80},
        {"fieldname": "tax_amount", "fieldtype": "Currency", "label": "Tax Amount", "width": 120},
        {"fieldname": "net_amount", "fieldtype": "Currency", "label": "Net Amount", "width": 120},
        {"fieldname": "status", "fieldtype": "Data", "label": "Status", "width": 80},
    ]

    tax_type = filters.get("tax_type") if filters else "Both"
    from_date = filters.get("from_date") if filters else None
    to_date = filters.get("to_date") if filters else None

    data = []

    # TCS entries
    if tax_type in ("TCS", "Both"):
        tcs_data = frappe.db.sql("""
            SELECT 'TCS' as entry_type, transaction_date as date,
                   buyer_name as party_name, buyer_pan as pan,
                   gross_amount, tcs_rate as tax_rate, tcs_amount as tax_amount,
                   net_amount, status
            FROM `tabTCS Statement`
            ORDER BY transaction_date DESC
        """, as_dict=True)
        data.extend(tcs_data)

    # TDS entries
    if tax_type in ("TDS", "Both"):
        tds_data = frappe.db.sql("""
            SELECT 'TDS' as entry_type, payment_date as date,
                   payee_name as party_name, payee_pan as pan,
                   gross_amount, tds_rate as tax_rate, tds_amount as tax_amount,
                   net_amount, status
            FROM `tabTDS Statement`
            ORDER BY payment_date DESC
        """, as_dict=True)
        data.extend(tds_data)

    data.sort(key=lambda x: x.get("date") or "", reverse=True)

    return columns, data
