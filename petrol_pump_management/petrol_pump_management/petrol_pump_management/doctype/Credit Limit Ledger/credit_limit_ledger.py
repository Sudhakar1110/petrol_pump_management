import frappe
from frappe.model.document import Document


class CreditLimitLedger(Document):
    def validate(self):
        self.available_amount = (self.limit_amount or 0) - (self.used_amount or 0)
        self.last_updated = frappe.utils.now_datetime()

    def update_used_amount(self, amount, operation='add'):
        if operation == 'add':
            self.used_amount = (self.used_amount or 0) + amount
        else:
            self.used_amount = max(0, (self.used_amount or 0) - amount)
        self.save(ignore_permissions=True)
