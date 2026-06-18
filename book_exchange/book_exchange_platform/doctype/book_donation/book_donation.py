# Copyright (c) 2026, Your Company and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import nowdate


class BookDonation(Document):
    def validate(self):
        self.validate_book()
        self.validate_donor()
        
    def validate_book(self):
        """Validate that book exists and belongs to donor"""
        book = frappe.get_doc("Book", self.book)
        if book.owner_member != self.donor:
            frappe.throw(_("You can only donate books you own"))
    
    def validate_donor(self):
        """Validate donor is a valid member"""
        if not frappe.db.exists("Member Profile", self.donor):
            frappe.throw(_("Invalid member profile"))
    
    def before_submit(self):
        """Update status"""
        self.status = "Submitted"
    
    def on_update_after_submit(self):
        """Handle status changes"""
        if self.status == "Approved":
            self.approved_by = frappe.session.user
            self.approval_date = nowdate()
        elif self.status == "Received":
            self.received_date = nowdate()
            # Update book status
            frappe.db.set_value("Book", self.book, "status", "Donated")


def on_submit(doc, method):
    """Send notification on submit"""
    # Send email to managers
    managers = frappe.get_all("Has Role", filters={"role": "Book Exchange Manager", "parenttype": "User"}, fields=["parent"])
    
    for manager in managers:
        frappe.sendmail(
            recipients=[manager.parent],
            subject=f"New Book Donation",
            message=f"""
                <p>Hello,</p>
                <p>A new book donation has been submitted.</p>
                <p><b>Donation:</b> {doc.name}</p>
                <p><b>Book:</b> {frappe.db.get_value('Book', doc.book, 'book_title')}</p>
                <p><b>Donor:</b> {frappe.db.get_value('Member Profile', doc.donor, 'full_name')}</p>
                <p>Please review and approve.</p>
            """
        )
