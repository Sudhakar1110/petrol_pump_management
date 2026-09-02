import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "nozzle", "fieldtype": "Data", "label": "Nozzle", "width": 120},
        {"fieldname": "fuel_type", "fieldtype": "Data", "label": "Fuel Type", "width": 100},
        {"fieldname": "total_sales", "fieldtype": "Int", "label": "No. of Sales", "width": 80},
        {"fieldname": "total_qty", "fieldtype": "Float", "label": "Total Qty (L)", "width": 120},
        {"fieldname": "total_amount", "fieldtype": "Currency", "label": "Total Amount", "width": 120},
        {"fieldname": "avg_rate", "fieldtype": "Currency", "label": "Avg Rate", "width": 100},
        {"fieldname": "cash_amount", "fieldtype": "Currency", "label": "Cash", "width": 100},
        {"fieldname": "credit_amount", "fieldtype": "Currency", "label": "Credit", "width": 100},
        {"fieldname": "card_upi_amount", "fieldtype": "Currency", "label": "Card/UPI", "width": 100},
    ]

    from_date = filters.get("from_date") if filters else None
    to_date = filters.get("to_date") if filters else None
    nozzle = filters.get("nozzle") if filters else None

    conditions = "WHERE fs.docstatus = 1"
    params = []
    if from_date:
        conditions += " AND fs.sale_date >= %s"
        params.append(from_date)
    if to_date:
        conditions += " AND fs.sale_date <= %s"
        params.append(to_date)
    if nozzle:
        conditions += " AND fs.nozzle = %s"
        params.append(nozzle)

    data = frappe.db.sql(f"""
        SELECT fs.nozzle, tm.fuel_type,
               COUNT(*) as total_sales,
               SUM(fs.qty_litres) as total_qty,
               SUM(fs.amount) as total_amount,
               ROUND(SUM(fs.amount)/NULLIF(SUM(fs.qty_litres),0), 2) as avg_rate,
               SUM(CASE WHEN fs.payment_mode = 'Cash' THEN fs.amount ELSE 0 END) as cash_amount,
               SUM(CASE WHEN fs.payment_mode = 'Credit' THEN fs.amount ELSE 0 END) as credit_amount,
               SUM(CASE WHEN fs.payment_mode IN ('Card','UPI') THEN fs.amount ELSE 0 END) as card_upi_amount
        FROM `tabFuel Sale` fs
        LEFT JOIN `tabNozzle Master` nm ON fs.nozzle = nm.name
        LEFT JOIN `tabTank Master` tm ON nm.tank = tm.name
        {conditions}
        GROUP BY fs.nozzle, tm.fuel_type
        ORDER BY fs.nozzle
    """, params, as_dict=True)

    return columns, data
