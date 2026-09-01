import frappe


def on_fuel_sale_submit(doc, method):
    """Handle Fuel Sale submission - create credit invoice if credit sale."""
    if doc.payment_mode == "Credit" and doc.customer:
        try:
            invoice = frappe.new_doc("Credit Sale Invoice")
            invoice.customer = doc.customer
            invoice.vehicle = doc.vehicle
            invoice.fuel_sale = doc.name
            invoice.amount = doc.amount
            invoice.due_date = frappe.utils.add_days(doc.sale_date, 30)
            invoice.status = "Unpaid"
            invoice.insert(ignore_permissions=True)
        except Exception:
            pass
