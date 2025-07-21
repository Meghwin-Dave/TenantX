# Copyright (c) 2025, CognitionXLogic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
import re


class StrategicBusinessUnit(Document):
	def validate(self):
		"""Validate SBU data before saving"""
		self.validate_sbu_code()
		self.validate_enterprise_association()
		self.validate_company_association()
		self.validate_business_segment()
		self.validate_sbu_head()
		self.validate_cost_center()
		self.validate_parent_sbu()
		self.create_cost_center_if_needed()
	
	def validate_sbu_code(self):
		"""Validate SBU code format and uniqueness"""
		if self.sbu_code:
			# Check for alphanumeric format
			if not re.match(r'^[A-Z0-9\-_]+$', self.sbu_code):
				frappe.throw(_("SBU Code must contain only uppercase letters, numbers, hyphens, and underscores"))
			
			# Check for minimum length
			if len(self.sbu_code) < 3:
				frappe.throw(_("SBU Code must be at least 3 characters long"))
			
			# Check for maximum length
			if len(self.sbu_code) > 20:
				frappe.throw(_("SBU Code cannot exceed 20 characters"))
			
			# Check for uniqueness
			existing = frappe.db.exists("Strategic Business Unit", {
				"sbu_code": self.sbu_code,
				"name": ["!=", self.name]
			})
			if existing:
				frappe.throw(_("SBU Code '{0}' already exists").format(self.sbu_code))
	
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
	
	def validate_business_segment(self):
		"""Validate business segment association"""
		if self.business_segment:
			if not frappe.db.exists("Business Segment", self.business_segment):
				frappe.throw(_("Business Segment '{0}' does not exist").format(self.business_segment))
	
	def validate_sbu_head(self):
		"""Validate SBU head assignment"""
		if self.sbu_head:
			# Check if employee exists
			if not frappe.db.exists("Employee", self.sbu_head):
				frappe.throw(_("Employee '{0}' does not exist").format(self.sbu_head))
			
			# Check if employee is active
			employee = frappe.get_doc("Employee", self.sbu_head)
			if employee.status != "Active":
				frappe.throw(_("SBU Head '{0}' is not an active employee").format(self.sbu_head))
	
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
	
	def validate_parent_sbu(self):
		"""Validate parent SBU association"""
		if self.parent_sbu:
			# Prevent self-parenting
			if self.parent_sbu == self.name:
				frappe.throw(_("SBU cannot be its own parent"))
			# Check if parent SBU exists and is active
			parent = frappe.get_doc("Strategic Business Unit", self.parent_sbu)
			if not parent.is_active:
				frappe.throw(_("Parent SBU '{0}' is not active").format(self.parent_sbu))
			# Check if parent SBU belongs to the same enterprise
			if self.enterprise and parent.enterprise and parent.enterprise != self.enterprise:
				frappe.throw(_("Parent SBU must belong to the same enterprise"))
			# Check if parent SBU belongs to the same company
			if self.company and parent.company and parent.company != self.company:
				frappe.throw(_("Parent SBU must belong to the same company"))
	
	def before_insert(self):
		"""Actions before SBU is inserted"""
		self.set_default_values()
	
	def set_default_values(self):
		"""Set default values for new SBU"""
		if not self.is_active:
			self.is_active = 1

	def create_cost_center_if_needed(self):
		"""Create a Cost Center if is_cost_center is checked and not already set"""
		if getattr(self, 'is_cost_center', 0) and self.company and not self.cost_center:
			# Check if a cost center with this name and company already exists
			existing = frappe.db.exists("Cost Center", {"cost_center_name": self.sbu_name, "company": self.company})
			if existing:
				self.cost_center = existing
			else:
				# Get the root cost center for the company
				parent_cost_center = frappe.db.get_value("Cost Center", {"company": self.company, "parent_cost_center": None}, "name")
				cc = frappe.get_doc({
					"doctype": "Cost Center",
					"cost_center_name": self.sbu_name,
					"company": self.company,
					"is_group": 0,
					"parent_cost_center": parent_cost_center
				})
				cc.insert(ignore_permissions=True)
				self.cost_center = cc.name
