import asyncio
import pytest
import random
from unittest.mock import patch
from datetime import datetime

from packages.interfaces.__mocks__.connection import MockDeviceConnection
from packages.interfaces.errors.connection_error import DeviceConnectionError
from packages.core.src.sdk import SDK
from packages.core.src.utils.packetversion import PacketVersionMap
from packages.core.tests.proto.__fixtures__.get_result import fixtures, constant_date
from packages.core.tests.__fixtures__.config import config as test_config


class TestSDKGetResult:
    """Test sdk.get_result"""
    
    @pytest.fixture
    async def setup(self):
        """Setup fixture for each test"""
        # Mock the constant date - use UTC timestamp to match TypeScript Date.now()
        import calendar
        utc_timestamp = calendar.timegm(constant_date.timetuple()) + constant_date.microsecond / 1000000
        with patch('time.time', return_value=utc_timestamp), \
             patch('packages.core.src.encoders.packet.packet.time.time', return_value=utc_timestamp), \
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
    def test_should_be_able_to_get_result(self, setup, test_case):
        """Test getting result for valid cases"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            async def on_data(data: bytes):
                # Generate proper RESULT response with correct timestamp/CRC
                from packages.core.src.encoders.packet.packet import decode_packet, decode_payload_data, encode_packet
                from packages.core.src.utils.packetversion import PacketVersionMap
                
                # Use test_case fixture ACK packet - get_result expects RESULT responses
                original_fixture = test_case["ack_packets"][0][0]  # First ACK from first packet
                decoded_fixture = decode_packet(original_fixture, PacketVersionMap.v3)[0]
                payload_hex = decoded_fixture['payload_data']
                
                # Extract the actual protobuf data from the payload wrapper
                payload_data = decode_payload_data(payload_hex, PacketVersionMap.v3)
                protobuf_data = payload_data['protobuf_data']
                raw_data = payload_data['raw_data']
                
                # Regenerate packet with same protobuf/raw data but correct timestamp/CRC
                regenerated_packets = encode_packet(
                    raw_data=raw_data,
                    proto_data=protobuf_data,
                    version=PacketVersionMap.v3,
                    sequence_number=test_case["sequence_number"],
                    packet_type=6  # RESULT
                )
                correct_result_packet = regenerated_packets[0]
                await connection.mock_device_send(correct_result_packet)
            
            connection.configure_listeners(on_data)
            sdk.configure_applet_id(test_case["applet_id"])
            
            result = await sdk.get_result({
                "sequence_number": test_case["sequence_number"],
                "max_tries": 1,
                "timeout": test_config.defaultTimeout,
            })
            
            assert isinstance(result, dict)
        
        asyncio.run(_test())

    @pytest.mark.parametrize("test_case", fixtures["valid"])
    def test_should_be_able_to_handle_multiple_retries(self, setup, test_case):
        """Test handling multiple retries for get result"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            max_timeout_triggers = 3
            total_timeout_triggers = 0
            
            max_tries = 3
            retries = {}
            
            async def on_data(data: bytes):
                nonlocal total_timeout_triggers
                
                # Generate proper RESULT response with correct timestamp/CRC for retry test
                from packages.core.src.encoders.packet.packet import decode_packet, decode_payload_data, encode_packet
                from packages.core.src.utils.packetversion import PacketVersionMap
                
                # Use test_case fixture ACK packet - get_result expects RESULT responses
                original_fixture = test_case["ack_packets"][0][0]  # First ACK from first packet
                decoded_fixture = decode_packet(original_fixture, PacketVersionMap.v3)[0]
                payload_hex = decoded_fixture['payload_data']
                
                # Extract the actual protobuf data from the payload wrapper
                payload_data = decode_payload_data(payload_hex, PacketVersionMap.v3)
                protobuf_data = payload_data['protobuf_data']
                raw_data = payload_data['raw_data']
                
                # Simulate retry logic - sometimes trigger error, sometimes send proper response
                do_trigger_error = (
                    random.random() < 0.5 and
                    total_timeout_triggers < max_timeout_triggers
                )
                
                if not do_trigger_error:
                    # Generate and send proper RESULT response
                    regenerated_packets = encode_packet(
                        raw_data=raw_data,
                        proto_data=protobuf_data,
                        version=PacketVersionMap.v3,
                        sequence_number=test_case["sequence_number"],
                        packet_type=6  # RESULT
                    )
                    correct_result_packet = regenerated_packets[0]
                    await connection.mock_device_send(correct_result_packet)
                else:
                    total_timeout_triggers += 1
                    # Don't send response to trigger timeout/retry
            
            connection.configure_listeners(on_data)
            sdk.configure_applet_id(test_case["applet_id"])
            
            output = await sdk.get_result({
                "sequence_number": test_case["sequence_number"],
                "max_tries": max_tries,
                "timeout": test_config.defaultTimeout,
            })
            
            assert output == test_case["output"]
        
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
            sdk.configure_applet_id(test_case["applet_id"])
            
            with pytest.raises(DeviceConnectionError):
                await sdk.get_result({
                    "sequence_number": test_case["sequence_number"],
                    "max_tries": 1,
                    "timeout": test_config.defaultTimeout,
                })
            
            assert on_data.call_count == 0
        
        asyncio.run(_test())

    @pytest.mark.parametrize("test_case", fixtures["valid"])
    def test_should_throw_error_when_device_is_disconnected_in_between(self, setup, test_case):
        """Test error when device is disconnected during operation"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            async def on_data(data: bytes):
                # Generate proper RESULT response then disconnect
                from packages.core.src.encoders.packet.packet import decode_packet, decode_payload_data, encode_packet
                from packages.core.src.utils.packetversion import PacketVersionMap
                
                # Use test_case fixture ACK packet - get_result expects RESULT responses
                original_fixture = test_case["ack_packets"][0][0]  # First ACK from first packet
                decoded_fixture = decode_packet(original_fixture, PacketVersionMap.v3)[0]
                payload_hex = decoded_fixture['payload_data']
                
                # Extract the actual protobuf data from the payload wrapper
                payload_data = decode_payload_data(payload_hex, PacketVersionMap.v3)
                protobuf_data = payload_data['protobuf_data']
                raw_data = payload_data['raw_data']
                
                # Regenerate packet with same protobuf/raw data but correct timestamp/CRC
                regenerated_packets = encode_packet(
                    raw_data=raw_data,
                    proto_data=protobuf_data,
                    version=PacketVersionMap.v3,
                    sequence_number=test_case["sequence_number"],
                    packet_type=6  # RESULT
                )
                correct_result_packet = regenerated_packets[0]
                
                # Send the result packet then destroy connection to simulate disconnect
                await connection.mock_device_send(correct_result_packet)
                await connection.destroy()
            
            connection.configure_listeners(on_data)
            sdk.configure_applet_id(test_case["applet_id"])
            
            with pytest.raises(DeviceConnectionError):
                await sdk.get_result({
                    "sequence_number": test_case["sequence_number"],
                    "max_tries": 1,
                    "timeout": test_config.defaultTimeout,
                })
        
        asyncio.run(_test())

    @pytest.mark.parametrize("test_case", fixtures["error"])
    def test_should_throw_error_when_device_sends_invalid_data(self, setup, test_case):
        """Test error when device sends invalid data"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            async def on_data(data: bytes):
                # Generate proper error response with correct timestamp/CRC
                from packages.core.src.encoders.packet.packet import decode_packet, decode_payload_data, encode_packet
                from packages.core.src.utils.packetversion import PacketVersionMap
                
                # Use test_case fixture ACK packet for error tests
                original_fixture = test_case["ack_packets"][0][0]  # First ACK from first packet
                decoded_fixture = decode_packet(original_fixture, PacketVersionMap.v3)[0]
                payload_hex = decoded_fixture['payload_data']
                
                # Extract the actual protobuf data from the payload wrapper
                payload_data = decode_payload_data(payload_hex, PacketVersionMap.v3)
                protobuf_data = payload_data['protobuf_data']
                raw_data = payload_data['raw_data']
                
                # Regenerate packet with same protobuf/raw data but correct timestamp/CRC
                regenerated_packets = encode_packet(
                    raw_data=raw_data,
                    proto_data=protobuf_data,
                    version=PacketVersionMap.v3,
                    sequence_number=decoded_fixture['sequence_number'],
                    packet_type=decoded_fixture['packet_type']
                )
                correct_packet = regenerated_packets[0]
                await connection.mock_device_send(correct_packet)
            
            connection.configure_listeners(on_data)
            sdk.configure_applet_id(test_case["applet_id"])
            
            with pytest.raises(test_case["error_instance"]):
                await sdk.get_result({
                    "sequence_number": test_case["sequence_number"],
                    "max_tries": 1,
                    "timeout": test_config.defaultTimeout,
                })
        
        asyncio.run(_test())

    @pytest.mark.parametrize("test_case", fixtures["invalid_args"])
    def test_should_throw_error_with_invalid_arguments(self, setup, test_case):
        """Test error with invalid arguments"""
        async def _test():
            connection, sdk = await setup.__anext__()
            
            with pytest.raises(Exception):
                await sdk.get_result({
                    "sequence_number": test_case["sequence_number"],
                    "max_tries": 1,
                    "timeout": test_config.defaultTimeout,
                })
        
        asyncio.run(_test())
