// Copyright (c) 2026, Your Company and contributors
// For license information, please see license.txt


frappe.ui.form.on('Book Donation', {
    refresh: function(frm) {
        // Add approve button for managers
        if (frm.doc.docstatus === 1 && frm.doc.status === 'Submitted') {
            if (frappe.user.has_role('Book Exchange Manager')) {
                frm.add_custom_button(__('Approve'), function() {
                    frm.set_value('status', 'Approved');
                    frm.save();
                }).addClass('btn-primary');
            }
        }
        
        // Add received button
        if (frm.doc.docstatus === 1 && frm.doc.status === 'Approved') {
            if (frappe.user.has_role('Book Exchange Manager')) {
                frm.add_custom_button(__('Mark as Received'), function() {
                    frm.set_value('status', 'Received');
                    frm.save();
                }).addClass('btn-success');
            }
        }
        
        // Set query for book
        frm.set_query('book', function() {
            return {
                filters: {
                    'owner_member': frm.doc.donor,
                    'status': ['in', ['Available', 'Reserved']]
                }
            };
        });
    },
    
    onload: function(frm) {
        // Set default donor
        if (frm.is_new() && !frm.doc.donor) {
            frappe.call({
                method: 'frappe.client.get_value',
                args: {
                    doctype: 'Member Profile',
                    filters: { user: frappe.session.user },
                    fieldname: 'name'
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value('donor', r.message.name);
                    }
                }
            });
        }
    }
});
