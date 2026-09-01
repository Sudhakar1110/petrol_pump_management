import frappe
from frappe.model.document import Document


class MeterReading(Document):
    def validate(self):
        if self.closing_reading and self.opening_reading:
            if self.closing_reading < self.opening_reading:
                frappe.throw("Closing reading cannot be less than opening reading")
            self.sale_qty = (self.closing_reading - self.opening_reading) - (self.testing_qty or 0)
            nozzle_doc = frappe.get_doc('Nozzle Master', self.nozzle)
            rate_doc = frappe.get_all(
                'Fuel Price Master',
                filters={'fuel_type': nozzle_doc.fuel_type, 'is_active': 1},
                limit=1, fields=['rate_per_litre']
            )
            if rate_doc:
                self.sale_amount = self.sale_qty * rate_doc[0].rate_per_litre
