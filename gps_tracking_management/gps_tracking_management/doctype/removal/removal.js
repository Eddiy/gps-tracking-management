// Copyright (c) 2017,  Bituls Company Limited and contributors
// For license information, please see license.txt
cur_frm.add_fetch()
cur_frm.fields_dict['installation'].get_query = function(doc, cdt, cdn) {
  return {
    filters:{"status": 'Installation Closed'
    }
  }
}
frappe.ui.form.on('Removal', {
	onload: function(frm) {

	},
	refresh: function(frm) {

	},
	validate: function(frm) {
		if (!frm.doc.technician && frm.doc.status=="Technician Assigned") {
			msgprint(__("You must select the technisian to assign removal"));
			validated = false;
			return
		}
		if (!frm.doc.verify_sim_card && frm.doc.status=="Removal Completed") {
			msgprint(__("You must verify the removed sim card"));
			validated = false;
			return
		}
		if (!frm.doc.verify_device && frm.doc.status=="Removal Completed") {
			msgprint(__("You must verify the removed device"));
			validated = false;
			return
		}


		if(!frm.doc.removal_certificate && frm.doc.status=="Removal Closed"){
			msgprint(__("You must upload removal certificate"));
			validated = false;
			return
		}
	},
	on_submit: function(frm) {
		if(frm.doc.status=="Removal Completed"){

            frappe.call({
                method:"gps_tracking_management.gps_tracking_management.doctype.removal.removal.transfer_device",
                args: {
                  'parent': 'Stock Entry',
                  'serial': frm.doc.device,
                  't_warehouse': frm.doc.technician_name,
                  's_warehouse': frm.doc.client,
                  'company': frm.doc.company,
                  'sim_no': frm.doc.sim_card
                },
                callback: function(r) {
                  if (!r.exc) {
                    msgprint(__("You getting somewhere"));
                  }
                }


            });


              validated= true;
              return
        }
	}


});
