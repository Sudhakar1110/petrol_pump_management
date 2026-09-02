import frappe
from frappe.utils import add_days, today, getdate, flt


def on_fuel_sale_submit(doc, method):
    """Handle Fuel Sale submission - create credit invoice if credit sale."""
    if doc.payment_mode == "Credit" and doc.customer:
        try:
            invoice = frappe.new_doc("Credit Sale Invoice")
            invoice.customer = doc.customer
            invoice.vehicle = doc.vehicle
            invoice.fuel_sale = doc.name
            invoice.amount = doc.amount
            invoice.due_date = add_days(doc.sale_date, 30)
            invoice.status = "Unpaid"
            invoice.insert(ignore_permissions=True)
        except Exception:
            pass

    # Award reward points (1 point per 100 rupees)
    if doc.customer and doc.amount:
        points = int(doc.amount / 100)
        if points > 0:
            try:
                rl = frappe.new_doc("Reward Points Ledger")
                rl.customer = doc.customer
                rl.transaction_type = "Earned"
                rl.points = points
                rl.fuel_sale = doc.name
                rl.transaction_date = doc.sale_date
                rl.remarks = f"Earned from sale {doc.name}"
                rl.insert(ignore_permissions=True)
            except Exception:
                pass


def on_fuel_sale_credit_check(doc, method):
    """Block credit sale if customer has exceeded limit."""
    if doc.payment_mode == "Credit" and doc.customer:
        customer = frappe.db.get_value("PP Customer", doc.customer, ["credit_limit", "is_blocked"])
        if customer and customer.is_blocked:
            frappe.throw(f"Credit sale blocked: Customer {doc.customer} has exceeded credit limit.")


def on_credit_invoice_submit(doc, method):
    """Handle Credit Sale Invoice submission."""
    # Update credit limit ledger
    _update_credit_limit(doc.customer)

    # Send SMS notification
    try:
        customer_mobile = frappe.db.get_value("PP Customer", doc.customer, "mobile")
        if customer_mobile:
            frappe.sendmail(
                recipients=[customer_mobile],
                subject=f"Credit Sale Invoice {doc.name}",
                message=f"Dear Customer,\n\nA credit sale of {frappe.format_doc(doc.amount, {'fieldtype': 'Currency'})} has been recorded against your account.\n\nDue Date: {doc.due_date}\nInvoice: {doc.name}\n\nPlease clear the dues by the due date.\n\nThank you.",
            )
    except Exception:
        pass


def update_credit_limit_ledger(doc, method):
    """Update credit limit ledger on invoice submit."""
    _update_credit_limit(doc.customer)


def on_payment_receipt_submit(doc, method):
    """Handle Payment Receipt submission."""
    # Update related credit invoice status
    _update_credit_limit(doc.customer)

    # Send SMS confirmation
    try:
        customer_mobile = frappe.db.get_value("PP Customer", doc.customer, "mobile")
        if customer_mobile:
            frappe.sendmail(
                recipients=[customer_mobile],
                subject=f"Payment Received - {doc.name}",
                message=f"Dear Customer,\n\nPayment of {frappe.format_doc(doc.amount_received, {'fieldtype': 'Currency'})} received successfully.\n\nReceipt: {doc.name}\nMode: {doc.payment_mode}\n\nThank you.",
            )
    except Exception:
        pass


def update_credit_limit_on_payment(doc, method):
    """Update credit limit ledger when payment is received."""
    _update_credit_limit(doc.customer)


def on_swipe_settlement_submit(doc, method):
    """Handle Swipe Settlement submission."""
    doc.difference = (doc.total_collected or 0) - (doc.total_sale_amount or 0)


def _update_credit_limit(customer):
    """Recalculate and update credit limit ledger for a customer."""
    if not customer:
        return
    try:
        cl = frappe.db.get_value("Credit Limit Ledger", {"customer": customer}, ["name", "limit_amount"], as_dict=True)
        if not cl:
            return

        total_unpaid = frappe.db.sql("""
            SELECT IFNULL(SUM(amount), 0) as total
            FROM `tabCredit Sale Invoice`
            WHERE customer = %s AND docstatus = 1 AND status != 'Paid'
        """, (customer,), as_dict=True)

        total_paid = frappe.db.sql("""
            SELECT IFNULL(SUM(amount_received), 0) as total
            FROM `tabPayment Receipt`
            WHERE customer = %s AND docstatus = 1
        """, (customer,), as_dict=True)

        used = (total_unpaid[0].total or 0) - (total_paid[0].total or 0)
        available = (cl.limit_amount or 0) - used

        frappe.db.set_value("Credit Limit Ledger", cl.name, {
            "used_amount": used,
            "available_amount": available,
            "last_updated": frappe.utils.now_datetime(),
        })

        # Auto-block if limit exceeded
        if available < 0 and cl.block_on_exceed:
            frappe.db.set_value("PP Customer", customer, "is_blocked", 1)
    except Exception:
        pass
