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

def send_notification(signer, ctx, body, username, user_was_disabled):
    try:
        ctx_data = dict(ctx.Config())
        topic_id = ctx_data['ONS_TOPIC_OCID']
        cloud_guard_problem = body["data"]["resourceName"]
        message_title = 'Suspicious user activity detected'
        message_body = 'Cybereason detected suspicions on user {username}'.format(username=username)
        if user_was_disabled:
            message_body = message_body + '\nThe account associated with the username was disabled'
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
    except Exception as ex:
        print("ERROR: Failed to retrieve function configuration data", ex, flush=True)
        raise
    
    # We can have multiple IP addresses. Loop through each one of them.
    cr_connection = get_cybereason_connection(server, port, username, password)
    # Check if the user has any suspicions
    num_suspicions = get_user_suspicions(cr_connection, oci_username)
    user_was_disabled = False
    if num_suspicions > 0 and handler_options['disable_user'] and disable_user:
        print('Disabling user {username} in Oracle'.format(username=username))
        user_was_disabled = True
        # TODO: Oracle
    if num_suspicions > 0 and handler_options['send_notifications'] and send_notifications:
        send_notification(signer, ctx, body, oci_username, user_was_disabled)

    return response.Response(
        ctx,
        response_data={"User" : oci_username, "Number_of_suspicions" : num_suspicions},
        headers={"Content-Type": "application/json"}
    )
