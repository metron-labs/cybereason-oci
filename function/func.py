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
from oci_handler_options import *


def handler(ctx, data: io.BytesIO=None):

    signer = get_signer()
    body = get_request_body(data)
    event_name = body["data"]["resourceName"].upper()
    cloud_guard_handler = CLOUD_GUARD_HANDLERS.get(event_name)
    response_data = None
    if cloud_guard_handler:
        # If we have options, then this Cloud Guard Problem is in scope
        print("Cloud Guard Response I support", flush=True)
        response_data = cloud_guard_handler['handler'](ctx, cloud_guard_handler['options'], data)
    else:
        msg = 'Resource Name ' + event_name + ' does not have a handler associated with it.'
        print(msg, flush=True)
        response_data = response.Response(
            ctx,
            response_data={"message": msg },
            headers={"Content-Type": "application/json"}
        )

    return response_data
