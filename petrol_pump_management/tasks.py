import frappe
from frappe.utils import today, add_days, getdate, flt, nowdate


def daily_stock_reconciliation():
    """Auto-compute daily stock register for each tank"""
    tanks = frappe.get_all("Tank Master", filters={"is_active": 1}, fields=["name", "fuel_type"])
    for tank in tanks:
        existing = frappe.db.exists("Daily Stock Register", {"tank": tank.name, "date": today()})
        if existing:
            continue
        # Get previous day closing stock
        prev = frappe.db.sql("""
            SELECT closing_stock FROM `tabDaily Stock Register`
            WHERE tank = %s AND date < %s ORDER BY date DESC LIMIT 1
        """, (tank.name, today()), as_dict=True)
        opening = prev[0].closing_stock if prev else 0
        # Get today's sales
        sales = frappe.db.sql("""
            SELECT IFNULL(SUM(fs.qty_litres), 0) as total_sale
            FROM `tabFuel Sale` fs
            JOIN `tabNozzle Master` nm ON fs.nozzle = nm.name
            WHERE nm.tank = %s AND fs.sale_date = %s AND fs.docstatus = 1
        """, (tank.name, today()), as_dict=True)
        # Get today's purchases
        purchases = frappe.db.sql("""
            SELECT IFNULL(SUM(received_qty), 0) as total_purchase
            FROM `tabStock Purchase Decantation`
            WHERE tank = %s AND DATE(decantation_datetime) = %s AND docstatus = 1
        """, (tank.name, today()), as_dict=True)
        sale_qty = sales[0].total_sale if sales else 0
        purchase_qty = purchases[0].total_purchase if purchases else 0
        closing = flt(opening) + flt(purchase_qty) - flt(sale_qty)
        dsr = frappe.get_doc({
            "doctype": "Daily Stock Register",
            "tank": tank.name,
            "date": today(),
            "opening_stock": opening,
            "purchase_qty": purchase_qty,
            "sale_qty": sale_qty,
            "closing_stock": closing,
        })
        dsr.insert(ignore_permissions=True)


def send_credit_reminders():
    """Send reminders for overdue credit invoices"""
    overdue = frappe.db.sql("""
        SELECT name, customer, due_date, balance_amount
        FROM `tabCredit Sale Invoice`
        WHERE due_date < %s AND status != 'Paid' AND docstatus = 1 AND balance_amount > 0
    """, (today(),), as_dict=True)
    for inv in overdue:
        try:
            settings = frappe.get_single("Notification Settings")
            if not settings.enable_sms:
                continue
            mobile = frappe.db.get_value("PP Customer", inv.customer, "mobile")
            if mobile and settings.sms_advance_reminder:
                msg = settings.sms_advance_reminder.format(
                    customer=inv.customer, amount=inv.balance_amount,
                    station=frappe.db.get_single_value("Station Configuration", "station_name") or "Station"
                )
                sms = frappe.get_doc({
                    "doctype": "SMS Log",
                    "recipient": mobile,
                    "message_type": "Advance Reminder",
                    "message": msg,
                    "reference_doctype": "Credit Sale Invoice",
                    "reference_name": inv.name,
                })
                sms.insert(ignore_permissions=True)
        except Exception:
            pass


def check_stock_levels():
    """Check stock levels and send alerts for low stock"""
    tanks = frappe.get_all("Tank Master", filters={"is_active": 1}, fields=["name", "fuel_type", "safe_stock_level", "current_stock"])
    for tank in tanks:
        if tank.safe_stock_level and tank.current_stock and tank.current_stock < tank.safe_stock_level:
            try:
                settings = frappe.get_single("Notification Settings")
                if settings.enable_sms:
                    station = frappe.db.get_single_value("Station Configuration", "station_name") or "Station"
                    msg = f"LOW STOCK ALERT: {tank.fuel_type} tank {tank.name} has only {tank.current_stock}L remaining. Safe level: {tank.safe_stock_level}L. - {station}"
                    sms = frappe.get_doc({
                        "doctype": "SMS Log",
                        "recipient": frappe.db.get_single_value("Station Configuration", "contact_email") or "",
                        "message_type": "Custom",
                        "message": msg,
                    })
                    sms.insert(ignore_permissions=True)
            except Exception:
                pass


