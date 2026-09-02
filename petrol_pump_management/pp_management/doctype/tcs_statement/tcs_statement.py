import frappe
from frappe.model.document import Document


class TCSStatement(Document):
    def validate(self):
        if self.gross_amount and self.tcs_rate:
            self.tcs_amount = round(self.gross_amount * self.tcs_rate / 100, 2)
            self.net_amount = (self.gross_amount or 0) + (self.tcs_amount or 0)
