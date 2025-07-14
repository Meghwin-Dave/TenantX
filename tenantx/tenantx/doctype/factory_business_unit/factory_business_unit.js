// Copyright (c) 2025, CognitionXLogic and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Factory Business Unit", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Factory Business Unit", {
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
    },
    setup: function(frm) {
        // Filter Factory Head to show only active employees of the selected company
        frm.set_query("factory_head", function() {
            return {
                filters: {
                    status: "Active",
                    company: frm.doc.company
                }
            };
        });

        // Filter Enterprise to show only those of the selected company
        frm.set_query("enterprise", function() {
            return {
                filters: {
                    company: frm.doc.company
                }
            };
        });

        // Filter SBU to show only those of the selected enterprise
        frm.set_query("sbu", function() {
            return {
                filters: {
                    enterprise: frm.doc.enterprise
                }
            };
        });

        // Filter Cost Center to show only those of the selected company
        frm.set_query("cost_center", function() {
            return {
                filters: {
                    company: frm.doc.company
                }
            };
        });

        frm.set_query("warehouse", function() {
            return {
                filters: {
                    company: frm.doc.company
                }
            };
        });
    }
});
