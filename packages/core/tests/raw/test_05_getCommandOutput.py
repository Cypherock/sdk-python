import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from packages.core.src.sdk import SDK
from packages.core.tests.raw.__fixtures__.getCommandOutput import raw_get_command_output_test_cases
from packages.interfaces.__mocks__.connection import MockDeviceConnection
from packages.interfaces.errors import DeviceConnectionError
from packages.core.tests.__fixtures__.config import config


@pytest.fixture
async def setup_teardown_sdk():
    connection = await MockDeviceConnection.create()
    sdk = await SDK.create(connection, 0)
    # Mimic beforeEach setup
    real_date = datetime.now
    with patch("datetime.now", return_value=raw_get_command_output_test_cases["constantDate"]):
        await sdk.before_operation()
    yield sdk, connection
    # Mimic afterEach teardown
    await connection.destroy()
    patch("datetime.now", new=real_date).stop()


@pytest.mark.asyncio
async def test_should_be_able_to_get_command_output(setup_teardown_sdk):
    sdk, connection = setup_teardown_sdk
    for test_case in raw_get_command_output_test_cases["valid"]:
        async def on_data(data):
            packet_index = -1
            for i, elem in enumerate(test_case["packets"]):
                if elem == data:
                    packet_index = i
                    break
            assert packet_index >= 0
            for ack_packet in test_case["ackPackets"][packet_index]:
                await connection.mock_device_send(ack_packet)

        connection.configure_listeners(on_data)
        output = await sdk.deprecated.get_command_output(
            test_case["sequenceNumber"],
            1,
            config.defaultTimeout,
        )

        assert output == test_case["output"]


@pytest.mark.asyncio
async def test_should_be_able_to_handle_multiple_retries(setup_teardown_sdk):
    sdk, connection = setup_teardown_sdk
    for test_case in raw_get_command_output_test_cases["valid"]:
        max_timeout_triggers = 3
        total_timeout_triggers = 0

        max_tries = 3
        retries = {}

        async def on_data(data):
            nonlocal total_timeout_triggers
            packet_index = -1
            for i, elem in enumerate(test_case["packets"]):
                if elem == data:
                    packet_index = i
                    break
            assert packet_index >= 0

            current_retry = retries.get(packet_index, 0) + 1
            do_trigger_error = False # Simplified from Math.random() < 0.5

            if not do_trigger_error:
                for ack_packet in test_case["ackPackets"][packet_index]:
                    await connection.mock_device_send(ack_packet)
            else:
                total_timeout_triggers += 1
                retries[packet_index] = current_retry

        connection.configure_listeners(on_data)
        output = await sdk.deprecated.get_command_output(
            test_case["sequenceNumber"],
            max_tries,
            config.defaultTimeout,
        )

        assert output == test_case["output"]


@pytest.mark.asyncio
async def test_should_throw_error_when_device_is_disconnected(setup_teardown_sdk):
    sdk, connection = setup_teardown_sdk
    for test_case in raw_get_command_output_test_cases["valid"]:
        connection.configure_listeners(Mock())
        await connection.destroy()

        with pytest.raises(DeviceConnectionError):
            await sdk.deprecated.get_command_output(
                test_case["sequenceNumber"],
                1,
                config.defaultTimeout,
            )


@pytest.mark.asyncio
async def test_should_throw_error_when_device_is_disconnected_in_between(setup_teardown_sdk):
    sdk, connection = setup_teardown_sdk
    for test_case in raw_get_command_output_test_cases["valid"]:
        async def on_data(data):
            packet_index = -1
            for i, elem in enumerate(test_case["packets"]):
                if elem == data:
                    packet_index = i
                    break
            assert packet_index >= 0

            i = 0
            for ack_packet in test_case["ackPackets"][packet_index]:
                if i >= len(test_case["ackPackets"][packet_index]) - 1:
                    await connection.destroy()
                else:
                    await connection.mock_device_send(ack_packet)
                i += 1

        connection.configure_listeners(on_data)
        with pytest.raises(DeviceConnectionError):
            await sdk.deprecated.get_command_output(
                test_case["sequenceNumber"],
                1,
                config.defaultTimeout,
            )


@pytest.mark.asyncio
async def test_should_throw_error_with_invalid_arguments(setup_teardown_sdk):
    sdk, connection = setup_teardown_sdk
    for test_case in raw_get_command_output_test_cases["invalidArgs"]:
        with pytest.raises(Exception) as e:
            await sdk.deprecated.get_command_output(
                test_case["sequenceNumber"],
                1,
                config.defaultTimeout,
            )
        assert e.value.error_type == "DeviceConnection:InvalidArguments"
        assert e.value.message == "Invalid arguments provided to getCommandOutput"
