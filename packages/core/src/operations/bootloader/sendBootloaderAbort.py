import asyncio
from typing import Optional, Dict, Any
from packages.interfaces.errors import (
    DeviceCommunicationError,
    DeviceCommunicationErrorType,
    DeviceConnectionError,
    DeviceConnectionErrorType,
)
from packages.interfaces import IDeviceConnection
from packages.util.utils.crypto import (
    hex_to_uint8array,
    uint8array_to_hex,
    assert_condition,
)
from packages.core.src import config
from packages.core.src.operations.helpers.can_retry import can_retry

ACK_PACKET = '18'


async def send_bootloader_abort(
    connection: IDeviceConnection,
    options: Optional[Dict[str, Any]] = None
) -> None:
    if options is None:
        options = {}

    timeout = options.get('timeout')
    first_timeout = options.get('first_timeout')
    max_tries = options.get('max_tries', 5)

    assert_condition(connection, 'Invalid connection')

    packets_list = ['41']
    data_list = [hex_to_uint8array(packet) for packet in packets_list]

    for index, data in enumerate(data_list):
        tries = 1
        inner_max_tries = max_tries
        first_error = None

        while tries <= inner_max_tries:
            try:
                await write_packet(
                    connection=connection,
                    data=data,
                    timeout=first_timeout if index == 0 else timeout,
                    recheck_time=config.v1.constants.RECHECK_TIME,
                )
                break  # Success
            except Exception as e:
                if not can_retry(e):
                    tries = inner_max_tries
                if not first_error:
                    first_error = e
                tries += 1

        if first_error:
            raise first_error
        else:
            raise DeviceCommunicationError(
                DeviceCommunicationErrorType.WRITE_ERROR
            )


async def write_packet(
    connection: IDeviceConnection,
    data: bytes,
    timeout: Optional[int] = 2000,
    recheck_time: int = 500  # in milliseconds
) -> None:
    is_completed = False
    recheck_task: Optional[asyncio.Task] = None
    timeout_task: Optional[asyncio.Task] = None

    def cleanup():
        nonlocal is_completed, recheck_task, timeout_task
        is_completed = True
        if recheck_task and not recheck_task.done():
            recheck_task.cancel()
        if timeout_task and not timeout_task.done():
            timeout_task.cancel()

    async def recheck_packet():
        nonlocal is_completed
        try:
            if not await connection.is_connected():
                cleanup()
                raise DeviceConnectionError(DeviceConnectionErrorType.CONNECTION_CLOSED)

            if is_completed:
                return

            raw_packet = await connection.receive()
            if not raw_packet:
                schedule_recheck()
                return

            e_packet_data = uint8array_to_hex(raw_packet)
            if ACK_PACKET in e_packet_data:
                cleanup()
                return

            schedule_recheck()
        except Exception:
            schedule_recheck()

    def schedule_recheck():
        nonlocal recheck_task
        if is_completed:
            return
        if recheck_task and not recheck_task.done():
            recheck_task.cancel()
        recheck_task = asyncio.create_task(delayed_recheck())

    async def delayed_recheck():
        await asyncio.sleep(recheck_time / 1000)
        await recheck_packet()

    try:
        await connection.send(data)

        # Start timeout
        if timeout:
            timeout_task = asyncio.create_task(asyncio.sleep(timeout / 1000))

        schedule_recheck()

        if timeout_task:
            await timeout_task
            if not is_completed:
                cleanup()
                raise DeviceCommunicationError(DeviceCommunicationErrorType.WRITE_TIMEOUT)

    except asyncio.CancelledError:
        # Ignore task cancellations
        pass
    except Exception as err:
        cleanup()
        raise err
