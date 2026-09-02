app_name = "petrol_pump_management"
app_title = "Petrol Pump Management"
app_publisher = "Bizaxl Optimisations LLP"
app_description = "Complete Petrol Pump / Fuel Station Management Application"
app_email = "markcom@bizaxl.com"
app_license = "MIT"
required_apps = ["frappe", "erpnext"]

# Install
# ------------------
after_install = "petrol_pump_management.setup.after_install"
after_migrate = "petrol_pump_management.setup.after_migrate"

# Fixtures
# ------------------
fixtures = [
    {
        "dt": "Station Configuration",
        "filters": [["name", "=", "Main Station"]],
    },
    {
        "dt": "Fuel Price Master",
        "filters": [["is_active", "=", 1]],
    },
]

# Jinja
# ------------------
jinja = {
    "methods": [
        "petrol_pump_management.utils.get_fuel_rate",
        "petrol_pump_management.utils.get_station_config",
    ],
}

# Scheduler Events
# ------------------
scheduler_events = {
    "daily": [
        "petrol_pump_management.tasks.daily_stock_reconciliation",
        "petrol_pump_management.tasks.send_credit_reminders",
        "petrol_pump_management.tasks.check_stock_levels",
        "petrol_pump_management.tasks.auto_block_credit_customers",
        "petrol_pump_management.tasks.send_expiry_alerts",
        "petrol_pump_management.tasks.expire_reward_points",
        "petrol_pump_management.tasks.send_limit_breach_sms",
        "petrol_pump_management.tasks.auto_calculate_evaporation",
        "petrol_pump_management.tasks.send_lube_expiry_alerts",
        "petrol_pump_management.tasks.send_daily_business_summary",
        "petrol_pump_management.tasks.send_birthday_anniversary_sms",
    ],
    "weekly": [
        "petrol_pump_management.tasks.generate_credit_statements",
        "petrol_pump_management.tasks.send_weekly_credit_email",
    ],
    "monthly": [
        "petrol_pump_management.tasks.generate_monthly_reports",
        "petrol_pump_management.tasks.calculate_late_interest",
        "petrol_pump_management.tasks.auto_generate_payroll",
        "petrol_pump_management.tasks.auto_generate_commission",
        "petrol_pump_management.tasks.send_monthly_statement_email",
    ],
}

# Doc Events
# ------------------
doc_events = {
    "Fuel Sale": {
        "on_submit": "petrol_pump_management.events.on_fuel_sale_submit",
    },
    "Credit Sale Invoice": {
        "on_submit": "petrol_pump_management.events.on_credit_invoice_submit",
    },
    "Payment Receipt": {
        "on_submit": "petrol_pump_management.events.on_payment_receipt_submit",
    },
    "Swipe Settlement": {
        "on_submit": "petrol_pump_management.events.on_swipe_settlement_submit",
    },
}

# Fixtures for new DocTypes
# ------------------
fixtures += [
    {"dt": "Commission Rule", "filters": [["is_active", "=", 1]]},
]
