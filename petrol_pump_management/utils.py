"""
Petrol Pump Management - Utility Functions
Helper functions used across the application
"""

import frappe


def get_fuel_rate(fuel_type):
    """Get current active fuel rate for Jinja templates."""
    rate = frappe.get_all(
        "Fuel Price Master",
        filters={"fuel_type": fuel_type, "is_active": 1},
        limit=1,
        fields=["rate_per_litre"],
    )
    if rate:
        return rate[0].rate_per_litre
    return 0


def get_station_config():
    """Get station configuration for Jinja templates."""
    return frappe.get_single_doc("Station Configuration")


def calculate_stock_variation(tank, date):
    """Calculate stock variation between meter sale and dip reading."""
    tank_doc = frappe.get_doc("Tank Master", tank)
    nozzles = frappe.get_all("Nozzle Master", filters={"tank": tank}, pluck="name")

    total_sale = 0
    if nozzles:
        result = frappe.db.sql(
            """
            SELECT COALESCE(SUM(qty_litres), 0)
            FROM `tabFuel Sale`
            WHERE nozzle IN ({nozzles})
            AND sale_date = %s
            AND docstatus = 1
        """.format(nozzles=",".join(["%s"] * len(nozzles))),
            tuple(nozzles) + (date,),
        )
        total_sale = result[0][0] if result else 0

    return {
        "tank": tank,
        "fuel_type": tank_doc.fuel_type,
        "total_sale": total_sale,
        "current_stock": tank_doc.current_stock,
    }


def get_customer_outstanding(customer):
    """Get total outstanding amount for a customer."""
    result = frappe.db.sql(
        """
        SELECT COALESCE(SUM(amount - COALESCE(amount_paid, 0)), 0)
        FROM `tabCredit Sale Invoice`
        WHERE customer = %s
        AND status IN ('Unpaid', 'Partially Paid', 'Overdue')
        AND docstatus = 1
    """,
        customer,
    )
    return result[0][0] if result else 0


def generate_sale_no():
    """Generate unique sale number."""
    import random

    return f"FS-{frappe.utils.today()}-{random.randint(1000, 9999)}"
