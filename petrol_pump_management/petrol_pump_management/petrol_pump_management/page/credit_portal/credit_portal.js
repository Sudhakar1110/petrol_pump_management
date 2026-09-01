frappe.pages['customer-credit-portal'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Customer Credit Portal',
        single_column: true
    });

    page.add_field({
        fieldname: 'customer_search',
        fieldtype: 'Link',
        label: 'Select Customer',
        options: 'PP Customer',
        onchange: function() {
            var customer = page.fields_dict.customer_search.get_value();
            if (customer) {
                frappe.call({
                    method: 'petrol_pump_management.api.get_customer_credit_balance',
                    args: { customer: customer },
                    callback: function(r) {
                        if (r.message) {
                            var d = r.message;
                            page.fields_dict.portal_info.$wrapper.html(
                                '<div class="row" style="padding:15px">' +
                                '<div class="col-md-3"><div class="card text-center"><div class="card-body">' +
                                '<h5 class="text-danger">₹' + (d.credit_limit||0).toLocaleString() + '</h5>' +
                                '<p class="text-muted">Credit Limit</p></div></div></div>' +
                                '<div class="col-md-3"><div class="card text-center"><div class="card-body">' +
                                '<h5 class="text-warning">₹' + (d.available_credit||0).toLocaleString() + '</h5>' +
                                '<p class="text-muted">Available Credit</p></div></div></div>' +
                                '<div class="col-md-3"><div class="card text-center"><div class="card-body">' +
                                '<h5 class="text-info">' + (d.credit_points||0) + '</h5>' +
                                '<p class="text-muted">Credit Points</p></div></div></div>' +
                                '<div class="col-md-3"><div class="card text-center"><div class="card-body">' +
                                '<h5 class="' + (d.is_blocked ? 'text-danger' : 'text-success') + '">' +
                                (d.is_blocked ? 'BLOCKED' : 'ACTIVE') + '</h5>' +
                                '<p class="text-muted">Account Status</p></div></div></div></div>'
                            );
                        }
                    }
                });
            }
        }
    });

    page.add_field({
        fieldname: 'portal_info',
        fieldtype: 'HTML',
        label: 'Portal Info'
    });

    page.fields_dict.portal_info.$wrapper.html(
        '<div class="text-center" style="padding:40px;color:#999">' +
        '<h4>Select a customer to view credit portal</h4>' +
        '<p>View credit balance, outstanding invoices, and payment history</p></div>'
    );
};
