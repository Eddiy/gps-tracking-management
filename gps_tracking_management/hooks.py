# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from frappe import _, msgprint, throw

app_name = "gps_tracking_management"
app_title = "GPS Tracking Management"
app_publisher = "Bituls Company Limited"
app_description = "App for Managing GPS Tracking Activities"
app_icon = "icon-book"
app_color = "#589494"
app_email = "info@bituls.com"
app_url = "https://frappe.io/apps/gps_tracking_management"
app_version = "0.0.1"


# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/library_management/css/library_management.css"
# app_include_js = "/assets/library_management/js/library_management.js"

# include js, css files in header of web template
# web_include_css = "/assets/library_management/css/library_management.css"
# web_include_js = "/assets/library_management/js/library_management.js"

# Installation
# ------------

# before_install = "library_management.install.before_install"
after_install = "gps_tracking_management.gps_tracking_management.hooks.doc_hooks.create_default_warehouses"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "library_management.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.core.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.core.doctype.event.event.has_permission",
# }
fixtures = ["Custom Field", "Workflow State", "Workflow Action", "Workflow"]
# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

doc_events = {
    "Employee": {
        "before_insert": "gps_tracking_management.gps_tracking_management.hooks.doc_hooks.make_warehouse"
        #"before_cancel": "property.property_management.hooks.doc_hooks.sales_invoice_cancel"
    },
    "Customer": {
        "before_insert": "gps_tracking_management.gps_tracking_management.hooks.doc_hooks.make_warehouse_for_customer"
    }
}


# Scheduled Tasks
# ---------------


# scheduler_events = {
# 	"all": [
# 		"library_management.tasks.all"
# 	],
# 	"daily": [
# 		"library_management.tasks.daily"
# 	],
# 	"hourly": [
# 		"library_management.tasks.hourly"
# 	],
# 	"weekly": [
# 		"library_management.tasks.weekly"
# 	]
# 	"monthly": [
# 		"library_management.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "library_management.install.before_tests"
