import frappe


def get_context(context):
    # Get recent donations
    context.recent_donations = frappe.db.sql("""
        SELECT 
            bd.name,
            bd.donation_date,
            b.book_title,
            m.full_name as donor_name,
            bd.status
        FROM `tabBook Donation` bd
        LEFT JOIN `tabBook` b ON bd.book = b.name
        LEFT JOIN `tabMember Profile` m ON bd.donor = m.name
        WHERE bd.docstatus = 1
        ORDER BY bd.modified DESC
        LIMIT 10
    """, as_dict=1)
