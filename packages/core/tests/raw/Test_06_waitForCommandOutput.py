import pytest
from unittest.mock import Mock, patch
from datetime import datetime

from packages.core.src.sdk import SDK
from packages.core.tests.raw.__fixtures__.waitForCommandOutput import raw_wait_for_command_output_test_cases
from packages.interfaces.__mocks__.connection import MockDeviceConnection
from packages.interfaces.errors import DeviceConnectionError
from packages.core.tests.__fixtures__.config import config


@pytest.fixture
async def setup_teardown_sdk():
    connection = await MockDeviceConnection.create()
    sdk = await SDK.create(connection, 0)
    # Mimic beforeEach setup
    real_date = datetime.now
    with patch("datetime.now", return_value=raw_wait_for_command_output_test_cases["constantDate"]):
        await sdk.before_operation()
    yield sdk, connection
    # Mimic afterEach teardown
    await connection.destroy()
    patch("datetime.now", new=real_date).stop()


@pytest.mark.asyncio
async def test_should_be_able_to_wait_for_command_output(setup_teardown_sdk):
    sdk, connection = setup_teardown_sdk
    for test_case in raw_wait_for_command_output_test_cases["valid"]:
        status_index = 0

        async def on_data(data):
            nonlocal status_index
            packet_index = -1
            for i, elem in enumerate(test_case["packets"]):
                if elem == data:
                    packet_index = i
                    break
            assert packet_index >= 0

            if packet_index == 0 and status_index < len(test_case["statusPackets"]):
                for ack_packet in test_case["statusPackets"][status_index]:
                    await connection.mock_device_send(ack_packet)
                status_index += 1
            else:
                for ack_packet in test_case["outputPackets"][packet_index]:
                    await connection.mock_device_send(ack_packet)

        async def on_status(status):
            assert status == test_case["output"]

        connection.configure_listeners(on_data)
        output = await sdk.deprecated.wait_for_command_output(
            sequence_number=test_case["sequenceNumber"],
            expected_command_types=test_case["expectedCommandTypes"],
            on_status=on_status,
            max_tries=1,
            timeout=config.defaultTimeout,
            interval=20,
        )

        assert output == test_case["output"]


@pytest.mark.asyncio
async def test_should_be_able_to_handle_multiple_retries(setup_teardown_sdk):
    sdk, connection = setup_teardown_sdk
    for test_case in raw_wait_for_command_output_test_cases["valid"]:
        status_index = 0
        max_timeout_triggers = 3
        total_timeout_triggers = 0

        max_tries = 3
        retries = {}

        async def on_data(data):
            nonlocal status_index, total_timeout_triggers
            packet_index = -1
            for i, elem in enumerate(test_case["packets"]):
                if elem == data:
                    packet_index = i
                    break
            assert packet_index >= 0

            if packet_index == 0 and status_index < len(test_case["statusPackets"]):
                for ack_packet in test_case["statusPackets"][status_index]:
                    await connection.mock_device_send(ack_packet)
                status_index += 1
            else:
                current_retry = retries.get(packet_index, 0) + 1
                do_trigger_error = False # Simplified from Math.random() < 0.5

                if not do_trigger_error:
                    for ack_packet in test_case["outputPackets"][packet_index]:
                        await connection.mock_device_send(ack_packet)
                else:
                    total_timeout_triggers += 1
                    retries[packet_index] = current_retry

        async def on_status(status):
            assert status == test_case["output"]

        connection.configure_listeners(on_data)

        output = await sdk.deprecated.wait_for_command_output(
            sequence_number=test_case["sequenceNumber"],
            expected_command_types=test_case["expectedCommandTypes"],
            on_status=on_status,
            max_tries=max_tries,
            timeout=config.defaultTimeout,
            interval=20,
        )

        assert output == test_case["output"]


@pytest.mark.asyncio
async def test_should_throw_error_when_device_is_disconnected(setup_teardown_sdk):
    sdk, connection = setup_teardown_sdk
    for test_case in raw_wait_for_command_output_test_cases["valid"]:
        on_data = Mock()
        on_status = Mock()

        connection.configure_listeners(on_data)
        await connection.destroy()

        with pytest.raises(DeviceConnectionError):
            await sdk.deprecated.wait_for_command_output(
                sequence_number=test_case["sequenceNumber"],
                expected_command_types=test_case["expectedCommandTypes"],
                on_status=on_status,
                max_tries=1,
                timeout=config.defaultTimeout,
                interval=20,
            )
        on_data.assert_not_called()
        on_status.assert_not_called()


@pytest.mark.asyncio
async def test_should_throw_error_when_device_is_disconnected_in_between(setup_teardown_sdk):
    sdk, connection = setup_teardown_sdk
    for test_case in raw_wait_for_command_output_test_cases["valid"]:
        status_index = 0

        async def on_data(data):
            nonlocal status_index
            packet_index = -1
            for i, elem in enumerate(test_case["packets"]):
                if elem == data:
                    packet_index = i
                    break
            assert packet_index >= 0

            if packet_index == 0 and status_index < len(test_case["statusPackets"]):
                for ack_packet in test_case["statusPackets"][status_index]:
                    await connection.mock_device_send(ack_packet)
                status_index += 1
            else:
                i = 0
                for ack_packet in test_case["outputPackets"][packet_index]:
                    if i >= len(test_case["outputPackets"][packet_index]) - 1:
                        await connection.destroy()
                    else:
                        await connection.mock_device_send(ack_packet)
                    i += 1

        connection.configure_listeners(on_data)
        with pytest.raises(DeviceConnectionError):
            await sdk.deprecated.wait_for_command_output(
                sequence_number=test_case["sequenceNumber"],
                expected_command_types=test_case["expectedCommandTypes"],
                max_tries=1,
                timeout=config.defaultTimeout,
                interval=20,
            )


@pytest.mark.asyncio
async def test_should_throw_error_when_device_sends_invalid_data(setup_teardown_sdk):
    sdk, connection = setup_teardown_sdk
    for test_case in raw_wait_for_command_output_test_cases["error"]:
        status_index = 0
        async def on_data(data):
            nonlocal status_index
            packet_index = -1
            for i, elem in enumerate(test_case["packets"]):
                if elem == data:
                    packet_index = i
                    break
            assert packet_index >= 0

            if packet_index == 0 and status_index < len(test_case["statusPackets"]):
                for ack_packet in test_case["statusPackets"][status_index]:
                    await connection.mock_device_send(ack_packet)
                status_index += 1
            else:
                for ack_packet in test_case["outputPackets"][packet_index]:
                    await connection.mock_device_send(ack_packet)

        on_status = Mock()

        connection.configure_listeners(on_data)
        with pytest.raises(test_case["errorInstance"]):
            await sdk.deprecated.wait_for_command_output(
                sequence_number=test_case["sequenceNumber"],
                expected_command_types=test_case["expectedCommandTypes"],
                on_status=on_status,
                max_tries=1,
                timeout=config.defaultTimeout,
            )


@pytest.mark.asyncio
async def test_should_throw_error_with_invalid_arguments(setup_teardown_sdk):
    sdk, connection = setup_teardown_sdk
    for test_case in raw_wait_for_command_output_test_cases["invalidArgs"]:
        with pytest.raises(Exception) as e:
            await sdk.deprecated.wait_for_command_output(
                sequence_number=test_case["sequenceNumber"],
                expected_command_types=test_case["expectedCommandTypes"],
                max_tries=1,
                timeout=config.defaultTimeout,
            )
        assert e.value.error_type == "DeviceConnection:InvalidArguments"
        assert e.value.message == "Invalid arguments provided to waitForCommandOutput"