# Copyright (c) 2026, Your Company and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe import _
from frappe.utils import nowdate


class BookExchangeRequest(Document):
    def validate(self):
        self.validate_books()
        self.validate_requester()
        
    def validate_books(self):
        """Validate that books exist and are available"""
        # Check offered book
        offered_book = frappe.get_doc("Book", self.offered_book)
        if offered_book.status != "Available":
            frappe.throw(_("Offered book is not available"))
        
        if offered_book.owner_member != self.requester:
            frappe.throw(_("You can only offer books you own"))
        
        # Check requested book
        requested_book = frappe.get_doc("Book", self.requested_book)
        if requested_book.status != "Available":
            frappe.throw(_("Requested book is not available"))
        
        if requested_book.owner_member == self.requester:
            frappe.throw(_("You cannot request your own book"))
        
        # Check if same books
        if self.offered_book == self.requested_book:
            frappe.throw(_("Cannot exchange a book with itself"))
    
    def validate_requester(self):
        """Validate requester is a valid member"""
        if not frappe.db.exists("Member Profile", self.requester):
            frappe.throw(_("Invalid member profile"))
    
    def before_submit(self):
        """Mark books as reserved"""
        self.status = "Pending"
        
        # Reserve both books
        frappe.db.set_value("Book", self.offered_book, "status", "Reserved")
        frappe.db.set_value("Book", self.requested_book, "status", "Reserved")
    
    def on_cancel(self):
        """Release books"""
        # Make books available again
        frappe.db.set_value("Book", self.offered_book, "status", "Available")
        frappe.db.set_value("Book", self.requested_book, "status", "Available")


def on_submit(doc, method):
    """Send notification on submit"""
    # Get book owner
    requested_book_owner = frappe.db.get_value("Book", doc.requested_book, "owner_member")
    owner_user = frappe.db.get_value("Member Profile", requested_book_owner, "user")
    
    if owner_user:
        # Send notification
        frappe.sendmail(
            recipients=[owner_user],
            subject=f"New Exchange Request for Your Book",
            message=f"""
                <p>Hello,</p>
                <p>A member has requested to exchange books with you.</p>
                <p><b>Exchange Request:</b> {doc.name}</p>
                <p><b>Offered Book:</b> {frappe.db.get_value('Book', doc.offered_book, 'book_title')}</p>
                <p><b>Requested Book:</b> {frappe.db.get_value('Book', doc.requested_book, 'book_title')}</p>
                <p>Please review the request in the system.</p>
            """
        )


def on_status_change(doc, method):
    """Handle status changes"""
    if doc.status == "Approved":
        create_exchange_transaction(doc)
    elif doc.status == "Rejected":
        # Release books
        frappe.db.set_value("Book", doc.offered_book, "status", "Available")
        frappe.db.set_value("Book", doc.requested_book, "status", "Available")
        doc.response_date = nowdate()


def create_exchange_transaction(doc):
    """Create exchange transaction when approved"""
    transaction = frappe.get_doc({
        "doctype": "Exchange Transaction",
        "exchange_request": doc.name,
        "exchange_date": nowdate(),
        "status": "Completed"
    })
    transaction.insert()
    transaction.submit()
    
    # Update books
    offered_book = frappe.get_doc("Book", doc.offered_book)
    requested_book = frappe.get_doc("Book", doc.requested_book)
    
    # Swap owners
    offered_book.owner_member = requested_book.owner_member
    offered_book.status = "Exchanged"
    offered_book.save()
    
    requested_book.owner_member = doc.requester
    requested_book.status = "Exchanged"
    requested_book.save()
    
    # Update request
    doc.exchange_transaction = transaction.name
    doc.response_date = nowdate()
    doc.status = "Completed"
