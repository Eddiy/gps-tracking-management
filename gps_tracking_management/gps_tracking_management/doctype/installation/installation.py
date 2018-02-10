# -*- coding: utf-8 -*-
# Copyright (c) 2017,  Bituls Company Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe.model.document import Document


class Installation(Document):
    pass


@frappe.whitelist()
def get_warehouse(name):
    technician = frappe.db.get_value("Employee", name, "employee_name")
    warehouse = frappe.db.get_value(
        "Warehouse", {"warehouse_name": technician})
    return warehouse
