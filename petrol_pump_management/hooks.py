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
    ],
    "monthly": [
        "petrol_pump_management.tasks.generate_monthly_reports",
    ],
}

# Doc Events
# ------------------
doc_events = {
    "Fuel Sale": {
        "on_submit": "petrol_pump_management.events.on_fuel_sale_submit",
    },
}
