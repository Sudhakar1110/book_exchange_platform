import frappe


def get_context(context):
    # Get recent exchanges
    context.recent_exchanges = frappe.db.sql("""
        SELECT 
            ber.name,
            ber.request_date,
            b1.book_title as offered_book_title,
            b2.book_title as requested_book_title,
            ber.status
        FROM `tabBook Exchange Request` ber
        LEFT JOIN `tabBook` b1 ON ber.offered_book = b1.name
        LEFT JOIN `tabBook` b2 ON ber.requested_book = b2.name
        WHERE ber.docstatus = 1
        ORDER BY ber.modified DESC
        LIMIT 10
    """, as_dict=1)
