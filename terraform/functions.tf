
provider "oci" {
  tenancy_ocid     = var.tenancy_ocid
  region           = var.region
}

# Terraform will take 5 minutes after destroying an application due to a known service issue.
# please refer: https://docs.cloud.oracle.com/iaas/Content/Functions/Tasks/functionsdeleting.htm
resource "oci_functions_application" "cybereason-responder" {
  #Required
  compartment_id = var.function_compartment_ocid
  display_name   = "cybereason-responder"
  subnet_ids     =  [var.function_subnet]
}

data "oci_core_subnet" "test_subnet" {
    #Required
    subnet_id = var.function_subnet
}

resource "oci_functions_function" "cybereason_responder_function" {
  #Required
  application_id = oci_functions_application.cybereason-responder.id
  display_name   = "cybereason-responder-function"
  image          = var.function_image
  memory_in_mbs  = "128"

  config = {
    "CYBEREASON_SERVER" = var.cybereason_server
    "CYBEREASON_PORT" = var.cybereason_port
    "CYBEREASON_USERNAME" = var.cybereason_username
    "CYBEREASON_SECRET_OCID" = var.cybereason_secret_ocid
    "SEND_NOTIFICATIONS" = var.cybereason_send_notifications
    "ONS_TOPIC_OCID" = var.cybereason_ons_topic_ocid
    "ISOLATE_MACHINE" = var.cybereason_isolate_machine
    "DISABLE_USER" = var.cybereason_disable_user
    "NEVER_DISABLE_USERS": var.oci_never_disable_users
  }
  image_digest       = var.function_image_digest
  timeout_in_seconds = "60"
}
