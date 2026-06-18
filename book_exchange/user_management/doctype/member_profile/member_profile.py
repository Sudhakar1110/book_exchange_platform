# Copyright (c) 2026, Your Company and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe import _


class MemberProfile(Document):
    def validate(self):
        self.validate_user()
        self.sync_user_details()
        
    def validate_user(self):
        """Validate that user exists and is active"""
        if not frappe.db.exists("User", self.user):
            frappe.throw(_("Invalid user"))
            
        user_enabled = frappe.db.get_value("User", self.user, "enabled")
        if not user_enabled:
            frappe.throw(_("User is disabled"))
    
    def sync_user_details(self):
        """Sync details from User doctype"""
        if self.user:
            user_doc = frappe.get_doc("User", self.user)
            self.full_name = user_doc.full_name
            self.email = user_doc.email
    
    def after_insert(self):
        """Assign Member role to user"""
        user = frappe.get_doc("User", self.user)
        if "Member" not in frappe.get_roles(self.user):
            user.add_roles("Member")
