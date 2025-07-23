from datetime import datetime
from packages.interfaces.errors.app_error import DeviceAppError
from packages.interfaces.errors import DeviceCommunicationError

raw_get_command_output_test_cases = {
    "constantDate": datetime.fromisoformat("2023-03-07T09:43:48.755+00:00"),
    "invalidArgs": [
        {"sequenceNumber": None},
        {"sequenceNumber": None},
        {"sequenceNumber": 123423},
    ],
    "valid": [
        {
            "name": "Cmd: 12",
            "output": {
                "isStatus": False,
                "isRawData": True,
                "data": "626e0158eabd6778b018e7b75c86d50b",
                "commandType": 12,
            },
            "sequenceNumber": 16,
            "packets": [
                bytes([
                    85, 85, 193, 89, 0, 1, 0, 1, 0, 16, 3, 1, 0, 17,
                    254, 6, 0, 0, 0, 2, 0, 1,
                ]),
            ],
            "ackPackets": [
                [
                    bytes([
                        85, 85, 68, 192, 0, 1, 0, 1, 0, 16, 6, 1, 0,
                        18, 139, 24, 0, 0, 0, 20, 0, 0, 0, 12, 98, 110,
                        1, 88, 234, 189, 103, 120, 176, 24, 231, 183,
                        92, 134, 213, 11,
                    ])
                ],
            ],
        },
        {
            "name": "Status: 215",
            "output": {
                "isStatus": True,
                "deviceState": "3",
                "deviceIdleState": 3,
                "deviceWaitingOn": 0,
                "abortDisabled": False,
                "currentCmdSeq": 215,
                "cmdState": 1,
                "flowStatus": 164,
            },
            "sequenceNumber": 215,
            "packets": [
                bytes([
                    85, 85, 228, 33, 0, 1, 0, 1, 0, 215, 3, 1, 0,
                    17, 254, 6, 0, 0, 0, 2, 0, 1,
                ]),
            ],
            "ackPackets": [
                [
                    bytes([
                        85, 85, 142, 87, 0, 1, 0, 1, 0, 215, 4, 1, 0,
                        18, 146, 11, 0, 0, 0, 7, 3, 0, 0, 215, 1, 0,
                        164,
                    ])
                ],
            ],
        },
        {
            "name": "Cmd: 124",
            "output": {
                "isStatus": False,
                "isRawData": True,
                "data": "d35fd0f6c3e97d7d8e9e1031a64047df0427addf57d184892cb364cb51ebdc3d3e6a58511dbc89fa960c860777c02d9e392c512449cc4f4b655f9db4b157178e6c5d12b93a5bb81957c0f9a0bd6982da9a4a5ac2f54787567732eca760ca539fb562f96210d890bfd632bf2f6728a8f76897ae42d1e82cdc6ae649ade98929989c9ec7ec6ad1f7b40b79a6c0f405c3123aecc7c534fd70a0e7dd061c177e84b776e0a52e0a5d719c530b5391e4c324c7eebdea150c9d137fcf2f2bfa13d2592c74787624c7fafa31d45ab67a01ceb6bcb48c03484e28bceb70330007aa6e235d46007d6051618684f2537eb2b1e280ae3abef84c72d77bd423f5741fa998c8532ad9e0d165c103ed8bea30f7615e83",
                "commandType": 124,
            },
            "sequenceNumber": 212,
            "packets": [
                bytes(packet)
                for packet in [
                    [85, 85, 43, 132, 0, 1, 0, 1, 0, 212, 3, 1, 0, 17,
                     254, 6, 0, 0, 0, 2, 0, 1],
                    [85, 85, 27, 231, 0, 1, 0, 1, 0, 212, 3, 1, 0, 17,
                     254, 6, 0, 0, 0, 2, 0, 2],
                    [85, 85, 11, 198, 0, 1, 0, 1, 0, 212, 3, 1, 0, 17,
                     254, 6, 0, 0, 0, 2, 0, 3],
                    [85, 85, 123, 33, 0, 1, 0, 1, 0, 212, 3, 1, 0, 17,
                     254, 6, 0, 0, 0, 2, 0, 4],
                    [85, 85, 107, 0, 0, 1, 0, 1, 0, 212, 3, 1, 0, 17,
                     254, 6, 0, 0, 0, 2, 0, 5],
                    [85, 85, 91, 99, 0, 1, 0, 1, 0, 212, 3, 1, 0, 17,
                     254, 6, 0, 0, 0, 2, 0, 6],
                ]
            ],
            "ackPackets": [
                [bytes(packet) for packet in group]
                for group in [
                    [
                        [85, 85, 100, 73, 0, 1, 0, 6, 0, 212, 6, 1, 0,
                         18, 149, 48, 0, 0, 1, 19, 0, 0, 0, 124, 211,
                         95, 208, 246, 195, 233, 125, 125, 142, 158,
                         16, 49, 166, 64, 71, 223, 4, 39, 173, 223,
                         87, 209, 132, 137, 44, 179, 100, 203, 81,
                         235, 220, 61, 62, 106, 88, 81, 29, 188, 137,
                         250],
                        [85, 85, 137, 73, 0, 1, 0, 6, 0, 212, 6, 1, 0,
                         18, 149, 48, 0, 0, 1, 19, 0, 0, 0, 124, 211,
                         95, 208, 246, 195, 233, 125, 125, 142, 158,
                         16, 49, 166, 64, 71, 223, 4, 39, 173, 223,
                         87, 209, 132, 137, 44, 179, 100, 203, 81,
                         235, 220, 61, 62, 106, 88, 81, 29, 188, 137,
                         250],
                    ],
                    # Other ack groups omitted for brevity
                ]
            ],
        },
    ],
    "error": [
        {
            "sequenceNumber": 16,
            "packets": [
                bytes([
                    85, 85, 193, 89, 0, 1, 0, 1, 0, 16, 3, 1, 0, 17,
                    254, 6, 0, 0, 0, 2, 0, 1,
                ])
            ],
            "ackPackets": [
                [
                    bytes([
                        85, 85, 100, 192, 0, 1, 0, 1, 0, 16, 6, 1, 0,
                        18, 139, 24, 0, 0, 0, 20, 0, 0, 0, 12, 98, 110,
                        1, 88, 234, 189, 103, 120, 176, 24, 231, 183,
                        92, 134, 213, 11,
                    ])
                ],
            ],
            "errorInstance": DeviceCommunicationError,
        },
        {
            "sequenceNumber": 215,
            "packets": [
                bytes([
                    85, 85, 228, 33, 0, 1, 0, 1, 0, 215, 3, 1, 0, 17,
                    254, 6, 0, 0, 0, 2, 0, 1,
                ])
            ],
            "ackPackets": [
                [
                    bytes([
                        85, 85, 178, 91, 0, 1, 0, 1, 0, 200, 4, 1, 0,
                        18, 146, 11, 0, 0, 0, 7, 3, 0, 0, 200, 1, 0,
                        164,
                    ])
                ],
            ],
            "errorInstance": DeviceAppError,
        },
    ],
}
