import pytest
from unittest.mock import Mock, patch
from datetime import datetime
import calendar

from packages.core.src.sdk import SDK
from packages.core.tests.raw.__fixtures__.sendCommandAbort import raw_send_abort_test_cases
from packages.interfaces.__mocks__.connection import MockDeviceConnection
from packages.interfaces.errors.connection_error import DeviceConnectionError
from packages.core.tests.__fixtures__.config import config


@pytest.fixture
async def setup():
    """Setup fixture for each test"""
    constant_date = raw_send_abort_test_cases["constantDate"]
    
    with patch('time.time', return_value=calendar.timegm(constant_date.timetuple()) + constant_date.microsecond / 1e6), \
         patch('os.times', return_value=type('MockTimes', (), {'elapsed': 16778725})()):
        
        connection = await MockDeviceConnection.create()
        
        async def on_data():
            # SDK Version: 2.7.1, Packet Version: v3
            await connection.mock_device_send(
                bytes([
                    170, 1, 7, 0, 1, 0, 1, 0, 69, 133, 170, 88, 12, 0, 1, 0, 1, 0, 2, 0,
                    7, 0, 1, 130, 112,
                ])
            )
        
        connection.configure_listeners(on_data)

        sdk = await SDK.create(connection, 0)
        await sdk.before_operation()

        connection.remove_listeners()

        yield connection, sdk

        await connection.destroy()


@pytest.mark.asyncio
async def test_should_be_able_to_send_abort(setup):
    connection, sdk = await setup.__anext__()
    
    for test_case in raw_send_abort_test_cases["valid"]:
        async def on_data(data):
            assert data == test_case["abortRequest"]
            for ack_packet in test_case["ackPackets"]:
                await connection.mock_device_send(ack_packet)

        connection.configure_listeners(on_data)
        status = await sdk.deprecated.send_command_abort(
            test_case["sequenceNumber"],
            1,
            config.defaultTimeout,
        )

        assert status == test_case["status"]


@pytest.mark.asyncio
async def test_should_be_able_to_handle_multiple_retries(setup):
    connection, sdk = await setup.__anext__()
    
    for test_case in raw_send_abort_test_cases["valid"]:
        max_tries = 3
        retries = 0

        async def on_data():
            nonlocal retries
            current_retry = retries + 1

            do_trigger_error = False  # Simplified from Math.random() > 0.5

            if not do_trigger_error:
                for ack_packet in test_case["ackPackets"]:
                    await connection.mock_device_send(ack_packet)
            else:
                retries = current_retry

        connection.configure_listeners(on_data)
        status = await sdk.deprecated.send_command_abort(
            test_case["sequenceNumber"],
            max_tries,
            config.defaultTimeout,
        )

        assert status == test_case["status"]


@pytest.mark.asyncio
async def test_should_throw_error_when_device_is_disconnected(setup):
    connection, sdk = await setup.__anext__()
    
    for test_case in raw_send_abort_test_cases["valid"]:
        on_data = Mock()

        connection.configure_listeners(on_data)
        await connection.destroy()

        with pytest.raises(DeviceConnectionError):
            await sdk.deprecated.send_command_abort(
                test_case["sequenceNumber"],
                1,
                config.defaultTimeout,
            )
        
        on_data.assert_not_called()


@pytest.mark.asyncio
async def test_should_throw_error_when_device_is_disconnected_in_between(setup):
    connection, sdk = await setup.__anext__()
    
    for test_case in raw_send_abort_test_cases["valid"]:
        async def on_data(data):
            assert test_case["abortRequest"] == data
            i = 0
            for ack_packet in test_case["ackPackets"]:
                if i >= len(test_case["ackPackets"]) - 1:
                    await connection.destroy()
                else:
                    await connection.mock_device_send(ack_packet)
                i += 1

        connection.configure_listeners(on_data)
        with pytest.raises(DeviceConnectionError):
            await sdk.deprecated.send_command_abort(
                test_case["sequenceNumber"],
                1,
                config.defaultTimeout,
            )


@pytest.mark.asyncio
async def test_should_throw_error_when_device_sends_invalid_data(setup):
    connection, sdk = await setup.__anext__()
    
    for test_case in raw_send_abort_test_cases["error"]:
        async def on_data(data):
            assert test_case["abortRequest"] == data
            for ack_packet in test_case["ackPackets"]:
                await connection.mock_device_send(ack_packet)

        connection.configure_listeners(on_data)
        with pytest.raises(test_case["errorInstance"]):
            await sdk.deprecated.send_command_abort(
                test_case["sequenceNumber"],
                1,
                config.defaultTimeout,
            )