# Copyright (c) 2026, Your Company and contributors
# For license information, please see license.txt


import frappe
from frappe.utils import nowdate, add_days


def send_pending_exchange_reminders():
    """Send reminders for pending exchange requests older than 7 days"""
    pending_requests = frappe.get_all(
        "Book Exchange Request",
        filters={
            "docstatus": 1,
            "status": "Pending",
            "request_date": ["<", add_days(nowdate(), -7)]
        },
        fields=["name", "requester", "requested_book"]
    )
    
    for request in pending_requests:
        # Get book owner
        requested_book_owner = frappe.db.get_value("Book", request.requested_book, "owner_member")
        owner_user = frappe.db.get_value("Member Profile", requested_book_owner, "user")
        
        if owner_user:
            frappe.sendmail(
                recipients=[owner_user],
                subject="Reminder: Pending Exchange Request",
                message=f"""
                    <p>Hello,</p>
                    <p>You have a pending exchange request that has been waiting for more than 7 days.</p>
                    <p><b>Exchange Request:</b> {request.name}</p>
                    <p>Please review and respond to the request.</p>
                """
            )
