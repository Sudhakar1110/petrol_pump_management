import frappe
from frappe.model.document import Document
from frappe.utils import getdate, add_months, flt


class SalarySlipEntry(Document):
    def validate(self):
        self.calculate_totals()
        self.auto_fill_fields()

    def auto_fill_fields(self):
        """Auto-fill employee name and basic salary from Employee Master"""
        if self.employee and not self.employee_name:
            emp = frappe.get_doc("Employee Master", self.employee)
            self.employee_name = emp.employee_name
            if emp.salary_type == "Fixed" and not self.basic_salary:
                self.basic_salary = emp.fixed_salary or 0

    def calculate_totals(self):
        self.overtime_pay = flt(self.overtime_hours) * flt(self.basic_salary or 0) / 30 / 8 * 1.5 if self.overtime_hours else 0
        self.total_earnings = flt(self.basic_salary or 0) + flt(self.overtime_pay or 0) + \
                              flt(self.commission_earned or 0) + flt(self.incentives or 0)
        self.total_deductions = flt(self.advance_deduction or 0) + flt(self.loan_deduction or 0) + \
                                flt(self.pf_deduction or 0) + flt(self.esi_deduction or 0) + \
                                flt(self.professional_tax or 0)
        self.net_salary = flt(self.total_earnings) - flt(self.total_deductions)

    def on_submit(self):
        self.status = "Submitted"
        # Auto-deduct advances
        self._deduct_advances()
        # Auto-calculate overtime from Overtime Log
        self._calculate_overtime()
        self.save(ignore_permissions=True)

    def _deduct_advances(self):
        """Deduct pending advances from salary"""
        advances = frappe.db.sql("""
            SELECT SUM(amount - recovered_amount) as pending
            FROM `tabAdvance Amount`
            WHERE employee = %s AND recovered_amount < amount AND docstatus = 1
        """, (self.employee,), as_dict=True)
        if advances and advances[0].pending:
            self.advance_deduction = advances[0].pending
            # Mark advances as recovered
            frappe.db.sql("""
                UPDATE `tabAdvance Amount`
                SET recovered_amount = amount
                WHERE employee = %s AND recovered_amount < amount AND docstatus = 1
            """, (self.employee,))

    def _calculate_overtime(self):
        """Calculate overtime from Overtime Log"""
        overtime = frappe.db.sql("""
            SELECT SUM(overtime_hours) as total_hours
            FROM `tabOvertime Log`
            WHERE employee = %s AND MONTH(overtime_date) = MONTH(CURDATE())
            AND YEAR(overtime_date) = YEAR(CURDATE()) AND docstatus = 1
        """, (self.employee,), as_dict=True)
        if overtime and overtime[0].total_hours:
            self.overtime_hours = overtime[0].total_hours


@frappe.whitelist()
def generate_salary_slips_for_month(pay_period):
    """Generate salary slips for all active employees"""
    employees = frappe.get_all("Employee Master", filters={"is_active": 1}, fields=["name", "employee_name"])
    slips = []
    for emp in employees:
        existing = frappe.db.exists("Salary Slip Entry", {"employee": emp.name, "pay_period": pay_period})
        if not existing:
            slip = frappe.get_doc({
                "doctype": "Salary Slip Entry",
                "employee": emp.name,
                "employee_name": emp.employee_name,
                "pay_period": pay_period,
                "status": "Draft"
            })
            slip.insert(ignore_permissions=True)
            slips.append(slip.name)
    return slips
