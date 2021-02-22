##### variables.tf #####
# This file contains all the variables that you will need to configure the
# Cybereason - Oracle Cloud Guard integration.
# Edit the variables to correspond to your Oracle Cloud tenant.

# The Oracle Tenancy (leave blank if you want Oracle Cloud to pre-populate it with your existing tenancy)
variable tenancy_ocid {
  description = "Enter the OCID of your Oracle Cloud Tenancy. Leave blank to pre-populate it with your existing tenancy."
}

# The Oracle Region (leave blank if you want Oracle Cloud to pre-populate it with your existing region)
variable region {
  description = "Enter the region of your Oracle Cloud Tenancy. Leave blank to pre-populate it with your default region."
}

# The Oracle Compartment where we have installed the Cybereason Responder function
variable function_compartment_ocid {
  description = "Enter the OCID of the compartment of your Oracle Cloud Tenancy where you have installed the Cybereason Responder function."
}

# Set the options required to configure the Cybereason Responder function
variable cybereason_server {
  description = "The Cybereason console to connect to (e.g. integration.cybereason.net)"
  default = "integration.cybereason.net"
}
variable cybereason_port {
  description = "The port used to connect to the Cybereason console. Default is 8443"
  default = "8443"
}
variable cybereason_username {
  description = "The username used to access the Cybereason console"
  default = "parag@metronlabs.io"
}
variable cybereason_secret_ocid {
  description = "The OCID of the Secret containing the password used to access the Cybereason server"
  default = "ocid1.vaultsecret.oc1.ap-mumbai-1.amaaaaaatca7veya5f5o3w52tbblxwkb7nsbkytz3aurfpakq5obuihtthbq"
}
variable cybereason_send_notifications {
  default = "True"
  description = "If True, then the Cybereason Responder will send notifications to a specified ONS topic"
}
variable cybereason_ons_topic_ocid {
  description = "The OCID of ONS Topic where we will send notifications"
}
variable cybereason_isolate_machine {
  default = "False"
  description = "If True, any machine flagged as suspicious will be isolated via the Cybereason sensor"
}
variable cybereason_disable_user {
  default = "False"
  description = "If True, any user that is flagged as suspicious in the Cybereason console will be disabled in Oracle"
}

# The Cybereason Responder function image contains code to run the query and remediation actions. You will need to
# first get the function installed and accessible in the compartment where you are going to apply the
# Terraform configuration. Once this is done, put the function_image OCID and the function_image_digest below.
variable function_subnet {
  description = "The VCN Subnet OCID of the subnet the function will execute in"
}

variable function_image {
  description = "The function image that contains the Cybereason Responder code"
}

variable function_image_digest {
  description = "The digest of the function image of the Cybereason Responder code. This is of the format sha256:xxx"
}

# Variables for the Target Configuration/Activity Detector and Responder recipes
variable target_configuration_detector_recipe_ocid {
  description = "The OCID of the Target Configuration Detector Recipe to be used"
}

variable target_activity_detector_recipe_ocid {
  description = "The OCID of the Target Activity Detector Recipe to be used"
}

variable target_responder_recipe_ocid {
  description = "The OCID of the Target Responder Recipe to be used"
}