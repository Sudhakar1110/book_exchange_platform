// Copyright (c) 2026, Your Company and contributors
// For license information, please see license.txt


frappe.ui.form.on('Member Profile', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('View Books'), function() {
                frappe.set_route('List', 'Book', {owner_member: frm.doc.name});
            });
            
            frm.add_custom_button(__('View Exchanges'), function() {
                frappe.set_route('List', 'Book Exchange Request', {requester: frm.doc.name});
            });
        }
    },
    
    user: function(frm) {
        if (frm.doc.user) {
            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'User',
                    name: frm.doc.user
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value('full_name', r.message.full_name);
                        frm.set_value('email', r.message.email);
                    }
                }
            });
        }
    }
});
