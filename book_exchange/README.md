# Book Exchange Platform

A lightweight Frappe v15 application for managing book exchanges and donations.

## Features

- **Book Management**: Catalog books with details like title, author, category, ISBN, and condition
- **User Management**: Member profiles with contact information
- **Exchange Management**: Request and approve book exchanges between members
- **Donation Management**: Accept and manage book donations
- **Reports**: Available books, exchange history, and donation tracking
- **Workflows**: Automated approval workflows for exchanges and donations
- **Notifications**: Email notifications for requests and approvals

## Installation

```bash
# Get the app
bench get-app book_exchange https://github.com/yourusername/book_exchange.git

# Install on site
bench --site your-site.local install-app book_exchange

# Run migrations
bench --site your-site.local migrate

# Restart
bench restart

# Clear cache
bench --site your-site.local clear-cache
```

## Demo Data

The app automatically creates demo data after installation:
- 20 books across 5 categories
- 10 member profiles
- 10 authors
- 10 sample exchange requests
- 5 sample donations

## Modules

1. **Book Management**: Books, categories, and authors
2. **User Management**: Member profiles
3. **Exchange Management**: Exchange requests and transactions
4. **Donation Management**: Book donations
5. **Reports**: Analytics and tracking

## Roles

- **System Manager**: Full access
- **Book Exchange Manager**: Manage all operations
- **Member**: Create books, request exchanges, donate books

## License

MIT
