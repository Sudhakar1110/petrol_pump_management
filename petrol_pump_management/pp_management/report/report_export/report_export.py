import frappe
from frappe import _
import csv
import io


def execute(filters=None):
    columns = [
        {"fieldname": "date", "fieldtype": "Date", "label": "Date", "width": 100},
        {"fieldname": "type", "fieldtype": "Data", "label": "Type", "width": 120},
        {"fieldname": "reference", "fieldtype": "Data", "label": "Reference", "width": 150},
        {"fieldname": "party", "fieldtype": "Data", "label": "Party", "width": 150},
        {"fieldname": "quantity", "fieldtype": "Float", "label": "Quantity", "width": 100},
        {"fieldname": "amount", "fieldtype": "Currency", "label": "Amount", "width": 120},
        {"fieldname": "payment_mode", "fieldtype": "Data", "label": "Payment Mode", "width": 100},
        {"fieldname": "status", "fieldtype": "Data", "label": "Status", "width": 80},
    ]

    report_type = filters.get("report_type") if filters else "All"
    from_date = filters.get("from_date") if filters else None
    to_date = filters.get("to_date") if filters else None

    conditions = "WHERE docstatus = 1"
    params = []
    if from_date:
        conditions += " AND sale_date >= %s"
        params.append(from_date)
    if to_date:
        conditions += " AND sale_date <= %s"
        params.append(to_date)

    data = []

    if report_type in ("Daily Sales", "All"):
        sales = frappe.db.sql(f"""
            SELECT sale_date as date, 'Fuel Sale' as type, name as reference,
                   COALESCE(customer, 'Cash') as party, qty_litres as quantity,
                   amount, payment_mode, 'Submitted' as status
            FROM `tabFuel Sale`
            {conditions}
            ORDER BY sale_date DESC
        """, params, as_dict=True)
        data.extend(sales)

    if report_type in ("Stock Register", "All"):
        stock = frappe.db.sql(f"""
            SELECT date, 'Stock Register' as type, name as reference,
                   tank as party, sale_qty as quantity,
                   0 as amount, '' as payment_mode, 'Active' as status
            FROM `tabDaily Stock Register`
            WHERE 1=1
            {"AND date >= %s" if from_date else ""}
            {"AND date <= %s" if to_date else ""}
            ORDER BY date DESC
        """, [p for p in [from_date, to_date] if p], as_dict=True)
        data.extend(stock)

    data.sort(key=lambda x: x.get("date") or "", reverse=True)

    # Create CSV download link
    if data:
        csv_content = io.StringIO()
        writer = csv.DictWriter(csv_content, fieldnames=[c["fieldname"] for c in columns])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

        file_name = f"report_export_{frappe.utils.now_datetime().strftime('%Y%m%d_%H%M%S')}.csv"
        csv_url = frappe.utils.get_url(f"/api/method/frappe.client.get_file?file_name={file_name}")

    return columns, data
