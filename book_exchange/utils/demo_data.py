# Copyright (c) 2026, Your Company and contributors
# For license information, please see license.txt


import frappe
from frappe import _
import random
from datetime import datetime, timedelta


def after_install():
    """Create demo data after installation"""
    create_roles()
    create_categories_and_authors()
    create_members()
    create_books()
    create_exchange_requests()
    create_donations()
    frappe.db.commit()


def after_migrate():
    """Run after migrations"""
    pass


def create_roles():
    """Create custom roles"""
    roles = ["Book Exchange Manager", "Member"]
    
    for role in roles:
        if not frappe.db.exists("Role", role):
            frappe.get_doc({
                "doctype": "Role",
                "role_name": role,
                "desk_access": 1
            }).insert(ignore_permissions=True)


def create_categories_and_authors():
    """Create sample categories and authors"""
    categories = [
        "Fiction",
        "Non-Fiction",
        "Science Fiction",
        "Mystery",
        "Romance"
    ]
    
    for category in categories:
        if not frappe.db.exists("Book Category", category):
            frappe.get_doc({
                "doctype": "Book Category",
                "category_name": category
            }).insert(ignore_permissions=True)
    
    authors = [
        "J.K. Rowling",
        "Stephen King",
        "Agatha Christie",
        "Dan Brown",
        "George R.R. Martin",
        "Jane Austen",
        "Ernest Hemingway",
        "Mark Twain",
        "Charles Dickens",
        "Leo Tolstoy"
    ]
    
    for author in authors:
        if not frappe.db.exists("Author", author):
            frappe.get_doc({
                "doctype": "Author",
                "author_name": author
            }).insert(ignore_permissions=True)


def create_members():
    """Create sample members"""
    members_data = [
        {"name": "John Doe", "email": "john@example.com", "phone": "1234567890"},
        {"name": "Jane Smith", "email": "jane@example.com", "phone": "0987654321"},
        {"name": "Bob Johnson", "email": "bob@example.com", "phone": "1122334455"},
        {"name": "Alice Brown", "email": "alice@example.com", "phone": "5544332211"},
        {"name": "Charlie Davis", "email": "charlie@example.com", "phone": "9988776655"},
        {"name": "Diana Wilson", "email": "diana@example.com", "phone": "6677889900"},
        {"name": "Eve Taylor", "email": "eve@example.com", "phone": "3344556677"},
        {"name": "Frank Moore", "email": "frank@example.com", "phone": "7788990011"},
        {"name": "Grace Lee", "email": "grace@example.com", "phone": "2233445566"},
        {"name": "Henry White", "email": "henry@example.com", "phone": "4455667788"}
    ]
    
    for member_data in members_data:
        # Create user if not exists
        if not frappe.db.exists("User", member_data["email"]):
            user = frappe.get_doc({
                "doctype": "User",
                "email": member_data["email"],
                "first_name": member_data["name"].split()[0],
                "last_name": " ".join(member_data["name"].split()[1:]) if len(member_data["name"].split()) > 1 else "",
                "enabled": 1,
                "send_welcome_email": 0
            })
            user.insert(ignore_permissions=True)
        
        # Create member profile if not exists
        if not frappe.db.exists("Member Profile", {"user": member_data["email"]}):
            frappe.get_doc({
                "doctype": "Member Profile",
                "user": member_data["email"],
                "full_name": member_data["name"],
                "email": member_data["email"],
                "phone": member_data["phone"],
                "enabled": 1
            }).insert(ignore_permissions=True)


