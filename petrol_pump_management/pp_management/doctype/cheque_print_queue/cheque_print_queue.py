import frappe
from frappe.model.document import Document


class ChequePrintQueue(Document):
    def validate(self):
        if self.amount and not self.amount_in_words:
            self.amount_in_words = self._number_to_words(self.amount)

    def _number_to_words(self, num):
        """Convert number to Indian currency words"""
        ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
                "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
                "Seventeen", "Eighteen", "Nineteen"]
        tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

        if num == 0:
            return "Zero Rupees Only"

        def _convert_chunk(n):
            if n == 0:
                return ""
            elif n < 20:
                return ones[n]
            elif n < 100:
                return tens[n // 10] + " " + ones[n % 10]
            else:
                return ones[n // 100] + " Hundred " + _convert_chunk(n % 100)

        num = int(num)
        result = ""
        if num >= 10000000:
            result += _convert_chunk(num // 10000000) + " Crore "
            num %= 10000000
        if num >= 100000:
            result += _convert_chunk(num // 100000) + " Lakh "
            num %= 100000
        if num >= 1000:
            result += _convert_chunk(num // 1000) + " Thousand "
            num %= 1000
        if num > 0:
            result += _convert_chunk(num)

        return result.strip() + " Rupees Only"

    def on_submit(self):
        self.status = "Printed"
        self.printed_on = frappe.utils.now_datetime()
        self.save(ignore_permissions=True)
