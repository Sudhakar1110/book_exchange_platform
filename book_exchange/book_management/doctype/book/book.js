// Copyright (c) 2026, Your Company and contributors
// For license information, please see license.txt


frappe.ui.form.on('Book', {
    refresh: function(frm) {
        // Add custom buttons
        if (frm.doc.status === 'Available' && !frm.is_new()) {
            frm.add_custom_button(__('Create Exchange Request'), function() {
                frappe.new_doc('Book Exchange Request', {
                    offered_book: frm.doc.name
                });
            });
            
            frm.add_custom_button(__('Donate'), function() {
                frappe.new_doc('Book Donation', {
                    book: frm.doc.name
                });
            });
        }
        
        // Set query for owner_member
        frm.set_query('owner_member', function() {
            return {
                filters: {
                    'enabled': 1
                }
            };
        });
    },
    
    onload: function(frm) {
        // Set default owner to current user's member profile
        if (frm.is_new() && !frm.doc.owner_member) {
            frappe.call({
                method: 'frappe.client.get_value',
                args: {
                    doctype: 'Member Profile',
                    filters: { user: frappe.session.user },
                    fieldname: 'name'
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value('owner_member', r.message.name);
                    }
                }
            });
        }
    }
});
