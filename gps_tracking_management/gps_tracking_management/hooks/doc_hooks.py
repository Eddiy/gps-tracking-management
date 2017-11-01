from __future__ import unicode_literals

import frappe
from frappe import _


def make_warehouse(doc, method):
    name, abbr = get_company()

    if doc.doctype == "Employee":
        if doc.is_technician:
            warehouse = frappe.get_doc({
                "doctype": "Warehouse",
                "warehouse_name": doc.employee_name,
                "email_id": doc.personal_email,
                "mobile_no": doc.cell_number,
                "parent_warehouse": "{0} - {1}".format(
                    _(name + " Technicians"),
                    abbr)
            })
            # The System Manager might not have permission to create a
            # Meeting
            warehouse.flags.ignore_permissions = True
            warehouse.insert()
            frappe.msgprint(_("Warehouse created for this technician"))
    else:
        if doc.customer_type == "Company":
            warehouse = frappe.get_doc({
                "doctype": "Warehouse",
                "warehouse_name": doc.customer_name,
                "parent_warehouse": "{0} - {1}".format(
                    _("Micro Finance Installations"), abbr)
            })
            warehouse.flags.ignore_permissions = True
            warehouse.insert()
            doc.set('warehouse', warehouse.name)
        else:
            warehouse = frappe.get_doc({
                "doctype": "Warehouse",
                "warehouse_name": doc.customer_name,
                "parent_warehouse": "{0} - {1}".format(
                    _(name + " Installations"),
                    abbr)
            })
            warehouse.flags.ignore_permissions = True
            warehouse.insert()
            doc.set('warehouse', warehouse.name)
        frappe.msgprint(_("Warehouse created for this customer"))


def create_default_warehouses():
    name, abbr = get_company()

    for wh_detail in [
        {"warehouse_name": _("Micro Finance Installations"), "is_group": 1},
        {"warehouse_name": _(name + " Installations"), "is_group": 1},
        {"warehouse_name": _(name + " Technicians"), "is_group": 1},
            {"warehouse_name": _(name + " Stores"), "is_group": 0}]:

        if not frappe.db.exists("Warehouse",
                                "{0} - {1}".format(wh_detail[
                                    "warehouse_name"],
                                    abbr)):
            stock_group = frappe.db.get_value("Account",
                                              {"account_type": "Stock",
                                               "is_group": 1,
                                               "company": name})
            if stock_group:
                warehouse = frappe.get_doc({
                    "doctype": "Warehouse",
                    "warehouse_name": wh_detail["warehouse_name"],
                    "is_group": wh_detail["is_group"],
                    "company": name,
                    "parent_warehouse": "{0} - {1}".format(_("All "
                                                             "Warehouses"),
                                                           abbr)
                })
                warehouse.flags.ignore_permissions = True
                warehouse.insert()


def get_company():
    company = frappe.get_all("Company", fields=["name", "abbr"])
    for values in company:
        name = values.name
        abbr = values.abbr
    return name, abbr
