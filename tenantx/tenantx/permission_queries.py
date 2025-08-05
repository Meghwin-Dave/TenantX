# Copyright (c) 2025, CognitionXLogic and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def get_permission_query_conditions_for_purchase_order(user):
	"""
	Permission query conditions for Purchase Order
	Checks if the cost center is linked to a Factory Business Unit or SBU that the user has access to
	"""
	if not user:
		user = frappe.session.user
	
	# System Manager sees everything
	if "System Manager" in frappe.get_roles(user):
		return ""
	
	# Get user's allowed Factory Business Units and SBUs
	allowed_factories = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Factory Business Unit'
	""", user)
	
	allowed_sbus = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Strategic Business Unit'
	""", user)
	
	# Get user's directly allowed cost centers
	allowed_cost_centers = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Cost Center'
	""", user)
	
	# If user has no permissions, they see nothing
	if not allowed_factories and not allowed_sbus and not allowed_cost_centers:
		return "1=0"
	
	conditions = []
	
	# Check if cost center is linked to allowed Factory Business Units
	if allowed_factories:
		conditions.append(f"""`tabPurchase Order`.`cost_center` IN (
			SELECT `cost_center` FROM `tabFactory Business Unit`
			WHERE `name` IN ({','.join(['%s'] * len(allowed_factories))})
		)""")
	
	# Check if cost center is linked to allowed SBUs
	if allowed_sbus:
		conditions.append(f"""`tabPurchase Order`.`cost_center` IN (
			SELECT `cost_center` FROM `tabStrategic Business Unit`
			WHERE `name` IN ({','.join(['%s'] * len(allowed_sbus))})
		)""")
	
	# Check if cost center is directly allowed
	if allowed_cost_centers:
		conditions.append(f"""`tabPurchase Order`.`cost_center` IN ({','.join(['%s'] * len(allowed_cost_centers))})""")
	
	# Combine conditions with OR
	if conditions:
		return "(" + " OR ".join(conditions) + ")"
	
	return "1=0"


def get_permission_query_conditions_for_sales_invoice(user):
	"""
	Permission query conditions for Sales Invoice
	Checks if the cost center is linked to a Factory Business Unit or SBU that the user has access to
	"""
	if not user:
		user = frappe.session.user
	
	# System Manager sees everything
	if "System Manager" in frappe.get_roles(user):
		return ""
	
	# Get user's allowed Factory Business Units and SBUs
	allowed_factories = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Factory Business Unit'
	""", user)
	
	allowed_sbus = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Strategic Business Unit'
	""", user)
	
	# Get user's directly allowed cost centers
	allowed_cost_centers = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Cost Center'
	""", user)
	
	# If user has no permissions, they see nothing
	if not allowed_factories and not allowed_sbus and not allowed_cost_centers:
		return "1=0"
	
	conditions = []
	
	# Check if cost center is linked to allowed Factory Business Units
	if allowed_factories:
		conditions.append(f"""`tabSales Invoice`.`cost_center` IN (
			SELECT `cost_center` FROM `tabFactory Business Unit`
			WHERE `name` IN ({','.join(['%s'] * len(allowed_factories))})
		)""")
	
	# Check if cost center is linked to allowed SBUs
	if allowed_sbus:
		conditions.append(f"""`tabSales Invoice`.`cost_center` IN (
			SELECT `cost_center` FROM `tabStrategic Business Unit`
			WHERE `name` IN ({','.join(['%s'] * len(allowed_sbus))})
		)""")
	
	# Check if cost center is directly allowed
	if allowed_cost_centers:
		conditions.append(f"""`tabSales Invoice`.`cost_center` IN ({','.join(['%s'] * len(allowed_cost_centers))})""")
	
	# Combine conditions with OR
	if conditions:
		return "(" + " OR ".join(conditions) + ")"
	
	return "1=0"


