import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "effective_from", "fieldtype": "Datetime", "label": "Effective From", "width": 160},
        {"fieldname": "fuel_type", "fieldtype": "Data", "label": "Fuel Type", "width": 120},
        {"fieldname": "previous_rate", "fieldtype": "Currency", "label": "Previous Rate", "width": 120},
        {"fieldname": "rate_per_litre", "fieldtype": "Currency", "label": "New Rate", "width": 120},
        {"fieldname": "change", "fieldtype": "Currency", "label": "Change", "width": 100},
        {"fieldname": "revised_by_name", "fieldtype": "Data", "label": "Revised By", "width": 150},
    ]
    data = frappe.db.sql("""
        SELECT fpm.effective_from, fpm.fuel_type, fpm.previous_rate,
               fpm.rate_per_litre,
               (fpm.rate_per_litre - COALESCE(fpm.previous_rate, fpm.rate_per_litre)) as change,
               u.full_name as revised_by_name
        FROM `tabFuel Price Master` fpm
        LEFT JOIN `tabUser` u ON fpm.revised_by = u.name
        ORDER BY fpm.effective_from DESC
    """, as_dict=True)
    return columns, data