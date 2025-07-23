import asyncio
import pytest
from unittest.mock import patch
from datetime import datetime

from packages.interfaces.__mocks__.connection import MockDeviceConnection
from packages.interfaces.errors.bootloader_error import DeviceBootloaderError, DeviceBootloaderErrorType, deviceBootloaderErrorTypeDetails
from packages.interfaces.errors.compatibility_error import DeviceCompatibilityError, DeviceCompatibilityErrorType, deviceCompatibilityErrorTypeDetails
from packages.core.src.sdk import SDK
from packages.core.src.utils.packetversion import PacketVersionMap
from packages.core.tests.proto.__fixtures__.get_status import constant_date
from packages.core.tests.__fixtures__.config import config as test_config


class TestDeviceProtoOperationV3:
    """Test Device Proto Operation: v3"""
    
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
                # Then send SDK Version packet: 3.0.1, Packet Version: v3 (from create.py fixture)
                await connection.mock_device_send(
                    bytes([170, 88, 12, 0, 1, 0, 1, 0, 3, 0, 0, 0, 1, 173, 177])
                )
            
            connection.configure_listeners(on_data)
            
            sdk = await SDK.create(connection, applet_id)
            await sdk.before_operation()
            connection.remove_listeners()
            
            yield connection, sdk
            
            await connection.destroy()

    def test_should_have_the_right_sdk_version_and_packet_version(self, setup):
        """Test SDK version and packet version configuration"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            assert sdk.get_version() == "3.0.1"
            assert sdk.get_packet_version() == PacketVersionMap.v3
            assert await sdk.is_supported() is True
        
        asyncio.run(_test())

    def test_should_be_able_to_get_status(self, setup):
        """Test basic status functionality"""
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
            
            status = await sdk.get_status()
            expected_status = {
                "device_idle_state": 3,
                "device_waiting_on": 2,
                "abort_disabled": False,
                "current_cmd_seq": 50,
                "cmd_state": 7,
                "flow_status": 132,
            }
            assert status == expected_status
        
        asyncio.run(_test())

    def test_should_be_able_to_send_query(self, setup):
        """Test send query functionality"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            async def on_data(data: bytes):
                assert data == bytes([
                    85, 85, 46, 15, 0, 1, 0, 1, 0, 16, 2, 1, 0, 17, 254, 24, 0, 4, 0, 16,
                    10, 2, 8, 12, 98, 110, 1, 88, 234, 189, 103, 120, 176, 24, 231, 183,
                    92, 134, 213, 11,
                ])
                await connection.mock_device_send(
                    bytes([
                        85, 85, 233, 246, 0, 1, 0, 1, 0, 16, 5, 1, 0, 5, 229, 0,
                    ])
                )
            
            connection.configure_listeners(on_data)
            
            await sdk.send_query(
                bytes([
                    98, 110, 1, 88, 234, 189, 103, 120, 176, 24, 231, 183, 92, 134, 213, 11,
                ]),
                {
                    "sequence_number": 16,
                    "max_tries": 1,
                }
            )
        
        asyncio.run(_test())

    def test_should_be_able_to_get_result(self, setup):
        """Test get result functionality"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            async def on_data(data: bytes):
                assert data == bytes([
                    85, 85, 193, 89, 0, 1, 0, 1, 0, 16, 3, 1, 0, 17, 254, 6, 0, 0, 0, 2,
                    0, 1,
                ])
                await connection.mock_device_send(
                    bytes([
                        85, 85, 10, 115, 0, 1, 0, 1, 0, 16, 6, 1, 0, 17, 254, 24, 0, 4, 0, 16,
                        10, 2, 8, 12, 98, 110, 1, 88, 234, 189, 103, 120, 176, 24, 231, 183,
                        92, 134, 213, 11,
                    ])
                )
            
            connection.configure_listeners(on_data)
            
            result = await sdk.get_result({"sequence_number": 16})
            
            expected_result = {
                "is_status": False,
                "result": bytes([
                    98, 110, 1, 88, 234, 189, 103, 120, 176, 24, 231, 183, 92, 134, 213, 11,
                ])
            }
            assert result == expected_result
        
        asyncio.run(_test())

    def test_should_be_able_to_wait_for_result(self, setup):
        """Test wait for result functionality"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            async def on_data(data: bytes):
                assert data == bytes([
                    85, 85, 193, 89, 0, 1, 0, 1, 0, 16, 3, 1, 0, 17, 254, 6, 0, 0, 0, 2,
                    0, 1,
                ])
                await connection.mock_device_send(
                    bytes([
                        85, 85, 10, 115, 0, 1, 0, 1, 0, 16, 6, 1, 0, 17, 254, 24, 0, 4, 0, 16,
                        10, 2, 8, 12, 98, 110, 1, 88, 234, 189, 103, 120, 176, 24, 231, 183,
                        92, 134, 213, 11,
                    ])
                )
            
            connection.configure_listeners(on_data)
            
            result = await sdk.wait_for_result({
                "sequence_number": 16,
                "options": {
                    "max_tries": 1,
                }
            })
            
            expected_result = bytes([
                98, 110, 1, 88, 234, 189, 103, 120, 176, 24, 231, 183, 92, 134, 213, 11,
            ])
            assert result == expected_result
        
        asyncio.run(_test())

    def test_should_be_able_to_send_abort(self, setup):
        """Test send abort functionality"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            has_sent_abort = False
            
            async def on_data(data: bytes):
                nonlocal has_sent_abort
                
                if not has_sent_abort:
                    assert data == bytes([
                        85, 85, 135, 124, 0, 1, 0, 1, 0, 18, 8, 1, 0, 17, 254, 0,
                    ])
                    await connection.mock_device_send(
                        bytes([
                            85, 85, 28, 162, 0, 1, 0, 1, 255, 255, 4, 1, 0, 17, 254, 15, 0, 11,
                            0, 0, 8, 2, 16, 3, 32, 18, 40, 7, 48, 132, 1,
                        ])
                    )
                    has_sent_abort = True
                else:
                    assert data == bytes([
                        85, 85, 169, 56, 0, 1, 0, 1, 255, 255, 1, 1, 0, 17, 254, 0,
                    ])
                    await connection.mock_device_send(
                        bytes([
                            85, 85, 30, 138, 0, 1, 0, 1, 255, 255, 4, 1, 1, 112, 220, 12, 0, 8,
                            0, 0, 8, 1, 16, 1, 32, 1, 40, 7,
                        ])
                    )
            
            connection.configure_listeners(on_data)
            
            result = await sdk.send_abort({"sequence_number": 18})
            
            expected_result = {
                "device_idle_state": 3,
                "device_waiting_on": 2,
                "abort_disabled": False,
                "current_cmd_seq": 18,
                "cmd_state": 7,
                "flow_status": 132,
            }
            assert result == expected_result
        
        asyncio.run(_test())

    def test_should_throw_error_when_accessing_functions_for_v1(self, setup):
        """Test error when accessing v1 legacy functions"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            invalid_sdk_operation_message = (
                deviceCompatibilityErrorTypeDetails[
                    DeviceCompatibilityErrorType.INVALID_SDK_OPERATION
                ]["message"]
            )
            
            with pytest.raises(DeviceCompatibilityError) as exc_info:
                await sdk.deprecated.send_legacy_command(1, "00")
            assert invalid_sdk_operation_message in str(exc_info.value)
            
            with pytest.raises(DeviceCompatibilityError) as exc_info:
                await sdk.deprecated.receive_legacy_command([1], 500)
            assert invalid_sdk_operation_message in str(exc_info.value)
        
        asyncio.run(_test())

    def test_should_throw_error_when_accessing_functions_for_raw_command(self, setup):
        """Test error when accessing raw command functions"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            invalid_sdk_operation_message = (
                deviceCompatibilityErrorTypeDetails[
                    DeviceCompatibilityErrorType.INVALID_SDK_OPERATION
                ]["message"]
            )
            
            with pytest.raises(DeviceCompatibilityError) as exc_info:
                await sdk.deprecated.send_command({
                    "command_type": 1,
                    "data": "00",
                    "sequence_number": 1,
                })
            assert invalid_sdk_operation_message in str(exc_info.value)
            
            with pytest.raises(DeviceCompatibilityError) as exc_info:
                await sdk.deprecated.get_command_output(1)
            assert invalid_sdk_operation_message in str(exc_info.value)
            
            with pytest.raises(DeviceCompatibilityError) as exc_info:
                await sdk.deprecated.wait_for_command_output({
                    "sequence_number": 1,
                    "expected_command_types": [1],
                })
            assert invalid_sdk_operation_message in str(exc_info.value)
            
            with pytest.raises(DeviceCompatibilityError) as exc_info:
                await sdk.deprecated.get_command_status()
            assert invalid_sdk_operation_message in str(exc_info.value)
            
            with pytest.raises(DeviceCompatibilityError) as exc_info:
                await sdk.deprecated.send_command_abort(1)
            assert invalid_sdk_operation_message in str(exc_info.value)
        
        asyncio.run(_test())

    def test_should_throw_error_when_accessing_bootloader_functions(self, setup):
        """Test error when accessing bootloader functions"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            not_in_bootloader_error = (
                deviceBootloaderErrorTypeDetails[
                    DeviceBootloaderErrorType.NOT_IN_BOOTLOADER
                ]["message"]
            )
            
            with pytest.raises(DeviceBootloaderError) as exc_info:
                await sdk.send_bootloader_abort()
            assert not_in_bootloader_error in str(exc_info.value)
            
            with pytest.raises(DeviceBootloaderError) as exc_info:
                await sdk.send_bootloader_data("12")
            assert not_in_bootloader_error in str(exc_info.value)
        
        asyncio.run(_test())
