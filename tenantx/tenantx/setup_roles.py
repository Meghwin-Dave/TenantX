# Copyright (c) 2025, CognitionXLogic and contributors
# For license information, please see license.txt

"""
Setup script for TenantX Core Roles
This script implements Phase 1 of the permission system roadmap
"""

import frappe
from frappe import _


def setup_core_roles():
	"""
	Create the essential roles for TenantX structure
	This implements Phase 1: Foundation - Role & DocType Permissions
	"""
	print("Setting up TenantX Core Roles...")
	
	roles_to_create = [
		{
			"role_name": "Enterprise Admin",
			"desk_access": 1,
			"description": "High-level user who can manage Enterprises and SBUs"
		},
		{
			"role_name": "SBU Head", 
			"desk_access": 1,
			"description": "Manages a specific Strategic Business Unit and its underlying factories"
		},
		{
			"role_name": "Factory Head",
			"desk_access": 1, 
			"description": "Manages a specific Factory Business Unit"
		},
		{
			"role_name": "Factory User",
			"desk_access": 1,
			"description": "A standard user who performs transactions within a factory"
		},
		{
			"role_name": "Liaison Officer",
			"desk_access": 1,
			"description": "Manages a specific Liaison Office"
		}
	]
	
	for role_data in roles_to_create:
		create_role_if_not_exists(role_data)
	
	print("Core roles setup completed!")


def create_role_if_not_exists(role_data):
	"""Create a role if it doesn't already exist"""
	role_name = role_data["role_name"]
	
	if not frappe.db.exists("Role", role_name):
		role_doc = frappe.get_doc({
			"doctype": "Role",
			"role_name": role_name,
			"desk_access": role_data["desk_access"],
			"description": role_data["description"]
		})
		role_doc.insert(ignore_permissions=True)
		print(f"✓ Created role: {role_name}")
	else:
		print(f"✓ Role already exists: {role_name}")


def setup_role_permissions():
	"""
	Set up global DocType permissions for the core roles
	This implements the role-based permission structure
	"""
	print("\nSetting up role permissions...")
	
	# Define permissions for each role
	role_permissions = {
		"Enterprise Admin": {
			"Enterprise": ["read", "write", "create", "delete", "submit", "cancel", "amend"],
			"Strategic Business Unit": ["read", "write", "create", "delete", "submit", "cancel", "amend"],
			"Factory Business Unit": ["read", "write", "create", "delete", "submit", "cancel", "amend"],
			"Liaison Office": ["read", "write", "create", "delete", "submit", "cancel", "amend"],
			"User Access Scope Profile": ["read", "write", "create", "delete"],
			"User Access Scope": ["read", "write", "create", "delete"]
		},
		"SBU Head": {
			"Strategic Business Unit": ["read", "write", "create", "submit", "cancel", "amend"],
			"Factory Business Unit": ["read", "write", "create", "submit", "cancel", "amend"],
			"Purchase Order": ["read", "write", "create", "submit", "cancel"],
			"Sales Invoice": ["read", "write", "create", "submit", "cancel"],
			"Purchase Invoice": ["read", "write", "create", "submit", "cancel"],
			"Sales Order": ["read", "write", "create", "submit", "cancel"],
			"Delivery Note": ["read", "write", "create", "submit", "cancel"],
			"Purchase Receipt": ["read", "write", "create", "submit", "cancel"],
			"Journal Entry": ["read", "write", "create", "submit", "cancel"]
		},
		"Factory Head": {
			"Factory Business Unit": ["read", "write", "create", "submit", "cancel", "amend"],
			"Purchase Order": ["read", "write", "create", "submit", "cancel"],
			"Sales Invoice": ["read", "write", "create", "submit", "cancel"],
			"Purchase Invoice": ["read", "write", "create", "submit", "cancel"],
			"Sales Order": ["read", "write", "create", "submit", "cancel"],
			"Delivery Note": ["read", "write", "create", "submit", "cancel"],
			"Purchase Receipt": ["read", "write", "create", "submit", "cancel"],
			"Journal Entry": ["read", "write", "create", "submit", "cancel"]
		},
		"Factory User": {
			"Factory Business Unit": ["read"],
			"Purchase Order": ["read", "write", "create", "submit"],
			"Sales Invoice": ["read", "write", "create", "submit"],
			"Purchase Invoice": ["read", "write", "create", "submit"],
			"Sales Order": ["read", "write", "create", "submit"],
			"Delivery Note": ["read", "write", "create", "submit"],
			"Purchase Receipt": ["read", "write", "create", "submit"],
			"Journal Entry": ["read", "write", "create", "submit"]
		},
		"Liaison Officer": {
			"Liaison Office": ["read", "write", "create", "submit", "cancel", "amend"],
			"Purchase Order": ["read", "write", "create", "submit"],
			"Sales Invoice": ["read", "write", "create", "submit"],
			"Purchase Invoice": ["read", "write", "create", "submit"],
			"Sales Order": ["read", "write", "create", "submit"],
			"Delivery Note": ["read", "write", "create", "submit"],
			"Purchase Receipt": ["read", "write", "create", "submit"],
			"Journal Entry": ["read", "write", "create", "submit"]
		}
	}
	
	for role_name, doctype_permissions in role_permissions.items():
		if frappe.db.exists("Role", role_name):
			set_role_permissions(role_name, doctype_permissions)
		else:
			print(f"⚠ Role {role_name} does not exist. Please create it first.")


