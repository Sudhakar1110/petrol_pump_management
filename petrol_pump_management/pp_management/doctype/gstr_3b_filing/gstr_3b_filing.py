import frappe
from frappe.model.document import Document
import json


class GSTR3BFiling(Document):
    def validate(self):
        self.calculate_totals()
        self.net_tax_payable = (self.total_igst + self.total_cgst + self.total_sgst) - \
                               (self.total_itc_igst + self.total_itc_cgst + self.total_itc_sgst)

    def calculate_totals(self):
        """Auto-calculate totals from fuel sales"""
        period_parts = self.filing_period.split("-")
        month = period_parts[0] if len(period_parts) > 0 else "01"
        year = period_parts[1] if len(period_parts) > 1 else "2026"
        from_date = f"{year}-{month}-01"
        to_date = frappe.utils.add_months(frappe.utils.getdate(from_date), 1)
        to_date = frappe.utils.add_days(to_date, -1)

        sales = frappe.db.sql("""
            SELECT SUM(amount) as total_amount, SUM(qty_litres) as total_qty
            FROM `tabFuel Sale`
            WHERE sale_date BETWEEN %s AND %s AND docstatus = 1
        """, (from_date, to_date), as_dict=True)

        if sales and sales[0].total_amount:
            self.total_taxable_value = sales[0].total_amount
            self.total_outward_supplies = sales[0].total_qty or 0
            self.total_cgst = round(sales[0].total_amount * 0.06, 2)
            self.total_sgst = round(sales[0].total_amount * 0.06, 2)
            self.total_igst = 0

    def on_submit(self):
        self.generate_gstr3b_xml()
        self.filing_status = "Generated"
        self.save(ignore_permissions=True)

    def generate_gstr3b_xml(self):
        gst_number = frappe.db.get_single_value("Station Configuration", "gst_number") or ""
        period_parts = self.filing_period.split("-")
        month = period_parts[0] if len(period_parts) > 0 else "01"
        year = period_parts[1] if len(period_parts) > 1 else "2026"

        xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<GSTR3B>
  <GSTIN>{gst_number}</GSTIN>
  <FP>{month}{year}</FP>
  <DT>{self.filing_date.strftime('%d-%m-%Y') if self.filing_date else ''}</DT>
  <GT>
    <GTIN>
      <POSUP>
        <TAXVAL>{self.total_taxable_value or 0}</TAXVAL>
        <TXP>{self.total_taxable_value or 0}</TXP>
      </POSUP>
    </GTIN>
  </GT>
  <SUPDT>
    <IDTR>
      <TXP>{self.total_taxable_value or 0}</TXP>
      <IAMT>{self.total_igst or 0}</IAMT>
      <CAMT>{self.total_cgst or 0}</CAMT>
      <SAMT>{self.total_sgst or 0}</SAMT>
    </IDTR>
  </SUPDT>
  <ITC>
    <IDTR>
      <IAMT>{self.total_itc_igst or 0}</IAMT>
      <CAMT>{self.total_itc_cgst or 0}</CAMT>
      <SAMT>{self.total_itc_sgst or 0}</SAMT>
    </IDTR>
  </ITC>
  <TXP>
    <TXPD>
      <TXP>{self.net_tax_payable or 0}</TXP>
    </TXPD>
  </TXP>
</GSTR3B>"""
        self.xml_output = xml


@frappe.whitelist()
def generate_gstr3b_for_period(from_date, to_date):
    """Auto-generate GSTR-3B for a date range"""
    filing = frappe.get_doc({
        "doctype": "GSTR-3B Filing",
        "filing_period": frappe.utils.getdate(from_date).strftime("%m-%Y"),
        "filing_date": frappe.utils.today(),
        "filing_status": "Draft"
    })
    filing.insert(ignore_permissions=True)
    return filing.name
