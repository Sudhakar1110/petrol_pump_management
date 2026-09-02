import frappe
from frappe.model.document import Document


class CreditRecoveryEntry(Document):
    def validate(self):
        if self.outstanding_amount and self.amount_collected:
            remaining = self.outstanding_amount - self.amount_collected
            if remaining <= 0:
                self.recovery_status = "Full"
            elif self.amount_collected > 0:
                self.recovery_status = "Partial"

        if self.customer and not self.outstanding_amount:
            balance = frappe.db.sql("""
                SELECT COALESCE(SUM(balance_amount), 0) as balance
                FROM `tabCredit Sale Invoice`
                WHERE customer = %s AND docstatus = 1 AND balance_amount > 0
            """, (self.customer,), as_dict=True)
            if balance:
                self.outstanding_amount = balance[0].balance

    def on_submit(self):
        """Create payment receipt if amount collected"""
        if self.amount_collected and self.amount_collected > 0:
            receipt = frappe.get_doc({
                "doctype": "Payment Receipt",
                "customer": self.customer,
                "amount": self.amount_collected,
                "mode": self.collection_mode or "Cash",
                "reference_no": self.reference_no,
                "received_on": self.recovery_date or frappe.utils.today(),
                "received_by": self.recovered_by
            })
            receipt.insert(ignore_permissions=True)
            receipt.submit()
