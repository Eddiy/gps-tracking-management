from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import flt, fmt_money, today


def make_warehouse(doc, method):
    """Create a warehouse when a new Employee(technician is created)  is added"""
    if doc.is_technician:
        warehouse = frappe.get_doc({
            "doctype": "Warehouse",
            "warehouse_name": doc.employee_name,
            "email_id": doc.personal_email,
            "mobile_no": doc.cell_number
        })
        # the System Manager might not have permission to create a Meeting
        warehouse.flags.ignore_permissions = True
        warehouse.insert()

        frappe.msgprint(_("Warehouse created for this technician"))


def make_warehouse_for_customer(doc, method):
    """make a warehouse when a a new customer is created"""
    warehouse = frappe.get_doc({
        "doctype": "Warehouse",
        "warehouse_name": doc.customer_name
    })
    warehouse.flags.ignore_permissions = True
    warehouse.insert()
    doc.set('warehouse', warehouse.name)
    frappe.msgprint(_("Warehouse created for this customer"))
