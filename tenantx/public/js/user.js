frappe.ui.form.on("User", {
	user_access_scope_profile: function(frm) {
		if (frm.doc.user_access_scope_profile) {
			frappe.call({
				method: "tenantx.api.get_user_access_scope_profile",
				args: {
					user_access_scope_profile: frm.doc.user_access_scope_profile,
				},
				callback: function(data) {
					if (data.message && Array.isArray(data.message)) {
						
						// Clear existing user access scope entries
						frm.set_value("user_access_scope", []);
						
						// Add new entries from the profile
						data.message.forEach(function(scope) {
							frm.add_child("user_access_scope", {
								scope_type: scope.scope_type,
								scope_name: scope.scope_name,
								read: scope.read,
								write: scope.write,
							});
						});
						
						// Refresh the child table to show the new data
						frm.refresh_field("user_access_scope");
					} else {
						frappe.msgprint({
							title: __('No Data'),
							message: __('No access scope data found for the selected profile.'),
							indicator: 'orange'
						});
					}
				},
				error: function(err) {
					console.error("Error fetching user access scope profile:", err);
					frappe.msgprint({
						title: __('Error'),
						message: __('Failed to load access scope profile. Please try again.'),
						indicator: 'red'
					});
				}
			});
		} else {
			// Clear the user access scope when no profile is selected
			frm.set_value("user_access_scope", []);
			frm.refresh_field("user_access_scope");
		}
	}
});