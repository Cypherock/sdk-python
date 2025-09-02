from packages.interfaces.errors.app_error import DeviceAppError, DeviceAppErrorType, deviceAppErrorTypeDetails
from .types import GetPublicKeyTestCase, QueryData, ResultData
from packages.app_btc.src.proto.generated.btc import Query, Result
from packages.app_btc.src.proto.generated.error import CardError

# Common parameters shared across error test cases
common_params = {
    'params': {
        'wallet_id': bytes([10]),
        'derivation_path': [0x80000000 + 44, 0x80000000, 0x80000000, 0, 0],
    },
    'queries': [
        QueryData(
            name='Initiate query',
            data=Query(
                get_public_key=Query.GetPublicKey(
                    initiate=Query.GetPublicKey.Initiate(
                        wallet_id=bytes([10]),
                        derivation_path=[0x8000002c, 0x80000000, 0x80000000, 0, 0],
                    )
                )
            ).SerializeToString()
        )
    ],
}

with_unknown_error = GetPublicKeyTestCase(
    name='With unknown error',
    params=common_params['params'],
    queries=common_params['queries'],
    results=[
        ResultData(
            name='error',
            data=bytes([10, 4, 18, 2, 8, 0])
        )
    ],
    error_instance=DeviceAppError,
    error_message=deviceAppErrorTypeDetails[DeviceAppErrorType.UNKNOWN_ERROR]['message'],
)

with_invalid_app_id = GetPublicKeyTestCase(
    name='With invalid msg from device',
    params=common_params['params'],
    queries=common_params['queries'],
    results=[
        ResultData(
            name='error',
            data=Result().SerializeToString()
        )
    ],
    error_instance=DeviceAppError,
    error_message=deviceAppErrorTypeDetails[DeviceAppErrorType.INVALID_MSG_FROM_DEVICE]['message'],
)

with_card_error = GetPublicKeyTestCase(
    name='With card error from device',
    params=common_params['params'],
    queries=common_params['queries'],
    results=[
        ResultData(
            name='error',
            data=Result(
                common_error=Result.CommonError(
                    card_error=CardError.CARD_ERROR_SW_FILE_INVALID
                )
            ).SerializeToString()
        )
    ],
    error_instance=DeviceAppError,
    error_message=deviceAppErrorTypeDetails[DeviceAppErrorType.CARD_OPERATION_FAILED]['sub_error'][CardError.CARD_ERROR_SW_FILE_INVALID]['message'],
)

error_fixtures = [
    with_unknown_error,
    with_invalid_app_id,
    with_card_error,
]

__all__ = ['error_fixtures']
