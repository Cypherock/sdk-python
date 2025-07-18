from typing import Optional
from packages.interfaces import IDeviceConnection
from packages.util.utils.assert_utils import assert_condition
from packages.util.utils.crypto import uint8array_to_hex
from packages.core.src.utils.logger import logger
from packages.core.src.utils.packetversion import PacketVersion
from packages.core.src.encoders.proto.generated.core import Msg, Command
from packages.core.src.operations.helpers.sendcommand import send_command as send_command_helper


async def send_query(
    connection: IDeviceConnection,
    applet_id: int,
    data: bytes,
    version: PacketVersion,
    sequence_number: int,
    max_tries: int = 5,
    timeout: Optional[int] = None,
) -> None:
    assert_condition(applet_id, 'Invalid appletId')
    assert_condition(data, 'Invalid data')

    assert_condition(applet_id >= 0, 'appletId cannot be negative')
    assert_condition(len(data) > 0, 'data cannot be empty')

    raw_data = uint8array_to_hex(data)
    logger.debug('Sending query', {'appletId': applet_id, 'rawData': raw_data})

    msg_data = uint8array_to_hex(
        bytes(Msg(cmd=Command(applet_id=applet_id)))
    )

    return await send_command_helper(
        connection=connection,
        proto_data=msg_data,
        raw_data=raw_data,
        version=version,
        max_tries=max_tries,
        sequence_number=sequence_number,
        timeout=timeout,
    )



