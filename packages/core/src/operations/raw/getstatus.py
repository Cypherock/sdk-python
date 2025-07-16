from typing import Optional
from packages.interfaces import IDeviceConnection
from packages.core.src.utils.packetversion import PacketVersion
from packages.core.src.encoders.raw import decode_status, StatusData
from packages.core.src.operations.helpers.getstatus import get_status as get_status_helper


async def get_status(
    connection: IDeviceConnection,
    version: PacketVersion,
    max_tries: int = 5,
    timeout: Optional[int] = None,
) -> StatusData:
    result = await get_status_helper(
        connection=connection,
        version=version,
        max_tries=max_tries,
        timeout=timeout,
    )
    raw_data = result["raw_data"]
    return decode_status(raw_data, version)
