from typing import TypeVar, Optional, Dict
from packages.interfaces import DeviceAppErrorType, DeviceAppError
from packages.util.utils.assert_utils import assert_condition

from ..encoders.proto.generated.types import ICommonError

T = TypeVar('T')


def assert_or_throw_invalid_result(condition: T) -> T:
    assert_condition(
        condition is not None,
        DeviceAppError(DeviceAppErrorType.INVALID_MSG_FROM_DEVICE)
    )
    return condition


def parse_common_error(error: Optional[ICommonError]) -> None:
    if error is None:
        return

    error_types_map: Dict[str, DeviceAppErrorType] = {
        'unknown_error': DeviceAppErrorType.UNKNOWN_ERROR,
        'device_setup_required': DeviceAppErrorType.DEVICE_SETUP_REQUIRED,
        'wallet_not_found': DeviceAppErrorType.WALLET_NOT_FOUND,
        'wallet_partial_state': DeviceAppErrorType.WALLET_PARTIAL_STATE,
        'card_error': DeviceAppErrorType.CARD_OPERATION_FAILED,
        'user_rejection': DeviceAppErrorType.USER_REJECTION,
        'corrupt_data': DeviceAppErrorType.CORRUPT_DATA,
    }

    for key in error.__dict__:
        value = getattr(error, key)
        if value is not None and key in error_types_map:
            raise DeviceAppError(error_types_map[key], value)

