import frappe
from frappe.model.document import Document

class StockPurchaseDecantation(Document):
    def validate(self):
        if self.invoiced_qty and self.received_qty:
            self.variation_pct = ((self.received_qty - self.invoiced_qty) / self.invoiced_qty) * 100
        if self.tank:
            self.fuel_type = frappe.db.get_value('Tank Master', self.tank, 'fuel_type')
    def on_submit(self):
        tank_doc = frappe.get_doc('Tank Master', self.tank)
        tank_doc.current_stock = (tank_doc.current_stock or 0) + self.received_qty
        tank_doc.save(ignore_permissions=True)
