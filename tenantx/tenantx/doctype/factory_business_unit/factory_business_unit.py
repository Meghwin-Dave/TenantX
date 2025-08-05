# Copyright (c) 2025, CognitionXLogic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
import re


class FactoryBusinessUnit(Document):
	def validate(self):
		"""Validate factory business unit data before saving"""
		self.validate_factory_code()
		self.validate_enterprise_association()
		self.validate_company_association()
		self.validate_sbu_association()
		self.validate_factory_category()
		self.validate_capacity()
		self.validate_factory_head()
		self.validate_cost_center()
		self.validate_contact_address()
		self.create_cost_center_if_needed()
	
	def validate_factory_code(self):
		"""Validate factory code format and uniqueness"""
		if self.factory_code:
			# Check for alphanumeric format
			if not re.match(r'^[A-Z0-9\-_]+$', self.factory_code):
				frappe.throw(_("Factory Code must contain only uppercase letters, numbers, hyphens, and underscores"))
			
			# Check for minimum length
			if len(self.factory_code) < 3:
				frappe.throw(_("Factory Code must be at least 3 characters long"))
			
			# Check for maximum length
			if len(self.factory_code) > 20:
				frappe.throw(_("Factory Code cannot exceed 20 characters"))
			
			# Check for uniqueness
			existing = frappe.db.exists("Factory Business Unit", {
				"factory_code": self.factory_code,
				"name": ["!=", self.name]
			})
			if existing:
				frappe.throw(_("Factory Code '{0}' already exists").format(self.factory_code))
	
	def validate_enterprise_association(self):
		"""Validate enterprise association"""
		if self.enterprise:
			# Check if enterprise exists and is active
			enterprise = frappe.get_doc("Enterprise", self.enterprise)
			if not enterprise.is_active:
				frappe.throw(_("Enterprise '{0}' is not active").format(self.enterprise))
	
	def validate_company_association(self):
		"""Validate company association"""
		if self.company:
			# Check if company exists and is active
			if not frappe.db.exists("Company", {"name": self.company}):
				frappe.throw(_("Company '{0}' does not exist").format(self.company))
			
			# Check if company matches enterprise company
			if self.enterprise:
				enterprise = frappe.get_doc("Enterprise", self.enterprise)
				if enterprise.company and enterprise.company != self.company:
					frappe.throw(_("Company must match the enterprise's company"))
	
	def validate_sbu_association(self):
		"""Validate SBU association"""
		if self.sbu:
			sbu = frappe.get_doc("Strategic Business Unit", self.sbu)
			
			# Check if SBU belongs to the same enterprise
			if sbu.enterprise != self.enterprise:
				frappe.throw(_("SBU must belong to the same enterprise"))
			
			# Check if SBU is active
			if not sbu.is_active:
				frappe.throw(_("SBU '{0}' is not active").format(self.sbu))
	
	def validate_factory_category(self):
		"""Validate factory category association"""
		if self.factory_category:
			if not frappe.db.exists("Factory Category", self.factory_category):
				frappe.throw(_("Factory Category '{0}' does not exist").format(self.factory_category))
	
	def validate_capacity(self):
		"""Validate capacity and UOM"""
		if self.capacity is not None:
			# Check for positive capacity
			if self.capacity <= 0:
				frappe.throw(_("Capacity must be greater than zero"))
			
			# Check if UOM is provided when capacity is set
			if self.capacity > 0 and not self.capacity_uom:
				frappe.throw(_("Capacity UOM is required when capacity is specified"))
		
		if self.capacity_uom:
			# Check if UOM exists
			if not frappe.db.exists("UOM", self.capacity_uom):
				frappe.throw(_("UOM '{0}' does not exist").format(self.capacity_uom))
	
	def validate_factory_head(self):
		"""Validate factory head assignment"""
		if self.factory_head:
			# Check if employee exists
			if not frappe.db.exists("Employee", self.factory_head):
				frappe.throw(_("Employee '{0}' does not exist").format(self.factory_head))
			
			# Check if employee is active
			employee = frappe.get_doc("Employee", self.factory_head)
			if employee.status != "Active":
				frappe.throw(_("Factory Head '{0}' is not an active employee").format(self.factory_head))
	
	def validate_cost_center(self):
		"""Validate cost center association"""
		if self.cost_center:
			# Check if cost center exists
			if not frappe.db.exists("Cost Center", self.cost_center):
				frappe.throw(_("Cost Center '{0}' does not exist").format(self.cost_center))
			
			# Check if cost center is active
			cost_center = frappe.get_doc("Cost Center", self.cost_center)
			if cost_center.disabled:
				frappe.throw(_("Cost Center '{0}' is disabled").format(self.cost_center))
	
	def validate_contact_address(self):
		"""Validate contact and address information"""
		if self.contact:
			if not frappe.db.exists("Contact", self.contact):
				frappe.throw(_("Contact '{0}' does not exist").format(self.contact))
		
		if self.address:
			if not frappe.db.exists("Address", self.address):
				frappe.throw(_("Address '{0}' does not exist").format(self.address))
	
	def on_update(self):
		"""Actions after factory business unit is updated"""
		self.update_sbu_references()
		self.update_related_documents()
	
	def update_sbu_references(self):
		"""Update SBU references if factory changes"""
		if self.has_value_changed("sbu"):
			# Update SBU's factory reference
			if self.sbu:
				frappe.db.set_value("Strategic Business Unit", self.sbu, "factory", self.name)
	
	def update_related_documents(self):
		"""Update related documents when factory changes"""
		# Update SBU if factory is deactivated
		if self.has_value_changed("is_active") and not self.is_active:
			if self.sbu:
				sbu = frappe.get_doc("Strategic Business Unit", self.sbu)
				if sbu.factory == self.name:
					frappe.db.set_value("Strategic Business Unit", self.sbu, "factory", "")
					frappe.msgprint(_("Factory reference has been removed from SBU '{0}'").format(self.sbu))
	
	def on_trash(self):
		"""Actions before factory business unit is deleted"""
		self.check_dependencies()
	
	def check_dependencies(self):
		"""Check for dependencies before deletion"""
		# Check for associated SBUs
		sbu_count = frappe.db.count("Strategic Business Unit", {"factory": self.name})
		if sbu_count > 0:
			frappe.throw(_("Cannot delete Factory Business Unit '{0}' as it is referenced by {1} SBU(s)").format(
				self.name, sbu_count))
	
	def before_insert(self):
		"""Actions before factory business unit is inserted"""
		self.set_default_values()
	
	def set_default_values(self):
		"""Set default values for new factory business unit"""
		if not self.is_active:
			self.is_active = 1

	def create_cost_center_if_needed(self):
		"""Create a Cost Center if is_cost_center is checked and not already set"""
		if getattr(self, 'is_cost_center', 0) and self.company and not self.cost_center:
			# Check if a cost center with this name and company already exists
			existing = frappe.db.exists("Cost Center", {"cost_center_name": self.factory_name, "company": self.company})
			if existing:
				self.cost_center = existing
			else:
				# Get the root cost center for the company
				parent_cost_center = frappe.db.get_value("Cost Center", {"company": self.company, "parent_cost_center": None}, "name")
				cc = frappe.get_doc({
					"doctype": "Cost Center",
					"cost_center_name": self.factory_name,
					"company": self.company,
					"is_group": 0,
					"parent_cost_center": parent_cost_center
				})
				cc.insert(ignore_permissions=True)
				self.cost_center = cc.name


def get_permission_query_conditions(user):
	"""
	Permission query conditions for Factory Business Unit
	This function checks User Permission records for the logged-in user and returns SQL conditions
	"""
	if not user:
		user = frappe.session.user
	
	# System Manager sees everything
	if "System Manager" in frappe.get_roles(user):
		return ""
	
	# This line fetches all Factory Business Units the user has been granted access to
	# via the User Permissions doctype, which we automated in the previous step.
	return """( `tabFactory Business Unit`.`name` IN (
		SELECT `for_value` FROM `tabUser Permission`
		WHERE `user`=%(user)s AND `allow`='Factory Business Unit'
	))"""
