"""
Petrol Pump Management - Document Events
Handlers for ERPNext document events
"""

import frappe


def on_submit_generic(doc, method):
    """
    Generic document event handler.
    Handles post-submit logic for petrol pump DocTypes.
    """
    pass


def boot_session(bootinfo):
    """
    Add petrol pump management data to boot session.
    """
    bootinfo.station_config = frappe.get_single_doc("Station Configuration")
    bootinfo.active_fuel_rates = frappe.get_all(
        "Fuel Price Master",
        filters={"is_active": 1},
        fields=["fuel_type", "rate_per_litre"],
    )
