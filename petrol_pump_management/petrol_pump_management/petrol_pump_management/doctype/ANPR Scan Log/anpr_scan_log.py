import frappe
from frappe.model.document import Document


class ANPRScanLog(Document):
    def validate(self):
        if not self.scan_datetime:
            self.scan_datetime = frappe.utils.now_datetime()
        if self.captured_plate and not self.matched_vehicle:
            vehicle = frappe.get_all(
                'Vehicle Master',
                filters={'vehicle_number': self.captured_plate, 'anpr_tag_status': 'Active'},
                limit=1
            )
            if vehicle:
                self.matched_vehicle = vehicle[0].name
                v_doc = frappe.get_doc('Vehicle Master', vehicle[0].name)
                self.matched_customer = v_doc.customer
                if v_doc.customer:
                    self.matched_customer_name = frappe.db.get_value('PP Customer', v_doc.customer, 'full_name')
                self.action_taken = 'Auto-billed' if self.confidence_score >= 80 else 'Manual Review'
            else:
                self.action_taken = 'Rejected'
