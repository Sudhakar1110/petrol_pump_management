import frappe
from frappe.model.document import Document


class TDSStatement(Document):
    def validate(self):
        if self.gross_amount and self.tds_rate:
            self.tds_amount = round(self.gross_amount * self.tds_rate / 100, 2)
            self.net_amount = (self.gross_amount or 0) - (self.tds_amount or 0)
