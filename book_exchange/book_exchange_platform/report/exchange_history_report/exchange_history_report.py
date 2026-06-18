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
            "label": _("Request ID"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Book Exchange Request",
            "width": 150
        },
        {
            "label": _("Request Date"),
            "fieldname": "request_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Requester"),
            "fieldname": "requester",
            "fieldtype": "Link",
            "options": "Member Profile",
            "width": 120
        },
        {
            "label": _("Requester Name"),
            "fieldname": "requester_name",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Offered Book"),
            "fieldname": "offered_book_title",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": _("Requested Book"),
            "fieldname": "requested_book_title",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": _("Status"),
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Response Date"),
            "fieldname": "response_date",
            "fieldtype": "Date",
            "width": 100
        }
    ]


def get_data(filters):
    conditions = []
    
    if filters and filters.get("from_date"):
        conditions.append(f"ber.request_date >= '{filters.get('from_date')}'")
    
    if filters and filters.get("to_date"):
        conditions.append(f"ber.request_date <= '{filters.get('to_date')}'")
    
    if filters and filters.get("status"):
        conditions.append(f"ber.status = '{filters.get('status')}'")
    
    if filters and filters.get("requester"):
        conditions.append(f"ber.requester = '{filters.get('requester')}'")
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    query = f"""
        SELECT
            ber.name,
            ber.request_date,
            ber.requester,
            m.full_name as requester_name,
            b1.book_title as offered_book_title,
            b2.book_title as requested_book_title,
            ber.status,
            ber.response_date
        FROM
            `tabBook Exchange Request` ber
        LEFT JOIN
            `tabMember Profile` m ON ber.requester = m.name
        LEFT JOIN
            `tabBook` b1 ON ber.offered_book = b1.name
        LEFT JOIN
            `tabBook` b2 ON ber.requested_book = b2.name
        WHERE
            ber.docstatus = 1 AND {where_clause}
        ORDER BY
            ber.request_date DESC
    """
    
    return frappe.db.sql(query, as_dict=1)
