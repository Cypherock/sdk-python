from packages.util.utils import create_flow_status
from .types import GetXpubsTestCase, QueryData, ResultData, StatusData, MockData
from packages.app_btc.src.proto.generated.btc import Query, Result

request_one_xpub = GetXpubsTestCase(
    name='Request 1 xpub',
    params={
        'wallet_id': bytes([
            199, 89, 252, 26, 32, 135, 183, 211, 90, 220, 38, 17, 160, 103, 233, 62,
            110, 172, 92, 20, 35, 250, 190, 146, 62, 8, 53, 86, 128, 26, 3, 187, 121,
            64,
        ]),
        'derivation_paths': [
            {
                'path': [0x80000000 + 44, 0x80000000, 0x80000000],
            },
        ],
    },
    queries=[
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
                                path=[0x80000000 + 44, 0x80000000, 0x80000000],
                            ),
                        ],
                    )
                )
            ).SerializeToString()
        )
    ],
    results=[
        ResultData(
            name='result',
            data=Result(
                get_xpubs=Result.GetXpubs(
                    result=Result.GetXpubs.Result(
                        xpubs=[
                            'xpub6BsXdv4PfBcemMJH8Pea913XswhLexTZQFSbRBbSaJ8jkpyi26r4qA9WALLLSYxiNRp8YiSwPqMuJGCyN6sRWRptY41SAS1Bha2u2yLvGks',
                        ],
                    )
                )
            ).SerializeToString(),
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
    mocks=MockData(event_calls=[[0], [1], [2], [3]]),
    output={
        'xpubs': [
            'xpub6BsXdv4PfBcemMJH8Pea913XswhLexTZQFSbRBbSaJ8jkpyi26r4qA9WALLLSYxiNRp8YiSwPqMuJGCyN6sRWRptY41SAS1Bha2u2yLvGks',
        ],
    },
)

request_four_xpubs = GetXpubsTestCase(
    name='Request 4 xpubs',
    params={
        'wallet_id': bytes([
            199, 89, 252, 26, 32, 135, 183, 211, 90, 220, 38, 17, 160, 103, 233, 62,
            110, 172, 92, 20, 35, 250, 190, 146, 62, 8, 53, 86, 128, 26, 3, 187, 121,
            64,
        ]),
        'derivation_paths': [
            {
                'path': [0x80000000 + 44, 0x80000000, 0x80000000],
            },
            {
                'path': [0x80000000 + 44, 0x80000000, 0x80000000 + 1],
            },
            {
                'path': [0x80000000 + 44, 0x80000000, 0x80000000 + 2],
            },
            {
                'path': [0x80000000 + 44, 0x80000000, 0x80000000 + 3],
            },
        ],
    },
    queries=[
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
                                path=[0x80000000 + 44, 0x80000000, 0x80000000],
                            ),
                            Query.GetXpubs.Initiate.DerivationPath(
                                path=[0x80000000 + 44, 0x80000000, 0x80000000 + 1],
                            ),
                            Query.GetXpubs.Initiate.DerivationPath(
                                path=[0x80000000 + 44, 0x80000000, 0x80000000 + 2],
                            ),
                            Query.GetXpubs.Initiate.DerivationPath(
                                path=[0x80000000 + 44, 0x80000000, 0x80000000 + 3],
                            ),
                        ],
                    )
                )
            ).SerializeToString()
        )
    ],
    results=[
        ResultData(
            name='result',
            data=Result(
                get_xpubs=Result.GetXpubs(
                    result=Result.GetXpubs.Result(
                        xpubs=[
                            'xpub6BsXdv4PfBcemMJH8Pea913XswhLexTZQFSbRBbSaJ8jkpyi26r4qA9WALLLSYxiNRp8YiSwPqMuJGCyN6sRWRptY41SAS1Bha2u2yLvGks',
                            'xpub6BsXdv4PfBceoqbjdgUr2WonPfBm7VHN64kxdzBjBvhcP7KWLRKLRM4MpvQJP5cHfJeJw5BbJNsGtnKCEdQwaZvVP4cbgb15XRS9oi4wj8J',
                            'xpub6BsXdv4PfBcese3x7arVEtwB5PoLn1pdLGjNTfpY2fTDX9VBFVRRjQA76MU8GL1Xbc8HHogjzLMjpCfMnBN9qKsbvvYTCnT7f23yHbXCNPf',
                            'xpub6BsXdv4PfBceujuiTDrhP3dQ3MRk7qRAdEdKhfJmvqPSqN2g9naZ79ZNxRHSSrea3eJEHpusbXMBHCnxuvFtTWqm8aJciNHgXUooXpfFd7U',
                        ],
                    )
                )
            ).SerializeToString(),
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
    mocks=MockData(event_calls=[[0], [1], [2], [3]]),
    output={
        'xpubs': [
            'xpub6BsXdv4PfBcemMJH8Pea913XswhLexTZQFSbRBbSaJ8jkpyi26r4qA9WALLLSYxiNRp8YiSwPqMuJGCyN6sRWRptY41SAS1Bha2u2yLvGks',
            'xpub6BsXdv4PfBceoqbjdgUr2WonPfBm7VHN64kxdzBjBvhcP7KWLRKLRM4MpvQJP5cHfJeJw5BbJNsGtnKCEdQwaZvVP4cbgb15XRS9oi4wj8J',
            'xpub6BsXdv4PfBcese3x7arVEtwB5PoLn1pdLGjNTfpY2fTDX9VBFVRRjQA76MU8GL1Xbc8HHogjzLMjpCfMnBN9qKsbvvYTCnT7f23yHbXCNPf',
            'xpub6BsXdv4PfBceujuiTDrhP3dQ3MRk7qRAdEdKhfJmvqPSqN2g9naZ79ZNxRHSSrea3eJEHpusbXMBHCnxuvFtTWqm8aJciNHgXUooXpfFd7U',
        ],
    },
)

valid_fixtures = [request_one_xpub, request_four_xpubs]

__all__ = ['valid_fixtures']
