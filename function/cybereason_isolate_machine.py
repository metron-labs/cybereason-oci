# Copyright (c) 2021 Cybereason Inc
# This code is licensed under MIT license (see LICENSE.md for details)

import logging
import oci
from cybereason_constants import *
from get_machine_from_ip import get_machine_from_ip


def isolate_machine(cr_connection, ip_address):
    # This function requests Cybereason to isolate machine of an ip address provided.
    print('Attempting to isolate machine specified by ip address {ip_address}'.format(ip_address=ip_address), flush=True)
    try:
        machines_dict = get_machine_from_ip(cr_connection, ip_address)
        sensor_ids = []
        for machine_id, machine_details in machines_dict.items():
            sensor_ids.append(str(machine_details['simpleValues']['pylumId']['values'][0]))
        
        # Isolating the machine of given ip address
        headers = { "Content-Type": "application/json" }
        isolate_url = 'https://{0}:{1}/rest/monitor/global/commands/isolate'.format(cr_connection['server'], cr_connection['port'])
        query = {"pylumIds": sensor_ids}
        print('Cybereason Sensor IDs to be isolated: ' + str(sensor_ids))
        res = cr_connection['session'].post(url=isolate_url, json=query, headers=headers, timeout=CR_REQUEST_TIMEOUT_SEC)

    except Exception as e:
        print('ERROR: Failed to isolate machine of given ip address {ip_address}'.format(ip_address=ip_address), e, flush=True)

    print('machine with ip address {ip_address} Isolated successfully...'.format(ip_address=ip_address))      
    return
