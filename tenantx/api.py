import frappe

@frappe.whitelist()
def get_user_access_scope_profile(user_access_scope_profile):
	return frappe.get_doc("User Access Scope Profile", user_access_scope_profile).access_details