import frappe
from frappe import _

def execute(filters=None):
    columns = [
        {"fieldname":"name","fieldtype":"Link","label":"Shift ID","options":"Shift","width":120},
        {"fieldname":"shift_date","fieldtype":"Date","label":"Date","width":120},
        {"fieldname":"salesman","fieldtype":"Data","label":"Salesman","width":150},
        {"fieldname":"opening_cash","fieldtype":"Currency","label":"Opening Cash","width":120},
        {"fieldname":"closing_cash","fieldtype":"Currency","label":"Closing Cash","width":120},
        {"fieldname":"total_sale_amount","fieldtype":"Currency","label":"Total Sale","width":120},
        {"fieldname":"cash_collected","fieldtype":"Currency","label":"Cash Collected","width":120},
        {"fieldname":"card_upi_amount","fieldtype":"Currency","label":"Card/UPI","width":120},
        {"fieldname":"credit_amount","fieldtype":"Currency","label":"Credit","width":120},
        {"fieldname":"status","fieldtype":"Data","label":"Status","width":100},
    ]
    conditions = "1=1"
    if filters.get("from_date"):
        conditions += f" AND t.shift_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND t.shift_date <= '{filters['to_date']}'"
    data = frappe.db.sql(f"""
        SELECT name, shift_date, salesman, opening_cash, closing_cash,
               total_sale_amount, cash_collected, card_upi_amount, credit_amount, status
        FROM `tabShift` t
        WHERE {conditions} AND t.docstatus = 1
        ORDER BY 1 DESC
    """, as_dict=True)
    return columns, data
