app_name = "petrol_pump_management"
app_title = "Petrol Pump Management"
app_publisher = "Bizaxl Optimisations LLP"
app_description = "Complete Petrol Pump / Fuel Station Management Application"
app_email = "markcom@bizaxl.com"
app_license = "MIT"
required_apps = ["frappe", "erpnext"]

after_install = "petrol_pump_management.setup.after_install"

jinja = {
    "methods": [
        "petrol_pump_management.utils.get_fuel_rate",
        "petrol_pump_management.utils.get_station_config",
    ],
}

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
