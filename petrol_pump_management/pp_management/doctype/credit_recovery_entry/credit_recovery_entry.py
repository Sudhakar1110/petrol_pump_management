import frappe
from frappe.model.document import Document


class CreditRecoveryEntry(Document):
    def validate(self):
        # Calculate balance after recovery
        collected = self.amount_collected or 0
        discount = self.discount or 0
        self.balance_after = (self.outstanding_amount or 0) - collected - discount

        if self.outstanding_amount and self.amount_collected:
            remaining = self.outstanding_amount - self.amount_collected - discount
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

        # Apply discount to oldest unpaid invoices
        if self.discount and self.discount > 0:
            self._apply_discount()

    def _apply_discount(self):
        """Apply discount/waiver to oldest unpaid invoices"""
        remaining_discount = self.discount
        invoices = frappe.db.sql("""
            SELECT name, balance_amount FROM `tabCredit Sale Invoice`
            WHERE customer = %s AND docstatus = 1 AND balance_amount > 0
            ORDER BY due_date ASC
        """, (self.customer,), as_dict=True)

        for inv in invoices:
            if remaining_discount <= 0:
                break
            apply = min(remaining_discount, inv.balance_amount)
            new_balance = inv.balance_amount - apply
            new_status = "Paid" if new_balance <= 0 else "Partially Paid"
            frappe.db.set_value("Credit Sale Invoice", inv.name, {
                "balance_amount": new_balance,
                "status": new_status
            })
            remaining_discount -= apply
