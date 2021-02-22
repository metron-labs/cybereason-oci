/*
 * Policies for dynamic groups
 */
resource "oci_identity_policy" "OCI-CR-policy-1" {
  name           = "OCI-CR-policy"
  description    = "Policy to enable FAAS for Cybereason Responder"
  compartment_id = var.tenancy_ocid

  statements = [
    "Allow service FAAS to read repos in tenancy",
    "Allow service FAAS to use virtual-network-family in tenancy",
    "Allow dynamic-group ${oci_identity_dynamic_group.cr-functions-group-1.name} to read virtual-network-family in tenancy",
    "Allow dynamic-group ${oci_identity_dynamic_group.cr-functions-group-1.name} to read instance-family in tenancy",
    "Allow dynamic-group ${oci_identity_dynamic_group.cr-functions-group-1.name} to use secret-family in tenancy",
    "Allow dynamic-group ${oci_identity_dynamic_group.cr-functions-group-1.name} to use ons-topics in tenancy",
    "Allow dynamic-group ${oci_identity_dynamic_group.cr-functions-group-1.name} to manage cloud-guard-problems in tenancy",
    "Allow dynamic-group ${oci_identity_dynamic_group.cr-functions-group-1.name} to read database-family in tenancy"
  ]
}

data "oci_identity_policies" "dynamic-policies-1" {
  compartment_id = var.tenancy_ocid

  filter {
    name   = "id"
    values = [oci_identity_policy.OCI-CR-policy-1.id]
  }
}

output "dynamicPolicies" {
  value = data.oci_identity_policies.dynamic-policies-1.policies
}