import frappe
from frappe.model.document import Document


class BankReconciliationEntry(Document):
    def validate(self):
        self.difference = (self.bank_balance or 0) - (self.book_balance or 0)
