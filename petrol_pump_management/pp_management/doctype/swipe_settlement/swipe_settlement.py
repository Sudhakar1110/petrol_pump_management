import frappe
from frappe.model.document import Document


class SwipeSettlement(Document):
    def validate(self):
        self.difference = (self.total_collected or 0) - (self.total_sale_amount or 0)
