from packages.interfaces.errors.app_error import DeviceAppError, DeviceAppErrorType, deviceAppErrorTypeDetails
from .types import GetXpubsTestCase, QueryData, ResultData
from packages.app_btc.src.proto.generated.btc import Query, Result

# Common parameters shared across error test cases
common_params = {
    'params': {
        'wallet_id': bytes([
            199, 89, 252, 26, 32, 135, 183, 211, 90, 220, 38, 17, 160, 103, 233, 62,
            110, 172, 92, 20, 35, 250, 190, 146, 62, 8, 53, 86, 128, 26, 3, 187, 121,
            64,
        ]),
        'derivation_paths': [
            {
                'path': [0x8000002c, 0x80000000, 0x80000000],
            },
        ],
    },
    'queries': [
        QueryData(
            name='Initiate query',
            data=Query(
                get_xpubs=Query.GetXpubs(
                    initiate=Query.GetXpubs.Initiate(
                        wallet_id=bytes([
                            199, 89, 252, 26, 32, 135, 183, 211, 90, 220, 38, 17, 160,
                            103, 233, 62, 110, 172, 92, 20, 35, 250, 190, 146, 62, 8, 53,
                            86, 128, 26, 3, 187, 121, 64,
                        ]),
                        derivation_paths=[
                            Query.GetXpubs.Initiate.DerivationPath(
                                path=[0x8000002c, 0x80000000, 0x80000000],
                            ),
                        ],
                    )
                )
            ).SerializeToString()
        )
    ],
}

with_unknown_error = GetXpubsTestCase(
    name='With unknown error',
    params=common_params['params'],
    queries=common_params['queries'],
    results=[
        ResultData(
            name='error',
            data=Result(
                common_error=Result.CommonError(
                    unknown_error=1
                )
            ).SerializeToString()
        )
    ],
    error_instance=DeviceAppError,
    error_message=deviceAppErrorTypeDetails[DeviceAppErrorType.UNKNOWN_ERROR]['message'],
)

with_invalid_app_id = GetXpubsTestCase(
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

error_fixtures = [
    with_unknown_error,
    with_invalid_app_id,
]

__all__ = ['error_fixtures']