def get_permission_query_conditions_for_purchase_invoice(user):
	"""
	Permission query conditions for Purchase Invoice
	Checks if the cost center is linked to a Factory Business Unit or SBU that the user has access to
	"""
	if not user:
		user = frappe.session.user
	
	# System Manager sees everything
	if "System Manager" in frappe.get_roles(user):
		return ""
	
	# Get user's allowed Factory Business Units and SBUs
	allowed_factories = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Factory Business Unit'
	""", user)
	
	allowed_sbus = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Strategic Business Unit'
	""", user)
	
	# Get user's directly allowed cost centers
	allowed_cost_centers = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Cost Center'
	""", user)
	
	# If user has no permissions, they see nothing
	if not allowed_factories and not allowed_sbus and not allowed_cost_centers:
		return "1=0"
	
	conditions = []
	
	# Check if cost center is linked to allowed Factory Business Units
	if allowed_factories:
		conditions.append(f"""`tabPurchase Invoice`.`cost_center` IN (
			SELECT `cost_center` FROM `tabFactory Business Unit`
			WHERE `name` IN ({','.join(['%s'] * len(allowed_factories))})
		)""")
	
	# Check if cost center is linked to allowed SBUs
	if allowed_sbus:
		conditions.append(f"""`tabPurchase Invoice`.`cost_center` IN (
			SELECT `cost_center` FROM `tabStrategic Business Unit`
			WHERE `name` IN ({','.join(['%s'] * len(allowed_sbus))})
		)""")
	
	# Check if cost center is directly allowed
	if allowed_cost_centers:
		conditions.append(f"""`tabPurchase Invoice`.`cost_center` IN ({','.join(['%s'] * len(allowed_cost_centers))})""")
	
	# Combine conditions with OR
	if conditions:
		return "(" + " OR ".join(conditions) + ")"
	
	return "1=0"


def get_permission_query_conditions_for_sales_order(user):
	"""
	Permission query conditions for Sales Order
	Checks if the cost center is linked to a Factory Business Unit or SBU that the user has access to
	"""
	if not user:
		user = frappe.session.user
	
	# System Manager sees everything
	if "System Manager" in frappe.get_roles(user):
		return ""
	
	# Get user's allowed Factory Business Units and SBUs
	allowed_factories = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Factory Business Unit'
	""", user)
	
	allowed_sbus = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Strategic Business Unit'
	""", user)
	
	# Get user's directly allowed cost centers
	allowed_cost_centers = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Cost Center'
	""", user)
	
	# If user has no permissions, they see nothing
	if not allowed_factories and not allowed_sbus and not allowed_cost_centers:
		return "1=0"
	
	conditions = []
	
	# Check if cost center is linked to allowed Factory Business Units
	if allowed_factories:
		conditions.append(f"""`tabSales Order`.`cost_center` IN (
			SELECT `cost_center` FROM `tabFactory Business Unit`
			WHERE `name` IN ({','.join(['%s'] * len(allowed_factories))})
		)""")
	
	# Check if cost center is linked to allowed SBUs
	if allowed_sbus:
		conditions.append(f"""`tabSales Order`.`cost_center` IN (
			SELECT `cost_center` FROM `tabStrategic Business Unit`
			WHERE `name` IN ({','.join(['%s'] * len(allowed_sbus))})
		)""")
	
	# Check if cost center is directly allowed
	if allowed_cost_centers:
		conditions.append(f"""`tabSales Order`.`cost_center` IN ({','.join(['%s'] * len(allowed_cost_centers))})""")
	
	# Combine conditions with OR
	if conditions:
		return "(" + " OR ".join(conditions) + ")"
	
	return "1=0"


