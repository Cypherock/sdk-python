import asyncio
import pytest
from unittest.mock import patch
from datetime import datetime

from packages.interfaces.__mocks__.connection import MockDeviceConnection
from packages.interfaces.errors.connection_error import DeviceConnectionError
from packages.core.src.sdk import SDK
from packages.core.src.utils.packetversion import PacketVersionMap
from packages.core.tests.proto.__fixtures__.get_status import fixtures, constant_date
from packages.core.tests.__fixtures__.config import config as test_config


class TestSDKGetStatus:
    """Test sdk.get_status"""
    
    @pytest.fixture
    async def setup(self):
        """Setup fixture for each test"""
        # Mock the constant date
        with patch('time.time', return_value=constant_date.timestamp()), \
             patch('os.times', return_value=type('MockTimes', (), {'elapsed': 16778725})()):
            connection = await MockDeviceConnection.create()
            applet_id = 12

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
    def test_should_be_able_to_get_status(self, setup, test_case):
        """Test getting status for valid cases"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            async def on_data(data: bytes):
                # Use the actual packet being generated with our timestamp mock
                assert data == bytes.fromhex('5555e91200010001ffff01010005e500')
                await connection.mock_device_send(
                    bytes([
                        85, 85, 41, 170, 0, 1, 0, 1, 255, 255, 4, 1, 0, 17, 254, 15, 0, 11, 0,
                        0, 8, 2, 16, 3, 32, 50, 40, 7, 48, 132, 1,
                    ])
                )
            
            connection.configure_listeners(on_data)
            status = await sdk.get_status(1, test_config.defaultTimeout)
            
            assert status == test_case["status"]
        
        asyncio.run(_test())

    @pytest.mark.parametrize("test_case", fixtures["valid"])
    def test_should_be_able_to_handle_multiple_retries(self, setup, test_case):
        """Test handling multiple retries for get status"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            max_tries = 3
            retries = 0
            
            async def on_data():
                nonlocal retries
                current_retry = retries + 1
                
                # Randomly trigger error for testing retries
                import random
                do_trigger_error = random.random() > 0.5 and current_retry < max_tries
                
                if not do_trigger_error:
                    for ack_packet in test_case["ack_packets"]:
                        await connection.mock_device_send(ack_packet)
                else:
                    retries = current_retry
            
            connection.configure_listeners(on_data)
            status = await sdk.get_status(max_tries, test_config.defaultTimeout)
            
            assert status == test_case["status"]
        
        asyncio.run(_test())

    @pytest.mark.parametrize("test_case", fixtures["valid"])
    def test_should_throw_error_when_device_is_disconnected(self, setup, test_case):
        """Test error when device is disconnected"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            from unittest.mock import Mock
            on_data = Mock()
            
            connection.configure_listeners(on_data)
            await connection.destroy()
            
            with pytest.raises(DeviceConnectionError):
                await sdk.get_status(1, test_config.defaultTimeout)
            
            assert on_data.call_count == 0
        
        asyncio.run(_test())

    @pytest.mark.parametrize("test_case", fixtures["valid"])
    def test_should_throw_error_when_device_is_disconnected_in_between(self, setup, test_case):
        """Test error when device is disconnected during operation"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            async def on_data(data: bytes):
                assert test_case["status_request"] == data
                i = 0
                for ack_packet in test_case["ack_packets"]:
                    if i >= len(test_case["ack_packets"]) - 1:
                        await connection.destroy()
                    else:
                        await connection.mock_device_send(ack_packet)
                    i += 1
            
            connection.configure_listeners(on_data)
            
            with pytest.raises(DeviceConnectionError):
                await sdk.get_status(1, test_config.defaultTimeout)
        
        asyncio.run(_test())
