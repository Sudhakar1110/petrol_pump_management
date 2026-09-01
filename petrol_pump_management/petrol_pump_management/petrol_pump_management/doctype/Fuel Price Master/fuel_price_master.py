import frappe
from frappe.model.document import Document


class FuelPriceMaster(Document):
    def validate(self):
        if self.is_active:
            existing = frappe.get_all(
                'Fuel Price Master',
                filters={'fuel_type': self.fuel_type, 'is_active': 1, 'name': ['!=', self.name]}
            )
            for doc in existing:
                frappe.db.set_value('Fuel Price Master', doc.name, 'is_active', 0)
        if not self.revised_by:
            self.revised_by = frappe.session.user
        if not self.previous_rate:
            last_rate = frappe.get_all(
                'Fuel Price Master',
                filters={'fuel_type': self.fuel_type},
                order_by='effective_from desc',
                limit=1,
                fields=['rate_per_litre']
            )
            if last_rate:
                self.previous_rate = last_rate[0].rate_per_litre
