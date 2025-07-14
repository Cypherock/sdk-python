import os
from typing import TypedDict, List, Dict
from enum import Enum
from packages.core.src.config import command as config
from packages.util.utils.assert_utils import assert_condition
from packages.util.utils import is_hex, uint8array_to_hex, hex_to_uint8array, int_to_uint_byte, crc16
from packages.core.src.utils.packetversion import PacketVersion, PacketVersionMap
from packages.interfaces.errors import DeviceCompatibilityError, DeviceCompatibilityErrorType

class DecodedPacketData(TypedDict):
    startOfFrame: str
    currentPacketNumber: int
    totalPacketNumber: int
    payloadData: str
    crc: str
    sequenceNumber: int
    packetType: int
    errorList: List[str]
    timestamp: int

class ErrorPacketRejectReason(Enum):
    NO_ERROR = 0
    CHECKSUM_ERROR = 1
    BUSY_PREVIOUS_CMD = 2
    OUT_OF_ORDER_CHUNK = 3
    INVALID_CHUNK_COUNT = 4
    INVALID_SEQUENCE_NO = 5
    INVALID_PAYLOAD_LENGTH = 6
    APP_BUFFER_BLOCKED = 7
    NO_MORE_CHUNKS = 8
    INVALID_PACKET_TYPE = 9
    INVALID_CHUNK_NO = 10
    INCOMPLETE_PACKET = 11

RejectReasonToMsgMap: Dict[ErrorPacketRejectReason, str] = {
    ErrorPacketRejectReason.NO_ERROR: 'No error',
    ErrorPacketRejectReason.CHECKSUM_ERROR: 'Checksum error',
    ErrorPacketRejectReason.BUSY_PREVIOUS_CMD: 'Device is busy on previous command',
    ErrorPacketRejectReason.OUT_OF_ORDER_CHUNK: 'Chunk out of order',
    ErrorPacketRejectReason.INVALID_CHUNK_COUNT: 'Invalid chunk count',
    ErrorPacketRejectReason.INVALID_SEQUENCE_NO: 'Invalid sequence number',
    ErrorPacketRejectReason.INVALID_PAYLOAD_LENGTH: 'Invalid payload length',
    ErrorPacketRejectReason.APP_BUFFER_BLOCKED: 'Application buffer blocked',
    ErrorPacketRejectReason.NO_MORE_CHUNKS: 'No more chunks',
    ErrorPacketRejectReason.INVALID_PACKET_TYPE: 'Invalid packet type',
    ErrorPacketRejectReason.INVALID_CHUNK_NO: 'Invalid chunk number',
    ErrorPacketRejectReason.INCOMPLETE_PACKET: 'Incomplete packet',
}

def encode_payload_data(
    raw_data: str,
    protobuf_data: str,
    version: PacketVersion,
) -> str:
    assert_condition(raw_data, 'Invalid rawData')
    assert_condition(protobuf_data, 'Invalid protobufData')
    assert_condition(version, 'Invalid version')
    assert_condition(is_hex(raw_data), 'Invalid hex in rawData')
    assert_condition(is_hex(protobuf_data), 'Invalid hex in protobufData')

    if version != PacketVersionMap.v3:
        raise DeviceCompatibilityError(
            DeviceCompatibilityErrorType.INVALID_SDK_OPERATION,
        )

    if len(raw_data) == 0 and len(protobuf_data) == 0:
        return ''

    usable_config = config.v3

    serialized_raw_data_length = int_to_uint_byte(
        len(raw_data) // 2,
        usable_config.radix.data_size,
    )
    serialized_protobuf_data_length = int_to_uint_byte(
        len(protobuf_data) // 2,
        usable_config.radix.data_size,
    )

    return (
        serialized_protobuf_data_length + serialized_raw_data_length + protobuf_data + raw_data
    )

