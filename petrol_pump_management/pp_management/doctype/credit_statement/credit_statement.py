import frappe
from frappe.model.document import Document


class CreditStatement(Document):
    def validate(self):
        self.closing_balance = (
            (self.opening_balance or 0)
            + (self.total_credit or 0)
            - (self.total_payment or 0)
            + (self.interest_charged or 0)
        )
