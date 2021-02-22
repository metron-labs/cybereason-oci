# Copyright (c) 2021 Cybereason Inc
# This code is licensed under MIT license (see LICENSE.md for details)

import oci
import base64
import json

def get_signer():
    signer = None
    try:
        signer = oci.auth.signers.get_resource_principals_signer()
    except Exception as ex:
        print('ERROR: Could not get signer from instance prinicpal', ex, flush=True)
        raise
    return signer

def get_request_body(data):
    body = None
    try:
        body = json.loads(data.getvalue())
        print("Event type: " + body["eventType"])
        print("Compartment name: " + body["data"]["compartmentName"])
    except (Exception) as ex:
        print('ERROR: Missing key in payload', ex, flush=True)
        raise
    return body

def get_instance_vnics(signer, instance_id, compartment_id):
    print(f'Instance ID: {instance_id}, Compartment ID: {compartment_id}')
    try:
        compute_client = oci.core.ComputeClient(config={}, signer=signer)
        instance_vnics = oci.pagination.list_call_get_all_results( 
            compute_client.list_vnic_attachments,
            compartment_id=compartment_id, instance_id=instance_id
            ).data
        return instance_vnics
    
    except Exception as ex:
        print("ERROR: getting VNICS in compartment failed", ex, flush=True)

def get_vnic_private_ips(signer, vnic_id):
    private_ips =[]
    try:
        network_client = oci.core.VirtualNetworkClient(config={}, signer=signer)
        vnic_private_ips = oci.pagination.list_call_get_all_results(
            network_client.list_private_ips,
            vnic_id=vnic_id
            ).data
        for private_ip in vnic_private_ips:
            private_ips.append(private_ip.ip_address)

        return private_ips

    except Exception as ex:
        RuntimeError("ERROR: getting Private IPs for a: {}" + str(ex.args))
        raise


def get_db_system_from_database(signer, database_id):
    db_sytstem_id = None

    db_client = oci.database.DatabaseClient(config={}, signer=signer)
    try:
        db_sytstem_id = db_client.get_database(database_id).data.db_system_id
    except Exception as e:
            raise RuntimeError("Failed to Database System Id from Database" + str(e.args))
    return db_sytstem_id

def get_database_ip(signer, compartment_id, db_system_id):
    db_private_ips = []

    db_client = oci.database.DatabaseClient(config={}, signer=signer)
    db_nodes = oci.pagination.list_call_get_all_results(
            db_client.list_db_nodes,
            compartment_id,
            db_system_id=db_system_id).data
    for db_node in db_nodes:
        # Adding DB Nodes VNICs to find IPs
        vnic_ips = get_vnic_private_ips(signer, db_node.vnic_id)

        for ip in vnic_ips:
            db_private_ips.append(ip)
    return db_private_ips

def get_instance_private_ips(signer, compartment_id, instance_id):
    
    # Storage for an instances private IP
    instance_private_ips =[]

    # Getting All VNICs in the compartment
    instance_vnics = get_instance_vnics(signer, instance_id, compartment_id)
    
    for instance_vnic in instance_vnics:
        private_ips = get_vnic_private_ips(signer, instance_vnic.vnic_id)
        for ip in private_ips:
            instance_private_ips.append(ip)

    return instance_private_ips

def get_password_from_secrets(signer, secret_ocid):
    #decrypted_secret_content = ""
    try:
        client = oci.secrets.SecretsClient({}, signer=signer)
        secret_content = client.get_secret_bundle(secret_ocid).data.secret_bundle_content.content.encode('utf-8')
        decrypted_secret_content = base64.b64decode(secret_content).decode("utf-8")
    except Exception as ex:
        print("ERROR: failed to retrieve the secret content", ex, flush=True)
        raise
    return decrypted_secret_content

def cloud_guard_remediate_problem(signer, problem_id ):
    # Creating Cloud Guard Client
    try:
        cloud_guard_client = oci.cloud_guard.CloudGuardClient(config={}, signer=signer)
    except Exception as ex: 
        print("ERROR: failed to create cloud guard client", ex, flush=True)
        raise

    try:
        # Create Remediation object
        remediate_problem = oci.cloud_guard.models.UpdateProblemStatusDetails(status="RESOLVED",comment="Resolved by Cybereason")

        # Remediate  Cloud Guard Problems  
        update_problem_status_response = cloud_guard_client.update_problem_status( problem_id=problem_id, update_problem_status_details=remediate_problem) 
        return update_problem_status_response.data

    except Exception as ex:
        print("ERROR: Failed to resolve cloud problem: ", problem_id)
        print("ERROR: Failure Message: ", ex, flush=True)
        raise