def encode_packet(
    raw_data: str = '',
    proto_data: str = '',
    version: PacketVersion = PacketVersionMap.v3,
    sequence_number: int = 0,
    packet_type: int = 0,
) -> List[bytes]:
    assert_condition(raw_data or proto_data, 'Invalid data')
    assert_condition(version, 'Invalid version')
    assert_condition(sequence_number is not None, 'Invalid sequenceNumber')
    assert_condition(packet_type is not None, 'Invalid packetType')

    if raw_data:
        assert_condition(is_hex(raw_data), 'Invalid hex in raw data')
    if proto_data:
        assert_condition(is_hex(proto_data), 'Invalid hex in proto data')

    assert_condition(packet_type > 0, 'Packet type cannot be negative')

    if version != PacketVersionMap.v3:
        raise DeviceCompatibilityError(
            DeviceCompatibilityErrorType.INVALID_SDK_OPERATION,
        )

    usable_config = config.v3

    serialized_sequence_number = int_to_uint_byte(
        sequence_number,
        usable_config.radix.sequence_number,
    )
    serialized_packet_type = int_to_uint_byte(
        packet_type,
        usable_config.radix.packet_type,
    )

    chunk_size = usable_config.constants.CHUNK_SIZE
    start_of_frame = usable_config.constants.START_OF_FRAME

    serialized_data = encode_payload_data(
        raw_data,
        proto_data,
        version,
    )

    rounds = (len(serialized_data) + chunk_size - 1) // chunk_size
    has_no_data = len(serialized_data) == 0
    if has_no_data:
        rounds = 1

    packet_list: List[bytes] = []

    for i in range(1, rounds + 1):
        current_packet_number = int_to_uint_byte(
            i,
            usable_config.radix.current_packet_number,
        )
        total_packet_number = int_to_uint_byte(
            rounds,
            usable_config.radix.total_packet,
        )
        data_chunk = serialized_data[
            (i - 1) * chunk_size : (i - 1) * chunk_size + chunk_size
        ]
        payload = data_chunk
        payload_length = int_to_uint_byte(
            len(data_chunk) // 2,
            usable_config.radix.payload_length,
        )
        serialized_timestamp = int_to_uint_byte(
            int(str(int(os.times().elapsed))[:usable_config.radix.timestamp_length // 4]),
            usable_config.radix.timestamp_length,
        )

        comm_data = (
            current_packet_number
            + total_packet_number
            + serialized_sequence_number
            + serialized_packet_type
            + serialized_timestamp
            + payload_length
            + payload
        )
        crc = int_to_uint_byte(
            crc16(hex_to_uint8array(comm_data)),
            usable_config.radix.crc,
        )
        packet = start_of_frame + crc + comm_data
        packet_list.append(hex_to_uint8array(packet))

    return packet_list

def decode_packet(
    param: bytes,
    version: PacketVersion,
) -> List[DecodedPacketData]:
    if version != PacketVersionMap.v3:
        raise DeviceCompatibilityError(
            DeviceCompatibilityErrorType.INVALID_SDK_OPERATION,
        )

    usable_config = config.v3
    start_of_frame = usable_config.constants.START_OF_FRAME

    data = uint8array_to_hex(param).lower()
    packet_list: List[DecodedPacketData] = []
    offset = data.find(start_of_frame)

    while len(data) > 0:
        offset = data.find(start_of_frame)
        if offset == -1:
            return packet_list

        start_of_frame = data[offset : offset + len(start_of_frame)]
        offset += len(start_of_frame)

        crc = data[offset : offset + usable_config.radix.crc // 4]
        offset += usable_config.radix.crc // 4

        current_packet_number = int(
            data[offset : offset + usable_config.radix.current_packet_number // 4],
            16,
        )
        offset += usable_config.radix.current_packet_number // 4

        total_packet_number = int(
            data[offset : offset + usable_config.radix.total_packet // 4],
            16,
        )
        offset += usable_config.radix.total_packet // 4

        sequence_number = int(
            data[offset : offset + usable_config.radix.sequence_number // 4],
            16,
        )
        offset += usable_config.radix.sequence_number // 4

        packet_type = int(
            data[offset : offset + usable_config.radix.packet_type // 4],
            16,
        )
        offset += usable_config.radix.packet_type // 4

        timestamp = int(
            data[offset : offset + usable_config.radix.timestamp_length // 4],
            16,
        )
        offset += usable_config.radix.timestamp_length // 4

        payload_length = int(
            data[offset : offset + usable_config.radix.payload_length // 4],
            16,
        )
        offset += usable_config.radix.payload_length // 4

        payload_data = ''
        if payload_length != 0:
            payload_data = data[offset : offset + payload_length * 2]
            offset += payload_length * 2
        data = data[offset:]

        comm_data = (
            int_to_uint_byte(
                current_packet_number, usable_config.radix.current_packet_number
            )
            + int_to_uint_byte(total_packet_number, usable_config.radix.total_packet)
            + int_to_uint_byte(sequence_number, usable_config.radix.sequence_number)
            + int_to_uint_byte(packet_type, usable_config.radix.packet_type)
            + int_to_uint_byte(timestamp, usable_config.radix.timestamp_length)
            + int_to_uint_byte(payload_length, usable_config.radix.payload_length)
            + payload_data
        )
        actual_crc = int_to_uint_byte(
            crc16(hex_to_uint8array(comm_data)),
            usable_config.radix.crc,
        )

        error_list = []
        if start_of_frame.upper() != start_of_frame.upper():
            error_list.append('Invalid Start of frame')
        if current_packet_number > total_packet_number:
            error_list.append('currentPacketNumber is greater than totalPacketNumber')
        if actual_crc.upper() != crc.upper():
            error_list.append('invalid crc')

        packet_list.append(
            DecodedPacketData(
                startOfFrame=start_of_frame,
                currentPacketNumber=current_packet_number,
                totalPacketNumber=total_packet_number,
                crc=crc,
                payloadData=payload_data,
                errorList=error_list,
                sequenceNumber=sequence_number,
                packetType=packet_type,
                timestamp=timestamp,
            )
        )
    return packet_list

def decode_payload_data(payload: str, version: PacketVersion) -> Dict[str, str]:
    assert_condition(payload, 'Invalid payload')
    assert_condition(version, 'Invalid version')
    assert_condition(is_hex(payload), 'Invalid hex in payload')

    if version != PacketVersionMap.v3:
        raise DeviceCompatibilityError(
            DeviceCompatibilityErrorType.INVALID_SDK_OPERATION,
        )

    usable_config = config.v3
    payload_offset = 0

    data_size_half = usable_config.radix.data_size // 4

    protobuf_data_size = int(payload[payload_offset:payload_offset + data_size_half], 16)
    payload_offset += data_size_half

    raw_data_size = int(payload[payload_offset:payload_offset + data_size_half], 16)
    payload_offset += data_size_half

    protobuf_data = payload[payload_offset:payload_offset + protobuf_data_size * 2]
    payload_offset += protobuf_data_size * 2

    raw_data = payload[payload_offset:payload_offset + raw_data_size * 2]
    payload_offset += raw_data_size * 2

    return {
        "protobufData": protobuf_data,
        "rawData": raw_data,
    }



