# Copyright (c) 2021 Cybereason Inc
# This code is licensed under MIT license (see LICENSE.md for details)

import requests
from cybereason_constants import *

def get_cybereason_connection(server, port, username, password):
    # Create a session
    print('Attempting to log in to the Cybereason console', flush=True)
    login_url = 'https://{0}:{1}/login.html'.format(server, port)
    post_body = {
        'username': username,
        'password': password
    }
    session = requests.Session()
    session.post(login_url, data=post_body, timeout=CR_REQUEST_TIMEOUT_SEC)   # Note that you can also specify verify=False and proxies=... here if you have certificate issues or a proxy server.

    # Verify session was created correctly
    if (session.cookies.get_dict().get('JSESSIONID') is None):
        print('ERROR: Unable to establish session with the Cybereason console', flush=True)
        exit('ERROR: Unable to establish session with the Cybereason console')
    else:
        print('Successfully established session with the Cybereason console', flush=True)

    # Return a connection object that can be reused
    return {
        'session': session,
        'server': server,
        'port': port
    }
