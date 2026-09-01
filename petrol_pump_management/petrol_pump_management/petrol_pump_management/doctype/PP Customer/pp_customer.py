import frappe
from frappe.model.document import Document


class PPCustomer(Document):
    def validate(self):
        if self.credit_limit and self.credit_limit < 0:
            frappe.throw("Credit Limit cannot be negative")

    def get_available_credit(self):
        used = frappe.db.sql(
            """SELECT COALESCE(SUM(amount), 0)
            FROM `tabCredit Sale Invoice`
            WHERE customer = %s AND status IN ('Unpaid', 'Partially Paid', 'Overdue')""",
            self.name
        )[0][0]
        return (self.credit_limit or 0) - used

    def is_credit_available(self, amount):
        if self.is_blocked:
            return False
        return self.get_available_credit() >= amount
