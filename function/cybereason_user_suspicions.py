# Copyright (c) 2021 Cybereason Inc
# This code is licensed under MIT license (see LICENSE.md for details)

import logging
from cybereason_constants import *


def get_user_suspicions(cr_connection, username):
    '''This function requests to cybereason for simple query to fetch suspicion details of the user provided.'''
    print('Fetching the number of suspicions for the user {username}'.format(username=username), flush=True)

    try:
        num_suspicions = 0
        max_results = 100
        url = 'https://{0}:{1}/rest/visualsearch/query/simple'.format(cr_connection['server'], cr_connection['port'])
        api_headers = {'Content-Type': 'application/json'}
        query = {
            "queryPath": [
                {
                    "requestedType": "User",
                    "filters": [
                        {
                            "facetName": "elementDisplayName",
                            "filterType": "ContainsIgnoreCase",
                            "values": [username]
                        }
                    ],
                    "connectionFeature": {
                        "elementInstanceType": "User",
                        "featureName": "ownerMachine"
                    }
                },
                {
                    "requestedType": "Machine",
                    "filters": [],
                    "connectionFeature": {
                        "elementInstanceType": "Machine",
                        "featureName": "processes"
                    }
                },
                {
                    "requestedType": "Process",
                    "filters": [
                        {
                            "facetName": "hasSuspicions",
                            "values": [True]
                        }
                    ],
                    "isResult": True
                }
            ],
            "totalResultLimit": 1000,
            "perGroupLimit": 100,
            "perFeatureLimit": 100,
            "templateContext": "SPECIFIC",
            "queryTimeout": 120000,
            "customFields": [
                "ownerMachine",
                "emailAddress",
                "elementDisplayName"
            ]
        }
        res = cr_connection['session'].post(url, json=query, headers=api_headers, timeout=CR_REQUEST_TIMEOUT_SEC)
        users_dict = res.json()["data"]["resultIdToElementDataMap"]
        for user_id, user_details in users_dict.items():
            print('User {username} has {suspicions} suspicions on machine {machine}'.format(
                username=username,
                suspicions=user_details['suspicionCount'],
                machine=user_details['elementValues']['ownerMachine']['elementValues'][0]['name']), flush=True)
            num_suspicions += user_details['suspicionCount']

    except Exception as e:
        print('ERROR: Failed to get suspicion count for the username {username}'.format(username=username), e, flush=True)
        raise

    print('Returning {suspicions} number of suspicions for user {username}'.format(suspicions=num_suspicions, username=username))
    return num_suspicions