def set_role_permissions(role_name, doctype_permissions):
	"""Set permissions for a specific role"""
	print(f"Setting permissions for role: {role_name}")
	
	for doctype, permissions in doctype_permissions.items():
		# Check if role permission already exists
		existing = frappe.db.get_value("Custom DocPerm", {
			"role": role_name,
			"parent": doctype
		})
		
		if not existing:
			# Create new role permission
			perm_doc = frappe.get_doc({
				"doctype": "Custom DocPerm",
				"role": role_name,
				"parent": doctype,
				"parentfield": "permissions",
				"parenttype": "Customize Form",
				"read": "read" in permissions,
				"write": "write" in permissions,
				"create": "create" in permissions,
				"delete": "delete" in permissions,
				"submit": "submit" in permissions,
				"cancel": "cancel" in permissions,
				"amend": "amend" in permissions,
				"report": False,
				"export": False,
				"share": False,
				"print": False,
				"email": False
			})
			perm_doc.insert(ignore_permissions=True)
			print(f"  ✓ Set permissions for {doctype}")
		else:
			print(f"  ✓ Permissions already exist for {doctype}")


def setup_field_level_permissions():
	"""
	Set up field-level permissions for Phase 3
	This implements fine-grained control over field access
	"""
	print("\nSetting up field-level permissions...")
	
	# Define field-level permissions
	field_permissions = {
		"Factory Business Unit": {
			"capacity": {
				"permission_level": 1,
				"roles_with_access": ["Factory Head", "SBU Head", "Enterprise Admin"]
			},
			"capacity_uom": {
				"permission_level": 1,
				"roles_with_access": ["Factory Head", "SBU Head", "Enterprise Admin"]
			},
			"cost_center": {
				"permission_level": 1,
				"roles_with_access": ["Factory Head", "SBU Head", "Enterprise Admin"]
			},
			"factory_head": {
				"permission_level": 1,
				"roles_with_access": ["Factory Head", "SBU Head", "Enterprise Admin"]
			}
		},
		"Strategic Business Unit": {
			"sbu_head": {
				"permission_level": 1,
				"roles_with_access": ["SBU Head", "Enterprise Admin"]
			},
			"cost_center": {
				"permission_level": 1,
				"roles_with_access": ["SBU Head", "Enterprise Admin"]
			},
			"parent_sbu": {
				"permission_level": 1,
				"roles_with_access": ["SBU Head", "Enterprise Admin"]
			}
		}
	}
	
	for doctype, fields in field_permissions.items():
		for field_name, field_config in fields.items():
			set_field_permission_level(doctype, field_name, field_config["permission_level"])


def set_field_permission_level(doctype, field_name, permission_level):
	"""Set permission level for a specific field"""
	try:
		# Update the field's permission level in the DocType
		frappe.db.sql("""
			UPDATE `tabCustom Field` 
			SET permlevel = %s 
			WHERE dt = %s AND fieldname = %s
		""", (permission_level, doctype, field_name))
		
		print(f"  ✓ Set permission level {permission_level} for {doctype}.{field_name}")
		
	except Exception as e:
		print(f"  ✗ Error setting permission level for {doctype}.{field_name}: {str(e)}")


def create_test_users():
	"""
	Create test users for each role for testing purposes
	"""
	print("\nCreating test users...")
	
	test_users = [
		{
			"email": "enterprise.admin@test.com",
			"first_name": "Enterprise",
			"last_name": "Admin",
			"role": "Enterprise Admin"
		},
		{
			"email": "sbu.head@test.com", 
			"first_name": "SBU",
			"last_name": "Head",
			"role": "SBU Head"
		},
		{
			"email": "factory.head@test.com",
			"first_name": "Factory",
			"last_name": "Head", 
			"role": "Factory Head"
		},
		{
			"email": "factory.user@test.com",
			"first_name": "Factory",
			"last_name": "User",
			"role": "Factory User"
		},
		{
			"email": "liaison.officer@test.com",
			"first_name": "Liaison",
			"last_name": "Officer",
			"role": "Liaison Officer"
		}
	]
	
	for user_data in test_users:
		create_test_user(user_data)


def create_test_user(user_data):
	"""Create a test user with the specified role"""
	email = user_data["email"]
	
	if not frappe.db.exists("User", email):
		user_doc = frappe.get_doc({
			"doctype": "User",
			"email": email,
			"first_name": user_data["first_name"],
			"last_name": user_data["last_name"],
			"send_welcome_email": 0,
			"user_type": "System User"
		})
		user_doc.insert(ignore_permissions=True)
		
		# Add role to user
		user_doc.add_roles(user_data["role"])
		
		print(f"✓ Created test user: {email} with role: {user_data['role']}")
	else:
		print(f"✓ Test user already exists: {email}")


def run_full_setup():
	"""
	Run the complete setup for all phases
	"""
	print("Starting TenantX Permission System Setup...")
	print("=" * 50)
	
	# Phase 1: Foundation - Role & DocType Permissions
	print("\nPhase 1: Setting up Core Roles and Permissions")
	setup_core_roles()
	setup_role_permissions()
	
	# Phase 3: Fine-Grained Control
	print("\nPhase 3: Setting up Field-Level Permissions")
	setup_field_level_permissions()
	
	# Create test users
	print("\nCreating Test Users")
	create_test_users()
	
	print("\n" + "=" * 50)
	print("TenantX Permission System Setup Complete!")
	print("\nNext Steps:")
	print("1. Assign users to roles")
	print("2. Set up User Access Scope for each user")
	print("3. Test the permission system")
	print("4. Configure workflows if needed")


if __name__ == "__main__":
	run_full_setup() 