def get_permission_query_conditions_for_delivery_note(user):
	"""
	Permission query conditions for Delivery Note
	Checks if the cost center is linked to a Factory Business Unit or SBU that the user has access to
	"""
	if not user:
		user = frappe.session.user
	
	# System Manager sees everything
	if "System Manager" in frappe.get_roles(user):
		return ""
	
	# Get user's allowed Factory Business Units and SBUs
	allowed_factories = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Factory Business Unit'
	""", user)
	
	allowed_sbus = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Strategic Business Unit'
	""", user)
	
	# Get user's directly allowed cost centers
	allowed_cost_centers = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Cost Center'
	""", user)
	
	# If user has no permissions, they see nothing
	if not allowed_factories and not allowed_sbus and not allowed_cost_centers:
		return "1=0"
	
	conditions = []
	
	# Check if cost center is linked to allowed Factory Business Units
	if allowed_factories:
		conditions.append(f"""`tabDelivery Note`.`cost_center` IN (
			SELECT `cost_center` FROM `tabFactory Business Unit`
			WHERE `name` IN ({','.join(['%s'] * len(allowed_factories))})
		)""")
	
	# Check if cost center is linked to allowed SBUs
	if allowed_sbus:
		conditions.append(f"""`tabDelivery Note`.`cost_center` IN (
			SELECT `cost_center` FROM `tabStrategic Business Unit`
			WHERE `name` IN ({','.join(['%s'] * len(allowed_sbus))})
		)""")
	
	# Check if cost center is directly allowed
	if allowed_cost_centers:
		conditions.append(f"""`tabDelivery Note`.`cost_center` IN ({','.join(['%s'] * len(allowed_cost_centers))})""")
	
	# Combine conditions with OR
	if conditions:
		return "(" + " OR ".join(conditions) + ")"
	
	return "1=0"


def get_permission_query_conditions_for_purchase_receipt(user):
	"""
	Permission query conditions for Purchase Receipt
	Checks if the cost center is linked to a Factory Business Unit or SBU that the user has access to
	"""
	if not user:
		user = frappe.session.user
	
	# System Manager sees everything
	if "System Manager" in frappe.get_roles(user):
		return ""
	
	# Get user's allowed Factory Business Units and SBUs
	allowed_factories = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Factory Business Unit'
	""", user)
	
	allowed_sbus = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Strategic Business Unit'
	""", user)
	
	# Get user's directly allowed cost centers
	allowed_cost_centers = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Cost Center'
	""", user)
	
	# If user has no permissions, they see nothing
	if not allowed_factories and not allowed_sbus and not allowed_cost_centers:
		return "1=0"
	
	conditions = []
	
	# Check if cost center is linked to allowed Factory Business Units
	if allowed_factories:
		conditions.append(f"""`tabPurchase Receipt`.`cost_center` IN (
			SELECT `cost_center` FROM `tabFactory Business Unit`
			WHERE `name` IN ({','.join(['%s'] * len(allowed_factories))})
		)""")
	
	# Check if cost center is linked to allowed SBUs
	if allowed_sbus:
		conditions.append(f"""`tabPurchase Receipt`.`cost_center` IN (
			SELECT `cost_center` FROM `tabStrategic Business Unit`
			WHERE `name` IN ({','.join(['%s'] * len(allowed_sbus))})
		)""")
	
	# Check if cost center is directly allowed
	if allowed_cost_centers:
		conditions.append(f"""`tabPurchase Receipt`.`cost_center` IN ({','.join(['%s'] * len(allowed_cost_centers))})""")
	
	# Combine conditions with OR
	if conditions:
		return "(" + " OR ".join(conditions) + ")"
	
	return "1=0"


def get_permission_query_conditions_for_journal_entry(user):
	"""
	Permission query conditions for Journal Entry
	Checks if any of the cost centers in the journal entry are linked to Factory Business Units or SBUs that the user has access to
	"""
	if not user:
		user = frappe.session.user
	
	# System Manager sees everything
	if "System Manager" in frappe.get_roles(user):
		return ""
	
	# Get user's allowed Factory Business Units and SBUs
	allowed_factories = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Factory Business Unit'
	""", user)
	
	allowed_sbus = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Strategic Business Unit'
	""", user)
	
	# Get user's directly allowed cost centers
	allowed_cost_centers = frappe.db.sql_list("""
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user` = %s AND `allow` = 'Cost Center'
	""", user)
	
	# If user has no permissions, they see nothing
	if not allowed_factories and not allowed_sbus and not allowed_cost_centers:
		return "1=0"
	
	conditions = []
	
	# Check if any cost center in the journal entry is linked to allowed Factory Business Units
	if allowed_factories:
		conditions.append(f"""EXISTS (
			SELECT 1 FROM `tabJournal Entry Account` jea
			WHERE jea.parent = `tabJournal Entry`.`name`
			AND jea.cost_center IN (
				SELECT `cost_center` FROM `tabFactory Business Unit`
				WHERE `name` IN ({','.join(['%s'] * len(allowed_factories))})
			)
		)""")
	
	# Check if any cost center in the journal entry is linked to allowed SBUs
	if allowed_sbus:
		conditions.append(f"""EXISTS (
			SELECT 1 FROM `tabJournal Entry Account` jea
			WHERE jea.parent = `tabJournal Entry`.`name`
			AND jea.cost_center IN (
				SELECT `cost_center` FROM `tabStrategic Business Unit`
				WHERE `name` IN ({','.join(['%s'] * len(allowed_sbus))})
			)
		)""")
	
	# Check if any cost center in the journal entry is directly allowed
	if allowed_cost_centers:
		conditions.append(f"""EXISTS (
			SELECT 1 FROM `tabJournal Entry Account` jea
			WHERE jea.parent = `tabJournal Entry`.`name`
			AND jea.cost_center IN ({','.join(['%s'] * len(allowed_cost_centers))})
		)""")
	
	# Combine conditions with OR
	if conditions:
		return "(" + " OR ".join(conditions) + ")"
	
	return "1=0" 