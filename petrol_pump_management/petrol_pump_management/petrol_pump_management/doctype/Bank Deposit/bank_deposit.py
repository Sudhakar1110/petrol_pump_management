import frappe
from frappe.model.document import Document


class BankDeposit(Document):
    def on_submit(self):
        self.status = "Deposited"
