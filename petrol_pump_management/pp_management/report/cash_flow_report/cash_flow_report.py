import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "date", "fieldtype": "Date", "label": "Date", "width": 120},
        {"fieldname": "opening_cash", "fieldtype": "Currency", "label": "Opening Cash", "width": 120},
        {"fieldname": "cash_receipts", "fieldtype": "Currency", "label": "Cash Receipts", "width": 120},
        {"fieldname": "digital_receipts", "fieldtype": "Currency", "label": "Digital Receipts", "width": 120},
        {"fieldname": "credit_sales", "fieldtype": "Currency", "label": "Credit Sales", "width": 120},
        {"fieldname": "expenses", "fieldtype": "Currency", "label": "Expenses", "width": 120},
        {"fieldname": "bank_deposit", "fieldtype": "Currency", "label": "Bank Deposit", "width": 120},
        {"fieldname": "closing_cash", "fieldtype": "Currency", "label": "Closing Cash", "width": 120},
    ]
    conditions = "1=1"
    if filters.get("from_date"):
        conditions += f" AND ds.settlement_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND ds.settlement_date <= '{filters['to_date']}'"

    data = frappe.db.sql(f"""
        SELECT ds.settlement_date as date,
               ds.opening_cash,
               IFNULL(fs_cash.total, 0) as cash_receipts,
               IFNULL(fs_digi.total, 0) as digital_receipts,
               IFNULL(fs_credit.total, 0) as credit_sales,
               IFNULL(exp.total, 0) as expenses,
               IFNULL(bd.total, 0) as bank_deposit,
               ds.closing_cash
        FROM `tabDay Settlement` ds
        LEFT JOIN (SELECT shift, SUM(amount) as total FROM `tabFuel Sale` WHERE payment_mode='Cash' AND docstatus=1 GROUP BY shift) fs_cash ON fs_cash.shift = ds.name
        LEFT JOIN (SELECT shift, SUM(amount) as total FROM `tabFuel Sale` WHERE payment_mode IN ('Card','UPI') AND docstatus=1 GROUP BY shift) fs_digi ON fs_digi.shift = ds.name
        LEFT JOIN (SELECT shift, SUM(amount) as total FROM `tabFuel Sale` WHERE payment_mode='Credit' AND docstatus=1 GROUP BY shift) fs_credit ON fs_credit.shift = ds.name
        LEFT JOIN (SELECT shift, SUM(amount) as total FROM `tabExpense Entry` WHERE shift=ds.name GROUP BY shift) exp ON 1=1
        LEFT JOIN (SELECT shift_link, SUM(amount) as total FROM `tabBank Deposit` GROUP BY shift_link) bd ON bd.shift_link = ds.name
        WHERE {conditions}
        ORDER BY ds.settlement_date DESC
    """, as_dict=True)

    return columns, data
