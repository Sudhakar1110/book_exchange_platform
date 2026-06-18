# Copyright (c) 2026, Your Company and contributors
# For license information, please see license.txt


import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    return [
        {
            "label": _("Donation ID"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Book Donation",
            "width": 150
        },
        {
            "label": _("Donation Date"),
            "fieldname": "donation_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Donor"),
            "fieldname": "donor",
            "fieldtype": "Link",
            "options": "Member Profile",
            "width": 120
        },
        {
            "label": _("Donor Name"),
            "fieldname": "donor_name",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Book Title"),
            "fieldname": "book_title",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": _("Author"),
            "fieldname": "author",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Category"),
            "fieldname": "category",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": _("Status"),
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Approval Date"),
            "fieldname": "approval_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Received Date"),
            "fieldname": "received_date",
            "fieldtype": "Date",
            "width": 100
        }
    ]


def get_data(filters):
    conditions = []
    
    if filters and filters.get("from_date"):
        conditions.append(f"bd.donation_date >= '{filters.get('from_date')}'")
    
    if filters and filters.get("to_date"):
        conditions.append(f"bd.donation_date <= '{filters.get('to_date')}'")
    
    if filters and filters.get("status"):
        conditions.append(f"bd.status = '{filters.get('status')}'")
    
    if filters and filters.get("donor"):
        conditions.append(f"bd.donor = '{filters.get('donor')}'")
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    query = f"""
        SELECT
            bd.name,
            bd.donation_date,
            bd.donor,
            m.full_name as donor_name,
            b.book_title,
            b.author,
            b.book_category as category,
            bd.status,
            bd.approval_date,
            bd.received_date
        FROM
            `tabBook Donation` bd
        LEFT JOIN
            `tabMember Profile` m ON bd.donor = m.name
        LEFT JOIN
            `tabBook` b ON bd.book = b.name
        WHERE
            bd.docstatus = 1 AND {where_clause}
        ORDER BY
            bd.donation_date DESC
    """
    
    return frappe.db.sql(query, as_dict=1)
