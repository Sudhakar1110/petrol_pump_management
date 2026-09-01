frappe.pages['customer-credit-portal'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({parent: wrapper, title: 'Customer Credit Portal', single_column: true});
    page.add_field({fieldname: 'info', fieldtype: 'HTML'});
    page.fields_dict.info.$wrapper.html('<div class="text-center" style="padding:20px"><h4>Customer Credit Portal</h4><p>Select a customer to view credit details</p></div>');
};
