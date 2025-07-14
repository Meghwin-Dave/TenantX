# Copyright (c) 2025, CognitionXLogic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
import re


class Enterprise(Document):
	def validate(self):
		"""Validate enterprise data before saving"""
		self.validate_enterprise_code()
		self.validate_tax_id()
		self.validate_hierarchy()
		self.validate_company_association()
		self.validate_contact_address()
	
	def validate_enterprise_code(self):
		"""Validate enterprise code format and uniqueness"""
		if self.enterprise_code:
			# Check for alphanumeric format
			if not re.match(r'^[A-Z0-9\-_]+$', self.enterprise_code):
				frappe.throw(_("Enterprise Code must contain only uppercase letters, numbers, hyphens, and underscores"))
			
			# Check for minimum length
			if len(self.enterprise_code) < 3:
				frappe.throw(_("Enterprise Code must be at least 3 characters long"))
			
			# Check for uniqueness
			existing = frappe.db.exists("Enterprise", {
				"enterprise_code": self.enterprise_code,
				"name": ["!=", self.name]
			})
			if existing:
				frappe.throw(_("Enterprise Code '{0}' already exists").format(self.enterprise_code))
	
	def validate_tax_id(self):
		"""Validate tax ID format if provided"""
		if self.tax_id:
			# Remove spaces and common separators for validation
			clean_tax_id = re.sub(r'[\s\-_\.]', '', self.tax_id)
			
			# Check for alphanumeric format
			if not re.match(r'^[A-Z0-9]+$', clean_tax_id):
				frappe.throw(_("Tax ID must contain only letters and numbers"))
			
			# Check for reasonable length (5-20 characters)
			if len(clean_tax_id) < 5 or len(clean_tax_id) > 20:
				frappe.throw(_("Tax ID must be between 5 and 20 characters long"))
	
	def validate_hierarchy(self):
		"""Validate enterprise hierarchy relationships"""
		if self.parent_enterprise:
			# Check if parent enterprise exists and is active
			parent = frappe.get_doc("Enterprise", self.parent_enterprise)
			if not parent.is_active:
				frappe.throw(_("Parent Enterprise '{0}' is not active").format(self.parent_enterprise))
			
			# Prevent circular references
			if self.name == self.parent_enterprise:
				frappe.throw(_("Enterprise cannot be its own parent"))
			
			# Check if parent is a group enterprise
			if not parent.is_group:
				frappe.throw(_("Parent Enterprise '{0}' must be marked as a group").format(self.parent_enterprise))
	
	def validate_company_association(self):
		"""Validate company association"""
		if self.company:
			# Check if company exists and is active
			if not frappe.db.exists("Company", {"name": self.company}):
				frappe.throw(_("Company '{0}' does not exist").format(self.company))
	
	def validate_contact_address(self):
		"""Validate contact and address information"""
		if self.contact:
			if not frappe.db.exists("Contact", self.contact):
				frappe.throw(_("Contact '{0}' does not exist").format(self.contact))
		
		if self.address:
			if not frappe.db.exists("Address", self.address):
				frappe.throw(_("Address '{0}' does not exist").format(self.address))
	
	def on_update(self):
		"""Actions to perform after enterprise is updated"""
		self.update_child_enterprises()
		self.update_related_documents()
	
	def update_child_enterprises(self):
		"""Update child enterprises if parent status changes"""
		if self.has_value_changed("is_active"):
			child_enterprises = frappe.get_all("Enterprise", 
				filters={"parent_enterprise": self.name}, 
				fields=["name", "is_active"])
			
			for child in child_enterprises:
				if not self.is_active and child.is_active:
					frappe.db.set_value("Enterprise", child.name, "is_active", 0)
					frappe.msgprint(_("Child Enterprise '{0}' has been deactivated").format(child.name))
	
	def update_related_documents(self):
		"""Update related documents when enterprise changes"""
		# Update SBUs if enterprise is deactivated
		if self.has_value_changed("is_active") and not self.is_active:
			sbus = frappe.get_all("Strategic Business Unit", 
				filters={"enterprise": self.name, "is_active": 1}, 
				fields=["name"])
			
			for sbu in sbus:
				frappe.db.set_value("Strategic Business Unit", sbu.name, "is_active", 0)
				frappe.msgprint(_("SBU '{0}' has been deactivated").format(sbu.name))
	
	def on_trash(self):
		"""Actions before enterprise is deleted"""
		self.check_dependencies()
	
	def check_dependencies(self):
		"""Check for dependencies before deletion"""
		# Check for child enterprises
		child_enterprises = frappe.db.count("Enterprise", {"parent_enterprise": self.name})
		if child_enterprises > 0:
			frappe.throw(_("Cannot delete Enterprise '{0}' as it has {1} child enterprise(s)").format(
				self.name, child_enterprises))
		
		# Check for associated SBUs
		sbu_count = frappe.db.count("Strategic Business Unit", {"enterprise": self.name})
		if sbu_count > 0:
			frappe.throw(_("Cannot delete Enterprise '{0}' as it has {1} associated SBU(s)").format(
				self.name, sbu_count))
		
		# Check for associated Factory Business Units
		factory_count = frappe.db.count("Factory Business Unit", {"enterprise": self.name})
		if factory_count > 0:
			frappe.throw(_("Cannot delete Enterprise '{0}' as it has {1} associated Factory Business Unit(s)").format(
				self.name, factory_count))
		
		# Check for associated Liaison Offices
		liaison_count = frappe.db.count("Liaison Office", {"enterprise": self.name})
		if liaison_count > 0:
			frappe.throw(_("Cannot delete Enterprise '{0}' as it has {1} associated Liaison Office(s)").format(
				self.name, liaison_count))
