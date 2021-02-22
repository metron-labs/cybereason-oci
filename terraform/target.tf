resource oci_cloud_guard_target target_root {
  compartment_id = var.tenancy_ocid
  display_name = "cybereason-responder-target"
  target_detector_recipes {
    detector_recipe_id = var.target_configuration_detector_recipe_ocid
  }
  target_detector_recipes {
    detector_recipe_id = var.target_activity_detector_recipe_ocid
  }
  target_resource_id   = var.tenancy_ocid
  target_resource_type = "COMPARTMENT"
  target_responder_recipes {
    responder_recipe_id = var.target_responder_recipe_ocid
  }
}
