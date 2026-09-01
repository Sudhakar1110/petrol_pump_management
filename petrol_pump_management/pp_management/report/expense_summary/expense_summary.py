import frappe
from frappe import _

def execute(filters=None):
    columns = [{"fieldname":"expense_date","fieldtype":"Date","label":"Date","width":120},{"fieldname":"expense_type","fieldtype":"Data","label":"Type","width":150},{"fieldname":"amount","fieldtype":"Currency","label":"Amount","width":120},{"fieldname":"payment_method","fieldtype":"Data","label":"Payment","width":120},{"fieldname":"status","fieldtype":"Data","label":"Status","width":100}]
    conditions = "1=1"
    if filters.get("from_date"):
        conditions += f" AND t.from_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND t.to_date >= '{filters['to_date']}'"
    data = frappe.db.sql(f"""
        SELECT expense_date, expense_type, amount, payment_method, status
        FROM `tabExpense Entry` t
        WHERE {conditions}
        ORDER BY 1 DESC
    """, as_dict=True)
    return columns, data
