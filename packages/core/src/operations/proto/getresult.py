from typing import Optional, Union, Dict
from packages.interfaces.errors.app_error import DeviceAppError, DeviceAppErrorType
from packages.interfaces import IDeviceConnection
from packages.util.utils.assert_utils import assert_condition
from packages.util.utils.crypto import hex_to_uint8array
from packages.core.src.utils.packetversion import PacketVersion
from packages.core.src.operations.helpers.getcommandoutput import get_command_output
from packages.core.src.encoders.proto.generated.core import Status, Msg, ErrorType


async def get_result(
    connection: IDeviceConnection,
    version: PacketVersion,
    sequence_number: int,
    applet_id: int,
    max_tries: int = 5,
    timeout: Optional[int] = None,
    allow_core_data: Optional[bool] = None
) -> Dict[str, Union[bool, Union[Status, bytes]]]:
    assert_condition(applet_id, 'Invalid appletId')

    command_output = await get_command_output(
        connection=connection,
        version=version,
        max_tries=max_tries,
        sequence_number=sequence_number,
        timeout=timeout
    )

    is_status = command_output["is_status"]
    protobuf_data = command_output["protobuf_data"]
    raw_data = command_output["raw_data"]

    output: Union[bytes, Status]
    
    if is_status:
        status = Status.parse(hex_to_uint8array(protobuf_data))
        if status.current_cmd_seq != sequence_number:
            raise DeviceAppError(DeviceAppErrorType.EXECUTING_OTHER_COMMAND)
        output = status
    else:
        msg = Msg.parse(hex_to_uint8array(protobuf_data))
        
        if msg.error:
            error_map = {
                ErrorType.NO_ERROR: DeviceAppErrorType.UNKNOWN_ERROR,
                ErrorType.UNRECOGNIZED: DeviceAppErrorType.UNKNOWN_ERROR,
                ErrorType.UNKNOWN_APP: DeviceAppErrorType.UNKNOWN_APP,
                ErrorType.INVALID_MSG: DeviceAppErrorType.INVALID_MSG,
                ErrorType.APP_NOT_ACTIVE: DeviceAppErrorType.APP_NOT_ACTIVE,
                ErrorType.APP_TIMEOUT_OCCURRED: DeviceAppErrorType.APP_TIMEOUT,
                ErrorType.DEVICE_SESSION_INVALID: DeviceAppErrorType.DEVICE_SESSION_INVALID,
            }
            raise DeviceAppError(error_map[msg.error.type])
        
        output = bytes()
        
        if not allow_core_data or msg.cmd:
            if not msg.cmd:
                raise DeviceAppError(DeviceAppErrorType.INVALID_MSG_FROM_DEVICE)
            
            if msg.cmd.applet_id != applet_id:
                raise DeviceAppError(DeviceAppErrorType.INVALID_APP_ID_FROM_DEVICE)
            
            output = hex_to_uint8array(raw_data)
        else:
            output = hex_to_uint8array(protobuf_data)

    return {"is_status": is_status, "result": output}
