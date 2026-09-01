import frappe
from frappe.model.document import Document


class TripVoucher(Document):
    def on_submit(self):
        self.status = "Received"
