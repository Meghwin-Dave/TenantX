# Copyright (c) 2025, CognitionXLogic and contributors
# For license information, please see license.txt

"""
Patch configuration for TenantX
This file contains configuration options for the TenantX permission system patches
"""

import frappe
from frappe import _


def get_patch_config():
	"""
	Get patch configuration settings
	"""
	return {
		# Whether to create test users during patch execution
		"create_test_users": frappe.conf.get('tenantx_create_test_users', True),
		
		# Whether to show setup completion messages
		"show_setup_messages": frappe.conf.get('tenantx_show_setup_messages', True),
		
		# Whether to log detailed patch information
		"detailed_logging": frappe.conf.get('tenantx_detailed_logging', True),
		
		# Whether to fail migration if patch encounters errors
		"fail_on_error": frappe.conf.get('tenantx_fail_on_error', False),
		
		# Roles to create (can be customized)
		"roles_to_create": [
			"Enterprise Admin",
			"SBU Head", 
			"Factory Head",
			"Factory User",
			"Liaison Officer"
		],
		
		# Test users to create (if enabled)
		"test_users": [
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
	}


def set_patch_config(key, value):
	"""
	Set patch configuration
	"""
	frappe.conf[key] = value


def is_production():
	"""
	Check if this is a production environment
	"""
	return frappe.conf.get('maintenance_mode') or frappe.conf.get('production_mode', False)


def should_create_test_users():
	"""
	Determine if test users should be created
	"""
	config = get_patch_config()
	
	# Don't create test users in production unless explicitly enabled
	if is_production() and not frappe.conf.get('tenantx_create_test_users_production', False):
		return False
	
	return config.get('create_test_users', True) 