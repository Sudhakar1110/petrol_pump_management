import frappe
from frappe.model.document import Document
from frappe.utils import flt


class TankerExpense(Document):
    def validate(self):
        self.calculate_totals()

    def calculate_totals(self):
        self.total_cost = flt(self.purchase_amount or 0) + flt(self.transport_cost or 0) + \
                          flt(self.loading_unloading or 0) + flt(self.toll_charges or 0) + \
                          flt(self.other_charges or 0)
        self.profit_loss = flt(self.actual_sale_value or 0) - flt(self.total_cost or 0)
        if self.total_cost > 0:
            self.margin_percentage = (flt(self.profit_loss) / flt(self.total_cost)) * 100
