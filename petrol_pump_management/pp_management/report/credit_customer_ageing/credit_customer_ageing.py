import frappe
from frappe import _

def execute(filters=None):
    columns = [{"fieldname":"customer","fieldtype":"Data","label":"Customer","width":180},{"fieldname":"amount","fieldtype":"Currency","label":"Amount","width":120},{"fieldname":"amount_paid","fieldtype":"Currency","label":"Paid","width":120},{"fieldname":"due_date","fieldtype":"Date","label":"Due Date","width":120},{"fieldname":"status","fieldtype":"Data","label":"Status","width":100}]
    conditions = "1=1"

    data = frappe.db.sql(f"""
        SELECT customer, amount, amount_paid, due_date, status
        FROM `tabCredit Sale Invoice` t
        WHERE {conditions}
        ORDER BY 1 DESC
    """, as_dict=True)
    return columns, data
