from typing import Optional
from packages.interfaces.errors import DeviceCompatibilityError, DeviceCompatibilityErrorType
from packages.interfaces import IDeviceConnection
from packages.util.utils.assert_utils import assert_condition
from packages.core.src.config import v3 as config_v3
from packages.core.src.utils.packetversion import PacketVersion, PacketVersionMap
from packages.core.src.encoders.packet.packet import encode_packet
from .writecommand import write_command
from .can_retry import can_retry


async def send_command(
        connection: IDeviceConnection,
        version: PacketVersion,
        sequence_number: int,
        raw_data: Optional[str] = None,
        proto_data: Optional[str] = None,
        max_tries: int = 5,
        timeout: Optional[int] = None
) -> None:
    assert_condition(connection, 'Invalid connection')
    assert_condition(raw_data or proto_data, 'Raw data or proto data is required')
    assert_condition(version, 'Invalid version')
    assert_condition(sequence_number, 'Invalid sequenceNumber')

    if version != PacketVersionMap.v3:
        raise DeviceCompatibilityError(
            DeviceCompatibilityErrorType.INVALID_SDK_OPERATION
        )

    usable_config = config_v3

    packets_list = encode_packet(
        raw_data=raw_data or '',
        proto_data=proto_data or '',
        version=version,
        sequence_number=sequence_number,
        packet_type=usable_config.commands.PACKET_TYPE.CMD
    )

    first_error: Optional[Exception] = None

    for packet in packets_list:
        tries = 1
        inner_max_tries = max_tries
        first_error = None
        is_success = False

        while tries <= inner_max_tries and not is_success:
            try:
                await write_command(
                    connection=connection,
                    packet=packet,
                    version=version,
                    sequence_number=sequence_number,
                    ack_packet_types=[usable_config.commands.PACKET_TYPE.CMD_ACK],
                    timeout=timeout
                )
                is_success = True

            except Exception as e:
                if not can_retry(e):
                    tries = inner_max_tries

                if not first_error:
                    first_error = e

            tries += 1

        if not is_success and first_error:
            raise first_error

