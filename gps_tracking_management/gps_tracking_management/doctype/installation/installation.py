# -*- coding: utf-8 -*-
# Copyright (c) 2017,  Bituls Company Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, cstr, nowdate, nowtime


class Installation(Document):
    pass


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

    t_warehouse = frappe.db.get_value(
        "Warehouse", {"warehouse_name": t_warehouse})
    s_warehouse = frappe.db.get_value(
        "Warehouse", {"warehouse_name": s_warehouse})
    tracker_entry.append("items",
                         {"item_code": tracker,
                          "t_warehouse": t_warehouse,
                          "s_warehouse": s_warehouse,
                          "serial_no": serial,
                          "qty": 1.000,
                          "uom": "Nos",
                          "conversion_factor": 1.000000,
                          "stock_uom": "Nos",
                          "transfer_qty": 1})
    sim_entry.append("items",
                     {"item_code": sim_card,
                      "t_warehouse": t_warehouse,
                      "s_warehouse": s_warehouse,
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
def get_warehouse(name):
    technician = frappe.db.get_value("Employee", name, "employee_name")
    warehouse = frappe.db.get_value(
        "Warehouse", {"warehouse_name": technician})
    return warehouse


@frappe.whitelist()
def close_communication(communication):
    ("Communication", communication, "status", "Closed")
