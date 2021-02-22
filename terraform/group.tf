
resource "oci_identity_dynamic_group" "cr-functions-group-1" {
  compartment_id = var.tenancy_ocid
  name           = "OCI-CR_dynamic_group"
  description    = "dynamic group created by terraform for OCI-Cybereason functions"
  matching_rule  = "ALL {resource.type = 'fnfunc', resource.compartment.id = '${var.function_compartment_ocid}'}"
}

data "oci_identity_dynamic_groups" "cr-functions-group-1" {
  compartment_id = var.tenancy_ocid

  filter {
    name   = "id"
    values = [oci_identity_dynamic_group.cr-functions-group-1.id]
  }
}

output "dynamicGroups" {
  value = data.oci_identity_dynamic_groups.cr-functions-group-1.dynamic_groups
}
