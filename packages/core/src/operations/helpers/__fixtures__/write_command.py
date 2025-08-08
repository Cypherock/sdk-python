from packages.interfaces.errors import DeviceCommunicationError
from packages.core.src.utils.packetversion import PacketVersionMap

write_command_helper_test_cases = {
    "invalid_args": [
        {
            "packet": bytes([10]),
            "sequence_number": 0,
            "ack_packet_types": [6],
            "version": PacketVersionMap.v1,
        },
        {
            "packet": bytes([10]),
            "sequence_number": 0,
            "ack_packet_types": [6],
            "version": PacketVersionMap.v2,
        },
        {
            "packet": bytes([10]),
            "sequence_number": 0,
            "ack_packet_types": [6],
            "version": "invalid",
        },
        {
            "connection": None,
            "packet": bytes([10]),
            "sequence_number": 0,
            "ack_packet_types": [6],
            "version": PacketVersionMap.v3,
        },
        {
            "packet": None,
            "sequence_number": 0,
            "ack_packet_types": [6],
            "version": PacketVersionMap.v3,
        },
        {
            "packet": bytes([10]),
            "sequence_number": None,
            "ack_packet_types": [6],
            "version": PacketVersionMap.v3,
        },
        {
            "packet": bytes([10]),
            "sequence_number": 0,
            "ack_packet_types": None,
            "version": PacketVersionMap.v3,
        },
        {
            "packet": bytes([10]),
            "sequence_number": 0,
            "ack_packet_types": [6],
            "version": None,
        },
        {
            "packet": bytes([]),
            "sequence_number": 0,
            "ack_packet_types": [6],
            "version": PacketVersionMap.v3,
        },
        {
            "packet": bytes([10]),
            "sequence_number": 0,
            "ack_packet_types": [],
            "version": PacketVersionMap.v3,
        },
    ],
    "valid": [
        {
            # Status Packet Request
            "packet": bytes([
                85, 85, 96, 77, 0, 1, 0, 1, 0, 1, 1, 1, 0, 5, 229, 0,
            ]),
            "ack_packets": [
                bytes([85, 85, 235, 13, 0, 1, 0, 1, 0, 1, 3, 1, 0, 5, 229, 0]),
            ],
            "decoded_ack_packet": {
                "start_of_frame": "5555",
                "current_packet_number": 1,
                "total_packet_number": 1,
                "crc": "eb0d",
                "payload_data": "",
                "error_list": [],
                "sequence_number": 1,
                "packet_type": 3,
                "timestamp": 16778725,
            },
            "ack_packet_types": [3],
            "sequence_number": 1,
        },
        {
            # Send Cmd
            "packet": bytes([
                85, 85, 251, 151, 0, 1, 0, 1, 0, 16, 2, 1, 0, 5, 229, 18, 0, 0, 0, 14,
                13, 132, 60, 156, 132, 72, 109, 130, 151, 242, 104, 195, 233, 47,
            ]),
            "ack_packets": [
                bytes([85, 85, 235, 13, 0, 1, 0, 1, 0, 1, 3, 1, 0, 5, 229, 0]),
                bytes([85, 85, 235, 13, 0, 1, 0, 1, 0, 1, 3, 1, 0, 5, 229, 0]),
                bytes([85, 85, 235, 13, 0, 1, 0, 1, 0, 1, 3, 1, 0, 5, 229, 0]),
                bytes([85, 85, 235, 13, 0, 1, 0, 1, 0, 1, 3, 1, 0, 5, 229, 0]),
                bytes([85, 85, 235, 13, 0, 1, 0, 1, 0, 1, 3, 1, 0, 5, 229, 0]),
                bytes([
                    85, 85, 233, 246, 0, 1, 0, 1, 0, 16, 5, 1, 0, 5, 229, 0,
                ]),
            ],
            "decoded_ack_packet": {
                "start_of_frame": "5555",
                "current_packet_number": 1,
                "total_packet_number": 1,
                "crc": "e9f6",
                "payload_data": "",
                "error_list": [],
                "sequence_number": 16,
                "packet_type": 5,
                "timestamp": 16778725,
            },
            "ack_packet_types": [5],
            "sequence_number": 16,
        },
    ],
    "error": [
        {
            # Invalid packet type
            "packet": bytes([
                85, 85, 96, 77, 0, 1, 0, 1, 0, 1, 1, 1, 0, 5, 229, 0,
            ]),
            "ack_packets": [
                bytes([85, 85, 235, 13, 0, 1, 0, 1, 0, 1, 3, 1, 0, 5, 229, 0]),
            ],
            "ack_packet_types": [1],
            "sequence_number": 1,
            "error_instance": DeviceCommunicationError,
        },
        {
            # Invalid sequence number
            "packet": bytes([
                85, 85, 251, 151, 0, 1, 0, 1, 0, 16, 2, 1, 0, 5, 229, 18, 0, 0, 0, 14,
                13, 132, 60, 156, 132, 72, 109, 130, 151, 242, 104, 195, 233, 47,
            ]),
            "ack_packets": [
                bytes([
                    85, 85, 233, 246, 0, 1, 0, 1, 0, 16, 5, 1, 0, 5, 229, 0,
                ]),
            ],
            "ack_packet_types": [5],
            "sequence_number": 12,
            "error_instance": DeviceCommunicationError,
        },
        {
            # Error Packet
            "packet": bytes([
                85, 85, 251, 151, 0, 1, 0, 1, 0, 16, 2, 1, 0, 5, 229, 18, 0, 0, 0, 14,
                13, 132, 60, 156, 132, 72, 109, 130, 151, 242, 104, 195, 233, 47,
            ]),
            "ack_packets": [
                bytes([
                    85, 85, 98, 182, 0, 1, 0, 1, 0, 16, 7, 1, 0, 5, 229, 0,
                ]),
            ],
            "ack_packet_types": [5],
            "sequence_number": 16,
            "error_instance": DeviceCommunicationError,
        },
    ],
}
