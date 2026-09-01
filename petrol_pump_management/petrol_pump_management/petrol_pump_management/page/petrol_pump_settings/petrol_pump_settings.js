frappe.pages['petrol-pump-settings'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Petrol Pump Settings',
        single_column: true
    });

    page.add_field({
        fieldname: 'settings_link',
        fieldtype: 'HTML'
    });

    page.fields_dict.settings_link.$wrapper.html(
        `<div class="row" style="padding: 20px;">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header"><h5>Station Configuration</h5></div>
                    <div class="card-body">
                        <a href="/app/station-configuration" class="btn btn-primary">Configure Station</a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header"><h5>Fuel Prices</h5></div>
                    <div class="card-body">
                        <a href="/app/fuel-price-master" class="btn btn-success">Manage Fuel Rates</a>
                    </div>
                </div>
            </div>
        </div>
        <div class="row" style="padding: 0 20px 20px;">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header"><h5>Tank Management</h5></div>
                    <div class="card-body">
                        <a href="/app/tank-master" class="btn btn-info">Manage Tanks</a>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header"><h5>Nozzle Management</h5></div>
                    <div class="card-body">
                        <a href="/app/nozzle-master" class="btn btn-warning">Manage Nozzles</a>
                    </div>
                </div>
            </div>
        </div>`
    );
};
