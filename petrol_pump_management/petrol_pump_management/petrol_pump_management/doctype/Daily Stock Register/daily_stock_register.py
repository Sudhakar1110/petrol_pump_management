import frappe
from frappe.model.document import Document


class DailyStockRegister(Document):
    def validate(self):
        if self.tank:
            self.fuel_type = frappe.db.get_value('Tank Master', self.tank, 'fuel_type')
        self.closing_stock = (self.opening_stock or 0) + (self.purchase_qty or 0) - (self.sale_qty or 0)
        if self.dip_closing_stock:
            self.variation = self.dip_closing_stock - self.closing_stock
