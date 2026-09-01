import frappe
from frappe import _


def execute(filters=None):
    columns = [
        {"fieldname": "shift_date", "fieldtype": "Date", "label": "Date", "width": 120},
        {"fieldname": "salesman_name", "fieldtype": "Data", "label": "Salesman", "width": 150},
        {"fieldname": "nozzle_no", "fieldtype": "Data", "label": "Nozzle", "width": 100},
        {"fieldname": "fuel_type", "fieldtype": "Data", "label": "Fuel Type", "width": 100},
        {"fieldname": "payment_mode", "fieldtype": "Data", "label": "Payment Mode", "width": 120},
        {"fieldname": "qty_litres", "fieldtype": "Float", "label": "Qty (Litres)", "width": 120},
        {"fieldname": "rate", "fieldtype": "Currency", "label": "Rate", "width": 100},
        {"fieldname": "amount", "fieldtype": "Currency", "label": "Amount", "width": 120},
    ]
    
    conditions = "fs.docstatus = 1"
    if filters.get("from_date"):
        conditions += f" AND fs.sale_date >= '{filters.from_date}'"
    if filters.get("to_date"):
        conditions += f" AND fs.sale_date <= '{filters.to_date}'"
    
    data = frappe.db.sql(f"""
        SELECT fs.sale_date as shift_date,
               em.employee_name as salesman_name,
               nm.nozzle_no,
               tm.fuel_type,
               fs.payment_mode,
               fs.qty_litres,
               fs.rate,
               fs.amount
        FROM `tabFuel Sale` fs
        LEFT JOIN `tabShift` s ON fs.shift = s.name
        LEFT JOIN `tabEmployee Master` em ON s.salesman = em.name
        LEFT JOIN `tabNozzle Master` nm ON fs.nozzle = nm.name
        LEFT JOIN `tabTank Master` tm ON nm.tank = tm.name
        WHERE {conditions}
        ORDER BY fs.sale_date DESC, em.employee_name
    """, as_dict=True)
    
    return columns, data
