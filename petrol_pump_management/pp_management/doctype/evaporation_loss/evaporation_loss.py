import frappe
from frappe.model.document import Document
from frappe.utils import flt


class EvaporationLoss(Document):
    def validate(self):
        self.calculate_loss()

    def calculate_loss(self):
        """Calculate evaporation loss from stock data"""
        if self.opening_stock and self.total_sales:
            self.expected_stock = flt(self.opening_stock) - flt(self.total_sales)
            if self.actual_stock is not None:
                self.evaporation_loss = flt(self.expected_stock) - flt(self.actual_stock)
                if self.expected_stock > 0:
                    self.loss_percentage = (flt(self.evaporation_loss) / flt(self.expected_stock)) * 100
                # Get current fuel rate for loss value
                rate = frappe.db.get_value("Fuel Price Master", {"fuel_type": self.fuel_type}, "rate_per_litre")
                if rate:
                    self.loss_value = flt(self.evaporation_loss) * flt(rate)

        # Set status based on loss percentage
        if self.loss_percentage:
            if self.loss_percentage > 2.0:
                self.status = "Critical"
            elif self.loss_percentage > 0.5:
                self.status = "Above Threshold"
            else:
                self.status = "Normal"


@frappe.whitelist()
def auto_calculate_evaporation_loss(tank, date=None):
    """Auto-calculate evaporation loss for a tank on a given date"""
    if not date:
        date = frappe.utils.today()

    dsr = frappe.db.sql("""
        SELECT opening_stock, sale_qty, closing_stock
        FROM `tabDaily Stock Register`
        WHERE tank = %s AND date = %s
    """, (tank, date), as_dict=True)

    if dsr:
        tank_doc = frappe.get_doc("Tank Master", tank)
        loss = frappe.get_doc({
            "doctype": "Evaporation Loss",
            "tank": tank,
            "date": date,
            "fuel_type": tank_doc.fuel_type,
            "opening_stock": dsr[0].opening_stock,
            "total_sales": dsr[0].sale_qty,
            "actual_stock": dsr[0].closing_stock,
            "closing_stock": dsr[0].closing_stock
        })
        loss.insert(ignore_permissions=True)
        return loss.name
    return None
