# Copyright (c) 2026, Your Company and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe import _


class Book(Document):
    def validate(self):
        self.validate_owner()
        
    def validate_owner(self):
        """Validate that the owner is a valid member"""
        if not frappe.db.exists("Member Profile", self.owner_member):
            frappe.throw(_("Invalid member profile"))
    
    def before_save(self):
        """Set default status if not set"""
        if not self.status:
            self.status = "Available"
    
    def on_trash(self):
        """Check if book is involved in any active exchanges"""
        active_exchanges = frappe.get_all(
            "Book Exchange Request",
            filters={
                "offered_book": self.name,
                "status": ["in", ["Pending", "Approved"]]
            }
        )
        
        if active_exchanges:
            frappe.throw(_("Cannot delete book involved in active exchange requests"))


def get_permission_query_conditions(user):
    """Permission query for Book list"""
    if not user:
        user = frappe.session.user
    
    if "System Manager" in frappe.get_roles(user):
        return None
    
    if "Book Exchange Manager" in frappe.get_roles(user):
        return None
    
    # Members can only see their own books and available books
    member = frappe.get_value("Member Profile", {"user": user}, "name")
    if member:
        return f"""(`tabBook`.`owner_member` = '{member}' OR `tabBook`.`status` = 'Available')"""
    
    return "1=0"


def has_permission(doc, ptype, user):
    """Permission check for individual Book documents"""
    if not user:
        user = frappe.session.user
    
    if "System Manager" in frappe.get_roles(user):
        return True
    
    if "Book Exchange Manager" in frappe.get_roles(user):
        return True
    
    member = frappe.get_value("Member Profile", {"user": user}, "name")
    
    if ptype == "read":
        return doc.status == "Available" or doc.owner_member == member
    
    if ptype in ["write", "delete"]:
        return doc.owner_member == member
    
    return False
