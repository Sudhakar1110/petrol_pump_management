import frappe
from frappe.model.document import Document
from frappe.utils import date_diff


class LeaveApplication(Document):
    def validate(self):
        if self.from_date and self.to_date:
            self.total_days = date_diff(self.to_date, self.from_date) + 1

    def on_update(self):
        if self.status == "Approved":
            self.approved_by = frappe.session.user
