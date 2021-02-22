# Copyright (c) 2021 Cybereason Inc
# This code is licensed under MIT license (see LICENSE.md for details)

from constants import *
from oci_handler_machine import machine_event_handler
from oci_handler_user import user_event_handler

CLOUD_GUARD_HANDLERS = {
    'INSTANCE IS NOT RUNNING ON ORACLE PUBLIC IMAGE': {
        'handler': machine_event_handler,
        'options': {
            'machine_type': MT_INSTANCE,
            'isolate_machine': True,
            'stop_instance': False,
            'send_notifications': True
        }
    },
    'INSTANCE IS PUBLICLY ACCESSIBLE': {
        'handler': machine_event_handler,
        'options': {
            'machine_type': MT_INSTANCE,
            'isolate_machine': True,
            'stop_instance': False,
            'send_notifications': True
        }
    },
    'INSTANCE IS RUNNING AN ORACLE PUBLIC IMAGE': {
        'handler': machine_event_handler,
        'options': {
            'machine_type': MT_INSTANCE,
            'isolate_machine': True,
            'stop_instance': False,
            'send_notifications': True
        }
        
    },
    'INSTANCE IS RUNNING WITHOUT REQUIRED TAGS': {
        'handler': machine_event_handler,
        'options': {
            'machine_type': MT_INSTANCE,
            'isolate_machine': True,
            'stop_instance': False,
            'send_notifications': True
        }
        
    },
    'INSTANCE HAS A PUBLIC IP ADDRESS': {
        'handler': machine_event_handler,
        'options': {
            'machine_type': MT_INSTANCE,
            'isolate_machine': True,
            'stop_instance': False,
            'send_notifications': True
        }
        
    },
    'DATABASE SYSTEM HAS PUBLIC IP ADDRESS': {
        'handler': machine_event_handler,
        'options': {
            'machine_type': MT_DATABASE_SYSTEM,
            'isolate_machine': True,
            'stop_instance': False,
            'send_notifications': True
        }
        
    },
    'DATABASE PATCH IS NOT APPLIED': {
        'handler': machine_event_handler,
        'options': {
            'machine_type': MT_DATABASE,
            'isolate_machine': True,
            'stop_instance': False,
            'send_notifications': True
        }
        
    },
    'DATABASE SYSTEM PATCH IS NOT APPLIED': {
        'handler': machine_event_handler,
        'options': {
            'machine_type': MT_DATABASE_SYSTEM,
            'isolate_machine': True,
            'stop_instance': False,
            'send_notifications': True
        }
        
    },
    'DATABASE SYSTEM VERSION IS NOT SANCTIONED': {
        'handler': machine_event_handler,
        'options': {
            'machine_type': MT_DATABASE_SYSTEM,
            'isolate_machine': True,
            'stop_instance': False,
            'send_notifications': True
        }
        
    },
    'DATABASE VERSION IS NOT SANCTIONED': {
        'handler': machine_event_handler,
        'options': {
            'machine_type': MT_DATABASE,
            'isolate_machine': True,
            'stop_instance': False,
            'send_notifications': True
        }
        
    },
    'USER HAS API KEYS': {
        'handler': user_event_handler,
        'options': {
            'disable_user': False,
            'send_notifications': True
        }
    },
    'USER ADDED TO GROUP': {
        'handler': user_event_handler,
        'options': {
            'disable_user': False,
            'send_notifications': True
        }
    },
    'SECURITY POLICY MODIFIED': {
        'handler': user_event_handler,
        'options': {
            'disable_user': False,
            'send_notifications': True
        }
    }
}
