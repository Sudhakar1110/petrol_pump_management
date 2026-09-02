import frappe
from frappe.model.document import Document
import json
from datetime import datetime


class GSTR1Filing(Document):
    def validate(self):
        self.calculate_totals()

    def calculate_totals(self):
        total_taxable = 0
        total_cgst = 0
        total_sgst = 0
        total_igst = 0
        if self.b2b_invoices:
            for inv in self.b2b_invoices:
                total_taxable += inv.taxable_value or 0
                total_cgst += inv.cgst or 0
                total_sgst += inv.sgst or 0
                total_igst += inv.igst or 0
        self.total_taxable_value = total_taxable
        self.total_cgst = total_cgst
        self.total_sgst = total_sgst
        self.total_igst = total_igst

    def on_submit(self):
        self.generate_gstr1_xml()
        self.filing_status = "Generated"
        self.save(ignore_permissions=True)

    def generate_gstr1_xml(self):
        """Generate GSTR-1 XML for GSTN upload"""
        gst_number = frappe.db.get_single_value("Station Configuration", "gst_number") or ""
        period_parts = self.filing_period.split("-")
        month = period_parts[0] if len(period_parts) > 0 else "01"
        year = period_parts[1] if len(period_parts) > 1 else "2026"

        xml_header = f"""<?xml version="1.0" encoding="UTF-8"?>
<olleyError>
  <Version>GS1.0.3</Version>
  <SourceDetails>
    <Source>Web</Source>
  </SourceDetails>
  <DocDetails>
    <DocTyp>GSTR1</DocTyp>
    <DocVer>1.03</DocVer>
  </DocDetails>
  <SupplierGstin>{gst_number}</SupplierGstin>
  <FilingPeriod>{month}{year}</FilingPeriod>
  <FilingDate>{self.filing_date.strftime('%d-%m-%Y') if self.filing_date else ''}</FilingDate>
</FilterWhere>
<IFiling>
  <GSTIN>{gst_number}</GSTIN>
  <FP>{month}{year}</FP>
  <B2B>"""

        invoice_rows = ""
        if self.b2b_invoices:
            for inv in self.b2b_invoices:
                invoice_rows += f"""
    <INV>
      <CTIN>{inv.buyer_gstin or ''}</CTIN>
      <INVNUM>{inv.invoice_number or ''}</INVNUM>
      <INVDT>{inv.invoice_date.strftime('%d-%m-%Y') if inv.invoice_date else ''}</INVDT>
      <VAL>{inv.taxable_value or 0}</VAL>
      <POS>{inv.place_of_supply or '01'}</POS>
      <TYP>{inv.invoice_type or 'Regular'}</TYP>
      <ITMS>
        <ITM>
          <NUM>1</NUM>
          <SLPRD>{inv.hsn_code or ''}</SLPRD>
          <TXVAL>{inv.taxable_value or 0}</TXVAL>
          <RT>{inv.tax_rate or 0}</RT>
          <IAMT>{inv.igst or 0}</IAMT>
          <CAMT>{inv.cgst or 0}</CAMT>
          <SAMT>{inv.sgst or 0}</SAMT>
          <CSAMT>{inv.cess or 0}</CSAMT>
        </ITM>
      </ITMS>
    </INV>"""

        xml_footer = """
  </B2B>
</IFiling>"""

        self.xml_output = xml_header + invoice_rows + xml_footer
        self.hsn_summary = json.dumps(self._get_hsn_summary(), indent=2)

    def _get_hsn_summary(self):
        """Generate HSN-wise summary"""
        hsn_data = {}
        if self.b2b_invoices:
            for inv in self.b2b_invoices:
                hsn = inv.hsn_code or "9999"
                if hsn not in hsn_data:
                    hsn_data[hsn] = {"hsn": hsn, "qty": 0, "value": 0, "cgst": 0, "sgst": 0, "igst": 0}
                hsn_data[hsn]["qty"] += inv.quantity or 0
                hsn_data[hsn]["value"] += inv.taxable_value or 0
                hsn_data[hsn]["cgst"] += inv.cgst or 0
                hsn_data[hsn]["sgst"] += inv.sgst or 0
                hsn_data[hsn]["igst"] += inv.igst or 0
        return list(hsn_data.values())


@frappe.whitelist()
def generate_gstr1_for_period(from_date, to_date):
    """Auto-generate GSTR-1 filing for a date range"""
    sales = frappe.db.sql("""
        SELECT name, customer, amount, sale_date, fuel_type, qty_litres
        FROM `tabFuel Sale`
        WHERE sale_date BETWEEN %s AND %s AND docstatus = 1
        ORDER BY sale_date
    """, (from_date, to_date), as_dict=True)

    filing = frappe.get_doc({
        "doctype": "GSTR-1 Filing",
        "filing_period": frappe.utils.getdate(from_date).strftime("%m-%Y"),
        "filing_date": frappe.utils.today(),
        "filing_status": "Draft"
    })

    for sale in sales:
        rate = (sale.amount / sale.qty_litres) if sale.qty_litres else 0
        cgst = round(sale.amount * 0.06, 2)
        sgst = round(sale.amount * 0.06, 2)
        filing.append("b2b_invoices", {
            "invoice_number": sale.name,
            "invoice_date": sale.sale_date,
            "buyer_name": sale.customer or "Cash Customer",
            "taxable_value": sale.amount,
            "tax_rate": round(rate, 2),
            "quantity": sale.qty_litres,
            "hsn_code": "2710" if sale.fuel_type == "Diesel" else "2710",
            "cgst": cgst,
            "sgst": sgst,
            "igst": 0,
            "cess": 0
        })

    filing.insert(ignore_permissions=True)
    return filing.name
