import frappe
from frappe.model.document import Document


class OvertimeLog(Document):
    def validate(self):
        self.total_amount = (self.hours or 0) * (self.rate_per_hour or 0)
