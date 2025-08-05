app_name = "tenantx"
app_title = "TenantX"
app_publisher = "CognitionXLogic"
app_description = "Manage multi level companies and warehouses with super ease"
app_email = "meghwin@cognitionx.tech"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "tenantx",
# 		"logo": "/assets/tenantx/logo.png",
# 		"title": "TenantX",
# 		"route": "/tenantx",
# 		"has_permission": "tenantx.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/tenantx/css/tenantx.css"
# app_include_js = "/assets/tenantx/js/tenantx.js"

# include js, css files in header of web template
# web_include_css = "/assets/tenantx/css/tenantx.css"
# web_include_js = "/assets/tenantx/js/tenantx.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "tenantx/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"User" : "public/js/user.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "tenantx/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "tenantx.utils.jinja_methods",
# 	"filters": "tenantx.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "tenantx.install.before_install"
# after_install = "tenantx.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "tenantx.uninstall.before_uninstall"
# after_uninstall = "tenantx.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "tenantx.utils.before_app_install"
# after_app_install = "tenantx.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "tenantx.utils.before_app_uninstall"
# after_app_uninstall = "tenantx.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "tenantx.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
	"Factory Business Unit": "tenantx.tenantx.doctype.factory_business_unit.factory_business_unit.get_permission_query_conditions",
	"Strategic Business Unit": "tenantx.tenantx.doctype.strategic_business_unit.strategic_business_unit.get_permission_query_conditions",
	"Purchase Order": "tenantx.tenantx.permission_queries.get_permission_query_conditions_for_purchase_order",
	"Sales Invoice": "tenantx.tenantx.permission_queries.get_permission_query_conditions_for_sales_invoice",
	"Purchase Invoice": "tenantx.tenantx.permission_queries.get_permission_query_conditions_for_purchase_invoice",
	"Sales Order": "tenantx.tenantx.permission_queries.get_permission_query_conditions_for_sales_order",
	"Delivery Note": "tenantx.tenantx.permission_queries.get_permission_query_conditions_for_delivery_note",
	"Purchase Receipt": "tenantx.tenantx.permission_queries.get_permission_query_conditions_for_purchase_receipt",
	"Journal Entry": "tenantx.tenantx.permission_queries.get_permission_query_conditions_for_journal_entry",
}

# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"User": {
		"on_update": "tenantx.tenantx.doc_events.user.on_update",
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"tenantx.tasks.all"
# 	],
# 	"daily": [
# 		"tenantx.tasks.daily"
# 	],
# 	"hourly": [
# 		"tenantx.tasks.hourly"
# 	],
# 	"weekly": [
# 		"tenantx.tasks.weekly"
# 	],
# 	"monthly": [
# 		"tenantx.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "tenantx.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "tenantx.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "tenantx.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["tenantx.utils.before_request"]
# after_request = ["tenantx.utils.after_request"]

# Job Events
# ----------
# before_job = ["tenantx.utils.before_job"]
# after_job = ["tenantx.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"tenantx.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Fixtures
# ----------
# Fixtures are used to export/import data that should be shared across sites
fixtures = [
	{
		"doctype": "Property Setter",
		"filters": [["module", "=", "TenantX"]]
	},
	{
		"doctype": "Custom Field",
		"filters": [["module", "=", "TenantX"]]
	}
]