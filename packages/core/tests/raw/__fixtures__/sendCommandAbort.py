from datetime import datetime

from packages.interfaces.errors import DeviceCommunicationError
from packages.interfaces.errors.app_error import DeviceAppError

raw_send_abort_test_cases = {
    "constant_date": datetime.fromisoformat("2023-03-07T09:43:48.755Z".replace("Z", "+00:00")),
    "invalid_args": [
        {
            "sequence_number": None,
        },
        {
            "sequence_number": None,
        },
        {
            "sequence_number": 123423,
        },
    ],
    "valid": [
        {
            "name": "CmdSeq: 18",
            "abort_request": bytearray([
                85, 85, 135, 124, 0, 1, 0, 1, 0, 18, 8, 1, 0, 17, 254, 0,
            ]),
            "ack_packets": [
                bytearray([
                    85, 85, 143, 73, 0, 1, 0, 1, 0, 18, 4, 1, 0, 18, 86, 11, 0, 0, 0, 7,
                    35, 0, 0, 18, 7, 0, 132,
                ]),
            ],
            "sequence_number": 18,
            "status": {
                "device_state": "23",
                "device_idle_state": 3,
                "device_waiting_on": 2,
                "abort_disabled": False,
                "current_cmd_seq": 18,
                "cmd_state": 7,
                "flow_status": 132,
                "is_status": True,
            },
        },
        {
            "name": "CmdSeq: 78",
            "abort_request": bytearray([
                85, 85, 63, 128, 0, 1, 0, 1, 0, 78, 8, 1, 0, 17, 254, 0,
            ]),
            "ack_packets": [
                bytearray([
                    170, 63, 27, 0, 2, 0, 2, 10, 16, 97, 6, 47, 150, 92, 178, 86, 238, 68,
                    168, 147, 34, 27, 233, 174, 197, 213, 124, 255, 32, 26,
                ]),
                bytearray([170, 1, 6, 0, 0, 0, 0, 0]),
                bytearray([
                    85, 85, 75, 43, 0, 1, 0, 1, 0, 78, 4, 1, 0, 18, 90, 11, 0, 0, 0, 7, 3,
                    0, 0, 78, 1, 0, 164,
                ]),
            ],
            "sequence_number": 78,
            "status": {
                "device_state": "3",
                "device_idle_state": 3,
                "device_waiting_on": 0,
                "abort_disabled": False,
                "current_cmd_seq": 78,
                "cmd_state": 1,
                "flow_status": 164,
                "is_status": True,
            },
        },
    ],
    "error": [
        {
            "name": "Invalid CRC",
            "abort_request": bytearray([
                85, 85, 135, 124, 0, 1, 0, 1, 0, 18, 8, 1, 0, 17, 254, 0,
            ]),
            "ack_packets": [
                bytearray([
                    85, 85, 100, 73, 0, 1, 0, 1, 0, 18, 4, 1, 0, 18, 86, 11, 0, 0, 0, 7,
                    35, 0, 0, 18, 7, 0, 132,
                ]),
            ],
            "sequence_number": 18,
            "error_instance": DeviceCommunicationError,
        },
        {
            "name": "Invalid sequenceNumber",
            "abort_request": bytearray([
                85, 85, 63, 128, 0, 1, 0, 1, 0, 78, 8, 1, 0, 17, 254, 0,
            ]),
            "ack_packets": [
                bytearray([
                    170, 63, 27, 0, 2, 0, 2, 10, 16, 97, 6, 47, 150, 92, 178, 86, 238, 68,
                    168, 147, 34, 27, 233, 174, 197, 213, 124, 255, 32, 26,
                ]),
                bytearray([170, 1, 6, 0, 0, 0, 0, 0]),
                bytearray([
                    85, 85, 143, 73, 0, 1, 0, 1, 0, 18, 4, 1, 0, 18, 86, 11, 0, 0, 0, 7,
                    35, 0, 0, 18, 7, 0, 132,
                ]),
            ],
            "error_instance": DeviceAppError,
            "sequence_number": 78,
        },
    ],
}

__all__ = ['raw_send_abort_test_cases']