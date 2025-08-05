# Copyright (c) 2025, CognitionXLogic and contributors
# For license information, please see license.txt

"""
Desktop configuration for TenantX
"""

from frappe import _

def get_data():
	return [
		{
			"module_name": "TenantX",
			"color": "grey",
			"icon": "octicon octicon-file-directory",
			"type": "module",
			"label": _("TenantX")
		}
	] 