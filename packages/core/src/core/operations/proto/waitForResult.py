from typing import Optional, Callable, Dict, Any
from interfaces import IDeviceConnection
from interfaces.errors.app_error import DeviceAppError, DeviceAppErrorType
from interfaces.errors.compatibility_error import DeviceCompatibilityError, DeviceCompatibilityErrorType
from util.utils.assert_utils import assert_condition
from util.utils.crypto import uint8array_to_hex
from util.utils.sleep import sleep
from ...utils.logger import logger
from ...utils.packetversion import PacketVersion, PacketVersionMap
from ...encoders.proto.generated.core_pb2 import CmdState, DeviceIdleState, Status
from .getresult import get_result


class IWaitForCommandOutputParams:
    def __init__(
        self,
        connection: IDeviceConnection,
        sequence_number: int,
        applet_id: int,
        on_status: Optional[Callable[[Status], None]] = None,
        version: PacketVersion = None,
        options: Optional[Dict[str, Any]] = None,
        allow_core_data: Optional[bool] = None,
    ):
        self.connection = connection
        self.sequence_number = sequence_number
        self.applet_id = applet_id
        self.on_status = on_status
        self.version = version
        self.options = options
        self.allow_core_data = allow_core_data


async def wait_for_result(
    connection: IDeviceConnection,
    sequence_number: int,
    applet_id: int,
    on_status: Optional[Callable[[Status], None]] = None,
    options: Optional[Dict[str, Any]] = None,
    version: PacketVersion = None,
    allow_core_data: Optional[bool] = None,
) -> bytes:
    assert_condition(connection, 'Invalid connection')
    assert_condition(sequence_number, 'Invalid sequenceNumber')
    assert_condition(applet_id, 'Invalid appletId')
    assert_condition(version, 'Invalid version')

    assert_condition(applet_id >= 0, 'appletId cannot be negative')

    if version != PacketVersionMap.v3:
        raise DeviceCompatibilityError(
            DeviceCompatibilityErrorType.INVALID_SDK_OPERATION
        )

    while True:
        response = await get_result(
            connection=connection,
            version=version,
            applet_id=applet_id,
            max_tries=options.get('maxTries', 5) if options else 5,
            sequence_number=sequence_number,
            timeout=options.get('timeout') if options else None,
            allow_core_data=allow_core_data,
        )

        if not response['is_status']:
            resp = response['result']

            logger.debug('Received result', {
                'result': uint8array_to_hex(resp),
                'appletId': applet_id,
            })

            return resp

        status = response['result']

        if (
            status.device_idle_state == DeviceIdleState.DEVICE_IDLE_STATE_DEVICE or
            status.current_cmd_seq != sequence_number
        ):
            raise DeviceAppError(DeviceAppErrorType.EXECUTING_OTHER_COMMAND)

        if status.cmd_state in [
            CmdState.CMD_STATE_DONE,
            CmdState.CMD_STATE_FAILED,
            CmdState.CMD_STATE_INVALID_CMD,
        ]:
            raise Exception(
                'Command status is done or rejected, but no output is received'
            )

        if status.device_idle_state == DeviceIdleState.DEVICE_IDLE_STATE_USB:
            if on_status:
                on_status(status)

        await sleep(options.get('interval', 200) if options else 200)