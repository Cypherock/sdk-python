import asyncio
import uuid
from typing import Any, List, Optional

import hid

from interfaces import (
    ConnectionTypeMap,
    DeviceConnectionError,
    DeviceConnectionErrorType,
    DeviceState,
    IDevice,
    IDeviceConnection,
    PoolData,
)

from .helpers import DataListener, get_available_devices
from .logger import logger


class DeviceConnection(IDeviceConnection):
    def __init__(self, device: IDevice, connection: Any):
        self.device: IDevice = device
        self.connection_id = str(uuid.uuid4())
        self.sequence_number = 0
        self.initialized = True
        self.is_port_open = True
        self.connection = connection

        listener_params = {
            "connection": self.connection,
            "device": self.device,
            "on_close": self.on_close,
            "on_error": self.on_error,
        }
        self.data_listener: DataListener = DataListener(listener_params)

    # pylint: disable=no-self-use
    async def get_connection_type(self) -> str:
        return ConnectionTypeMap.HID.value

    @staticmethod
    async def connect(device: IDevice):
        # Create HID device connection
        # Check which API is available
        connection = None
        device_path = device["path"]
        # Ensure path is bytes if it's a string (hidapi may need bytes)
        if isinstance(device_path, str):
            device_path_bytes = device_path.encode("utf-8")
        else:
            device_path_bytes = device_path
        
        if hasattr(hid, "Device"):
            # Newer hidapi API - try different initialization methods
            # Note: hid.Device() requires vid/pid or path parameter
            try:
                # Try passing path as bytes to constructor (most specific)
                connection = await asyncio.to_thread(hid.Device, path=device_path_bytes)  # type: ignore
            except (TypeError, ValueError):
                try:
                    # Try with string path
                    connection = await asyncio.to_thread(hid.Device, path=device["path"])  # type: ignore
                except (TypeError, ValueError):
                    # Fallback: try with vid/pid if available
                    if "vendor_id" in device and "product_id" in device:
                        try:
                            connection = await asyncio.to_thread(
                                hid.Device, device["vendor_id"], device["product_id"]  # type: ignore
                            )
                        except (TypeError, ValueError, AttributeError) as e:
                            raise RuntimeError(
                                f"Failed to create HID device connection: {e}. "
                                "Tried: Device(path=bytes), Device(path=str), and Device(vid, pid). "
                                "Please check your hidapi installation."
                            )
                    else:
                        raise RuntimeError(
                            "Failed to create HID device connection: "
                            "No path or vid/pid available. "
                            "Tried: Device(path=bytes) and Device(path=str). "
                            "Please check your hidapi installation."
                        )
        elif hasattr(hid, "device"):
            # Older hidapi API
            connection = hid.device()  # type: ignore
            try:
                await asyncio.to_thread(connection.open_path, device_path_bytes)
            except (TypeError, AttributeError):
                await asyncio.to_thread(connection.open_path, device["path"])
        elif hasattr(hid, "open_path"):
            # Alternative API: open_path as module-level function
            try:
                connection = await asyncio.to_thread(hid.open_path, device_path_bytes)  # type: ignore
            except (TypeError, ValueError):
                connection = await asyncio.to_thread(hid.open_path, device["path"])  # type: ignore
        else:
            raise RuntimeError(
                "HID library does not support device creation. "
                "The 'hid' module is missing required methods (Device, device, or open_path). "
                "Please reinstall the 'hidapi' package: "
                "poetry run pip install --force-reinstall --no-cache-dir hid"
            )
        return DeviceConnection(device, connection)

    @staticmethod
    async def list():
        return await get_available_devices()

    @staticmethod
    async def create():
        devices = await get_available_devices()
        if not devices:
            raise DeviceConnectionError(DeviceConnectionErrorType.NOT_CONNECTED)
        device_to_connect = devices[0]
        # Create HID device connection using connect() method
        return await DeviceConnection.connect(device_to_connect)

    @staticmethod
    async def get_available_connection():
        connection_info = await get_available_devices()
        return connection_info

    async def get_device_state(self) -> DeviceState:
        return self.device["device_state"]

    async def is_initialized(self) -> bool:
        return self.initialized

    async def get_new_sequence_number(self) -> int:
        self.sequence_number += 1
        return self.sequence_number

    async def get_sequence_number(self) -> int:
        return self.sequence_number

    async def is_connected(self) -> bool:
        return self.is_port_open

    async def destroy(self) -> None:
        if not self.is_port_open:
            return

        await self.data_listener.destroy()
        try:
            self.connection.close()
        except Exception as error:
            logger.warn("Error while closing device connection")
            logger.warn(error)

    async def before_operation(self) -> None:
        self.data_listener.start_listening()

    async def after_operation(self) -> None:
        self.data_listener.stop_listening()

    async def send(self, data: bytearray) -> None:
        data_to_write = [0x00] + list(data) + [0x00] * (64 - len(data))
        await asyncio.to_thread(self.connection.write, bytes(data_to_write))

    async def receive(self) -> Optional[bytearray]:
        result = await self.data_listener.receive()
        return bytearray(result) if result is not None else None

    async def peek(self) -> List[PoolData]:
        return self.data_listener.peek()

    def on_close(self):
        self.is_port_open = False

    def on_error(self, error: Exception):
        logger.error("Error on device connection callback")
        logger.error(error)
