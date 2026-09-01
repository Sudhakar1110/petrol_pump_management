app_name = "petrol_pump_management"
app_title = "Petrol Pump Management"
app_publisher = "Bizaxl Optimisations LLP"
app_description = "Complete Petrol Pump / Fuel Station Management Application"
app_email = "markcom@bizaxl.com"
app_license = "MIT"
required_apps = ["frappe", "erpnext"]

# Includes
# ------------------

app_include_css = "/assets/petrol_pump_management/css/petrol_pump.css"
app_include_js = "/assets/petrol_pump_management/js/petrol_pump.js"

# Boot session
boot_session = "petrol_pump_management.events.boot_session"

# Document Events
# ------------------

doc_events = {
    "#": {
        "on_submit": "petrol_pump_management.events.on_submit_generic",
    },
}

# Website
# ------------------

website_route_rules = [
    {
        "from_route": "/pp/<path:app_path>",
        "to_route": "petrol_pump_management",
    },
]

# Role and Permission Setup
# ------------------

# After install
after_install = "petrol_pump_management.setup.after_install"

# Fixtures for export
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [["module", "=", "Petrol Pump Management"]],
    },
    {
        "dt": "Property Setter",
        "filters": [["module", "=", "Petrol Pump Management"]],
    },
]

# Override whitelisted methods
override_whitelisted_methods = {
    "petrol_pump_management.api.get_fuel_rate": "petrol_pump_management.api.get_fuel_rate",
    "petrol_pump_management.api.create_credit_sale": "petrol_pump_management.api.create_credit_sale",
}

# Jinja
jinja = {
    "methods": [
        "petrol_pump_management.utils.get_fuel_rate",
        "petrol_pump_management.utils.get_station_config",
    ],
}

# Scheduler Events
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
