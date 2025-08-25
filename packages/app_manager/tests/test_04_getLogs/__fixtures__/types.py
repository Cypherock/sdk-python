from typing import List, Any, Optional, TypedDict


class IGetLogsQuery(TypedDict):
    name: str
    data: bytes


class IGetLogsResultStatus(TypedDict, total=False):
    flowStatus: int
    expectEventCalls: Optional[List[int]]


class IGetLogsResult(TypedDict, total=False):
    name: str
    data: bytes
    statuses: Optional[List[IGetLogsResultStatus]]


class IGetLogsMocks(TypedDict, total=False):
    eventCalls: Optional[List[List[int]]]


class IGetLogsTestCase(TypedDict, total=False):
    name: str
    queries: List[IGetLogsQuery]
    results: List[IGetLogsResult]
    mocks: Optional[IGetLogsMocks]
    errorInstance: Optional[Any]
    errorMessage: Optional[str]
    output: Optional[str]


class IFixtures(TypedDict):
    valid: List[IGetLogsTestCase]
    invalidData: List[IGetLogsTestCase]
    error: List[IGetLogsTestCase]
