# Copyright (c) 2026, Your Company and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document


class ExchangeTransaction(Document):
    def validate(self):
        self.validate_exchange_request()
        
    def validate_exchange_request(self):
        """Validate that exchange request exists and is approved"""
        if not frappe.db.exists("Book Exchange Request", self.exchange_request):
            frappe.throw("Invalid exchange request")