def auto_block_credit_customers():
    """Auto-block customers who exceeded credit limit"""
    customers = frappe.db.sql("""
        SELECT c.name, c.credit_limit, c.is_blocked,
               IFNULL(SUM(inv.balance_amount), 0) as outstanding
        FROM `tabPP Customer` c
        LEFT JOIN `tabCredit Sale Invoice` inv ON inv.customer = c.name AND inv.docstatus = 1 AND inv.balance_amount > 0
        WHERE c.is_blocked = 0
        GROUP BY c.name
        HAVING outstanding > c.credit_limit AND c.credit_limit > 0
    """, as_dict=True)
    for cust in customers:
        frappe.db.set_value("PP Customer", cust.name, "is_blocked", 1)
        # Send limit breach SMS
        try:
            settings = frappe.get_single("Notification Settings")
            if settings.enable_sms and settings.sms_limit_breach:
                mobile = frappe.db.get_value("PP Customer", cust.name, "mobile")
                station = frappe.db.get_single_value("Station Configuration", "station_name") or "Station"
                if mobile:
                    msg = settings.sms_limit_breach.format(
                        customer=cust.name, limit=cust.credit_limit,
                        balance=cust.outstanding, station=station
                    )
                    sms = frappe.get_doc({
                        "doctype": "SMS Log",
                        "recipient": mobile,
                        "message_type": "Limit Breach",
                        "message": msg,
                    })
                    sms.insert(ignore_permissions=True)
        except Exception:
            pass


def send_expiry_alerts():
    """Send alerts for items expiring soon"""
    lube_stock = frappe.db.sql("""
        SELECT name, lube_name, expiry_date, quantity
        FROM `tabLube Stock`
        WHERE expiry_date BETWEEN %s AND %s AND quantity > 0
    """, (today(), add_days(today(), 30)), as_dict=True)
    for lube in lube_stock:
        try:
            settings = frappe.get_single("Notification Settings")
            if settings.enable_sms:
                station = frappe.db.get_single_value("Station Configuration", "station_name") or "Station"
                msg = f"EXPIRY ALERT: {lube.lube_name} expires on {lube.expiry_date}. Remaining: {lube.quantity}. - {station}"
                sms = frappe.get_doc({
                    "doctype": "SMS Log",
                    "recipient": frappe.db.get_single_value("Station Configuration", "contact_email") or "",
                    "message_type": "Renewal Alert",
                    "message": msg,
                })
                sms.insert(ignore_permissions=True)
        except Exception:
            pass


def expire_reward_points():
    """Expire reward points older than 1 year"""
    frappe.db.sql("""
        UPDATE `tabReward Points Ledger`
        SET status = 'Expired'
        WHERE transaction_type = 'Earned' AND status = 'Active'
        AND transaction_date < DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
    """)


def generate_credit_statements():
    """Auto-generate weekly credit statements for all customers with outstanding"""
    customers = frappe.db.sql("""
        SELECT DISTINCT customer FROM `tabCredit Sale Invoice`
        WHERE docstatus = 1 AND balance_amount > 0
    """, as_dict=True)
    for cust in customers:
        existing = frappe.db.exists("Credit Statement", {
            "customer": cust.customer,
            "period_start": add_days(today(), -7),
        })
        if existing:
            continue
        invoices = frappe.db.sql("""
            SELECT name, amount, balance_amount, due_date
            FROM `tabCredit Sale Invoice`
            WHERE customer = %s AND docstatus = 1 AND balance_amount > 0
        """, (cust.customer,), as_dict=True)
        total_outstanding = sum(inv.balance_amount or 0 for inv in invoices)
        statement = frappe.get_doc({
            "doctype": "Credit Statement",
            "customer": cust.customer,
            "period_start": add_days(today(), -7),
            "period_end": today(),
            "total_outstanding": total_outstanding,
            "status": "Generated",
        })
        for inv in invoices:
            statement.append("invoices", {
                "invoice_number": inv.name,
                "amount": inv.amount,
                "balance_amount": inv.balance_amount,
                "due_date": inv.due_date,
            })
        statement.insert(ignore_permissions=True)


