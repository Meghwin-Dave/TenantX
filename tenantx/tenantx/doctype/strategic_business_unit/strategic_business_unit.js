// Copyright (c) 2025, CognitionXLogic and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Strategic Business Unit", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on("Strategic Business Unit", {
    setup: function(frm) {
        // Filter SBU Head to show only active employees of the selected company
        frm.set_query("sbu_head", function() {
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

        // Filter Factory to show only those of the selected company
        frm.set_query("factory", function() {
            return {
                filters: {
                    company: frm.doc.company,
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
    },
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('Create Child SBU'), function() {
                frappe.new_doc('Strategic Business Unit', {
                    parent_sbu: frm.doc.name,
                    company: frm.doc.company,
                    enterprise: frm.doc.enterprise
                });
            }, __('Create'));
            frm.add_custom_button(__('Create Supplier'), function() {
                frappe.new_doc('Supplier', {
                    custom_strategic_business_unit: frm.doc.name,
                    company: frm.doc.company,
                    custom_enterprise: frm.doc.enterprise
                });
            }, __('Create'));
        }
    }
});
