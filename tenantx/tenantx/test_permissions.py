# Copyright (c) 2025, CognitionXLogic and contributors
# For license information, please see license.txt

"""
Test script for TenantX Permission System
This script helps verify that the permission system is working correctly
"""

import frappe
from frappe import _


def test_permission_system():
	"""
	Test the permission system to ensure it's working correctly
	"""
	print("Testing TenantX Permission System...")
	
	# Test 1: Check if permission query functions exist
	test_permission_functions_exist()
	
	# Test 2: Test Factory Business Unit permissions
	test_factory_business_unit_permissions()
	
	# Test 3: Test Strategic Business Unit permissions
	test_strategic_business_unit_permissions()
	
	# Test 4: Test transactional document permissions
	test_transactional_document_permissions()
	
	print("Permission system tests completed!")


def test_permission_functions_exist():
	"""Test if all permission query functions exist and are callable"""
	print("\n1. Testing permission functions exist...")
	
	functions_to_test = [
		"tenantx.tenantx.doctype.factory_business_unit.factory_business_unit.get_permission_query_conditions",
		"tenantx.tenantx.doctype.strategic_business_unit.strategic_business_unit.get_permission_query_conditions",
		"tenantx.tenantx.permission_queries.get_permission_query_conditions_for_purchase_order",
		"tenantx.tenantx.permission_queries.get_permission_query_conditions_for_sales_invoice",
		"tenantx.tenantx.permission_queries.get_permission_query_conditions_for_purchase_invoice",
		"tenantx.tenantx.permission_queries.get_permission_query_conditions_for_sales_order",
		"tenantx.tenantx.permission_queries.get_permission_query_conditions_for_delivery_note",
		"tenantx.tenantx.permission_queries.get_permission_query_conditions_for_purchase_receipt",
		"tenantx.tenantx.permission_queries.get_permission_query_conditions_for_journal_entry",
	]
	
	for func_path in functions_to_test:
		try:
			func = frappe.get_attr(func_path)
			result = func("test@example.com")
			print(f"✓ {func_path} - OK")
		except Exception as e:
			print(f"✗ {func_path} - ERROR: {str(e)}")


def test_factory_business_unit_permissions():
	"""Test Factory Business Unit permission queries"""
	print("\n2. Testing Factory Business Unit permissions...")
	
	try:
		from tenantx.tenantx.doctype.factory_business_unit.factory_business_unit import get_permission_query_conditions
		
		# Test with System Manager
		system_manager_condition = get_permission_query_conditions("Administrator")
		print(f"System Manager condition: {system_manager_condition}")
		
		# Test with regular user (no permissions)
		regular_user_condition = get_permission_query_conditions("test@example.com")
		print(f"Regular user condition: {regular_user_condition}")
		
		print("✓ Factory Business Unit permissions - OK")
		
	except Exception as e:
		print(f"✗ Factory Business Unit permissions - ERROR: {str(e)}")


def test_strategic_business_unit_permissions():
	"""Test Strategic Business Unit permission queries"""
	print("\n3. Testing Strategic Business Unit permissions...")
	
	try:
		from tenantx.tenantx.doctype.strategic_business_unit.strategic_business_unit import get_permission_query_conditions
		
		# Test with System Manager
		system_manager_condition = get_permission_query_conditions("Administrator")
		print(f"System Manager condition: {system_manager_condition}")
		
		# Test with regular user (no permissions)
		regular_user_condition = get_permission_query_conditions("test@example.com")
		print(f"Regular user condition: {regular_user_condition}")
		
		print("✓ Strategic Business Unit permissions - OK")
		
	except Exception as e:
		print(f"✗ Strategic Business Unit permissions - ERROR: {str(e)}")


