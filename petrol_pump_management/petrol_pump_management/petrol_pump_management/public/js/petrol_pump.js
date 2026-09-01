// Petrol Pump Management - Client Script

frappe.provide('petrol_pump_management');

petrol_pump_management = {
    get_fuel_rate: function(fuel_type) {
        return frappe.call({
            method: 'petrol_pump_management.api.get_fuel_rate',
            args: { fuel_type: fuel_type }
        });
    },

    get_credit_balance: function(customer) {
        return frappe.call({
            method: 'petrol_pump_management.api.get_customer_credit_balance',
            args: { customer: customer }
        });
    }
};
