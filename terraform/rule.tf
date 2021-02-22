
resource oci_events_rule cr_event_rule {
  actions {
    actions {
      action_type = "FAAS"
      function_id = oci_functions_function.cybereason_responder_function.id
      is_enabled  = "true"
    }
  }
  compartment_id = var.tenancy_ocid
  condition      = "{\"eventType\":[\"com.oraclecloud.cloudguard.problemdetected\" ],\"data\":{}}"
  
  description  = "Rules to fire Cybereason Responder FAAS on Oracle Cloud Guard events"
  display_name = "cybereason-responder-rules"
  
  is_enabled = "true"
}
