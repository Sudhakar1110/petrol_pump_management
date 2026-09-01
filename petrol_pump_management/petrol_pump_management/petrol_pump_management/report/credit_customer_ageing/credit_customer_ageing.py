import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "customer_name", "fieldtype": "Data", "label": "Customer", "width": 180},
        {"fieldname": "credit_limit", "fieldtype": "Currency", "label": "Credit Limit", "width": 120},
        {"fieldname": "tot
