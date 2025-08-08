from datetime import datetime

# Constant date for mocking Date.now() in tests
constant_date = datetime(2023, 3, 7, 9, 43, 48, 755000)

# Get status test fixtures
fixtures = {
    "valid": [
        {
            "name": "CmdSeq: 50",
            "status_request": bytes([
                85, 85, 169, 56, 0, 1, 0, 1, 255, 255, 1, 1, 0, 17, 254, 0,
            ]),
            "ack_packets": [
                bytes([
                    85, 85, 41, 170, 0, 1, 0, 1, 255, 255, 4, 1, 0, 17, 254, 15, 0, 11, 0,
                    0, 8, 2, 16, 3, 32, 50, 40, 7, 48, 132, 1,
                ])
            ],
            "status": {
                "device_idle_state": 3,
                "device_waiting_on": 2,
                "abort_disabled": False,
                "current_cmd_seq": 50,
                "cmd_state": 7,
                "flow_status": 132,
            }
        },
        {
            "name": "CmdSeq: 3842",
            "status_request": bytes([
                85, 85, 169, 56, 0, 1, 0, 1, 255, 255, 1, 1, 0, 17, 254, 0,
            ]),
            "ack_packets": [
                bytes([
                    170, 63, 27, 0, 2, 0, 2, 10, 16, 97, 6, 47, 150, 92, 178, 86, 238, 68,
                    168, 147, 34, 27, 233, 174, 197, 213, 124, 255, 32, 26,
                ]),
                bytes([170, 1, 6, 0, 0, 0, 0, 0]),
                bytes([
                    85, 85, 18, 100, 0, 1, 0, 1, 255, 255, 4, 1, 0, 17, 254, 14, 0, 10, 0,
                    0, 16, 3, 32, 130, 30, 40, 1, 48, 164, 1,
                ])
            ],
            "status": {
                "device_idle_state": 3,
                "device_waiting_on": 0,
                "abort_disabled": False,
                "current_cmd_seq": 3842,
                "cmd_state": 1,
                "flow_status": 164,
            }
        }
    ]
}
