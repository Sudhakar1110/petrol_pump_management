import frappe
from frappe.model.document import Document


class LubeStock(Document):
    def validate(self):
        self.closing_qty = (self.opening_qty or 0) + (self.purchase_qty or 0) - (self.sold_qty or 0)
