import frappe
from frappe.model.document import Document
import random

class FuelSale(Document):
    def validate(self):
        self.amount = (self.qty_litres or 0) * (self.rate or 0)
    def autoname(self):
        self.sale_no = f"FS-{self.sale_date}-{random.randint(1000,9999)}"
