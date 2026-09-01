// Petrol Pump Management - Client Library
frappe.provide('petrol_pump');
petrol_pump = {
    get_fuel_rate: function(fuel_type) {
        return frappe.call({method:'petrol_pump_management.api.get_fuel_rate', args:{fuel_type}});
    }
};
