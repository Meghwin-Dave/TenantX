# Copyright (c) 2025, CognitionXLogic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class FactoryCategory(Document):
	def validate(self):
		"""Validate factory category data before saving"""
		self.validate_factory_category_name()
		self.validate_description()
	
	def validate_factory_category_name(self):
		"""Validate factory category name"""
		if self.factory_category:
			# Check for minimum length
			if len(self.factory_category.strip()) < 2:
				frappe.throw(_("Factory Category name must be at least 2 characters long"))
			
			# Check for maximum length
			if len(self.factory_category) > 100:
				frappe.throw(_("Factory Category name cannot exceed 100 characters"))
			
			# Check for uniqueness
			existing = frappe.db.exists("Factory Category", {
				"factory_category": self.factory_category,
				"name": ["!=", self.name]
			})
			if existing:
				frappe.throw(_("Factory Category '{0}' already exists").format(self.factory_category))
			
			# Check for special characters (allow only letters, numbers, spaces, and common punctuation)
			if not frappe.utils.validate_name(self.factory_category, throw=False):
				frappe.throw(_("Factory Category name contains invalid characters"))
	
	def validate_description(self):
		"""Validate description field"""
		if self.description:
			# Check for maximum length
			if len(self.description) > 500:
				frappe.throw(_("Description cannot exceed 500 characters"))
			
			# Check for minimum meaningful content
			if len(self.description.strip()) < 10:
				frappe.msgprint(_("Description should be more detailed for better documentation"), alert=True)
	
	def on_trash(self):
		"""Actions before factory category is deleted"""
		self.check_dependencies()
	
	def check_dependencies(self):
		"""Check for dependencies before deletion"""
		# Check for associated factory business units
		factory_count = frappe.db.count("Factory Business Unit", {"factory_category": self.name})
		if factory_count > 0:
			frappe.throw(_("Cannot delete Factory Category '{0}' as it is used by {1} Factory Business Unit(s)").format(
				self.name, factory_count))