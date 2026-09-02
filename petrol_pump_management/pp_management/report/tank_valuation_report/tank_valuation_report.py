import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "tank", "fieldtype": "Data", "label": "Tank", "width": 100},
        {"fieldname": "fuel_type", "fieldtype": "Data", "label": "Fuel Type", "width": 100},
        {"fieldname": "capacity", "fieldtype": "Float", "label": "Capacity (L)", "width": 100},
        {"fieldname": "current_stock", "fieldtype": "Float", "label": "Current Stock (L)", "width": 120},
        {"fieldname": "current_rate", "fieldtype": "Currency", "label": "Current Rate", "width": 100},
        {"fieldname": "stock_value", "fieldtype": "Currency", "label": "Stock Value", "width": 120},
        {"fieldname": "utilization", "fieldtype": "Percent", "label": "Utilization %", "width": 100},
        {"fieldname": "safe_level", "fieldtype": "Float", "label": "Safe Level (L)", "width": 100},
        {"fieldname": "status", "fieldtype": "Data", "label": "Status", "width": 80},
    ]

    tank = filters.get("tank") if filters else None
    conditions = "WHERE tm.is_active = 1"
    params = []
    if tank:
        conditions += " AND tm.name = %s"
        params.append(tank)

    data = frappe.db.sql(f"""
        SELECT tm.name as tank, tm.fuel_type,
               tm.capacity_litres as capacity,
               tm.current_stock,
               COALESCE(fpm.rate_per_litre, 0) as current_rate,
               ROUND(COALESCE(tm.current_stock, 0) * COALESCE(fpm.rate_per_litre, 0), 2) as stock_value,
               ROUND(COALESCE(tm.current_stock, 0) / NULLIF(tm.capacity_litres, 0) * 100, 1) as utilization,
               tm.safe_stock_level as safe_level,
               CASE
                   WHEN tm.current_stock < tm.safe_stock_level THEN 'Low Stock'
                   WHEN tm.current_stock > tm.capacity_litres * 0.9 THEN 'Near Full'
                   ELSE 'Normal'
               END as status
        FROM `tabTank Master` tm
        LEFT JOIN `tabFuel Price Master` fpm ON tm.fuel_type = fpm.fuel_type AND fpm.is_active = 1
        {conditions}
        ORDER BY tm.fuel_type, tm.name
    """, params, as_dict=True)

    return columns, data
