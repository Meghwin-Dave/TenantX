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
    }
});
