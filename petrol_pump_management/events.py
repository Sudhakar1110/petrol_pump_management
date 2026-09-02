import frappe
from frappe.utils import add_days, today, getdate, flt


def on_fuel_sale_submit(doc, method):
    """Handle Fuel Sale submission - credit check, credit invoice, reward points, SMS."""
    # Block credit sale if customer has exceeded limit
    if doc.payment_mode == "Credit" and doc.customer:
        customer = frappe.db.get_value("PP Customer", doc.customer, ["credit_limit", "is_blocked"])
        if customer and customer.is_blocked:
            frappe.throw(f"Credit sale blocked: Customer {doc.customer} has exceeded credit limit.")

        # Auto-create credit sale invoice
        try:
            invoice = frappe.new_doc("Credit Sale Invoice")
            invoice.customer = doc.customer
            invoice.vehicle = doc.vehicle
            invoice.fuel_sale = doc.name
            invoice.amount = doc.amount
            invoice.due_date = add_days(doc.sale_date, 30)
            invoice.status = "Unpaid"
            invoice.insert(ignore_permissions=True)
            invoice.submit()

            # Send SMS for credit sale
            _send_credit_sale_sms(doc.customer, doc.name, doc.amount, doc.qty_litres,
                                  doc.fuel_type, invoice.balance_amount)
        except Exception:
            pass

    # Send SMS for cash sale
    if doc.payment_mode in ("Cash", "Card", "UPI") and doc.customer:
        _send_cash_sale_sms(doc.customer, doc.name, doc.amount, doc.payment_mode)

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


def on_credit_invoice_submit(doc, method):
    """Handle Credit Sale Invoice submission - update limit, send SMS."""
    _update_credit_limit(doc.customer)


def on_payment_receipt_submit(doc, method):
    """Handle Payment Receipt submission - update limit, send SMS."""
    _update_credit_limit(doc.customer)
    _send_payment_receipt_sms(doc.customer, doc.name, doc.amount, doc.mode)


def on_swipe_settlement_submit(doc, method):
    """Handle Swipe Settlement submission."""
    pass


def _send_credit_sale_sms(customer, sale_name, amount, qty, fuel_type, balance):
    """Send SMS on credit sale"""
    try:
        settings = frappe.get_single("Notification Settings")
        if not settings.enable_sms:
            return
        mobile = frappe.db.get_value("PP Customer", customer, "mobile")
        station = frappe.db.get_single_value("Station Configuration", "station_name") or "Station"
        if mobile and settings.sms_credit_sale:
            msg = settings.sms_credit_sale.format(
                customer=customer, amount=amount, qty=qty,
                fuel_type=fuel_type or "", balance=balance or 0, station=station
            )
            sms = frappe.get_doc({
                "doctype": "SMS Log",
                "recipient": mobile,
                "message_type": "Credit Sale",
                "message": msg,
                "reference_doctype": "Fuel Sale",
                "reference_name": sale_name,
            })
            sms.insert(ignore_permissions=True)
    except Exception:
        pass


def _send_cash_sale_sms(customer, sale_name, amount, payment_mode):
    """Send SMS on cash/card/UPI sale"""
    try:
        settings = frappe.get_single("Notification Settings")
        if not settings.enable_sms:
            return
        mobile = frappe.db.get_value("PP Customer", customer, "mobile")
        station = frappe.db.get_single_value("Station Configuration", "station_name") or "Station"
        if mobile:
            msg = f"Dear {customer}, payment of Rs.{amount} received via {payment_mode}. Thank you! - {station}"
            sms = frappe.get_doc({
                "doctype": "SMS Log",
                "recipient": mobile,
                "message_type": "Payment Receipt",
                "message": msg,
                "reference_doctype": "Fuel Sale",
                "reference_name": sale_name,
            })
            sms.insert(ignore_permissions=True)
    except Exception:
        pass


def _send_payment_receipt_sms(customer, receipt_name, amount, mode):
    """Send SMS on payment receipt"""
    try:
        settings = frappe.get_single("Notification Settings")
        if not settings.enable_sms:
            return
        mobile = frappe.db.get_value("PP Customer", customer, "mobile")
        balance = frappe.db.sql("""
            SELECT IFNULL(SUM(balance_amount), 0) as balance
            FROM `tabCredit Sale Invoice`
            WHERE customer = %s AND docstatus = 1 AND balance_amount > 0
        """, (customer,), as_dict=True)
        station = frappe.db.get_single_value("Station Configuration", "station_name") or "Station"
        if mobile and settings.sms_payment_receipt:
            msg = settings.sms_payment_receipt.format(
                customer=customer, amount=amount, mode=mode or "Cash",
                balance=balance[0].balance if balance else 0, station=station
            )
            sms = frappe.get_doc({
                "doctype": "SMS Log",
                "recipient": mobile,
                "message_type": "Payment Receipt",
                "message": msg,
                "reference_doctype": "Payment Receipt",
                "reference_name": receipt_name,
            })
            sms.insert(ignore_permissions=True)
    except Exception:
        pass


def _update_credit_limit(customer):
    """Recalculate and update credit limit ledger for a customer."""
    if not customer:
        return
    try:
        cl = frappe.db.get_value("Credit Limit Ledger", {"customer": customer}, ["name", "limit_amount"], as_dict=True)
        if not cl:
            return

        total_unpaid = frappe.db.sql("""
            SELECT IFNULL(SUM(balance_amount), 0) as total
            FROM `tabCredit Sale Invoice`
            WHERE customer = %s AND docstatus = 1 AND status != 'Paid'
        """, (customer,), as_dict=True)

        used = total_unpaid[0].total or 0
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
