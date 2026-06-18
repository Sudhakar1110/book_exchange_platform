// Copyright (c) 2026, Your Company and contributors
// For license information, please see license.txt

frappe.require(["assets/book_exchange/css/book_exchange.css"]);

// Book Exchange Page Scripts
frappe.pages['book-exchange'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Book Exchange',
        single_column: true
    });
    
    page.set_primary_action(__('Add Book'), function() {
        frappe.new_doc('Book');
    }, 'octicon octicon-plus');
    
    // Load books
    page.add_inner_button(__('Browse Books'), function() {
        frappe.set_route('List', 'Book');
    });
    
    page.add_inner_button(__('My Books'), function() {
        frappe.set_route('List', 'Book', { owner_member: frappe.session.user });
    });
    
    // Render content
    $(wrapper).find('.layout-main').html(`
        <div class="book-exchange-section">
            <div class="book-exchange-header">
                <h1>Welcome to Book Exchange Platform</h1>
                <p>Exchange and donate books with other members</p>
            </div>
            <div class="row">
                <div class="col-md-4">
                    <div class="card text-center">
                        <div class="card-body">
                            <h3>Browse Books</h3>
                            <p>Discover books available for exchange</p>
                            <button class="btn btn-primary" onclick="frappe.set_route('List', 'Book')">
                                Browse Now
                            </button>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center">
                        <div class="card-body">
                            <h3>Exchange Books</h3>
                            <p>Request to exchange books with others</p>
                            <button class="btn btn-success" onclick="frappe.new_doc('Book Exchange Request')">
                                Start Exchange
                            </button>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card text-center">
                        <div class="card-body">
                            <h3>Donate Books</h3>
                            <p>Give your books to the community</p>
                            <button class="btn btn-info" onclick="frappe.new_doc('Book Donation')">
                                Donate Now
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `);
};

// Dashboard widget for available books count
frappe.dashboard_utils = frappe.dashboard_utils || {};

frappe.dashboard_utils.get_book_stats = function() {
    return frappe.call({
        method: 'book_exchange.utils.dashboard.get_book_stats',
        freeze: true
    });
};
