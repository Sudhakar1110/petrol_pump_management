import frappe
from frappe.model.document import Document


class CreditSaleInvoice(Document):
    def validate(self):
        self.balance_amount = (self.amount or 0) - (self.amount_paid or 0)
        if self.balance_amount <= 0 and self.amount_paid:
            self.status = 'Paid'
        elif self.amount_paid and self.amount_paid > 0:
            self.status = 'Partially Paid'

    def on_submit(self):
        customer = frappe.get_doc('PP Customer', self.customer)
        ledger = frappe.get_all('Credit Limit Ledger', filters={'customer': self.customer}, limit=1)
        if ledger:
            ledger_doc = frappe.get_doc('Credit Limit Ledger', ledger[0].name)
            ledger_doc.update_used_amount(self.amount, 'add')
        else:
            ledger_doc = frappe.new_doc('Credit Limit Ledger')
            ledger_doc.customer = self.customer
            ledger_doc.limit_amount = customer.credit_limit
            ledger_doc.used_amount = self.amount
            ledger_doc.block_on_exceed = 1
            ledger_doc.insert(ignore_permissions=True)
