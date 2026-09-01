import frappe

def get_fuel_rate(fuel_type):
    rate = frappe.get_all("Fuel Price Master", filters={"fuel_type": fuel_type, "is_active": 1}, limit=1, fields=["rate_per_litre"])
    return rate[0].rate_per_litre if rate else 0

def get_station_config():
    return frappe.get_single_doc("Station Configuration")
