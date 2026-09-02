import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "shift_date", "fieldtype": "Date", "label": "Date", "width": 100},
        {"fieldname": "employee_name", "fieldtype": "Data", "label": "Employee", "width": 150},
        {"fieldname": "opening_cash", "fieldtype": "Currency", "label": "Opening Cash", "width": 110},
        {"fieldname": "expected_collection", "fieldtype": "Currency", "label": "Expected Collection", "width": 130},
        {"fieldname": "actual_collection", "fieldtype": "Currency", "label": "Actual Collection", "width": 130},
        {"fieldname": "shortage", "fieldtype": "Currency", "label": "Shortage", "width": 100},
        {"fieldname": "status", "fieldtype": "Data", "label": "Status", "width": 80},
    ]

    from_date = filters.get("from_date") if filters else None
    to_date = filters.get("to_date") if filters else None
    employee = filters.get("employee") if filters else None

    conditions = "WHERE s.docstatus = 1"
    params = []
    if from_date:
        conditions += " AND s.shift_date >= %s"
        params.append(from_date)
    if to_date:
        conditions += " AND s.shift_date <= %s"
        params.append(to_date)
    if employee:
        conditions += " AND s.salesman = %s"
        params.append(employee)

    data = frappe.db.sql(f"""
        SELECT s.shift_date, em.employee_name,
               s.opening_cash,
               COALESCE(s.total_sale_amount, 0) as expected_collection,
               COALESCE(s.cash_collected, 0) as actual_collection,
               COALESCE(s.total_sale_amount, 0) - COALESCE(s.cash_collected, 0) as shortage,
               s.status
        FROM `tabShift` s
        LEFT JOIN `tabEmployee Master` em ON s.salesman = em.name
        {conditions}
        ORDER BY s.shift_date DESC, em.employee_name
    """, params, as_dict=True)

    # Add status coloring
    for row in data:
        if row.shortage and row.shortage > 0:
            row["status"] = "Shortage"
        elif row.shortage and row.shortage < 0:
            row["status"] = "Excess"
        else:
            row["status"] = "Balanced"

    return columns, data
