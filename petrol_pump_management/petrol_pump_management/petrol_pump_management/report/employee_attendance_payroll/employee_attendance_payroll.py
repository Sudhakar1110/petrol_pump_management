import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "employee_name", "fieldtype": "Data", "label": "Employee", "width": 180},
        {"fieldname": "role", "fieldtype": "Data", "label": "Role", "width": 120},
        {"fieldname": "total_shifts", "fieldtype": "Int", "label": "Total Shifts", "width": 100},
        {"fieldname": "total_sales", "fieldtype": "Currency", "label": "Total Sales", "width": 140},
        {"fieldname": "total_shortage", "fieldtype": "Currency", "label": "Total Shortage", "width": 120},
        {"fieldname": "salary_type", "fieldtype": "Data", "label": "Salary Type", "width": 120},
    ]
    conditions = "s.docstatus = 1"
    if filters.get("from_date"):
        conditions += f" AND s.shift_date >= '{filters['from_date']}'"
    if filters.get("to_date"):
        conditions += f" AND s.shift_date <= '{filters['to_date']}'"
    data = frappe.db.sql(f"""
        SELECT em.employee_name, em.role, em.salary_type,
               COUNT(s.name) as total_shifts,
               COALESCE(SUM(s.total_sale_amount), 0) as total_sales,
               COALESCE(SUM(s.cash_shortage), 0) as total_shortage
        FROM `tabEmployee Master` em
        LEFT JOIN `tabShift` s ON s.salesman = em.name AND {conditions}
        WHERE em.is_active = 1
        GROUP BY em.name
        ORDER BY em.employee_name
    """, as_dict=True)
    return columns, data