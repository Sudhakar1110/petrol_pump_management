import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "employee_name", "fieldtype": "Data", "label": "Employee", "width": 150},
        {"fieldname": "pay_period", "fieldtype": "Data", "label": "Period", "width": 100},
        {"fieldname": "days_worked", "fieldtype": "Int", "label": "Days", "width": 60},
        {"fieldname": "basic_salary", "fieldtype": "Currency", "label": "Basic", "width": 100},
        {"fieldname": "overtime_pay", "fieldtype": "Currency", "label": "OT Pay", "width": 100},
        {"fieldname": "commission_earned", "fieldtype": "Currency", "label": "Commission", "width": 100},
        {"fieldname": "incentives", "fieldtype": "Currency", "label": "Incentives", "width": 100},
        {"fieldname": "total_earnings", "fieldtype": "Currency", "label": "Total Earnings", "width": 120},
        {"fieldname": "total_deductions", "fieldtype": "Currency", "label": "Deductions", "width": 100},
        {"fieldname": "net_salary", "fieldtype": "Currency", "label": "Net Salary", "width": 120},
        {"fieldname": "status", "fieldtype": "Data", "label": "Status", "width": 80},
    ]

    conditions = "WHERE 1=1"
    params = []
    if filters and filters.get("pay_period"):
        conditions += " AND pay_period = %s"
        params.append(filters.get("pay_period"))
    if filters and filters.get("employee"):
        conditions += " AND employee = %s"
        params.append(filters.get("employee"))

    data = frappe.db.sql(f"""
        SELECT employee_name, pay_period, days_worked, basic_salary,
               overtime_pay, commission_earned, incentives,
               total_earnings, total_deductions, net_salary, status
        FROM `tabSalary Slip Entry`
        {conditions}
        ORDER BY employee_name, pay_period DESC
    """, params, as_dict=True)

    return columns, data
