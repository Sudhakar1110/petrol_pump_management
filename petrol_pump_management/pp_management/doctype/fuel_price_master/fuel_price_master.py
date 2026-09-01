import frappe
from frappe.model.document import Document

class FuelPriceMaster(Document):
    def validate(self):
        if self.is_active:
            for d in frappe.get_all('Fuel Price Master', filters={'fuel_type':self.fuel_type,'is_active':1,'name':['!=',self.name]}):
                frappe.db.set_value('Fuel Price Master', d.name, 'is_active', 0)
