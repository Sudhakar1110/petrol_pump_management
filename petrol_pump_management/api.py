"""
Petrol Pump Management - API Methods
Whitelisted methods for external access
"""

import frappe
from frappe import _


@frappe.whitelist()
def get_fuel_rate(fuel_type):
    """Get current active fuel rate for a given fuel type."""
    rate = frappe.get_all(
        "Fuel Price Master",
        filters={"fuel_type": fuel_type, "is_active": 1},
        limit=1,
        fields=["rate_per_litre", "effective_from"],
    )
    if rate:
        return {"rate": rate[0].rate_per_litre, "effective_from": rate[0].effective_from}
    return {"rate": 0, "effective_from": None}


@frappe.whitelist()
def create_credit_sale(nozzle, qty_litres, customer, vehicle=None):
    """Create a credit fuel sale with automatic invoice generation."""
    nozzle_doc = frappe.get_doc("Nozzle Master", nozzle)
    fuel_type = frappe.db.get_value("Tank Master", nozzle_doc.tank, "fuel_type")
    rate_doc = get_fuel_rate(fuel_type)

    if not rate_doc.get("rate"):
        frappe.throw(_("No active fuel rate found for {0}").format(fuel_type))

    sale = frappe.new_doc("Fuel Sale")
    sale.nozzle = nozzle
    sale.qty_litres = qty_litres
    sale.rate = rate_doc["rate"]
    sale.payment_mode = "Credit"
    sale.customer = customer
    if vehicle:
        sale.vehicle = vehicle
    sale.insert(ignore_permissions=True)
    sale.submit()

    return {"sale_no": sale.sale_no, "amount": sale.amount, "name": sale.name}


@frappe.whitelist()
def get_customer_credit_balance(customer):
    """Get current credit balance and available limit for a customer."""
    customer_doc = frappe.get_doc("PP Customer", customer)
    available = customer_doc.get_available_credit()

    return {
        "customer": customer,
        "credit_limit": customer_doc.credit_limit,
        "available_credit": available,
        "is_blocked": customer_doc.is_blocked,
        "credit_points": customer_doc.credit_points,
    }


@frappe.whitelist()
def match_anpr_plate(plate_number, camera_id):
    """Match a captured ANPR plate against vehicle master and create scan log."""
    scan_log = frappe.new_doc("ANPR Scan Log")
    scan_log.captured_plate = plate_number
    scan_log.camera_id = camera_id
    scan_log.scan_datetime = frappe.utils.now_datetime()
    scan_log.confidence_score = 95.0
    scan_log.insert(ignore_permissions=True)

    return {
        "scan_log": scan_log.name,
        "matched_vehicle": scan_log.matched_vehicle,
        "matched_customer": scan_log.matched_customer,
        "action_taken": scan_log.action_taken,
    }


@frappe.whitelist()
def get_shift_summary(shift):
    """Get summary of a shift including sales, cash, and shortage details."""
    shift_doc = frappe.get_doc("Shift", shift)
    shift_doc.calculate_totals()

    return {
        "shift": shift,
        "salesman": shift_doc.salesman,
        "total_sale_amount": shift_doc.total_sale_amount,
        "cash_collected": shift_doc.cash_collected,
        "card_upi_amount": shift_doc.card_upi_amount,
        "credit_amount": shift_doc.credit_amount,
        "opening_cash": shift_doc.opening_cash,
        "closing_cash": shift_doc.closing_cash,
        "cash_shortage": shift_doc.cash_shortage,
    }


@frappe.whitelist()
def get_daily_stock_summary(date=None, tank=None):
    """Get daily stock summary for all tanks or a specific tank."""
    filters = {}
    if date:
        filters["date"] = date
    else:
        filters["date"] = frappe.utils.today()
    if tank:
        filters["tank"] = tank

    entries = frappe.get_all(
        "Daily Stock Register",
        filters=filters,
        fields=["tank", "fuel_type", "opening_stock", "purchase_qty", "sale_qty", "closing_stock", "variation"],
    )

    return entries


@frappe.whitelist()
def get_station_configuration():
    """Get current station configuration."""
    config = frappe.get_single_doc("Station Configuration")
    return {
        "station_name": config.station_name,
        "gst_number": config.gst_number,
        "dealer_licence_no": config.dealer_licence_no,
        "default_fuel_unit": config.default_fuel_unit,
        "default_currency": config.default_currency,
    }


@frappe.whitelist()
def settle_shift(shift, closing_cash):
    """Settle a shift with closing cash and calculate shortage."""
    shift_doc = frappe.get_doc("Shift", shift)
    shift_doc.closing_cash = closing_cash
    shift_doc.calculate_totals()
    shift_doc.save(ignore_permissions=True)

    return {
        "shift": shift,
        "total_sale_amount": shift_doc.total_sale_amount,
        "cash_collected": shift_doc.cash_collected,
        "cash_shortage": shift_doc.cash_shortage,
        "status": shift_doc.status,
    }
