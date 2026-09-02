import frappe
from frappe.model.document import Document
import csv
import io


class BankStatementImport(Document):
    def validate(self):
        self.parse_statement()

    def parse_statement(self):
        """Parse uploaded CSV bank statement"""
        if not self.statement_file:
            return

        try:
            file_url = self.statement_file
            file_content = frappe.get_file(file_url)
            content = file_content.decode('utf-8') if isinstance(file_content, bytes) else file_content
            reader = csv.DictReader(io.StringIO(content))

            total_credit = 0
            total_debit = 0
            matched = 0
            unmatched = 0

            self.transactions = []
            for row in reader:
                date = row.get("Date") or row.get("date") or row.get("Txn Date") or ""
                description = row.get("Description") or row.get("Narration") or row.get("remarks") or ""
                debit = float(row.get("Debit") or row.get("Withdrawal") or row.get("debit") or 0)
                credit = float(row.get("Credit") or row.get("Deposit") or row.get("credit") or 0)
                ref = row.get("Ref No") or row.get("Cheque No") or row.get("UTR") or row.get("reference") or ""

                # Try to match with existing transactions
                match_ref = self._match_transaction(date, debit, credit, description)

                self.append("transactions", {
                    "transaction_date": date,
                    "description": description,
                    "debit": debit,
                    "credit": credit,
                    "reference_no": ref,
                    "match_status": "Matched" if match_ref else "Unmatched",
                    "matched_reference": match_ref or ""
                })

                total_credit += credit
                total_debit += debit
                if match_ref:
                    matched += 1
                else:
                    unmatched += 1

            self.total_credit = total_credit
            self.total_debit = total_debit
            self.matched_count = matched
            self.unmatched_count = unmatched
            self.status = "Parsed"
        except Exception as e:
            frappe.throw(f"Error parsing bank statement: {str(e)}")

    def _match_transaction(self, date, debit, credit, description):
        """Try to match bank transaction with internal records"""
        amount = credit if credit > 0 else debit
        if amount <= 0:
            return None

        # Try matching with Payment Receipts
        receipt = frappe.db.sql("""
            SELECT name FROM `tabPayment Receipt`
            WHERE ABS(amount - %s) < 1
            AND DATE(received_on) BETWEEN DATE_SUB(%s, INTERVAL 3 DAY) AND DATE_ADD(%s, INTERVAL 3 DAY)
            AND docstatus = 1 LIMIT 1
        """, (amount, date, date), as_dict=True)
        if receipt:
            return receipt[0].name

        # Try matching with Bank Deposits
        deposit = frappe.db.sql("""
            SELECT name FROM `tabBank Deposit`
            WHERE ABS(amount - %s) < 1
            AND DATE(deposit_date) BETWEEN DATE_SUB(%s, INTERVAL 3 DAY) AND DATE_ADD(%s, INTERVAL 3 DAY)
            AND docstatus = 1 LIMIT 1
        """, (amount, date, date), as_dict=True)
        if deposit:
            return deposit[0].name

        # Try matching with Expenses
        expense = frappe.db.sql("""
            SELECT name FROM `tabExpense Entry`
            WHERE ABS(amount - %s) < 1
            AND DATE(expense_date) BETWEEN DATE_SUB(%s, INTERVAL 3 DAY) AND DATE_ADD(%s, INTERVAL 3 DAY)
            AND docstatus = 1 LIMIT 1
        """, (amount, date, date), as_dict=True)
        if expense:
            return expense[0].name

        return None
