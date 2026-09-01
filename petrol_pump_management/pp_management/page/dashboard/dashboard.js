frappe.pages['petrol-pump-dashboard'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({parent: wrapper, title: 'Petrol Pump Dashboard', single_column: true});
    page.add_field({fieldname: 'info', fieldtype: 'HTML'});
    page.fields_dict.info.$wrapper.html('<div class="text-center" style="padding:20px"><h4>Petrol Pump Management</h4><p>Use the sidebar to navigate to DocTypes and Reports</p></div>');
};
