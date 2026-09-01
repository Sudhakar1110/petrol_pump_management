import frappe
from frappe.model.document import Document

class CreditSaleInvoice(Document):
    def validate(self):
        self.balance_amount = (self.amount or 0) - (self.amount_paid or 0)
        if self.balance_amount <= 0 and self.amount_paid:
            self.status = 'Paid'
        elif self.amount_paid and self.amount_paid > 0:
            self.status = 'Partially Paid'
