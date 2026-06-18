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
            "label": _("Book ID"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Book",
            "width": 120
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
            "fieldtype": "Link",
            "options": "Author",
            "width": 150
        },
        {
            "label": _("Category"),
            "fieldname": "book_category",
            "fieldtype": "Link",
            "options": "Book Category",
            "width": 120
        },
        {
            "label": _("Condition"),
            "fieldname": "condition",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Status"),
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 100
        },
        {
            "label": _("Owner"),
            "fieldname": "owner_member",
            "fieldtype": "Link",
            "options": "Member Profile",
            "width": 120
        },
        {
            "label": _("Owner Name"),
            "fieldname": "owner_name",
            "fieldtype": "Data",
            "width": 150
        }
    ]


def get_data(filters):
    conditions = []
    
    if filters and filters.get("book_category"):
        conditions.append(f"b.book_category = '{filters.get('book_category')}'")
    
    if filters and filters.get("author"):
        conditions.append(f"b.author = '{filters.get('author')}'")
    
    if filters and filters.get("condition"):
        conditions.append(f"b.condition = '{filters.get('condition')}'")
    
    # Always filter for available books
    conditions.append("b.status = 'Available'")
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    query = f"""
        SELECT
            b.name,
            b.book_title,
            b.author,
            b.book_category,
            b.condition,
            b.status,
            b.owner_member,
            m.full_name as owner_name
        FROM
            `tabBook` b
        LEFT JOIN
            `tabMember Profile` m ON b.owner_member = m.name
        WHERE
            {where_clause}
        ORDER BY
            b.book_title
    """
    
    return frappe.db.sql(query, as_dict=1)
