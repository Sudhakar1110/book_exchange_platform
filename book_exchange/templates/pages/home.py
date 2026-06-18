import frappe


def get_context(context):
    # Get featured available books
    context.books = frappe.get_all(
        "Book",
        filters={"status": "Available"},
        fields=["name", "book_title", "author", "book_category", "condition", "status", "book_image"],
        limit=8
    )
    
    context.categories = frappe.get_all(
        "Book Category",
        fields=["name", "category_name"],
        limit=10
    )
    
    # Get stats
    context.total_books = frappe.db.count("Book", {"status": "Available"})
    context.total_members = frappe.db.count("Member Profile", {"enabled": 1})
    context.total_exchanges = frappe.db.count("Exchange Transaction", {"status": "Completed"})
    context.total_donations = frappe.db.count("Book Donation", {"status": "Received"})
