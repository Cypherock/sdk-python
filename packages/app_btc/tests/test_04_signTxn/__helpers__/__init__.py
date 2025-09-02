from typing import TYPE_CHECKING
from unittest.mock import MagicMock
from packages.app_btc.tests.__helpers__ import (
    setup_mocks as super_setup_mocks,
    clear_mocks as super_clear_mocks,
    expect_mock_calls as super_expect_mock_calls,
)
from packages.app_btc.src.proto.generated.btc import Query, Result

if TYPE_CHECKING:
    from packages.app_btc.tests.test_04_signTxn.__fixtures__.types import SignTxnTestCase


def setup_mocks(test_case: 'SignTxnTestCase') -> MagicMock:
    """Setup mocks for signTxn test case."""
    return super_setup_mocks(test_case)


def clear_mocks() -> None:
    """Clear all mocks for signTxn tests."""
    super_clear_mocks()


def expect_mock_calls(test_case: 'SignTxnTestCase', on_event: MagicMock) -> None:
    """Verify mock calls for signTxn test case."""
    super_expect_mock_calls(test_case, on_event)


def query_to_bytes(query_data: dict) -> bytes:
    """Convert query data to bytes using protobuf serialization."""
    return Query(**query_data).SerializeToString()


def result_to_bytes(result_data: dict) -> bytes:
    """Convert result data to bytes using protobuf serialization."""
    return Result(**result_data).SerializeToString()


__all__ = [
    'setup_mocks',
    'clear_mocks', 
    'expect_mock_calls',
    'query_to_bytes',
    'result_to_bytes',
]
