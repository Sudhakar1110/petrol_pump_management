frappe.pages['petrol-pump-dashboard'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Petrol Pump Dashboard',
        single_column: true
    });

    // Station Info
    frappe.call({
        method: 'petrol_pump_management.api.get_station_configuration',
        callback: function(r) {
            if (r.message) {
                page.add_field({
                    fieldname: 'station_info',
                    fieldtype: 'HTML',
                    label: 'Station'
                });
                page.fields_dict.station_info.$wrapper.html(
                    `<div class="row" style="padding: 15px;">
                        <div class="col-md-3">
                            <div class="card text-center">
                                <div class="card-body">
                                    <h5 class="card-title">${r.message.station_name || 'N/A'}</h5>
                                    <p class="text-muted">Station Name</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="card text-center">
                                <div class="card-body">
                                    <h5 class="card-title">${r.message.gst_number || 'N/A'}</h5>
                                    <p class="text-muted">GST Number</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="card text-center">
                                <div class="card-body">
                                    <h5 class="card-title">${r.message.default_fuel_unit || 'Litre'}</h5>
                                    <p class="text-muted">Fuel Unit</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-3">
                            <div class="card text-center">
                                <div class="card-body">
                                    <h5 class="card-title">${r.message.default_currency || 'INR'}</h5>
                                    <p class="text-muted">Currency</p>
                                </div>
                            </div>
                        </div>
                    </div>`
                );
            }
        }
    });

    // Quick Links Section
    page.add_field({
        fieldname: 'quick_links',
        fieldtype: 'HTML',
        label: 'Quick Actions'
    });

    page.fields_dict.quick_links.$wrapper.html(
        `<div class="row" style="padding: 15px;">
            <div class="col-md-3">
                <a href="/app/fuel-sale" class="btn btn-primary btn-block">Record Fuel Sale</a>
            </div>
            <div class="col-md-3">
                <a href="/app/shift" class="btn btn-success btn-block">Manage Shift</a>
            </div>
            <div class="col-md-3">
                <a href="/app/credit-sale-invoice" class="btn btn-warning btn-block">Credit Invoices</a>
            </div>
            <div class="col-md-3">
                <a href="/app/daily-stock-register" class="btn btn-info btn-block">Stock Register</a>
            </div>
        </div>
        <div class="row" style="padding: 5px 15px 15px;">
            <div class="col-md-3">
                <a href="/app/fuel-price-master" class="btn btn-secondary btn-block">Update Fuel Rate</a>
            </div>
            <div class="col-md-3">
                <a href="/app/stock-purchase-decantation" class="btn btn-danger btn-block">Record Decantation</a>
            </div>
            <div class="col-md-3">
                <a href="/app/payment-receipt" class="btn btn-primary btn-block">Record Payment</a>
            </div>
            <div class="col-md-3">
                <a href="/app/employee-master" class="btn btn-success btn-block">Employee Master</a>
            </div>
        </div>`
    );

    // Reports Section
    page.add_field({
        fieldname: 'reports_section',
        fieldtype: 'HTML',
        label: 'Reports'
    });

    page.fields_dict.reports_section.$wrapper.html(
        `<div class="row" style="padding: 15px;">
            <div class="col-md-4">
                <a href="/report/Daily Sales Summary" class="btn btn-outline-primary btn-block">Daily Sales Summary</a>
            </div>
            <div class="col-md-4">
                <a href="/report/Shift Settlement Report" class="btn btn-outline-success btn-block">Shift Settlement</a>
            </div>
            <div class="col-md-4">
                <a href="/report/Stock Variation Report" class="btn btn-outline-info btn-block">Stock Variation</a>
            </div>
        </div>
        <div class="row" style="padding: 5px 15px 15px;">
            <div class="col-md-4">
                <a href="/report/Credit Customer Ageing" class="btn btn-outline-warning btn-block">Credit Ageing</a>
            </div>
            <div class="col-md-4">
                <a href="/report/GST VAT Summary" class="btn btn-outline-danger btn-block">GST Summary</a>
            </div>
            <div class="col-md-4">
                <a href="/report/Profit Loss Statement" class="btn btn-outline-secondary btn-block">P&L Statement</a>
            </div>
        </div>`
    );
};
