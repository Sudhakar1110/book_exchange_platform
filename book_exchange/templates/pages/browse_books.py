import frappe


def get_context(context):
    # Get query parameters
    search = frappe.form_dict.get("search", "")
    category = frappe.form_dict.get("category", "")
    condition = frappe.form_dict.get("condition", "")
    page = frappe.form_dict.get("page", 1)
    
    if isinstance(page, str):
        page = int(page) if page.isdigit() else 1
    
    # Build filters
    filters = {"status": "Available"}
    
    if search:
        filters["book_title"] = ["like", f"%{search}%"]
    if category:
        filters["book_category"] = category
    if condition:
        filters["condition"] = condition
    
    # Pagination
    limit_start = (page - 1) * 12
    limit_page = 12
    
    # Get books
    context.books = frappe.get_all(
        "Book",
        filters=filters,
        fields=["name", "book_title", "author", "book_category", "condition", "isbn", "book_image", "description"],
        limit_start=limit_start,
        limit_page=limit_page
    )
    
    # Get total count for pagination
    total_books = frappe.db.count("Book", filters=filters)
    context.total_pages = (total_books + 11) // 12
    context.page = page
    context.search = search
    context.category = category
    context.condition = condition
    
    # Get categories for filter
    context.categories = frappe.get_all(
        "Book Category",
        fields=["name", "category_name"]
    )
