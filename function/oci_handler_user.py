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
from cybereason_user_suspicions import get_user_suspicions
from oci_utils import *
from constants import *

def send_notification(signer, ctx, body, username, message_body):
    try:
        ctx_data = dict(ctx.Config())
        topic_id = ctx_data['ONS_TOPIC_OCID']
        cloud_guard_problem = body["data"]["resourceName"]
        message_title = 'Suspicious user activity detected'
        notification_message = {"default": "Cloud Guard Finding", "body": message_body, "title": message_title} 
        ons = oci.ons.NotificationDataPlaneClient(config={}, signer=signer)
        ons.publish_message(topic_id, notification_message)
    except (Exception) as ex:
        print('ERROR: Failed to publish message to topic', ex, flush=True)
        raise            

def get_user_from_payload(event_payload):

    resource_id = event_payload["data"]["additionalDetails"]["resourceId"]
    print('Resource ID for event is ' + resource_id, flush=True)
    resource_name = event_payload["data"]["additionalDetails"]["resourceName"]
    print('Resource Name for event is ' + resource_name, flush=True)

    # The payload for each event type may be different. Make sure that we extract the correct user id from it.
    user_extractor = {
        'USER HAS API KEYS': lambda: resource_name,
        'USER ADDED TO GROUP': lambda: resource_id.split('/')[1],
        'SECURITY POLICY MODIFIED': lambda: resource_id.split('/')[1]
    }
    event_name = event_payload["data"]["resourceName"].upper()
    oci_username = user_extractor.get(event_name, lambda: 'ERROR: No user extractor defined for event ' + event_name)()
    return oci_username

def oci_disable_user(signer, problem_id):
    try:
        cloud_guard_client = oci.cloud_guard.CloudGuardClient(config={}, signer=signer)
    except Exception as ex: 
        print("ERROR: failed to create cloud guard client", ex, flush=True)
        raise
    
    try:
        trigger_responder_details = oci.cloud_guard.models.TriggerResponderDetails(responder_rule_id='DISABLE_IAM_USER')
        response = cloud_guard_client.trigger_responder(problem_id, trigger_responder_details)
        print(response.data, flush=True)
    except Exception as ex:
        print("ERROR: Failed to disable user with problem id: ", problem_id)
        print("ERROR: Failure Message: ", ex, flush=True)
        raise

def user_event_handler(ctx, handler_options, data: io.BytesIO=None):

    signer = get_signer()
    body = get_request_body(data)
    oci_username = get_user_from_payload(body)

    # Get details required to query the Cybereason server
    try:
        ctx_data = dict(ctx.Config())
        server = ctx_data['CYBEREASON_SERVER']
        port = ctx_data['CYBEREASON_PORT']
        username = ctx_data['CYBEREASON_USERNAME']
        password = get_password_from_secrets(signer, ctx_data['CYBEREASON_SECRET_OCID'])
        disable_user = ctx_data['DISABLE_USER'].lower()
        send_notifications = ctx_data['SEND_NOTIFICATIONS'].lower()
        never_disable_users = json.loads(ctx_data['NEVER_DISABLE_USERS'])
    except Exception as ex:
        print("ERROR: Failed to retrieve function configuration data", ex, flush=True)
        raise
    
    # We can have multiple IP addresses. Loop through each one of them.
    cr_connection = get_cybereason_connection(server, port, username, password)
    # Check if the user has any suspicions
    num_suspicions = 1 # get_user_suspicions(cr_connection, oci_username)
    user_was_disabled_message = 'Cybereason detected {num_suspicions} suspicions on user {username}.'.format(username=oci_username, num_suspicions=num_suspicions)
    if num_suspicions > 0 and handler_options['disable_user'] and disable_user:
        if oci_username in never_disable_users:
            user_was_disabled_message += ', but it is in the list of users specified by NEVER_DISABLE_USERS.'
            user_was_disabled_message += '\nWe will not disable the user account.'
        else:
            print('Disabling user {username} in Oracle'.format(username=oci_username), flush=True)
            oci_disable_user(signer, body["data"]["resourceId"])
            user_was_disabled_message += ' The account associated with the username was disabled'
    print(user_was_disabled_message, flush=True)

    if num_suspicions > 0 and handler_options['send_notifications'] and send_notifications:
        send_notification(signer, ctx, body, oci_username, user_was_disabled_message)

    return response.Response(
        ctx,
        response_data={"User" : oci_username, "Number_of_suspicions" : num_suspicions},
        headers={"Content-Type": "application/json"}
    )
