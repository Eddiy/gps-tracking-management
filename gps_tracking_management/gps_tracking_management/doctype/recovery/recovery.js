// Copyright (c) 2017,  Bituls Company Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Recovery', {
    onload: function (frm) {

     },

    validate: function (frm) {
        if (!frm.doc.microfinance_contact && frm.doc.status == 'Request Confirmed') {
            frappe.msgprint(__(frm.doc.workflow_state))
            frappe.msgprint(__('You must select the microfinance representative'))
            validated = false
            return
        }
        if (!frm.doc.request_was_sent && frm.doc.status == 'Request Confirmed') {
            frappe.msgprint(__('You must select if the recovery request was made or not.'))
            validated = false // eslint-disable-line no-undef
            return
        }
        if (!frm.doc.vehicle_recovered && frm.doc.status == 'Recovery Closed') {
            frappe.msgprint(__('You must select if the vehicle has been recovered or not.'))
            validated = false // eslint-disable-line no-undef
            return
        }

    }

})
