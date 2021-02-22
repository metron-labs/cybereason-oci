# Copyright (c) 2021 Cybereason Inc
# This code is licensed under MIT license (see LICENSE.md for details)

from get_machine_from_ip import get_machine_from_ip
from cybereason_constants import *


# Given an IP address, find the machine details
def _get_machine_details_from_ip(cr_connection, ip_address):
    
    machines_dict = get_machine_from_ip(cr_connection, ip_address)
    
    # Simplify the responses to return machine details
    machine_details_map = {}
    for machine_guid, result in machines_dict.items():
        machine_details_map[machine_guid] = result['simpleValues']['elementDisplayName']['values'][0]
    return machine_details_map

def _get_suspicious_processes_count_for_machines(cr_connection, machine_details_map):
    print('Fetching suspicious processes for machines', flush=True)
    max_results = 100
    headers = { 'Content-Type': 'application/json' }
    malop_url = 'https://{0}:{1}/rest/visualsearch/query/simple'.format(cr_connection['server'], cr_connection['port'])
    query = {
        'customFields': ['suspiciousProcesses', 'processes'],
        'templateContext': 'DETAILS',
        'queryPath': [
            {
                'guidList': list(machine_details_map.keys()),
                'requestedType': 'Machine',
                'result': True

            }
        ],
        'totalResultLimit': max_results,
        'perGroupLimit': max_results,
        'perFeatureLimit': max_results,
        'queryTimeout': 120000
    }
    res = cr_connection['session'].post(url=malop_url, json=query, headers=headers, timeout=CR_REQUEST_TIMEOUT_SEC)
    res_json = res.json()
    print('Received suspicious processes for machines', flush=True)
    num_total_suspicions = 0
    for machine_guid, result in res_json['data']['resultIdToElementDataMap'].items():
        suspicious_processes = result['elementValues'].get('suspiciousProcesses')
        if suspicious_processes:
            num_total_suspicions = num_total_suspicions + suspicious_processes['totalValues']
            print('suspiciousProcesses: {process_count} suspicious processes found for machine {machine_name}'.format(process_count=suspicious_processes['totalValues'], machine_name=machine_details_map[machine_guid]), flush=True)
        else:
            print('suspiciousProcesses: No suspicious processes found for machine {machine_name}'.format(machine_name=machine_details_map[machine_guid]), flush=True)
        processes = result['elementValues'].get('processes')
        if processes:
            num_suspicious_processes = processes['totalSuspicious']
            num_total_suspicions = num_total_suspicions + num_suspicious_processes
            print('processes: {process_count} suspicious processes found for machine {machine_name}'.format(process_count=num_suspicious_processes, machine_name=machine_details_map[machine_guid]), flush=True)
        else:
            print('processes: No suspicious processes found for machine {machine_name}'.format(machine_name=machine_details_map[machine_guid]), flush=True)
    return num_total_suspicions

def is_suspicious(cr_connection, ip_address):
    machine_details_map = _get_machine_details_from_ip(cr_connection, ip_address)
    num_machines = len(machine_details_map.items())
    if num_machines == 0:
        print('Warning: Cybereason API did not return any machines matching IP {ip_address}'.format(ip_address=ip_address), flush=True)
        return False
    elif num_machines > 1:
        print('Warning: Expected exactly one machine from Cybereason API, received {num_machines}. Will return True if any machine has suspicions.'.format(num_machines=num_machines), flush=True)

    return _get_suspicious_processes_count_for_machines(cr_connection, machine_details_map)
