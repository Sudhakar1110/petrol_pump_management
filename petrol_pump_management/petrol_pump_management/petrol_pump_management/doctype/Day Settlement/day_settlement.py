import frappe
from frappe.model.document import Document


class DaySettlement(Document):
    def validate(self):
        self.cash_shortage = (self.total_cash or 0) - ((self.closing_hand_cash or 0) - (self.opening_hand_cash or 0))

    def on_submit(self):
        self.status = "Settled"
