import asyncio
import pytest
from unittest.mock import patch
from datetime import datetime

from packages.interfaces.__mocks__.connection import MockDeviceConnection
from packages.interfaces.errors.bootloader_error import DeviceBootloaderError, DeviceBootloaderErrorType, deviceBootloaderErrorTypeDetails
from packages.interfaces.errors.compatibility_error import DeviceCompatibilityError, DeviceCompatibilityErrorType, deviceCompatibilityErrorTypeDetails
from packages.core.src.sdk import SDK
from packages.core.src.utils.packetversion import PacketVersionMap
from packages.core.tests.__fixtures__.config import config as test_config


class TestDeviceRawOperationV3:
    """Test Device Raw Operation: v3"""

    @pytest.fixture
    async def setup(self):
        """Setup fixture for each test"""
        constant_date = datetime(2023, 3, 7, 9, 43, 48, 755000)
        with patch('time.time', return_value=constant_date.timestamp()), \
             patch('os.times', return_value=type('MockTimes', (), {'elapsed': 16778725})()):
            connection = await MockDeviceConnection.create()
            applet_id = 0

            async def on_data():
                # SDK Version: 2.7.1, Packet Version: v3
                await connection.mock_device_send(
                    bytes([
                        170, 1, 7, 0, 1, 0, 1, 0, 69, 133, 170, 88, 12, 0, 1, 0, 1, 0, 3, 0, 0, 0, 1, 173, 177
                    ])
                )
            connection.configure_listeners(on_data)

            sdk = await SDK.create(connection, applet_id)
            await sdk.before_operation()
            connection.remove_listeners()

            yield connection, sdk

            await connection.destroy()

    def test_should_have_the_right_sdk_version_and_packet_version(self, setup):
        async def _test():
            connection, sdk = await setup.__anext__()
            assert sdk.get_version() == "3.0.1"
            assert sdk.get_packet_version() == PacketVersionMap.v3
            assert await sdk.deprecated.is_raw_operation_supported() is True
        asyncio.run(_test())

    def test_should_be_able_to_get_status(self, setup):
        async def _test():
            connection, sdk = await setup.__anext__()
            async def on_data(data: bytes):
                assert data == bytes([
                    85, 85, 169, 56, 0, 1, 0, 1, 255, 255, 1, 1, 0, 17, 254, 0
                ])
                await connection.mock_device_send(bytes([
                    85, 85, 193, 143, 0, 1, 0, 1, 255, 255, 4, 1, 0, 18, 8, 11, 0, 0, 0, 7, 35, 0, 0, 50, 7, 0, 132
                ]))
            connection.configure_listeners(on_data)
            status = await sdk.deprecated.get_command_status()
            assert status == {
                "deviceState": "23",
                "deviceIdleState": 3,
                "deviceWaitingOn": 2,
                "abortDisabled": False,
                "currentCmdSeq": 50,
                "cmdState": 7,
                "flowStatus": 132,
                "isStatus": True,
            }
        asyncio.run(_test())

    def test_should_be_able_to_send_command(self, setup):
        async def _test():
            connection, sdk = await setup.__anext__()
            async def on_data(data: bytes):
                assert data == bytes([
                    85, 85, 70, 22, 0, 1, 0, 1, 0, 16, 2, 1, 0, 17, 254, 24, 0, 0, 0, 20, 0, 0, 0, 12, 98, 110, 1, 88, 234, 189, 103, 120, 176, 24, 231, 183, 92, 134, 213, 11
                ])
                await connection.mock_device_send(bytes([
                    85, 85, 233, 246, 0, 1, 0, 1, 0, 16, 5, 1, 0, 5, 229, 0
                ]))
            connection.configure_listeners(on_data)
            await connection.before_operation()
            await sdk.deprecated.send_command({
                "data": "626e0158eabd6778b018e7b75c86d50b",
                "commandType": 12,
                "sequenceNumber": 16,
                "maxTries": 1,
            })
        asyncio.run(_test())

    def test_should_be_able_to_get_command_output(self, setup):
        async def _test():
            connection, sdk = await setup.__anext__()
            async def on_data(data: bytes):
                assert data == bytes([
                    85, 85, 193, 89, 0, 1, 0, 1, 0, 16, 3, 1, 0, 17, 254, 6, 0, 0, 0, 2, 0, 1
                ])
                await connection.mock_device_send(bytes([
                    85, 85, 68, 192, 0, 1, 0, 1, 0, 16, 6, 1, 0, 18, 139, 24, 0, 0, 0, 20, 0, 0, 0, 12, 98, 110, 1, 88, 234, 189, 103, 120, 176, 24, 231, 183, 92, 134, 213, 11
                ]))
            connection.configure_listeners(on_data)
            result = await sdk.deprecated.get_command_output(16, 1)
            assert result == {
                "isStatus": False,
                "isRawData": True,
                "data": "626e0158eabd6778b018e7b75c86d50b",
                "commandType": 12,
            }
        asyncio.run(_test())

    def test_should_be_able_to_wait_for_command_output(self, setup):
        async def _test():
            connection, sdk = await setup.__anext__()
            async def on_data(data: bytes):
                assert data == bytes([
                    85, 85, 193, 89, 0, 1, 0, 1, 0, 16, 3, 1, 0, 17, 254, 6, 0, 0, 0, 2, 0, 1
                ])
                await connection.mock_device_send(bytes([
                    85, 85, 68, 192, 0, 1, 0, 1, 0, 16, 6, 1, 0, 18, 139, 24, 0, 0, 0, 20, 0, 0, 0, 12, 98, 110, 1, 88, 234, 189, 103, 120, 176, 24, 231, 183, 92, 134, 213, 11
                ]))
            connection.configure_listeners(on_data)
            result = await sdk.deprecated.wait_for_command_output({
                "sequenceNumber": 16,
                "expectedCommandTypes": [12],
                "options": {
                    "maxTries": 1,
                    "timeout": test_config.defaultTimeout,
                },
            })
            assert result == {
                "isStatus": False,
                "isRawData": True,
                "data": "626e0158eabd6778b018e7b75c86d50b",
                "commandType": 12,
            }
        asyncio.run(_test())

    def test_should_be_able_to_send_abort(self, setup):
        async def _test():
            connection, sdk = await setup.__anext__()
            async def on_data(data: bytes):
                assert data == bytes([
                    85, 85, 135, 124, 0, 1, 0, 1, 0, 18, 8, 1, 0, 17, 254, 0
                ])
                await connection.mock_device_send(bytes([
                    85, 85, 143, 73, 0, 1, 0, 1, 0, 18, 4, 1, 0, 18, 86, 11, 0, 0, 0, 7, 35, 0, 0, 18, 7, 0, 132
                ]))
            connection.configure_listeners(on_data)
            result = await sdk.deprecated.send_command_abort(18)
            assert result == {
                "deviceState": "23",
                "deviceIdleState": 3,
                "deviceWaitingOn": 2,
                "abortDisabled": False,
                "currentCmdSeq": 18,
                "cmdState": 7,
                "flowStatus": 132,
                "isStatus": True,
            }
        asyncio.run(_test())

    def test_should_throw_error_when_accessing_functions_for_v1(self, setup):
        async def _test():
            connection, sdk = await setup.__anext__()
            invalid_sdk_operation_message = deviceCompatibilityErrorTypeDetails[DeviceCompatibilityErrorType.INVALID_SDK_OPERATION]["message"]
            with pytest.raises(DeviceCompatibilityError) as excinfo:
                await sdk.deprecated.send_legacy_command(1, "00")
            assert invalid_sdk_operation_message in str(excinfo.value)
            with pytest.raises(DeviceCompatibilityError) as excinfo:
                await sdk.deprecated.receive_legacy_command([1], 500)
            assert invalid_sdk_operation_message in str(excinfo.value)
        asyncio.run(_test())

    def test_should_throw_error_when_accessing_functions_for_proto(self, setup):
        async def _test():
            connection, sdk = await setup.__anext__()
            invalid_sdk_operation_message = deviceCompatibilityErrorTypeDetails[DeviceCompatibilityErrorType.INVALID_SDK_OPERATION]["message"]
            with pytest.raises(DeviceCompatibilityError) as excinfo:
                await sdk.send_query(bytes([10]))
            assert invalid_sdk_operation_message in str(excinfo.value)
            with pytest.raises(DeviceCompatibilityError) as excinfo:
                await sdk.get_result()
            assert invalid_sdk_operation_message in str(excinfo.value)
            with pytest.raises(DeviceCompatibilityError) as excinfo:
                await sdk.wait_for_result()
            assert invalid_sdk_operation_message in str(excinfo.value)
            with pytest.raises(DeviceCompatibilityError) as excinfo:
                await sdk.get_status()
            assert invalid_sdk_operation_message in str(excinfo.value)
            with pytest.raises(DeviceCompatibilityError) as excinfo:
                await sdk.send_abort()
            assert invalid_sdk_operation_message in str(excinfo.value)
        asyncio.run(_test())

    def test_should_throw_error_when_accessing_bootloader_functions(self, setup):
        async def _test():
            connection, sdk = await setup.__anext__()
            not_in_bootloader_error = deviceBootloaderErrorTypeDetails[DeviceBootloaderErrorType.NOT_IN_BOOTLOADER]["message"]
            with pytest.raises(DeviceBootloaderError) as excinfo:
                await sdk.send_bootloader_abort()
            assert not_in_bootloader_error in str(excinfo.value)
            with pytest.raises(DeviceBootloaderError) as excinfo:
                await sdk.send_bootloader_data("12")
            assert not_in_bootloader_error in str(excinfo.value)
        asyncio.run(_test())
