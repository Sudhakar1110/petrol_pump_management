import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "date", "fieldtype": "Date", "label": "Date", "width": 100},
        {"fieldname": "tank", "fieldtype": "Data", "label": "Tank", "width": 100},
        {"fieldname": "fuel_type", "fieldtype": "Data", "label": "Fuel Type", "width": 100},
        {"fieldname": "opening_stock", "fieldtype": "Float", "label": "Opening (Dip)", "width": 110},
        {"fieldname": "purchase_qty", "fieldtype": "Float", "label": "Purchase", "width": 100},
        {"fieldname": "meter_sale", "fieldtype": "Float", "label": "Meter Sale", "width": 100},
        {"fieldname": "expected_closing", "fieldtype": "Float", "label": "Expected Closing", "width": 120},
        {"fieldname": "actual_closing", "fieldtype": "Float", "label": "Actual Closing (Dip)", "width": 130},
        {"fieldname": "variation", "fieldtype": "Float", "label": "Variation", "width": 100},
        {"fieldname": "variation_pct", "fieldtype": "Percent", "label": "Var %", "width": 80},
    ]

    from_date = filters.get("from_date") if filters else None
    to_date = filters.get("to_date") if filters else None
    tank = filters.get("tank") if filters else None

    conditions = "WHERE 1=1"
    params = []
    if from_date:
        conditions += " AND dsr.date >= %s"
        params.append(from_date)
    if to_date:
        conditions += " AND dsr.date <= %s"
        params.append(to_date)
    if tank:
        conditions += " AND dsr.tank = %s"
        params.append(tank)

    data = frappe.db.sql(f"""
        SELECT dsr.date, dsr.tank, tm.fuel_type,
               dsr.opening_stock, dsr.purchase_qty, dsr.sale_qty as meter_sale,
               (dsr.opening_stock + dsr.purchase_qty - dsr.sale_qty) as expected_closing,
               dsr.closing_stock as actual_closing,
               ((dsr.opening_stock + dsr.purchase_qty - dsr.sale_qty) - dsr.closing_stock) as variation,
               ROUND(((dsr.opening_stock + dsr.purchase_qty - dsr.sale_qty) - dsr.closing_stock) / NULLIF(dsr.opening_stock + dsr.purchase_qty - dsr.sale_qty, 0) * 100, 2) as variation_pct
        FROM `tabDaily Stock Register` dsr
        LEFT JOIN `tabTank Master` tm ON dsr.tank = tm.name
        {conditions}
        ORDER BY dsr.date DESC, dsr.tank
    """, params, as_dict=True)

    return columns, data
