"""
Petrol Pump Management - Scheduled Tasks
Daily and monthly automated tasks
"""

import frappe


def daily_stock_reconciliation():
    """Daily task to reconcile stock across all active tanks."""
    tanks = frappe.get_all("Tank Master", filters={"is_active": 1})
    today = frappe.utils.today()

    for tank in tanks:
        existing = frappe.get_all(
            "Daily Stock Register",
            filters={"tank": tank.name, "date": today},
            limit=1,
        )
        if not existing:
            # Get previous day's closing stock
            prev = frappe.get_all(
                "Daily Stock Register",
                filters={"tank": tank.name},
                order_by="date desc",
                limit=1,
                fields=["closing_stock"],
            )
            opening = prev[0].closing_stock if prev else tank.current_stock or 0

            dsr = frappe.new_doc("Daily Stock Register")
            dsr.tank = tank.name
            dsr.date = today
            dsr.opening_stock = opening
            dsr.flags.ignore_permissions = True
            dsr.insert()


def send_credit_reminders():
    """Daily task to send reminders for overdue credit invoices."""
    overdue = frappe.get_all(
        "Credit Sale Invoice",
        filters={"status": ["in", ["Unpaid", "Partially Paid"]], "due_date": ["<", frappe.utils.today()]},
        fields=["name", "customer", "balance_amount", "due_date"],
    )

    for inv in overdue:
        customer = frappe.get_doc("PP Customer", inv.customer)
        frappe.sendmail(
            recipients=[customer.email] if customer.email else [],
            subject=f"Payment Reminder - Invoice {inv.name}",
            message=f"Dear {customer.full_name},<br><br>"
            f"Your invoice {inv.name} of Rs. {inv.balance_amount} "
            f"was due on {inv.due_date}. Please arrange payment at the earliest.<br><br>"
            f"Regards,<br>{frappe.db.get_single_value('Station Configuration', 'station_name') or 'Fuel Station'}",
        )

        # SMS reminder
        if customer.mobile:
            frappe.sendmail(
                recipients=[],
                subject="Credit Payment Reminder",
                message=f"Dear {customer.full_name}, your fuel credit payment of Rs. {inv.balance_amount} is overdue. Please pay at the earliest.",
            )


def check_stock_levels():
    """Daily task to check stock levels and send reorder alerts."""
    tanks = frappe.get_all(
        "Tank Master",
        filters={"is_active": 1},
        fields=["name", "tank_no", "fuel_type", "current_stock", "safe_stock_level"],
    )

    for tank in tanks:
        if tank.safe_stock_level and tank.current_stock and tank.current_stock < tank.safe_stock_level:
            frappe.sendmail(
                recipients=[],
                subject=f"Low Stock Alert - Tank {tank.tank_no}",
                message=f"Tank {tank.tank_no} ({tank.fuel_type}) is running low. "
                f"Current stock: {tank.current_stock} litres, "
                f"Safe level: {tank.safe_stock_level} litres. "
                f"Please arrange fuel replenishment.",
            )


def generate_monthly_reports():
    """Monthly task to generate credit statements and compliance reports."""
    # Generate credit statements for all active customers
    customers = frappe.get_all(
        "PP Customer",
        filters={"credit_limit": [">", 0]},
        fields=["name", "full_name", "email"],
    )

    for cust in customers:
        unpaid = frappe.get_all(
            "Credit Sale Invoice",
            filters={"customer": cust.name, "status": ["in", ["Unpaid", "Partially Paid", "Overdue"]]},
            fields=["name", "amount", "amount_paid", "due_date", "sale_date"],
        )

        if unpaid and cust.email:
            html = f"<h3>Monthly Credit Statement - {cust.full_name}</h3>"
            html += "<table border='1' cellpadding='5'><tr><th>Invoice</th><th>Amount</th><th>Paid</th><th>Balance</th><th>Due Date</th></tr>"
            for inv in unpaid:
                balance = (inv.amount or 0) - (inv.amount_paid or 0)
                html += f"<tr><td>{inv.name}</td><td>{inv.amount}</td><td>{inv.amount_paid or 0}</td><td>{balance}</td><td>{inv.due_date}</td></tr>"
            html += "</table>"

            frappe.sendmail(
                recipients=[cust.email],
                subject=f"Monthly Credit Statement - {cust.full_name}",
                message=html,
            )
