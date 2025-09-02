from packages.interfaces.errors.app_error import DeviceAppError, DeviceAppErrorType, deviceAppErrorTypeDetails
from .types import GetPublicKeyTestCase, QueryData, ResultData
from packages.app_btc.src.proto.generated.btc import Query

# Common parameters for invalid data tests
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
                        derivation_path=[0x80000000 + 44, 0x80000000, 0x80000000, 0, 0],
                    )
                )
            ).SerializeToString()
        )
    ],
    'error_instance': DeviceAppError,
    'error_message': deviceAppErrorTypeDetails[DeviceAppErrorType.INVALID_MSG_FROM_DEVICE]['message'],
}

invalid_data_fixtures = [
    GetPublicKeyTestCase(
        name='Invalid data',
        results=[
            ResultData(
                name='error',
                data=bytes([
                    109, 112, 102, 98, 72, 57, 117, 109, 75, 69, 83, 117, 117, 49, 103,
                    78, 100, 105, 87, 83, 116, 106, 71, 54, 67, 110, 104, 77, 86, 49, 113,
                    97, 78, 111, 50, 98, 118, 52, 67, 113, 72, 122, 120, 85, 98, 53, 86,
                    68, 115, 86, 52, 77, 86, 112, 83, 70, 86, 78, 121, 121, 109, 83, 112,
                    98, 74, 76, 55, 57, 75, 89, 86, 57, 75, 56, 88, 82, 100, 105, 98, 70,
                    109, 118, 54, 116, 86, 54, 116, 50, 122, 52, 100, 87, 110, 111, 110,
                    78, 52, 78, 77, 89, 109,
                ])
            )
        ],
        **common_params
    ),
    GetPublicKeyTestCase(
        name='Invalid data',
        results=[
            ResultData(
                name='error',
                data=bytes([
                    10, 34, 10, 3, 90, 221, 135, 18, 2, 8, 1, 24, 1, 34, 11, 8, 2, 18, 7,
                    8,
                ])
            )
        ],
        **common_params
    ),
    GetPublicKeyTestCase(
        name='Invalid data',
        results=[
            ResultData(
                name='error',
                data=bytes([10])
            )
        ],
        **common_params
    ),
    GetPublicKeyTestCase(
        name='Invalid data',
        results=[
            ResultData(
                name='error',
                data=bytes([])
            )
        ],
        **common_params
    ),
]

__all__ = ['invalid_data_fixtures']
