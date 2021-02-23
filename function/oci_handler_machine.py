# Copyright (c) 2021 Cybereason Inc
# This code is licensed under MIT license (see LICENSE.md for details)

import json
import requests
import oci
import io
import base64
import logging
import hashlib

from fdk import response

from cybereason_connection import get_cybereason_connection
from cybereason_machine_suspicions import is_suspicious
from cybereason_isolate_machine import isolate_machine
from oci_utils import *
from constants import *

def get_private_ips(machine_type, signer, compartment_id, resource_id):
    # Getting the instances private IPs
    private_ips = []        
    if machine_type == MT_INSTANCE:
        private_ips = get_instance_private_ips(signer,compartment_id,resource_id)
    elif machine_type == MT_DATABASE:
        db_system_id = get_db_system_from_database(signer, resource_id)
        private_ips = get_database_ip(signer, compartment_id, db_system_id)
    elif machine_type == MT_DATABASE_SYSTEM:
        private_ips = get_database_ip(signer, compartment_id,resource_id)

    if not private_ips:
        print("No IPs found for resource: " + resource_id, flush=True)
        private_ips = []
        
    return private_ips

def send_notification(signer, ctx, body, remediated):
    try:
        ctx_data = dict(ctx.Config())
        topic_id = ctx_data.get('ONS_TOPIC_OCID')
        if not topic_id:
            print('WARNING: No ONS topic OCID provided. Cannot publish message to topic.', flush=True)
            return
        cloud_guard_problem = body["data"]["resourceName"]
        if remediated:
            message_title = "Cloud Guard Problem " + cloud_guard_problem + " Isolated by Cybereason"
        
            message_body = f'Cloud Guard has detected problem with {body["data"]["resourceName"].lower()}. Cybereason also detected suspicious activity and has isolated the machine to remediate the Cloud Guard Problem.'
            message_body = message_body + f'\nFor more information go to the OCI Cloud Guard Console and look for {cloud_guard_problem}'
        else:  
            message_title = "Cloud Guard Finding " + cloud_guard_problem + " Suspicious Activity Detected by Cybereason"

            message_body = f'Cloud Guard has detected a {body["data"]["resourceName"].lower()} and Cybereason also detected suspicious activity.'
            message_body = message_body + f'\nFor more information go to the OCI Cloud Guard Console and look for {cloud_guard_problem}'
        notification_message = {"default": "Cloud Guard Finding", "body": message_body, "title": message_title} 
        ons = oci.ons.NotificationDataPlaneClient(config={}, signer=signer)
        ons.publish_message(topic_id, notification_message)
    except (Exception) as ex:
        print('ERROR: Failed to publish message to topic', ex, flush=True)
        raise            

def machine_event_handler(ctx, handler_options, data: io.BytesIO=None):

    print("Cloud Guard Response I support", flush=True)

    signer = get_signer()
    number_of_findings = 0  # The number of findings from the Cybereason console
    private_ips = []        # Private IPs associate with the OCI Instance
    body = get_request_body(data)

    # Getting Instance's IP to query Cybereason
    resource_id = body["data"]["additionalDetails"]["resourceId"]
    compartment_id = body["data"]["compartmentId"]
    private_ips = get_private_ips(handler_options['machine_type'], signer, compartment_id, resource_id)
    try:
        ctx_data = dict(ctx.Config())
        server = ctx_data['CYBEREASON_SERVER']
        port = ctx_data['CYBEREASON_PORT']
        username = ctx_data['CYBEREASON_USERNAME']
        password = get_password_from_secrets(signer, ctx_data['CYBEREASON_SECRET_OCID'])
        cr_isolate_machine = ctx_data.get('ISOLATE_MACHINE', 'False').lower()
        send_notifications = ctx_data.get('SEND_NOTIFICATIONS', 'False'].lower()
    except Exception as ex:
        print("ERROR: Failed to retrieve function configuration data", ex, flush=True)
        raise
    
    # We can have multiple IP addresses. Loop through each one of them.
    cr_connection = get_cybereason_connection(server, port, username, password)
    for ipaddr in private_ips:
        number_of_findings = is_suspicious(cr_connection, ipaddr)
        if number_of_findings > 0:
            # We have some suspicious findings from Cybereason
            print('Cybereason found {number_of_findings} issues in the machine specified by ip address {ip_address}'.format(ip_address=ipaddr, number_of_findings=number_of_findings), flush=True)
            if handler_options['isolate_machine'] and (cr_isolate_machine == 'true'):
                isolate_machine(cr_connection, ipaddr)
                cloud_guard_remediate_problem(signer, body["data"]["resourceId"])
            # Determining if what notification to send to the user
            if handler_options['send_notifications'] and (send_notifications == 'true') and handler_options['isolate_machine'] and (cr_isolate_machine == 'true'):
                send_notification(signer, ctx, body, True)

            if handler_options['send_notifications'] and (send_notifications == 'true'):
                send_notification(signer, ctx, body, False)

    return response.Response(
        ctx,
        response_data={"Private_IPs" : private_ips, "Number_of_findings" : number_of_findings},
        headers={"Content-Type": "application/json"}
    )
