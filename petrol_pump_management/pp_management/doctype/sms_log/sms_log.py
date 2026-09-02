import frappe
from frappe.model.document import Document
import json
import urllib.request
import urllib.parse


class SMSLog(Document):
    def validate(self):
        if self.recipient and not self.recipient.startswith("+") and len(self.recipient) < 10:
            frappe.msgprint("Please enter a valid mobile number with country code")

    def after_insert(self):
        """Auto-send SMS after insert"""
        send_sms(self)


@frappe.whitelist()
def send_sms(sms_log_doc):
    """Send SMS via configured gateway"""
    settings = frappe.get_single("Notification Settings")
    if not settings.enable_sms:
        sms_log_doc.status = "Pending"
        sms_log_doc.save(ignore_permissions=True)
        return

    try:
        if settings.sms_gateway == "Twilio":
            result = _send_via_twilio(settings, sms_log_doc.recipient, sms_log_doc.message)
        elif settings.sms_gateway == "MSG91":
            result = _send_via_msg91(settings, sms_log_doc.recipient, sms_log_doc.message)
        else:
            # Generic HTTP API
            result = _send_via_http_api(settings, sms_log_doc.recipient, sms_log_doc.message)

        sms_log_doc.status = "Sent"
        sms_log_doc.sent_on = frappe.utils.now_datetime()
        sms_log_doc.gateway_response = str(result)
        sms_log_doc.save(ignore_permissions=True)
    except Exception as e:
        sms_log_doc.status = "Failed"
        sms_log_doc.error_message = str(e)
        sms_log_doc.save(ignore_permissions=True)
        frappe.log_error(f"SMS Send Failed: {e}", "SMS Gateway")


def _send_via_twilio(settings, to_number, message):
    """Send via Twilio API"""
    url = f"https://api.twilio.com/2010-04-01/Accounts/{settings.twilio_account_sid}/Messages.json"
    data = urllib.parse.urlencode({
        "To": to_number,
        "From": settings.twilio_from_number,
        "Body": message
    }).encode()
    auth = f"{settings.twilio_account_sid}:{settings.twilio_auth_token}"
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"Basic {frappe.safe_encode(auth)}")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())


def _send_via_msg91(settings, to_number, message):
    """Send via MSG91 API"""
    url = "https://api.msg91.com/api/v5/flow"
    payload = json.dumps({
        "integrated_number": settings.msg91_number,
        "content_type": "text",
        "payload": {"country": settings.msg91_country or "91", "to": [to_number], "message": message}
    }).encode()
    req = urllib.request.Request(url, data=payload, method="POST")
    req.add_header("authkey", settings.msg91_authkey)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())


def _send_via_http_api(settings, to_number, message):
    """Send via generic HTTP API"""
    url = settings.custom_sms_api_url
    if not url:
        frappe.throw("SMS API URL not configured in Notification Settings")
    payload = settings.custom_sms_payload_format.format(
        to=to_number, message=message, api_key=settings.custom_sms_api_key
    )
    req = urllib.request.Request(url, data=payload.encode(), method="POST")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())


@frappe.whitelist()
def send_notification(recipient, message_type, message, reference_doctype=None, reference_name=None):
    """Create and send SMS notification"""
    sms = frappe.get_doc({
        "doctype": "SMS Log",
        "recipient": recipient,
        "message_type": message_type,
        "message": message,
        "reference_doctype": reference_doctype,
        "reference_name": reference_name,
    })
    sms.insert(ignore_permissions=True)
    return sms.name
