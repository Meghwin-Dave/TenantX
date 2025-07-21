frappe.ui.form.on("Enterprise", {
    address: function(frm) {
        if (frm.doc.address) {
            frappe.call({
                method: "frappe.contacts.doctype.address.address.get_address_display",
                args: {
                    "address_dict": frm.doc.address
                },
                callback: function(r) {
                    if (r.message) {
                        // Replace <br> with newlines
                        frm.set_value("address_display", r.message.replace(/<br\s*\/?>/gi, ","));
                    }
                }
            });
        } else {
            frm.set_value("address_display", "");
        }
    },
    refresh: function(frm) {
        frm.set_query("parent_enterprise", function() {
            return {
                filters: {
                    company: frm.doc.company
                }
            };
        });
        if (frm.doc.address) {
            frappe.call({
                method: "frappe.contacts.doctype.address.address.get_address_display",
                args: {
                    "address_dict": frm.doc.address
                },
                callback: function(r) {
                    if (r.message) {
                        // Replace <br> with newlines
                        frm.set_value("address_display", r.message.replace(/<br\s*\/?>/gi, ","));
                    }
                }
            });
        }
        // Add button to create child enterprise
        if (!frm.is_new()) {
            frm.add_custom_button(__('Create Child Enterprise'), function() {
                frappe.new_doc('Enterprise', { parent_enterprise: frm.doc.name, company: frm.doc.company });
            }, __('Create'));
            frm.add_custom_button(__('Create Supplier'), function() {
                frappe.new_doc('Supplier', {
                    custom_enterprise: frm.doc.name,
                    company: frm.doc.company
                });
            }, __('Create'));
        }
    },
    
});
