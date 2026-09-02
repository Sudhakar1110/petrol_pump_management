import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "employee_name", "fieldtype": "Data", "label": "Employee", "width": 150},
        {"fieldname": "total_shifts", "fieldtype": "Int", "label": "Shifts", "width": 60},
        {"fieldname": "total_expected", "fieldtype": "Currency", "label": "Total Expected", "width": 120},
        {"fieldname": "total_actual", "fieldtype": "Currency", "label": "Total Actual", "width": 120},
        {"fieldname": "total_shortage", "fieldtype": "Currency", "label": "Total Shortage", "width": 120},
        {"fieldname": "avg_shortage", "fieldtype": "Currency", "label": "Avg Shortage/Shift", "width": 130},
    ]

    pay_period = filters.get("pay_period") if filters else None
    employee = filters.get("employee") if filters else None

    if not pay_period:
        from frappe.utils import getdate
        pay_period = getdate(frappe.utils.today()).strftime("%m-%Y")

    period_parts = pay_period.split("-")
    month = period_parts[0] if len(period_parts) > 0 else "01"
    year = period_parts[1] if len(period_parts) > 1 else "2026"
    from_date = f"{year}-{month}-01"

    conditions = "WHERE s.docstatus = 1 AND MONTH(s.shift_date) = %s AND YEAR(s.shift_date) = %s"
    params = [int(month), int(year)]
    if employee:
        conditions += " AND s.salesman = %s"
        params.append(employee)

    data = frappe.db.sql(f"""
        SELECT em.employee_name,
               COUNT(*) as total_shifts,
               SUM(COALESCE(s.total_sale_amount, 0)) as total_expected,
               SUM(COALESCE(s.cash_collected, 0)) as total_actual,
               SUM(COALESCE(s.total_sale_amount, 0) - COALESCE(s.cash_collected, 0)) as total_shortage,
               ROUND((SUM(COALESCE(s.total_sale_amount, 0) - COALESCE(s.cash_collected, 0))) / COUNT(*), 2) as avg_shortage
        FROM `tabShift` s
        LEFT JOIN `tabEmployee Master` em ON s.salesman = em.name
        {conditions}
        GROUP BY s.salesman, em.employee_name
        ORDER BY total_shortage DESC
    """, params, as_dict=True)

    return columns, data
