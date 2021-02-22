# Copyright (c) 2021 Cybereason Inc
# This code is licensed under MIT license (see LICENSE.md for details)

import logging
import oci
from cybereason_constants import *


def get_machine_from_ip(cr_connection, ip_address):
    '''This function requests to cybereason for simple query to fetch machine details of an ip address provided.'''
    print('Fetching the machine details from ip address {ip_address}'.format(ip_address=ip_address), flush=True)
    try:
        max_results = 100
        url = 'https://{0}:{1}/rest/visualsearch/query/simple'.format(cr_connection['server'], cr_connection['port'])
        api_headers = {'Content-Type': 'application/json'}
        query = {
            'customFields': ['elementDisplayName'],
            'templateContext': 'SPECIFIC',
            'queryPath': [
                {
                    'requestedType': 'Process',
                    'filters': [
                        {
                            'facetName': 'hasSuspicions',
                            'values': [True]
                        }
                    ],
                    'connectionFeature': {
                        'elementInstanceType': 'Process',
                        'featureName': 'ownerMachine'
                    }
                },
                {
                    'requestedType': 'Machine',
                    'filters': [],
                    'connectionFeature': {
                        'elementInstanceType': 'Machine',
                        'featureName': 'networkInterfaces'
                    },
                    'isResult': True
                },
                {
                    'requestedType': 'NetworkInterface',
                    'filters': [],
                    'connectionFeature': {
                        'elementInstanceType': 'NetworkInterface',
                        'featureName': 'ipAddress'
                    }
                },
                {
                    'requestedType': 'IpAddress',
                    'filters': [
                        {
                            'facetName': 'elementDisplayName',
                            'filterType': 'MatchesWildcard',
                            'values': [ip_address]
                        }
                    ]
                }
            ],
            'totalResultLimit': max_results,
            'perGroupLimit': max_results,
            'perFeatureLimit': max_results,
            'queryTimeout': 120000,
            'customFields': [
                        "pylumId",
                        "elementDisplayName"
                    ]
        }
        res = cr_connection['session'].post(url, json=query, headers=api_headers, timeout=CR_REQUEST_TIMEOUT_SEC)
        machines_dict = res.json()["data"]["resultIdToElementDataMap"]

    except Exception as e:
        print('ERROR: Failed to query the Cybereason console', e, flush=True)

    return machines_dict