def create_books():
    """Create sample books"""
    books_data = [
        {"title": "Harry Potter and the Philosopher's Stone", "author": "J.K. Rowling", "category": "Fiction", "isbn": "9780747532699"},
        {"title": "The Shining", "author": "Stephen King", "category": "Fiction", "isbn": "9780307743657"},
        {"title": "Murder on the Orient Express", "author": "Agatha Christie", "category": "Mystery", "isbn": "9780062693662"},
        {"title": "The Da Vinci Code", "author": "Dan Brown", "category": "Mystery", "isbn": "9780307474278"},
        {"title": "A Game of Thrones", "author": "George R.R. Martin", "category": "Science Fiction", "isbn": "9780553593716"},
        {"title": "Pride and Prejudice", "author": "Jane Austen", "category": "Romance", "isbn": "9780141439518"},
        {"title": "The Old Man and the Sea", "author": "Ernest Hemingway", "category": "Fiction", "isbn": "9780684801223"},
        {"title": "The Adventures of Tom Sawyer", "author": "Mark Twain", "category": "Fiction", "isbn": "9780143107330"},
        {"title": "Great Expectations", "author": "Charles Dickens", "category": "Fiction", "isbn": "9780141439563"},
        {"title": "War and Peace", "author": "Leo Tolstoy", "category": "Fiction", "isbn": "9780307266934"},
        {"title": "Harry Potter and the Chamber of Secrets", "author": "J.K. Rowling", "category": "Fiction", "isbn": "9780439064873"},
        {"title": "IT", "author": "Stephen King", "category": "Fiction", "isbn": "9781501142970"},
        {"title": "And Then There Were None", "author": "Agatha Christie", "category": "Mystery", "isbn": "9780062073488"},
        {"title": "Angels & Demons", "author": "Dan Brown", "category": "Mystery", "isbn": "9781416524793"},
        {"title": "A Clash of Kings", "author": "George R.R. Martin", "category": "Science Fiction", "isbn": "9780553381696"},
        {"title": "Sense and Sensibility", "author": "Jane Austen", "category": "Romance", "isbn": "9780141439662"},
        {"title": "A Farewell to Arms", "author": "Ernest Hemingway", "category": "Fiction", "isbn": "9780684801469"},
        {"title": "Adventures of Huckleberry Finn", "author": "Mark Twain", "category": "Fiction", "isbn": "9780143107323"},
        {"title": "Oliver Twist", "author": "Charles Dickens", "category": "Fiction", "isbn": "9780141439747"},
        {"title": "Anna Karenina", "author": "Leo Tolstoy", "category": "Fiction", "isbn": "9780143035008"}
    ]
    
    members = frappe.get_all("Member Profile", pluck="name")
    conditions = ["New", "Like New", "Good", "Fair"]
    
    for book_data in books_data:
        if not frappe.db.exists("Book", {"isbn": book_data["isbn"]}):
            frappe.get_doc({
                "doctype": "Book",
                "book_title": book_data["title"],
                "author": book_data["author"],
                "book_category": book_data["category"],
                "isbn": book_data["isbn"],
                "condition": random.choice(conditions),
                "status": "Available",
                "owner_member": random.choice(members),
                "description": f"A wonderful book about {book_data['title']}"
            }).insert(ignore_permissions=True)


def create_exchange_requests():
    """Create sample exchange requests"""
    books = frappe.get_all("Book", filters={"status": "Available"}, pluck="name")
    
    if len(books) < 10:
        return
    
    for i in range(10):
        offered_book = random.choice(books)
        requested_book = random.choice(books)
        
        # Make sure we're not exchanging the same book
        while offered_book == requested_book:
            requested_book = random.choice(books)
        
        # Get owners
        offered_owner = frappe.db.get_value("Book", offered_book, "owner_member")
        requested_owner = frappe.db.get_value("Book", requested_book, "owner_member")
        
        # Make sure owners are different
        if offered_owner != requested_owner:
            doc = frappe.get_doc({
                "doctype": "Book Exchange Request",
                "requester": offered_owner,
                "offered_book": offered_book,
                "requested_book": requested_book,
                "request_date": (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),
                "status": "Draft",
                "notes": f"I would like to exchange books"
            })
            doc.insert(ignore_permissions=True)
            
            # Submit some requests
            if random.random() > 0.5:
                doc.submit()


def create_donations():
    """Create sample donations"""
    books = frappe.get_all("Book", filters={"status": "Available"}, limit=5, pluck="name")
    
    for book in books:
        owner = frappe.db.get_value("Book", book, "owner_member")
        
        doc = frappe.get_doc({
            "doctype": "Book Donation",
            "donor": owner,
            "book": book,
            "donation_date": (datetime.now() - timedelta(days=random.randint(1, 20))).strftime("%Y-%m-%d"),
            "status": "Draft",
            "notes": "I would like to donate this book to the platform"
        })
        doc.insert(ignore_permissions=True)
        
        # Submit some donations
        if random.random() > 0.3:
            doc.submit()
