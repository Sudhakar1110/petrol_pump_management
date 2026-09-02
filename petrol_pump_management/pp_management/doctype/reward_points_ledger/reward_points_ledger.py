import frappe
from frappe.model.document import Document


class RewardPointsLedger(Document):
    def validate(self):
        if self.transaction_type == "Redeemed":
            self.points = -abs(self.points)
        # Compute running balance
        prev = frappe.db.sql(
            "SELECT running_balance FROM `tabReward Points Ledger` WHERE customer=%s AND name != %s ORDER BY creation DESC LIMIT 1",
            (self.customer, self.name),
            as_dict=True,
        )
        prev_bal = prev[0].running_balance if prev else 0
        self.running_balance = prev_bal + (self.points or 0)
