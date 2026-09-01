import frappe
from frappe.model.document import Document
import random


class FuelSale(Document):
    def validate(self):
        self.amount = (self.qty_litres or 0) * (self.rate or 0)
        if not self.fuel_type and self.nozzle:
            nozzle_doc = frappe.get_doc('Nozzle Master', self.nozzle)
            self.fuel_type = frappe.db.get_value('Tank Master', nozzle_doc.tank, 'fuel_type')

    def autoname(self):
        self.sale_no = f"FS-{self.sale_date}-{random.randint(1000,9999)}"

    def on_submit(self):
        if self.payment_mode == 'Credit':
            if not self.customer:
                frappe.throw("Customer is required for credit sales")
            self.create_credit_invoice()

    def create_credit_invoice(self):
        invoice = frappe.new_doc('Credit Sale Invoice')
        invoice.customer = self.customer
        invoice.vehicle = self.vehicle
        invoice.fuel_sale = self.name
        invoice.amount = self.amount
        invoice.due_date = frappe.utils.add_days(self.sale_date, 30)
        invoice.status = 'Unpaid'
        invoice.insert(ignore_permissions=True)
        frappe.msgprint(f"Credit Invoice {invoice.name} created")
