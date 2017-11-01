// Copyright (c) 2017,  Bituls Company Limited and contributors
// For license information, please see license.txt
cur_frm.add_fetch()
var warehouse;

cur_frm.fields_dict['device_serial'].get_query = function (doc, cdt, cdn) {
   return {
        filters: {
            'warehouse' : warehouse,
            'item_name': "Tracker"
        }
    }
}
cur_frm.fields_dict['sim_card'].get_query = function(doc, cdt, cdn) {
   return {
       filters:{
               'warehouse': warehouse,
               'item_name': "GSM"
       }
      }
}


frappe.ui.form.on('Installation', {
  onload: function(frm) {

  },
  get_warehouse: function(frm){
     frappe.call({
                 method:"gps_tracking_management.gps_tracking_management.doctype.installation.installation.get_warehouse",
                 args: {
                   'name': doc.client
                 },
                 callback: function(r) {
                     warehouse=r;

                 }


               });
  },
  refresh: function(frm) {

  },

  validate: function(frm) {

    if (frm.doc.vehicle && frm.doc.status=="New") {
      frm.set_value("verified_license_plate", frm.doc.vehicle);
    }
    if(!frm.doc.customer_name && frm.doc.status=="Customer Contacted"){
      msgprint(_(frm.doc.workflow_state))
      msgprint(__("You must select the custmer to be contacted"));
      validated = false;
      return
    }
    if(!frm.doc.in_office && frm.doc.status=="Customer Contacted"){
      msgprint(__("You must select if the installation will be done in office or not"));
      validated = false;
      return
    }
    if(!frm.doc.installation_location && frm.doc.in_office=="No" && frm.doc.status=="Customer Contacted")
    {
      msgprint(__("You must enter the out of office installation location"));
      validated = false;
      return
    }
    if (frm.doc.in_office=="Yes") {
      frm.set_value("verified_location", "Bituls Parking")
    }
    else{
      frm.set_value("verified_location", frm.doc.installation_location)

    }
    if(!frm.doc.technician && frm.doc.status=="Technician Assigned"){
      msgprint(__("You must select the technician"));
      validated = false;
      return
    }
    if(!frm.doc.verify_license_plate && frm.doc.status=="Installation Complete"){
      msgprint(__("You must verify vehicle's license plate"));
      validated = false;
      return
    }
    if(!frm.doc.verify_location && frm.doc.status=="Installation Complete"){
      msgprint(__("You must verify installation location"));
      validated = false;
      return
    }
    if(!frm.doc.verified_location && frm.doc.status=="Installation Complete"){
      msgprint(__("You must verify installation location"));
      validated = false;
      return
    }
    if(!frm.doc.ignition_status && frm.doc.status=="Installation Complete"){
      msgprint(__("You must select the ignition status of the installation"));
      validated = false;
      return
    }


    if(!frm.doc.device_reflecting && frm.doc.status=="Installation Verified"){
      msgprint(__("You must select if device is reflecting or not"));
      validated = false;
      return
    }
    if(!frm.doc.installation_certificate && frm.doc.status=="Certificate Issued"){
      msgprint(__("You must upload installation certificate"));
      validated = false;
      return
    }
    if(!frm.doc.front_licence_plate && frm.doc.status=="Installation Closed"){
      msgprint(__("You must upload the front licence plate photo"));
      validated = false;
      return
    }
    if(!frm.doc.rear_licence_plate && frm.doc.status=="Installation Closed"){
      msgprint(__("You must upload the rear licence plate photo"));
      validated = false;
      return
    }
    if(!frm.doc.installation_location_photo && frm.doc.status=="Installation Closed"){
      msgprint(__("You must upload the photo of where device is installed in the car"));
      validated = false;
      return
    }

  },
  in_office: function(frm) {

    if(!frm.doc.in_office){
      msgprint(__("You must select if the installation will be done in office or not"));
      validated = false;
      return
    }
  },
  on_submit: function(frm) {


  },
  refresh: function(frm){

    if(frm.doc.technician){
        frappe.call({
                   method:"gps_tracking_management.gps_tracking_management.doctype.installation.installation.get_warehouse",
                   args: {
                     'name': frm.doc.technician

                   },
                   callback: function(r) {
                       warehouse=r.message;


                   }


        });
    }


  },
  status: function(frm){

           if(frm.doc.workflow_state=="Installation Complete"){
             frappe.call({
               method:"gps_tracking_management.gps_tracking_management.doctype.installation.installation.transfer_device",
               args: {
                 'parent': 'Stock Entry',
                 'serial': frm.doc.device_serial,
                 't_warehouse': frm.doc.client,
                 's_warehouse': frm.doc.technician_name,
                 'company': frm.doc.company,
                 'sim_no':frm.doc.sim_card
               },
               callback: function(r) {
                 if (!r.exc) {

                 }
               }


             });
           }

  }

});
