import frappe

def execute(filters=None):
    columns = [
        {"fieldname": "member", "label": "Member", "fieldtype": "Link", "options": "Member Profile", "width": 200},
        {"fieldname": "full_name", "label": "Full Name", "fieldtype": "Data", "width": 150},
        {"fieldname": "join_date", "label": "Join Date", "fieldtype": "Date", "width": 120},
        {"fieldname": "total_books_donated", "label": "Total Books Donated", "fieldtype": "Int", "width": 150},
        {"fieldname": "total_exchanges", "label": "Total Exchanges", "fieldtype": "Int", "width": 150}
    ]
    
    data = []
    
    members = frappe.get_all("Member Profile", fields=["name", "full_name", "join_date"])
    for member in members:
        donations = frappe.db.count("Book Donation", {"donor": member.name})
        exchanges = frappe.db.count("Exchange Transaction", {"member": member.name})
        
        data.append({
            "member": member.name,
            "full_name": member.full_name,
            "join_date": member.join_date,
            "total_books_donated": donations,
            "total_exchanges": exchanges
        })
        
    return columns, data
