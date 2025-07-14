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
		self.validate_factory_association()
		self.validate_sbu_head()
		self.validate_cost_center()
		self.validate_naming_series()
	
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
	
	def validate_factory_association(self):
		"""Validate factory business unit association"""
		if self.factory:
			factory = frappe.get_doc("Factory Business Unit", self.factory)
			
			# Check if factory belongs to the same enterprise
			if factory.enterprise != self.enterprise:
				frappe.throw(_("Factory Business Unit must belong to the same enterprise"))
			
			# Check if factory is active
			if not factory.is_active:
				frappe.throw(_("Factory Business Unit '{0}' is not active").format(self.factory))
	
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
	
	def validate_naming_series(self):
		"""Validate naming series format"""
		if self.naming_series:
			if not self.naming_series.startswith("SBU-"):
				frappe.throw(_("SBU naming series must start with 'SBU-'"))
	
	def on_update(self):
		"""Actions after SBU is updated"""
		self.update_factory_references()
		self.update_related_documents()
	
	def update_factory_references(self):
		"""Update factory references if SBU changes"""
		if self.has_value_changed("name"):
			# Update factory business units that reference this SBU
			factories = frappe.get_all("Factory Business Unit", 
				filters={"sbu": self.name}, 
				fields=["name"])
			
			for factory in factories:
				frappe.db.set_value("Factory Business Unit", factory.name, "sbu", self.name)
	
	def update_related_documents(self):
		"""Update related documents when SBU changes"""
		# Update factory business units if SBU is deactivated
		if self.has_value_changed("is_active") and not self.is_active:
			factories = frappe.get_all("Factory Business Unit", 
				filters={"sbu": self.name, "is_active": 1}, 
				fields=["name"])
			
			for factory in factories:
				frappe.db.set_value("Factory Business Unit", factory.name, "is_active", 0)
				frappe.msgprint(_("Factory Business Unit '{0}' has been deactivated").format(factory.name))
	
	def on_trash(self):
		"""Actions before SBU is deleted"""
		self.check_dependencies()
	
	def check_dependencies(self):
		"""Check for dependencies before deletion"""
		# Check for associated factory business units
		factory_count = frappe.db.count("Factory Business Unit", {"sbu": self.name})
		if factory_count > 0:
			frappe.throw(_("Cannot delete SBU '{0}' as it has {1} associated Factory Business Unit(s)").format(
				self.name, factory_count))
	
	def before_insert(self):
		"""Actions before SBU is inserted"""
		self.set_default_values()
	
	def set_default_values(self):
		"""Set default values for new SBU"""
		if not self.is_active:
			self.is_active = 1
