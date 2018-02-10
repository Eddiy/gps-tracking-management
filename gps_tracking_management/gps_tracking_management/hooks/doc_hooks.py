from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.utils import nowdate


def create_default_warehouses():
    company = get_company("Company")
    if company:
        name = company[0].name
        abbr = company[0].abbr
        for wh_detail in [
            {"warehouse_name": _("All Warehouses"), "is_group": 1},
            {"warehouse_name": _(
                "Micro Finance Installations"),
                "is_group": 1},
            {"warehouse_name": _(name + " Installations"), "is_group": 1},
            {"warehouse_name": _(name + " Technicians"), "is_group": 1},
            {"warehouse_name": _(name + " Stores"), "is_group": 0}]:

            if not frappe.db.exists("Warehouse", "{0} - {1}".format(wh_detail["warehouse_name"], abbr)):
                warehouse = frappe.get_doc({
                    "doctype": "Warehouse",
                    "warehouse_name": wh_detail["warehouse_name"],
                    "is_group": wh_detail["is_group"],
                    "company": name,
                    "parent_warehouse":
                        "{0} - {1}".format(_("All Warehouses"), abbr)
                        if not wh_detail["warehouse_name"] == "All Warehouses" else ""
                })
                warehouse.flags.ignore_permissions = True
                warehouse.insert()


def create_defaults(doc, method):
    name = doc.company_name
    abbr = doc.abbr

    for wh_detail in [
        {"warehouse_name": _("All Warehouses"), "is_group": 1},
        {"warehouse_name": _(
            "Micro Finance Installations"),
            "is_group": 1},
        {"warehouse_name": _(name + " Installations"), "is_group": 1},
        {"warehouse_name": _(name + " Technicians"), "is_group": 1},
        {"warehouse_name": _(name + " Stores"), "is_group": 0}]:

        if not frappe.db.exists("Warehouse", "{0} - {1}".format(wh_detail["warehouse_name"], abbr)):
            warehouse = frappe.get_doc({
                "doctype": "Warehouse",
                "warehouse_name": wh_detail["warehouse_name"],
                "is_group": wh_detail["is_group"],
                "company": name,
                "parent_warehouse":
                    "{0} - {1}".format(_("All Warehouses"), abbr)
                    if not wh_detail["warehouse_name"] == "All Warehouses" else ""
            })
            warehouse.flags.ignore_permissions = True
            warehouse.insert()

        # else:
        #     frappe.throw(_("Cannot continue"))


def make_warehouse(doc, method):
    company = get_company("Company")

    name = company[0].name
    abbr = company[0].abbr

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
    else:
        if doc.customer_group == "Bituls Tracking":
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


def get_company(doc):
    company_details = frappe.get_all(doc, fields=["name", "abbr"])
    if company_details:
        return company_details


def create_customer_group():
    customer_g = "Bituls Tracking"

    if not frappe.db.exists("Customer Group", customer_g):
        customer_group = frappe.get_doc({
            "doctype": "Customer Group",
            "customer_group_name": "Bituls Tracking",
            "parent_customer_group": "All Customer Groups",
            "is_group": 0
        })
        customer_group.flags.ignore_permissions = True
        customer_group.insert()


def create_customer_g():
    for c_detail in [
        {"customer_group_name": _("All Customer Groups"), "is_group": 1},
        {"customer_group_name": _("Bituls Tracking"), "is_group": 0}]:

        if not frappe.db.exists("Customer Group", c_detail["customer_group_name"]):
            customer_group = frappe.get_doc({
                "doctype": "Customer Group",
                "customer_group_name": c_detail["customer_group_name"],
                "is_group": c_detail["is_group"],
                "parent_customer_group": "All Customer Groups"
                if not c_detail["customer_group_name"] == "All Customer Groups" else ""

            })
            customer_group.flags.ignore_permissions = True
            customer_group.insert()


def set_installation(doc, method):
    frappe.db.set_value("Communication", doc.communication, "installation", doc.name)


def set_removal(doc, method):
    frappe.db.set_value("Communication", doc.communication, "removal", doc.name)


@frappe.whitelist()
def transfer_device(parent, serial, t_warehouse, s_warehouse, company, sim_no, tracker, sim_card):
    tracker_entry = frappe.get_doc({
        "doctype": parent,
        "posting_date": nowdate(),
        "purpose": "Material Transfer",
        "company": company
    })
    sim_entry = frappe.get_doc({
        "doctype": parent,
        "posting_date": nowdate(),
        "purpose": "Material Transfer",
        "company": company
    })

    tg_warehouse = frappe.db.get_value(
        "Warehouse", {"warehouse_name": t_warehouse})
    sr_warehouse = frappe.db.get_value(
        "Warehouse", {"warehouse_name": s_warehouse})
    tracker_entry.append("items",
                         {"item_code": tracker,
                          "t_warehouse": tg_warehouse,
                          "s_warehouse": sr_warehouse,
                          "serial_no": serial,
                          "qty": 1.000,
                          "uom": "Nos",
                          "conversion_factor": 1.000000,
                          "stock_uom": "Nos",
                          "transfer_qty": 1})
    sim_entry.append("items",
                     {"item_code": sim_card,
                      "t_warehouse": tg_warehouse,
                      "s_warehouse": sr_warehouse,
                      "serial_no": sim_no,
                      "qty": 1.000,
                      "uom": "Nos",
                      "conversion_factor": 1.000000,
                      "stock_uom": "Nos",
                      "transfer_qty": 1})
    tracker_entry.insert()
    tracker_entry.submit()
    frappe.msgprint(_("Device transferred"))
    sim_entry.insert()
    sim_entry.submit()
    frappe.msgprint(_("Sim card transferred"))


@frappe.whitelist()
def close_communication(communication):
    frappe.db.set_value("Communication", communication, "status", "Closed")
