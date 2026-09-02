import frappe
from frappe.model.document import Document
from frappe.utils import flt


class CommissionPayment(Document):
    def validate(self):
        self.auto_calculate_commission()

    def auto_calculate_commission(self):
        """Auto-calculate commission based on Commission Rules"""
        if not self.employee or not self.commission_period:
            return

        period_parts = self.commission_period.split("-")
        month = period_parts[0] if len(period_parts) > 0 else "01"
        year = period_parts[1] if len(period_parts) > 1 else "2026"
        from_date = f"{year}-{month}-01"
        to_date = frappe.utils.add_months(frappe.utils.getdate(from_date), 1)
        to_date = frappe.utils.add_days(to_date, -1)

        # Get employee shifts for the period
        shifts = frappe.db.sql("""
            SELECT name FROM `tabShift`
            WHERE salesman = %s AND shift_date BETWEEN %s AND %s AND docstatus = 1
        """, (self.employee, from_date, to_date), as_dict=True)

        if not shifts:
            return

        shift_names = [s.name for s in shifts]

        # Get total sales through those shifts
        sales = frappe.db.sql("""
            SELECT SUM(qty_litres) as total_qty, SUM(amount) as total_amount
            FROM `tabFuel Sale`
            WHERE shift IN %s AND docstatus = 1
        """, (shift_names,), as_dict=True)

        if sales and sales[0].total_qty:
            self.total_fuel_sold = sales[0].total_qty
            self.total_sales_value = sales[0].total_amount

            # Get applicable commission rule
            rule = frappe.db.sql("""
                SELECT commission_per_litre, min_qty, max_qty
                FROM `tabCommission Rule`
                WHERE %s >= COALESCE(min_qty, 0)
                AND (%s <= max_qty OR max_qty IS NULL)
                AND is_active = 1
                ORDER BY min_qty DESC LIMIT 1
            """, (self.total_fuel_sold, self.total_fuel_sold), as_dict=True)

            if rule:
                self.commission_rate = rule[0].commission_per_litre or 0
                self.commission_amount = flt(self.total_fuel_sold) * flt(self.commission_rate)
                self.net_commission = flt(self.commission_amount) + flt(self.bonus or 0) - flt(self.deductions or 0)
            else:
                # Default commission: 0.10 per litre
                self.commission_rate = 0.10
                self.commission_amount = flt(self.total_fuel_sold) * 0.10
                self.net_commission = flt(self.commission_amount) + flt(self.bonus or 0) - flt(self.deductions or 0)


@frappe.whitelist()
def generate_commission_for_month(commission_period):
    """Generate commission payments for all active employees"""
    employees = frappe.get_all("Employee Master", filters={"is_active": 1, "role": ["in", ["Salesman", "DSM"]]}, fields=["name", "employee_name"])
    payments = []
    for emp in employees:
        existing = frappe.db.exists("Commission Payment", {"employee": emp.name, "commission_period": commission_period})
        if not existing:
            payment = frappe.get_doc({
                "doctype": "Commission Payment",
                "employee": emp.name,
                "employee_name": emp.employee_name,
                "commission_period": commission_period,
                "payment_status": "Pending"
            })
            payment.insert(ignore_permissions=True)
            payments.append(payment.name)
    return payments
