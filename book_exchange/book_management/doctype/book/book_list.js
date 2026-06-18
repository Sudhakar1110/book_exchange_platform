frappe.listview_settings['Book'] = {
    add_fields: ['status', 'condition', 'book_category'],
    get_indicator: function(doc) {
        if (doc.status === 'Available') {
            return [__('Available'), 'green', 'status,=,Available'];
        } else if (doc.status === 'Reserved') {
            return [__('Reserved'), 'orange', 'status,=,Reserved'];
        } else if (doc.status === 'Exchanged') {
            return [__('Exchanged'), 'blue', 'status,=,Exchanged'];
        } else if (doc.status === 'Donated') {
            return [__('Donated'), 'gray', 'status,=,Donated'];
        }
    }
};
