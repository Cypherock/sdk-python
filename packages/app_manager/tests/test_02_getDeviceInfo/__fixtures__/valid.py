from typing import List
from .types import IGetDeviceInfoTestCase

with_one_applet: IGetDeviceInfoTestCase = {
    'name': 'Info with 1 applet',
    'query': bytes([10, 2, 10, 0]),
    'result': bytes([
        10, 32, 10, 30, 10, 12, 123, 43, 26, 231, 42, 86, 91, 130, 41, 55, 186, 203,
        18, 2, 8, 1, 24, 1, 34, 8, 8, 12, 18, 4, 8, 1, 24, 26,
    ]),
    'output': {
        'device_serial': bytes([
            123, 43, 26, 231, 42, 86, 91, 130, 41, 55, 186, 203,
        ]),
        'firmware_version': {
            'major': 1,
            'minor': 0,
            'patch': 0,
        },
        'is_authenticated': True,
        'applet_list': [
            {
                'id': 12,
                'version': {
                    'major': 1,
                    'minor': 0,
                    'patch': 26,
                },
            },
        ],
        'onboarding_step': 0,
        'is_initial': False,
    },
}

with_two_applet: IGetDeviceInfoTestCase = {
    'name': 'Info with 2 applets',
    'query': bytes([10, 2, 10, 0]),
    'result': bytes([
        10, 36, 10, 34, 10, 3, 90, 221, 135, 18, 2, 8, 1, 24, 1, 34, 11, 8, 2, 18,
        7, 8, 93, 16, 214, 1, 24, 26, 34, 8, 8, 12, 18, 4, 8, 1, 24, 26,
    ]),
    'output': {
        'device_serial': bytes([90, 221, 135]),
        'firmware_version': {
            'major': 1,
            'minor': 0,
            'patch': 0,
        },
        'is_authenticated': True,
        'applet_list': [
            {
                'id': 2,
                'version': {
                    'major': 93,
                    'minor': 214,
                    'patch': 26,
                },
            },
            {
                'id': 12,
                'version': {
                    'major': 1,
                    'minor': 0,
                    'patch': 26,
                },
            },
        ],
        'onboarding_step': 0,
        'is_initial': False,
    },
}

with_only_device_serial: IGetDeviceInfoTestCase = {
    'name': 'Only device serial',
    'query': bytes([10, 2, 10, 0]),
    'result': bytes([10, 6, 10, 4, 10, 2, 12, 124]),
    'output': {
        'device_serial': bytes([12, 124]),
        'firmware_version': None,
        'is_authenticated': False,
        'applet_list': [],
        'onboarding_step': 0,
        'is_initial': False,
    },
}

with_partial_data: IGetDeviceInfoTestCase = {
    'name': 'Partial data',
    'query': bytes([10, 2, 10, 0]),
    'result': bytes([10, 11, 10, 9, 10, 5, 234, 21, 53, 31, 64, 24, 1]),
    'output': {
        'device_serial': bytes([234, 21, 53, 31, 64]),
        'firmware_version': None,
        'is_authenticated': True,
        'applet_list': [],
        'onboarding_step': 0,
        'is_initial': False,
    },
}

with_initial_states: IGetDeviceInfoTestCase = {
    'name': 'With initial states',
    'query': bytes([10, 2, 10, 0]),
    'result': bytes([
        10, 36, 10, 34, 10, 12, 123, 43, 26, 231, 42, 86, 91, 130, 41, 55, 186, 203,
        18, 2, 8, 1, 24, 1, 34, 8, 8, 12, 18, 4, 8, 1, 24, 26, 40, 1, 48, 4,
    ]),
    'output': {
        'device_serial': bytes([
            123, 43, 26, 231, 42, 86, 91, 130, 41, 55, 186, 203,
        ]),
        'firmware_version': {
            'major': 1,
            'minor': 0,
            'patch': 0,
        },
        'is_authenticated': True,
        'applet_list': [
            {
                'id': 12,
                'version': {
                    'major': 1,
                    'minor': 0,
                    'patch': 26,
                },
            },
        ],
        'is_initial': True,
        'onboarding_step': 4,
    },
}

valid: List[IGetDeviceInfoTestCase] = [
    with_one_applet,
    with_two_applet,
    with_only_device_serial,
    with_partial_data,
    with_initial_states,
]
