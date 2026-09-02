import frappe
from frappe.model.document import Document


class EmailLog(Document):
    def after_insert(self):
        send_email_notification(self)


@frappe.whitelist()
def send_email_notification(email_doc):
    """Send email using Frappe's built-in email system"""
    settings = frappe.get_single("PP Notification Settings")
    if not settings.enable_email:
        return

    try:
        frappe.sendmail(
            recipients=[email_doc.recipient_email],
            subject=email_doc.subject,
            message=email_doc.message_html,
            now=True
        )
        email_doc.status = "Sent"
        email_doc.sent_on = frappe.utils.now_datetime()
        email_doc.save(ignore_permissions=True)
    except Exception as e:
        email_doc.status = "Failed"
        email_doc.error_message = str(e)
        email_doc.save(ignore_permissions=True)
        frappe.log_error(f"Email Send Failed: {e}", "Email Gateway")


@frappe.whitelist()
def send_email(recipient_email, subject, email_type, message_html, reference_doctype=None, reference_name=None):
    """Create and send email notification"""
    email_doc = frappe.get_doc({
        "doctype": "Email Log",
        "recipient_email": recipient_email,
        "subject": subject,
        "email_type": email_type,
        "message_html": message_html,
        "reference_doctype": reference_doctype,
        "reference_name": reference_name,
    })
    email_doc.insert(ignore_permissions=True)
    return email_doc.name
