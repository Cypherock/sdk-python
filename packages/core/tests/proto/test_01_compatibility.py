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
        applet_id = 1
        connection = await MockDeviceConnection.create()

        # Mock time and packet timestamps for consistency
        import calendar
        utc_timestamp = calendar.timegm(constant_date.timetuple()) + constant_date.microsecond / 1000000
        with patch('time.time', return_value=utc_timestamp), \
             patch('packages.core.src.encoders.packet.packet.time.time', return_value=utc_timestamp), \
             patch('os.times', return_value=type('MockTimes', (), {'elapsed': 16778725})()):
            
            # Setup device connection
            async def on_data(data: bytes):
                # Use the fixture's ACK packet which should be correct for Python
                await connection.mock_device_send(
                    bytes([
                        85, 85, 41, 170, 0, 1, 0, 1, 255, 255, 4, 1, 0, 17, 254, 15, 0, 11, 0,
                        0, 8, 2, 16, 3, 32, 50, 40, 7, 48, 132, 1,
                    ])
                )

            connection.configure_listeners(on_data)
            
            sdk = await SDK.create(connection, applet_id)
            await sdk.before_operation()
            connection.remove_listeners()
            
            yield connection, sdk
            
            await connection.destroy()

    def test_should_be_able_to_get_status(self, setup):
        async def _test():
            connection, sdk = await setup.__anext__()

            async def on_data(data: bytes):
                # Generate dynamic STATUS response with correct timestamp and CRC
                from packages.core.src.encoders.packet.packet import encode_packet
                from packages.core.src.utils.packetversion import PacketVersionMap
                
                ack_packets = encode_packet(
                    raw_data='',
                    proto_data='',
                    version=PacketVersionMap.v3,
                    sequence_number=255,  # STATUS packets use sequence 255
                    packet_type=4  # STATUS
                )
                status_response = ack_packets[0]
                await connection.mock_device_send(status_response)

            connection.configure_listeners(on_data)
            result = await sdk.get_status()
            assert isinstance(result, dict)

        asyncio.run(_test())

    def test_should_be_able_to_send_query(self, setup):
        async def _test():
            connection, sdk = await setup.__anext__()

            async def on_data(data: bytes):
                # Generate ACK packet with correct timestamp and CRC
                from packages.core.src.encoders.packet.packet import encode_packet
                from packages.core.src.utils.packetversion import PacketVersionMap
                
                ack_packets = encode_packet(
                    raw_data='',
                    proto_data='',
                    version=PacketVersionMap.v3,
                    sequence_number=16,  # Test sequence number
                    packet_type=5  # CMD_ACK
                )
                correct_ack = ack_packets[0]
                await connection.mock_device_send(correct_ack)

            connection.configure_listeners(on_data)
            sdk.configure_applet_id(12)

            await sdk.send_query(
                bytes([98, 110, 1, 88, 234, 189, 103, 120, 176, 24, 231, 183, 92, 134, 213, 11]),
                {
                    "sequence_number": 16,
                    "max_tries": 1,
                    "timeout": test_config.defaultTimeout,
                }
            )

        asyncio.run(_test())

    def test_should_be_able_to_get_result(self, setup):
        async def _test():
            connection, sdk = await setup.__anext__()

            async def on_data(data: bytes):
                # Generate dynamic RESULT response with correct timestamp and CRC
                from packages.core.src.encoders.packet.packet import encode_packet
                from packages.core.src.utils.packetversion import PacketVersionMap
                
                ack_packets = encode_packet(
                    raw_data='',
                    proto_data='',
                    version=PacketVersionMap.v3,
                    sequence_number=16,
                    packet_type=6  # RESULT
                )
                result_response = ack_packets[0]
                await connection.mock_device_send(result_response)

            connection.configure_listeners(on_data)
            sdk.configure_applet_id(12)

            result = await sdk.get_result({
                "sequence_number": 16,
                "max_tries": 1,
                "timeout": test_config.defaultTimeout,
            })
            assert result["is_status"] is False

        asyncio.run(_test())

    def test_should_be_able_to_wait_for_result(self, setup):
        async def _test():
            connection, sdk = await setup.__anext__()

            async def on_data(data: bytes):
                # Generate dynamic RESULT response with correct timestamp and CRC
                from packages.core.src.encoders.packet.packet import encode_packet
                from packages.core.src.utils.packetversion import PacketVersionMap
                
                ack_packets = encode_packet(
                    raw_data='',
                    proto_data='',
                    version=PacketVersionMap.v3,
                    sequence_number=16,
                    packet_type=6  # RESULT
                )
                result_response = ack_packets[0]
                await connection.mock_device_send(result_response)

            connection.configure_listeners(on_data)
            sdk.configure_applet_id(12)

            result = await sdk.wait_for_result({
                "sequence_number": 16,
                "max_tries": 1,
                "timeout": test_config.defaultTimeout,
            })
            assert result is not None

        asyncio.run(_test())

    def test_should_be_able_to_send_abort(self, setup):
        async def _test():
            connection, sdk = await setup.__anext__()

            async def on_data(data: bytes):
                # Generate dynamic STATUS response with correct timestamp and CRC
                from packages.core.src.encoders.packet.packet import encode_packet
                from packages.core.src.utils.packetversion import PacketVersionMap
                
                ack_packets = encode_packet(
                    raw_data='',
                    proto_data='',
                    version=PacketVersionMap.v3,
                    sequence_number=255,  # STATUS packets use sequence 255
                    packet_type=4  # STATUS
                )
                status_response = ack_packets[0]
                await connection.mock_device_send(status_response)

            connection.configure_listeners(on_data)

            result = await sdk.send_abort({
                "sequence_number": 18,
                "max_tries": 1,
                "timeout": test_config.defaultTimeout,
            })
            assert isinstance(result, dict)

        asyncio.run(_test())
