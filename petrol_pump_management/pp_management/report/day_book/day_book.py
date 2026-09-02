import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "time", "fieldtype": "Data", "label": "Time", "width": 100},
        {"fieldname": "type", "fieldtype": "Data", "label": "Type", "width": 120},
        {"fieldname": "reference", "fieldtype": "Data", "label": "Reference", "width": 150},
        {"fieldname": "party", "fieldtype": "Data", "label": "Party", "width": 150},
        {"fieldname": "debit", "fieldtype": "Currency", "label": "Debit", "width": 120},
        {"fieldname": "credit", "fieldtype": "Currency", "label": "Credit", "width": 120},
        {"fieldname": "payment_mode", "fieldtype": "Data", "label": "Payment Mode", "width": 100},
    ]

    date = filters.get("date") if filters else None
    if not date:
        from frappe.utils import today
        date = today()

    data = []

    # Fuel Sales
    sales = frappe.db.sql("""
        SELECT creation, name, customer, amount, payment_mode
        FROM `tabFuel Sale`
        WHERE sale_date = %s AND docstatus = 1
        ORDER BY creation
    """, (date,), as_dict=True)
    for s in sales:
        data.append({"time": str(s.creation)[-8:], "type": "Fuel Sale", "reference": s.name,
                      "party": s.customer or "Cash Customer", "debit": 0, "credit": s.amount,
                      "payment_mode": s.payment_mode})

    # Credit Sales
    credit = frappe.db.sql("""
        SELECT creation, name, customer, amount
        FROM `tabCredit Sale Invoice`
        WHERE due_date = %s AND docstatus = 1
        ORDER BY creation
    """, (date,), as_dict=True)
    for c in credit:
        data.append({"time": str(c.creation)[-8:], "type": "Credit Sale", "reference": c.name,
                      "party": c.customer, "debit": c.amount, "credit": 0,
                      "payment_mode": "Credit"})

    # Payments Received
    payments = frappe.db.sql("""
        SELECT creation, name, customer, amount, mode
        FROM `tabPayment Receipt`
        WHERE DATE(received_on) = %s AND docstatus = 1
        ORDER BY creation
    """, (date,), as_dict=True)
    for p in payments:
        data.append({"time": str(p.creation)[-8:], "type": "Payment Received", "reference": p.name,
                      "party": p.customer, "debit": 0, "credit": p.amount,
                      "payment_mode": p.mode})

    # Expenses
    expenses = frappe.db.sql("""
        SELECT creation, name, expense_type, amount
        FROM `tabExpense Entry`
        WHERE expense_date = %s AND docstatus = 1
        ORDER BY creation
    """, (date,), as_dict=True)
    for e in expenses:
        data.append({"time": str(e.creation)[-8:], "type": "Expense", "reference": e.name,
                      "party": e.expense_type, "debit": e.amount, "credit": 0,
                      "payment_mode": ""})

    # Sort by time
    data.sort(key=lambda x: x.get("time", ""))

    return columns, data
