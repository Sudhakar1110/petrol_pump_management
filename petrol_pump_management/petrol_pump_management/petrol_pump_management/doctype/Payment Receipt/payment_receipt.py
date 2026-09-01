import frappe
from frappe.model.document import Document


class PaymentReceipt(Document):
    def validate(self):
        if self.invoices:
            total = sum(inv.amount for inv in self.invoices)
            if total != self.amount:
                frappe.throw(f"Invoice total ({total}) does not match receipt amount ({self.amount})")

    def on_submit(self):
        for inv_row in self.invoices:
            inv = frappe.get_doc('Credit Sale Invoice', inv_row.credit_sale_invoice)
            inv.amount_paid = (inv.amount_paid or 0) + inv_row.amount
            inv.balance_amount = inv.amount - inv.amount_paid
            if inv.balance_amount <= 0:
                inv.status = 'Paid'
            elif inv.amount_paid > 0:
                inv.status = 'Partially Paid'
            inv.save(ignore_permissions=True)
            ledger = frappe.get_all('Credit Limit Ledger', filters={'customer': self.customer}, limit=1)
            if ledger:
                ledger_doc = frappe.get_doc('Credit Limit Ledger', ledger[0].name)
                ledger_doc.update_used_amount(inv_row.amount, 'subtract')
