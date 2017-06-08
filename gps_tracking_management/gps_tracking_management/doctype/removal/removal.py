# -*- coding: utf-8 -*-
# Copyright (c) 2017,  Bituls Company Limited and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, cstr, nowdate, nowtime

class Removal(Document):
	pass
@frappe.whitelist()
def transfer_device(parent, serial, t_warehouse, s_warehouse, company, sim_no):
    device_entry = frappe.get_doc({
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
    frappe.msgprint(_(s_warehouse))
    t_warehouse = frappe.db.get_value("Warehouse", {"warehouse_name": t_warehouse})
    s_warehouse = frappe.db.get_value("Warehouse", {"warehouse_name": s_warehouse})

    device_entry.append("items", {"item_code": "Tracker", "t_warehouse": t_warehouse, "s_warehouse": s_warehouse, "serial_no":serial,  "qty": 1.000, "uom": "Nos", "conversion_factor":  1.000000 , "stock_uom": "Nos",   "transfer_qty": 1 })
    sim_entry.append("items", {"item_code": "Tracker", "t_warehouse": t_warehouse, "s_warehouse": s_warehouse, "serial_no":sim_no,  "qty": 1.000, "uom": "Nos", "conversion_factor":  1.000000 , "stock_uom": "Nos",   "transfer_qty": 1 })

    device_entry.insert()
    device_entry.submit()
    frappe.msgprint(_("Device transferred"))
    sim_entry.insert()
    sim_entry.submit()
    frappe.msgprint(_("Sim Card transferred"))