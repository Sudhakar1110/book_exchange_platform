// Copyright (c) 2026, Your Company and contributors
// For license information, please see license.txt


frappe.ui.form.on('Book Exchange Request', {
    refresh: function(frm) {
        // Add approve/reject buttons
        if (frm.doc.docstatus === 1 && frm.doc.status === 'Pending') {
            // Check if current user is the owner of requested book
            frappe.call({
                method: 'frappe.client.get_value',
                args: {
                    doctype: 'Book',
                    filters: { name: frm.doc.requested_book },
                    fieldname: 'owner_member'
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.call({
                            method: 'frappe.client.get_value',
                            args: {
                                doctype: 'Member Profile',
                                filters: { user: frappe.session.user },
                                fieldname: 'name'
                            },
                            callback: function(r2) {
                                if (r2.message && r2.message.name === r.message.owner_member) {
                                    frm.add_custom_button(__('Approve'), function() {
                                        frm.set_value('status', 'Approved');
                                        frm.save();
                                    }).addClass('btn-primary');
                                    
                                    frm.add_custom_button(__('Reject'), function() {
                                        frm.set_value('status', 'Rejected');
                                        frm.save();
                                    }).addClass('btn-danger');
                                }
                            }
                        });
                    }
                }
            });
        }
        
        // Set query filters
        frm.set_query('offered_book', function() {
            return {
                filters: {
                    'owner_member': frm.doc.requester,
                    'status': 'Available'
                }
            };
        });
        
        frm.set_query('requested_book', function() {
            return {
                filters: {
                    'owner_member': ['!=', frm.doc.requester],
                    'status': 'Available'
                }
            };
        });
    },
    
    onload: function(frm) {
        // Set default requester
        if (frm.is_new() && !frm.doc.requester) {
            frappe.call({
                method: 'frappe.client.get_value',
                args: {
                    doctype: 'Member Profile',
                    filters: { user: frappe.session.user },
                    fieldname: 'name'
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value('requester', r.message.name);
                    }
                }
            });
        }
    }
});
