# Copyright (c) 2025, CognitionXLogic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _


class BusinessSegment(Document):
	def validate(self):
		"""Validate business segment data before saving"""
		self.validate_segment_name()
		self.validate_description()
	
	def validate_segment_name(self):
		"""Validate business segment name"""
		if self.segment_name:
			# Check for minimum length
			if len(self.segment_name.strip()) < 2:
				frappe.throw(_("Business Segment name must be at least 2 characters long"))
			
			# Check for maximum length
			if len(self.segment_name) > 100:
				frappe.throw(_("Business Segment name cannot exceed 100 characters"))
			
			# Check for uniqueness
			existing = frappe.db.exists("Business Segment", {
				"segment_name": self.segment_name,
				"name": ["!=", self.name]
			})
			if existing:
				frappe.throw(_("Business Segment '{0}' already exists").format(self.segment_name))
			
			# Check for special characters (allow only letters, numbers, spaces, and common punctuation)
			if not frappe.utils.validate_name(self.segment_name, throw=False):
				frappe.throw(_("Business Segment name contains invalid characters"))
	
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
		"""Actions before business segment is deleted"""
		self.check_dependencies()
	
	def check_dependencies(self):
		"""Check for dependencies before deletion"""
		# Check for associated strategic business units
		sbu_count = frappe.db.count("Strategic Business Unit", {"business_segment": self.name})
		if sbu_count > 0:
			frappe.throw(_("Cannot delete Business Segment '{0}' as it is used by {1} Strategic Business Unit(s)").format(
				self.name, sbu_count))