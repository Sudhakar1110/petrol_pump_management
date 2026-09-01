import frappe
from frappe.model.document import Document


class Shift(Document):
    def validate(self):
        if self.status == 'Closed' and not self.closing_cash:
            frappe.throw("Closing Cash is required to close a shift")

    def on_submit(self):
        self.status = 'Closed'

    def calculate_totals(self):
        sales = frappe.get_all(
            'Fuel Sale',
            filters={'shift': self.name, 'docstatus': 1},
            fields=['amount', 'payment_mode']
        )
        self.total_sale_amount = sum(s.amount or 0 for s in sales)
        self.cash_collected = sum(s.amount or 0 for s in sales if s.payment_mode == 'Cash')
        self.card_upi_amount = sum(s.amount or 0 for s in sales if s.payment_mode in ('Card', 'UPI', 'Petro-card'))
        self.credit_amount = sum(s.amount or 0 for s in sales if s.payment_mode == 'Credit')