def test_transactional_document_permissions():
	"""Test transactional document permission queries"""
	print("\n4. Testing transactional document permissions...")
	
	try:
		from tenantx.tenantx.permission_queries import (
			get_permission_query_conditions_for_purchase_order,
			get_permission_query_conditions_for_sales_invoice
		)
		
		# Test Purchase Order permissions
		po_condition = get_permission_query_conditions_for_purchase_order("test@example.com")
		print(f"Purchase Order condition: {po_condition}")
		
		# Test Sales Invoice permissions
		si_condition = get_permission_query_conditions_for_sales_invoice("test@example.com")
		print(f"Sales Invoice condition: {si_condition}")
		
		print("✓ Transactional document permissions - OK")
		
	except Exception as e:
		print(f"✗ Transactional document permissions - ERROR: {str(e)}")


def check_user_permissions(user):
	"""
	Check what permissions a user has
	"""
	print(f"\nChecking permissions for user: {user}")
	
	# Check Factory Business Unit permissions
	factory_permissions = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Factory Business Unit'
	""", user)
	print(f"Factory Business Unit permissions: {factory_permissions}")
	
	# Check Strategic Business Unit permissions
	sbu_permissions = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Strategic Business Unit'
	""", user)
	print(f"Strategic Business Unit permissions: {sbu_permissions}")
	
	# Check Cost Center permissions
	cost_center_permissions = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Cost Center'
	""", user)
	print(f"Cost Center permissions: {cost_center_permissions}")
	
	return {
		'factories': factory_permissions,
		'sbus': sbu_permissions,
		'cost_centers': cost_center_permissions
	}


def check_cost_center_associations():
	"""
	Check cost center associations with Factory Business Units and SBUs
	"""
	print("\nChecking cost center associations...")
	
	# Check Factory Business Units with cost centers
	factory_cost_centers = frappe.db.sql("""
		SELECT name, factory_name, cost_center 
		FROM `tabFactory Business Unit`
		WHERE cost_center IS NOT NULL
	""", as_dict=True)
	print(f"Factory Business Units with cost centers: {len(factory_cost_centers)}")
	for fbu in factory_cost_centers[:5]:  # Show first 5
		print(f"  {fbu.name} ({fbu.factory_name}) -> {fbu.cost_center}")
	
	# Check Strategic Business Units with cost centers
	sbu_cost_centers = frappe.db.sql("""
		SELECT name, sbu_name, cost_center 
		FROM `tabStrategic Business Unit`
		WHERE cost_center IS NOT NULL
	""", as_dict=True)
	print(f"Strategic Business Units with cost centers: {len(sbu_cost_centers)}")
	for sbu in sbu_cost_centers[:5]:  # Show first 5
		print(f"  {sbu.name} ({sbu.sbu_name}) -> {sbu.cost_center}")


def create_test_user_permissions():
	"""
	Create test user permissions for testing
	"""
	print("\nCreating test user permissions...")
	
	# Check if test user exists
	if not frappe.db.exists("User", "test@example.com"):
		print("Test user does not exist. Please create a test user first.")
		return
	
	# Create test Factory Business Unit permission
	if not frappe.db.exists("User Permission", {
		"user": "test@example.com",
		"allow": "Factory Business Unit",
		"for_value": "TEST-FACTORY-001"
	}):
		frappe.get_doc({
			"doctype": "User Permission",
			"user": "test@example.com",
			"allow": "Factory Business Unit",
			"for_value": "TEST-FACTORY-001"
		}).insert(ignore_permissions=True)
		print("Created test Factory Business Unit permission")
	
	# Create test Strategic Business Unit permission
	if not frappe.db.exists("User Permission", {
		"user": "test@example.com",
		"allow": "Strategic Business Unit",
		"for_value": "TEST-SBU-001"
	}):
		frappe.get_doc({
			"doctype": "User Permission",
			"user": "test@example.com",
			"allow": "Strategic Business Unit",
			"for_value": "TEST-SBU-001"
		}).insert(ignore_permissions=True)
		print("Created test Strategic Business Unit permission")
	
	print("Test user permissions created!")


if __name__ == "__main__":
	# Run the tests
	test_permission_system()
	
	# Check cost center associations
	check_cost_center_associations()
	
	# Check permissions for current user
	current_user = frappe.session.user
	check_user_permissions(current_user) 