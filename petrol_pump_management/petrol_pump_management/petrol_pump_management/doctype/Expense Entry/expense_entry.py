import frappe
from frappe.model.document import Document


class ExpenseEntry(Document):
    def validate(self):
        if self.amount and self.amount < 0:
            frappe.throw("Expense amount cannot be negative")

    def on_submit(self):
        self.approved_by = frappe.session.user
        self.status = "Approved"
