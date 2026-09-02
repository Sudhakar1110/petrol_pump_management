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
               ds.opening_hand_cash as opening_cash,
               IFNULL(cash.total, 0) as cash_receipts,
               IFNULL(digi.total, 0) as digital_receipts,
               IFNULL(cred.total, 0) as credit_sales,
               IFNULL(exp.total, 0) as expenses,
               IFNULL(bd.total, 0) as bank_deposit,
               ds.closing_hand_cash as closing_cash
        FROM `tabDay Settlement` ds
        LEFT JOIN (
            SELECT sale_date, SUM(amount) as total
            FROM `tabFuel Sale`
            WHERE payment_mode = 'Cash' AND docstatus = 1
            GROUP BY sale_date
        ) cash ON cash.sale_date = ds.settlement_date
        LEFT JOIN (
            SELECT sale_date, SUM(amount) as total
            FROM `tabFuel Sale`
            WHERE payment_mode IN ('Card', 'UPI') AND docstatus = 1
            GROUP BY sale_date
        ) digi ON digi.sale_date = ds.settlement_date
        LEFT JOIN (
            SELECT sale_date, SUM(amount) as total
            FROM `tabFuel Sale`
            WHERE payment_mode = 'Credit' AND docstatus = 1
            GROUP BY sale_date
        ) cred ON cred.sale_date = ds.settlement_date
        LEFT JOIN (
            SELECT expense_date, SUM(amount) as total
            FROM `tabExpense Entry`
            WHERE docstatus = 1
            GROUP BY expense_date
        ) exp ON exp.expense_date = ds.settlement_date
        LEFT JOIN (
            SELECT deposit_date, SUM(amount) as total
            FROM `tabBank Deposit`
            WHERE docstatus = 1
            GROUP BY deposit_date
        ) bd ON bd.deposit_date = ds.settlement_date
        WHERE {conditions}
        ORDER BY ds.settlement_date DESC
    """, as_dict=True)

    return columns, data
