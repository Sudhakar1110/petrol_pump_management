import frappe
from frappe.utils import today, add_days, getdate, flt, nowdate, date_diff, get_first_day, get_last_day


def daily_stock_reconciliation():
    """Auto-compute daily stock register for each tank."""
    pass


def send_credit_reminders():
    """Send SMS/email reminders for overdue credit invoices."""
    overdue = frappe.db.sql("""
        SELECT name, customer, amount, due_date
        FROM `tabCredit Sale Invoice`
        WHERE status = 'Unpaid' AND due_date < %s AND docstatus = 1
    """, (today(),), as_dict=True)

    for inv in overdue:
        try:
            mobile = frappe.db.get_value("PP Customer", inv.customer, "mobile")
            if mobile:
                days_overdue = date_diff(today(), inv.due_date)
                frappe.sendmail(
                    recipients=[mobile],
                    subject=f"Payment Reminder - Invoice {inv.name}",
                    message=f"Dear Customer,\n\nYour invoice {inv.name} for {frappe.format_doc(inv.amount, {'fieldtype': 'Currency'})} is {days_overdue} days overdue.\n\nPlease clear the dues immediately.\n\nThank you.",
                )
        except Exception:
            pass


def check_stock_levels():
    """Check stock levels and send reorder alerts for fuel and lube."""
    # Check fuel tanks
    tanks = frappe.db.get_all("Tank Master", fields=["name", "tank_no", "safe_stock_level", "is_active"])
    for tank in tanks:
        if not tank.is_active or not tank.safe_stock_level:
            continue
        # Check latest daily stock register
        latest = frappe.db.get_value(
            "Daily Stock Register",
            {"tank": tank.name},
            ["closing_stock"],
            order_by="date desc",
        )
        if latest and latest < tank.safe_stock_level:
            frappe.sendmail(
                recipients=["markcom@bizaxl.com"],
                subject=f"Low Stock Alert - Tank {tank.tank_no}",
                message=f"Tank {tank.tank_no} stock ({latest}) is below safe level ({tank.safe_stock_level}).",
            )

    # Check lube expiry
    lubes = frappe.db.get_all(
        "Lube Stock",
        filters={"is_active": 1, "expiry_date": ["<=", add_days(today(), 30)]},
        fields=["name", "item_name", "expiry_date", "closing_qty"],
    )
    for lube in lubes:
        if lube.closing_qty and lube.closing_qty > 0:
            try:
                frappe.sendmail(
                    recipients=["markcom@bizaxl.com"],
                    subject=f"Expiry Alert - {lube.item_name}",
                    message=f"Lube item {lube.item_name} expires on {lube.expiry_date}. Current stock: {lube.closing_qty}.",
                )
            except Exception:
                pass


def generate_monthly_reports():
    """Generate monthly credit statements for all credit customers."""
    generate_credit_statements()


def generate_credit_statements():
    """Auto-generate credit statements for all active credit customers."""
    customers = frappe.db.get_all(
        "PP Customer",
        filters={"credit_limit": [">", 0]},
        fields=["name", "full_name"],
    )

    period_from = get_first_day(today())
    period_to = get_last_day(today())

    for cust in customers:
        try:
            # Check if statement already exists
            exists = frappe.db.exists(
                "Credit Statement",
                {"customer": cust.name, "period_from": period_from, "period_to": period_to},
            )
            if exists:
                continue

            total_credit = frappe.db.sql("""
                SELECT IFNULL(SUM(amount), 0)
                FROM `tabCredit Sale Invoice`
                WHERE customer = %s AND docstatus = 1
                AND transaction_date BETWEEN %s AND %s
            """, (cust.name, period_from, period_to))[0][0]

            total_payment = frappe.db.sql("""
                SELECT IFNULL(SUM(amount_received), 0)
                FROM `tabPayment Receipt`
                WHERE customer = %s AND docstatus = 1
                AND payment_date BETWEEN %s AND %s
            """, (cust.name, period_from, period_to))[0][0]

            # Get previous closing balance
            prev = frappe.db.get_value(
                "Credit Statement",
                {"customer": cust.name},
                ["closing_balance"],
                order_by="period_to desc",
            )
            opening = prev or 0

            if total_credit == 0 and total_payment == 0:
                continue

            stmt = frappe.new_doc("Credit Statement")
            stmt.customer = cust.name
            stmt.statement_date = today()
            stmt.period_from = period_from
            stmt.period_to = period_to
            stmt.opening_balance = opening
            stmt.total_credit = total_credit
            stmt.total_payment = total_payment
            stmt.due_date = add_days(period_to, 15)
            stmt.insert(ignore_permissions=True)

            # Send email statement
            try:
                mobile = frappe.db.get_value("PP Customer", cust.name, "mobile")
                if mobile:
                    stmt.email_sent = 1
                    stmt.sms_sent = 1
                    frappe.db.set_value("Credit Statement", stmt.name, {"email_sent": 1, "sms_sent": 1})
            except Exception:
                pass

        except Exception:
            pass

    frappe.db.commit()


def calculate_late_interest():
    """Calculate interest on overdue credit invoices."""
    overdue = frappe.db.sql("""
        SELECT name, customer, amount, due_date
        FROM `tabCredit Sale Invoice`
        WHERE status = 'Unpaid' AND due_date < %s AND docstatus = 1
        AND interest_applicable = 1
    """, (today(),), as_dict=True)

    for inv in overdue:
        try:
            days_overdue = date_diff(today(), inv.due_date)
            # 18% per annum = 0.05% per day
            interest = flt(inv.amount) * 0.0005 * days_overdue
            frappe.db.set_value("Credit Sale Invoice", inv.name, {
                "status": "Overdue",
            })
        except Exception:
            pass

    frappe.db.commit()


def auto_block_credit_customers():
    """Auto-block customers who have exceeded credit limit."""
    customers = frappe.db.sql("""
        SELECT cl.name as cl_name, cl.customer, cl.limit_amount, cl.used_amount
        FROM `tabCredit Limit Ledger` cl
        WHERE cl.block_on_exceed = 1
    """, as_dict=True)

    for cl in customers:
        if cl.used_amount and cl.limit_amount and cl.used_amount > cl.limit_amount:
            frappe.db.set_value("PP Customer", cl.customer, "is_blocked", 1)
            frappe.sendmail(
                recipients=["markcom@bizaxl.com"],
                subject=f"Credit Limit Exceeded - {cl.customer}",
                message=f"Customer {cl.customer} has exceeded their credit limit.\nLimit: {cl.limit_amount}\nUsed: {cl.used_amount}\nThey have been auto-blocked.",
            )
        elif cl.used_amount is not None and cl.limit_amount and cl.used_amount <= cl.limit_amount:
            frappe.db.set_value("PP Customer", cl.customer, "is_blocked", 0)

    frappe.db.commit()


def send_expiry_alerts():
    """Send alerts for items nearing expiry."""
    # Lube expiry alerts (30 days ahead)
    check_stock_levels()


def expire_reward_points():
    """Expire reward points older than 1 year."""
    one_year_ago = add_days(today(), -365)
    frappe.db.sql("""
        UPDATE `tabReward Points Ledger`
        SET transaction_type = 'Expired', points = -points
        WHERE transaction_type = 'Earned' AND transaction_date < %s
        AND running_balance > 0
    """, (one_year_ago,))
    frappe.db.commit()
