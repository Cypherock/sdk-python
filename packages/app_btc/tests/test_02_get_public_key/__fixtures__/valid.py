from packages.util.utils import create_flow_status
from .types import GetPublicKeyTestCase, QueryData, ResultData, StatusData, MockData
from packages.app_btc.src.proto.generated.btc import Query

request_address = GetPublicKeyTestCase(
    name='Request Address',
    params={
        'wallet_id': bytes([
            199, 89, 252, 26, 32, 135, 183, 211, 90, 220, 38, 17, 160, 103, 233, 62,
            110, 172, 92, 20, 35, 250, 190, 146, 62, 8, 53, 86, 128, 26, 3, 187, 121,
            64,
        ]),
        'derivation_path': [0x80000000 + 44, 0x80000000, 0x80000000, 0, 0],
    },
    queries=[
        QueryData(
            name='Initiate query',
            data=Query(
                get_public_key=Query.GetPublicKey(
                    initiate=Query.GetPublicKey.Initiate(
                        wallet_id=bytes([
                            199, 89, 252, 26, 32, 135, 183, 211, 90, 220, 38, 17, 160,
                            103, 233, 62, 110, 172, 92, 20, 35, 250, 190, 146, 62, 8, 53,
                            86, 128, 26, 3, 187, 121, 64,
                        ]),
                        derivation_path=[0x80000000 + 44, 0x80000000, 0x80000000, 0, 0],
                    )
                )
            ).SerializeToString()
        )
    ],
    results=[
        ResultData(
            name='result',
            data=bytes([
                10, 37, 10, 35, 10, 33, 3, 41, 155, 232, 126, 245, 18, 49, 110, 235,
                225, 178, 60, 48, 53, 109, 26, 117, 222, 193, 192, 185, 147, 11, 59,
                191, 155, 17, 129, 230, 183, 171, 92,
            ]),
            statuses=[
                StatusData(
                    flow_status=create_flow_status(0, 0),
                    expect_event_calls=[0],
                ),
                StatusData(
                    flow_status=create_flow_status(1, 0),
                    expect_event_calls=[1],
                ),
                StatusData(
                    flow_status=create_flow_status(2, 1),
                    expect_event_calls=[2],
                ),
            ],
        )
    ],
    mocks=MockData(event_calls=[[0], [1], [2], [3], [4]]),
    output={
        'public_key': bytes([
            3, 41, 155, 232, 126, 245, 18, 49, 110, 235, 225, 178, 60, 48, 53, 109,
            26, 117, 222, 193, 192, 185, 147, 11, 59, 191, 155, 17, 129, 230, 183,
            171, 92,
        ]),
        'address': '1B87oKEs97mnEC9zi2Pkn8BNT9cAExEqYF',
    },
)

valid_fixtures = [request_address]

__all__ = ['valid_fixtures']
