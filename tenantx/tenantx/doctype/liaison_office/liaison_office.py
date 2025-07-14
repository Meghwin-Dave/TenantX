# Copyright (c) 2025, CognitionXLogic and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _
import re


class LiaisonOffice(Document):
	def validate(self):
		"""Validate liaison office data before saving"""
		self.validate_office_code()
		self.validate_enterprise_association()
		self.validate_country()
		self.validate_liaison_head()
		self.validate_contact_address()
	
	def validate_office_code(self):
		"""Validate office code format and uniqueness"""
		if self.office_code:
			# Check for alphanumeric format
			if not re.match(r'^[A-Z0-9\-_]+$', self.office_code):
				frappe.throw(_("Office Code must contain only uppercase letters, numbers, hyphens, and underscores"))
			
			# Check for minimum length
			if len(self.office_code) < 3:
				frappe.throw(_("Office Code must be at least 3 characters long"))
			
			# Check for maximum length
			if len(self.office_code) > 20:
				frappe.throw(_("Office Code cannot exceed 20 characters"))
			
			# Check for uniqueness
			existing = frappe.db.exists("Liaison Office", {
				"office_code": self.office_code,
				"name": ["!=", self.name]
			})
			if existing:
				frappe.throw(_("Office Code '{0}' already exists").format(self.office_code))
	
	def validate_enterprise_association(self):
		"""Validate enterprise association"""
		if self.enterprise:
			# Check if enterprise exists and is active
			enterprise = frappe.get_doc("Enterprise", self.enterprise)
			if not enterprise.is_active:
				frappe.throw(_("Enterprise '{0}' is not active").format(self.enterprise))
		
			# Check for duplicate liaison offices in the same country for the same enterprise
			if self.country:
				existing_office = frappe.db.exists("Liaison Office", {
					"enterprise": self.enterprise,
					"country": self.country,
					"name": ["!=", self.name]
				})
				if existing_office:
					frappe.throw(_("Liaison Office already exists for Enterprise '{0}' in Country '{1}'").format(
						self.enterprise, self.country))
	
	def validate_country(self):
		"""Validate country association"""
		if self.country:
			# Check if country exists
			if not frappe.db.exists("Country", self.country):
				frappe.throw(_("Country '{0}' does not exist").format(self.country))
			
	
	def validate_liaison_head(self):
		"""Validate liaison head assignment"""
		if self.liaison_head:
			# Check if employee exists
			if not frappe.db.exists("Employee", self.liaison_head):
				frappe.throw(_("Employee '{0}' does not exist").format(self.liaison_head))
			
			# Check if employee is active
			employee = frappe.get_doc("Employee", self.liaison_head)
			if employee.status != "Active":
				frappe.throw(_("Liaison Head '{0}' is not an active employee").format(self.liaison_head))
			
			# Check if employee is already assigned to another liaison office
			existing_assignment = frappe.db.exists("Liaison Office", {
				"liaison_head": self.liaison_head,
				"name": ["!=", self.name],
				"is_active": 1
			})
			if existing_assignment:
				frappe.msgprint(_("Employee '{0}' is already assigned to another active liaison office").format(
					self.liaison_head), alert=True)
	
	def validate_contact_address(self):
		"""Validate contact and address information"""
		if self.contact:
			if not frappe.db.exists("Contact", self.contact):
				frappe.throw(_("Contact '{0}' does not exist").format(self.contact))
		
		if self.address:
			if not frappe.db.exists("Address", self.address):
				frappe.throw(_("Address '{0}' does not exist").format(self.address))
			
			# Check if address country matches liaison office country
			if self.country:
				address = frappe.get_doc("Address", self.address)
				if address.country and address.country != self.country:
					frappe.msgprint(_("Address country '{0}' does not match liaison office country '{1}'").format(
						address.country, self.country), alert=True)
	
	def on_update(self):
		"""Actions after liaison office is updated"""
		self.update_related_documents()
	
	def update_related_documents(self):
		"""Update related documents when liaison office changes"""
		# Update employee assignments if liaison office is deactivated
		if self.has_value_changed("is_active") and not self.is_active:
			if self.liaison_head:
				frappe.msgprint(_("Liaison Head '{0}' assignment has been deactivated").format(self.liaison_head))
	
	def on_trash(self):
		"""Actions before liaison office is deleted"""
		self.check_dependencies()
	
	def check_dependencies(self):
		"""Check for dependencies before deletion"""
		# Check for active liaison head assignment
		if self.liaison_head:
			frappe.msgprint(_("Liaison Head '{0}' assignment will be removed").format(self.liaison_head), alert=True)
	
	def before_insert(self):
		"""Actions before liaison office is inserted"""
		self.set_default_values()
	
	def set_default_values(self):
		"""Set default values for new liaison office"""
		if not self.is_active:
			self.is_active = 1
	
	def after_insert(self):
		"""Actions after liaison office is inserted"""
		self.create_default_contact_address()
	
	def create_default_contact_address(self):
		"""Create default contact and address if not provided"""
		if not self.contact and self.liaison_head:
			# Create contact from employee
			employee = frappe.get_doc("Employee", self.liaison_head)
			if employee.user_id:
				contact = frappe.get_doc({
					"doctype": "Contact",
					"first_name": employee.first_name or employee.employee_name,
					"last_name": employee.last_name or "",
					"user": employee.user_id,
					"is_primary_contact": 1
				})
				contact.insert(ignore_permissions=True)
				self.contact = contact.name
				self.save()
