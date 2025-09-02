from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from unittest.mock import MagicMock, AsyncMock
import pytest

from packages.app_btc.src.__mocks__ import sdk as sdk_mocks


@dataclass
class QueryData:
    name: str
    data: bytes


@dataclass
class StatusData:
    flow_status: int
    expect_event_calls: Optional[List[int]] = None


@dataclass
class ResultData:
    name: str
    data: bytes
    statuses: Optional[List[StatusData]] = None


@dataclass
class MockData:
    event_calls: Optional[List[List[int]]] = None


@dataclass
class TestCase:
    queries: List[QueryData]
    results: List[ResultData]
    mocks: Optional[MockData] = None


def setup_mocks(test_case: TestCase) -> MagicMock:
    """Setup SDK mocks for test case execution."""
    on_event = MagicMock()
    
    # Mock sendQuery for each query
    for _ in test_case.queries:
        sdk_mocks.send_query.return_value = AsyncMock(return_value=None)()
    
    # Mock waitForResult for each result
    for result in test_case.results:
        async def mock_wait_for_result(params=None):
            if params and hasattr(params, 'on_status') and params.on_status and result.statuses:
                on_event_calls = 0
                
                for status in result.statuses:
                    # Call onStatus with flowStatus
                    await params.on_status({'flow_status': status.flow_status})
                    
                    if status.expect_event_calls is not None:
                        for i, expected_call in enumerate(status.expect_event_calls):
                            mock_index = len(on_event.call_args_list) - len(status.expect_event_calls) + i
                            
                            # Verify the mock call
                            assert on_event.call_args_list[mock_index] == ((expected_call,),)
                        
                        on_event_calls += len(status.expect_event_calls)
                        assert on_event.call_count == on_event_calls
                    else:
                        assert on_event.call_count == on_event_calls
            
            return result.data
        
        sdk_mocks.wait_for_result.side_effect = mock_wait_for_result
    
    return on_event


def clear_mocks() -> None:
    """Clear all SDK mocks."""
    sdk_mocks.reset_mocks()


def expect_mock_calls(test_case: TestCase, on_event: MagicMock) -> None:
    """Verify mock calls match expected test case."""
    # Verify runOperation was called once
    assert sdk_mocks.run_operation.call_count == 1
    
    # Verify sendQuery calls match expected queries
    send_query_calls = [call[0][0] for call in sdk_mocks.send_query.call_args_list]
    expected_query_data = [query.data for query in test_case.queries]
    assert send_query_calls == expected_query_data
    
    # Verify event calls if specified
    if test_case.mocks and test_case.mocks.event_calls:
        actual_calls = [list(call[0]) for call in on_event.call_args_list]
        assert actual_calls == test_case.mocks.event_calls


__all__ = [
    'QueryData',
    'StatusData', 
    'ResultData',
    'MockData',
    'TestCase',
    'setup_mocks',
    'clear_mocks',
    'expect_mock_calls',
]
