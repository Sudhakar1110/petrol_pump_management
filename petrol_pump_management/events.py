"""
Petrol Pump Management - Document Events
Handlers for ERPNext document events
"""

import frappe


def on_submit_sales_invoice(doc, method):
    """Handle Sales Invoice submission - sync with petrol pump records."""
    pass


def on_submit_payment_entry(doc, method):
    """Handle Payment Entry submission - update credit ledgers."""
    pass