def calculate_late_interest():
    """Calculate interest on overdue credit invoices"""
    overdue = frappe.db.sql("""
        SELECT name, customer, due_date, balance_amount
        FROM `tabCredit Sale Invoice`
        WHERE due_date < %s AND status != 'Paid' AND docstatus = 1
        AND balance_amount > 0 AND interest_applicable = 1
    """, (today(),), as_dict=True)
    for inv in overdue:
        overdue_days = (getdate(today()) - getdate(inv.due_date)).days
        if overdue_days > 0:
            interest_rate = 18  # 18% per annum = 1.5% per month
            interest = round((inv.balance_amount * interest_rate * overdue_days) / (365 * 100), 2)
            if interest > 0:
                frappe.db.set_value("Credit Sale Invoice", inv.name, "interest_amount", interest)


def generate_monthly_reports():
    """Generate monthly business reports"""
    pass  # Reports are generated on-demand via the UI


def send_limit_breach_sms():
    """Send SMS for credit limit breaches"""
    auto_block_credit_customers()


def auto_calculate_evaporation():
    """Auto-calculate evaporation loss for all active tanks"""
    tanks = frappe.get_all("Tank Master", filters={"is_active": 1}, fields=["name"])
    for tank in tanks:
        try:
            from petrol_pump_management.pp_management.doctype.evaporation_loss.evaporation_loss import auto_calculate_evaporation_loss
            auto_calculate_evaporation_loss(tank.name, add_days(today(), -1))
        except Exception:
            pass


def send_lube_expiry_alerts():
    """Send alerts for lube stock expiring soon"""
    send_expiry_alerts()


def send_weekly_credit_email():
    """Send weekly credit statement emails to customers"""
    customers = frappe.db.sql("""
        SELECT DISTINCT c.name, c.mobile
        FROM `tabPP Customer` c
        JOIN `tabCredit Sale Invoice` inv ON inv.customer = c.name
        WHERE inv.docstatus = 1 AND inv.balance_amount > 0
    """, as_dict=True)
    for cust in customers:
        try:
            settings = frappe.get_single("Notification Settings")
            if not settings.enable_email:
                continue
            statement = frappe.db.get_value("Credit Statement", {"customer": cust.name}, "name", order_by="creation desc")
            if statement:
                stmt_doc = frappe.get_doc("Credit Statement", statement)
                email = frappe.get_doc({
                    "doctype": "Email Log",
                    "recipient_email": cust.mobile,
                    "subject": f"Credit Statement - {cust.name}",
                    "email_type": "Credit Statement",
                    "message_html": f"<h3>Credit Statement</h3><p>Outstanding: Rs.{stmt_doc.total_outstanding}</p>",
                    "reference_doctype": "Credit Statement",
                    "reference_name": statement,
                })
                email.insert(ignore_permissions=True)
        except Exception:
            pass


def auto_generate_payroll():
    """Auto-generate salary slips for all active employees"""
    from petrol_pump_management.pp_management.doctype.salary_slip_entry.salary_slip_entry import generate_salary_slips_for_month
    period = getdate(today()).strftime("%m-%Y")
    generate_salary_slips_for_month(period)


def auto_generate_commission():
    """Auto-generate commission payments for all salesmen"""
    from petrol_pump_management.pp_management.doctype.commission_payment.commission_payment import generate_commission_for_month
    period = getdate(today()).strftime("%m-%Y")
    generate_commission_for_month(period)


def send_monthly_statement_email():
    """Send monthly credit statements via email"""
    send_weekly_credit_email()
