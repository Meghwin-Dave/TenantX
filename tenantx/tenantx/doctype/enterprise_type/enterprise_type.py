# Copyright (c) 2025, CognitionXLogic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class EnterpriseType(Document):
	def validate(self):
		"""Validate enterprise type data before saving"""
		self.validate_enterprise_type_name()
		self.validate_description()
	
	def validate_enterprise_type_name(self):
		"""Validate enterprise type name"""
		if self.enterprise_type:
			# Check for minimum length
			if len(self.enterprise_type.strip()) < 2:
				frappe.throw(_("Enterprise Type name must be at least 2 characters long"))
			
			# Check for maximum length
			if len(self.enterprise_type) > 100:
				frappe.throw(_("Enterprise Type name cannot exceed 100 characters"))
			
			# Check for uniqueness
			existing = frappe.db.exists("Enterprise Type", {
				"enterprise_type": self.enterprise_type,
				"name": ["!=", self.name]
			})
			if existing:
				frappe.throw(_("Enterprise Type '{0}' already exists").format(self.enterprise_type))
			
			# Check for special characters (allow only letters, numbers, spaces, and common punctuation)
			if not frappe.utils.validate_name(self.enterprise_type, throw=False):
				frappe.throw(_("Enterprise Type name contains invalid characters"))
	
	def validate_description(self):
		"""Validate description field"""
		if self.description:
			# Check for maximum length
			if len(self.description) > 500:
				frappe.throw(_("Description cannot exceed 500 characters"))
	
	def on_trash(self):
		"""Actions before enterprise type is deleted"""
		self.check_dependencies()
	
	def check_dependencies(self):
		"""Check for dependencies before deletion"""
		# Check for associated enterprises
		enterprise_count = frappe.db.count("Enterprise", {"enterprise_type": self.name})
		if enterprise_count > 0:
			frappe.throw(_("Cannot delete Enterprise Type '{0}' as it is used by {1} enterprise(s)").format(
				self.name, enterprise_count))