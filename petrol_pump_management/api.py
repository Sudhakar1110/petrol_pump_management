import frappe

@frappe.whitelist()
def get_fuel_rate(fuel_type):
    rate = frappe.get_all("Fuel Price Master", filters={"fuel_type": fuel_type, "is_active": 1}, limit=1, fields=["rate_per_litre"])
    return {"rate": rate[0].rate_per_litre if rate else 0}

@frappe.whitelist()
def get_customer_credit_balance(customer):
    doc = frappe.get_doc("PP Customer", customer)
    return {"customer": customer, "credit_limit": doc.credit_limit, "credit_points": doc.credit_points, "is_blocked": doc.is_blocked}
