from . import __version__ as app_version


app_name = "book_exchange"
app_title = "Book Exchange Platform"
app_publisher = "Your Company"
app_description = "A simple book exchange and donation platform"
app_email = "info@yourcompany.com"
app_license = "MIT"


# Includes in <head>
# ------------------


app_include_css = "/assets/book_exchange/css/book_exchange.css"
app_include_js = "/assets/book_exchange/js/book_exchange.js"


# Installation
# ------------


after_install = "book_exchange.utils.demo_data.after_install"
after_migrate = "book_exchange.utils.demo_data.after_migrate"


# Fixtures
# --------


fixtures = [
    {
        "dt": "Workflow",
        "filters": [
            ["name", "in", ["Book Exchange Request Workflow", "Book Donation Workflow"]]
        ]
    },
    {
        "dt": "Workflow State",
        "filters": [
            ["workflow_name", "in", ["Book Exchange Request Workflow", "Book Donation Workflow"]]
        ]
    },
    {
        "dt": "Workflow Action Master",
        "filters": [
            ["workflow_name", "in", ["Book Exchange Request Workflow", "Book Donation Workflow"]]
        ]
    },
    {
        "dt": "Custom Field",
        "filters": [
            ["name", "in", []]
        ]
    }
]


# DocEvents
# ---------


doc_events = {
    "Book Exchange Request": {
        "on_submit": "book_exchange.exchange_management.doctype.book_exchange_request.book_exchange_request.on_submit",
        "on_update_after_submit": "book_exchange.exchange_management.doctype.book_exchange_request.book_exchange_request.on_status_change"
    },
    "Book Donation": {
        "on_submit": "book_exchange.donation_management.doctype.book_donation.book_donation.on_submit"
    }
}


# Scheduled Tasks
# ---------------


scheduler_events = {
    "daily": [
        "book_exchange.utils.notifications.send_pending_exchange_reminders"
    ]
}


# Permissions
# -----------


permission_query_conditions = {
    "Book": "book_exchange.book_management.doctype.book.book.get_permission_query_conditions",
}


has_permission = {
    "Book": "book_exchange.book_management.doctype.book.book.has_permission",
}


# Website
# -------


website_route_rules = [
    {"from_route": "/book-exchange/<path:app_path>", "to_route": "book-exchange"},
]


# Portal Settings
# ---------------


portal_menu_items = [
    {"title": "My Books", "route": "/my-books", "reference_doctype": "Book"},
    {"title": "My Exchange Requests", "route": "/my-exchange-requests", "reference_doctype": "Book Exchange Request"},
    {"title": "My Donations", "route": "/my-donations", "reference_doctype": "Book Donation"}
]


# Update Website Context
# ----------------------


update_website_context = [
    "book_exchange.templates.pages.home.get_context"
]
