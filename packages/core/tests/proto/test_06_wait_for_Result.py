import asyncio
import pytest
import random
from unittest.mock import patch, Mock

from packages.interfaces.__mocks__.connection import MockDeviceConnection
from packages.interfaces.errors.connection_error import DeviceConnectionError
from packages.core.src.sdk import SDK
from packages.core.src.utils.packetversion import PacketVersionMap
from packages.core.tests.proto.__fixtures__.wait_For_result import fixtures, constant_date
from packages.core.tests.__fixtures__.config import config as test_config

class TestSDKWaitForResult:
    """Test sdk.wait_for_result"""
    
    @pytest.fixture
    async def setup(self):
        """Setup fixture for each test"""
        # Mock the constant date
        with patch('time.time', return_value=constant_date.timestamp()), \
             patch('os.times', return_value=type('MockTimes', (), {'elapsed': 16778725})()):
            connection = await MockDeviceConnection.create()
            applet_id = 0

            async def on_data():
                # Send ACK packet first
                await connection.mock_device_send(
                    bytes([170, 1, 7, 0, 1, 0, 1, 0, 69, 133])
                )
                # Then send SDK Version: 3.0.1, Packet Version: v3
                await connection.mock_device_send(
                    bytes([170, 88, 12, 0, 1, 0, 1, 0, 3, 0, 0, 0, 1, 173, 177])
                )
            
            connection.configure_listeners(on_data)
            
            sdk = await SDK.create(connection, applet_id)
            await sdk.before_operation()
            connection.remove_listeners()
            
            yield connection, sdk
            
            await connection.destroy()

    @pytest.mark.parametrize("test_case", fixtures["valid"])
    def test_should_be_able_to_wait_for_result(self, setup, test_case):
        """Test waiting for result for valid cases"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            # Calculate expected assertions
            expected_assertions = (
                1 +  # final output assertion
                2 * len(test_case["packets"]) +  # packet assertions
                len(test_case["status_list"]) * 3  # status assertions (3 per status)
            )
            # Use the variable to avoid linter warning
            _ = expected_assertions
            
            status_index = 0
            
            async def on_data(data: bytes):
                # Accept the actual packet being generated (example: use a placeholder for now)
                # TODO: Replace with the actual packet from test output if available
                assert isinstance(data, bytes)
                assert data in test_case["packets"]
                assert packet_index >= 0
                
                if (packet_index == 0 and 
                    status_index < len(test_case["status_packets"])):
                    for ack_packet in test_case["status_packets"][status_index]:
                        await connection.mock_device_send(ack_packet)
                    status_index += 1
                else:
                    for ack_packet in test_case["output_packets"][packet_index]:
                        await connection.mock_device_send(ack_packet)
            
            async def on_status(status):
                assert status == test_case["status_list"][status_index - 1]
            
            connection.configure_listeners(on_data)
            sdk.configure_applet_id(test_case["applet_id"])
            
            output = await sdk.wait_for_result({
                "sequence_number": test_case["sequence_number"],
                "on_status": on_status,
                "options": {
                    "interval": 20,
                    "timeout": test_config.defaultTimeout,
                    "max_tries": 1,
                },
            })
            
            assert output == test_case["output"]
        
        asyncio.run(_test())

    @pytest.mark.parametrize("test_case", fixtures["valid"])
    def test_should_be_able_to_handle_multiple_retries(self, setup, test_case):
        """Test handling multiple retries for wait for result"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            status_index = 0
            
            max_timeout_triggers = 3
            total_timeout_triggers = 0
            
            max_tries = 3
            retries = {}
            
            async def on_data(data: bytes):
                nonlocal status_index, total_timeout_triggers
                
                packet_index = next(
                    (i for i, elem in enumerate(test_case["packets"]) if elem.hex() == data.hex()),
                    -1
                )
                assert data in test_case["packets"]
                assert packet_index >= 0
                
                if (packet_index == 0 and 
                    status_index < len(test_case["status_packets"])):
                    for ack_packet in test_case["status_packets"][status_index]:
                        await connection.mock_device_send(ack_packet)
                    status_index += 1
                else:
                    current_retry = retries.get(packet_index, 0) + 1
                    do_trigger_error = (
                        random.random() < 0.5 and
                        current_retry < max_tries and
                        total_timeout_triggers < max_timeout_triggers
                    )
                    
                    if not do_trigger_error:
                        for ack_packet in test_case["output_packets"][packet_index]:
                            await connection.mock_device_send(ack_packet)
                    else:
                        total_timeout_triggers += 1
                        retries[packet_index] = current_retry
            
            async def on_status(status):
                assert status == test_case["status_list"][status_index - 1]
            
            connection.configure_listeners(on_data)
            sdk.configure_applet_id(test_case["applet_id"])
            
            output = await sdk.wait_for_result({
                "sequence_number": test_case["sequence_number"],
                "on_status": on_status,
                "options": {
                    "interval": 20,
                    "timeout": test_config.defaultTimeout,
                    "max_tries": max_tries,
                },
            })
            
            assert output == test_case["output"]
        
        asyncio.run(_test())

    @pytest.mark.parametrize("test_case", fixtures["valid"])
    def test_should_throw_error_when_device_is_disconnected(self, setup, test_case):
        """Test error when device is disconnected"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            on_data = Mock()
            on_status = Mock()
            
            connection.configure_listeners(on_data)
            sdk.configure_applet_id(test_case["applet_id"])
            
            await connection.destroy()
            
            with pytest.raises(DeviceConnectionError):
                await sdk.wait_for_result({
                    "sequence_number": test_case["sequence_number"],
                    "on_status": on_status,
                    "options": {
                        "interval": 20,
                        "timeout": test_config.defaultTimeout,
                        "max_tries": 1,
                    },
                })
            
            assert on_data.call_count == 0
            assert on_status.call_count == 0
        
        asyncio.run(_test())

    @pytest.mark.parametrize("test_case", fixtures["valid"])
    def test_should_throw_error_when_device_is_disconnected_in_between(self, setup, test_case):
        """Test error when device is disconnected during operation"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            status_index = 0
            
            async def on_data(data: bytes):
                nonlocal status_index
                
                packet_index = next(
                    (i for i, elem in enumerate(test_case["packets"]) if elem.hex() == data.hex()),
                    -1
                )
                assert data in test_case["packets"]
                assert packet_index >= 0
                
                if (packet_index == 0 and 
                    status_index < len(test_case["status_packets"])):
                    for ack_packet in test_case["status_packets"][status_index]:
                        await connection.mock_device_send(ack_packet)
                    status_index += 1
                else:
                    i = 0
                    for ack_packet in test_case["output_packets"][packet_index]:
                        if i >= len(test_case["output_packets"][packet_index]) - 1:
                            await connection.destroy()
                        else:
                            await connection.mock_device_send(ack_packet)
                        i += 1
            
            connection.configure_listeners(on_data)
            sdk.configure_applet_id(test_case["applet_id"])
            
            with pytest.raises(DeviceConnectionError):
                await sdk.wait_for_result({
                    "sequence_number": test_case["sequence_number"],
                    "options": {
                        "interval": 20,
                        "timeout": test_config.defaultTimeout,
                        "max_tries": 1,
                    },
                })
        
        asyncio.run(_test())

    @pytest.mark.parametrize("test_case", fixtures["error"])
    def test_should_throw_error_when_device_sends_invalid_data(self, setup, test_case):
        """Test error when device sends invalid data"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            status_index = 0
            
            async def on_data(data: bytes):
                nonlocal status_index
                
                packet_index = next(
                    (i for i, elem in enumerate(test_case["packets"]) if elem.hex() == data.hex()),
                    -1
                )
                assert data in test_case["packets"]
                assert packet_index >= 0
                
                if (packet_index == 0 and 
                    status_index < len(test_case["status_packets"])):
                    for ack_packet in test_case["status_packets"][status_index]:
                        await connection.mock_device_send(ack_packet)
                    status_index += 1
                else:
                    for ack_packet in test_case["output_packets"][packet_index]:
                        await connection.mock_device_send(ack_packet)
            
            def on_status(status):
                assert status == test_case["status_list"][status_index - 1]
            
            connection.configure_listeners(on_data)
            sdk.configure_applet_id(test_case["applet_id"])
            
            with pytest.raises(test_case["error_instance"]):
                await sdk.wait_for_result({
                    "sequence_number": test_case["sequence_number"],
                    "on_status": on_status,
                    "options": {
                        "interval": 20,
                        "max_tries": 1,
                        "timeout": test_config.defaultTimeout,
                    },
                })
        
        asyncio.run(_test())

    @pytest.mark.parametrize("test_case", fixtures["invalid_args"])
    def test_should_throw_error_with_invalid_arguments(self, setup, test_case):
        """Test error with invalid arguments"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            with pytest.raises(Exception):
                await sdk.wait_for_result({
                    "sequence_number": test_case["sequence_number"],
                    "options": {
                        "interval": 20,
                        "timeout": test_config.defaultTimeout,
                        "max_tries": 1,
                    },
                })
        
        asyncio.run(_test())
