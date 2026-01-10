import asyncio
import threading
import time
import uuid
from typing import Any, Dict, Optional

from interfaces import IDevice, PoolData

from ..logger import logger
from .connection import get_available_devices


class DataListener:
    def __init__(self, params: Dict[str, Any]):
        self.connection = params["connection"]
        self.device: IDevice = params["device"]
        self.on_close_callback = params.get("on_close")
        self.on_error_callback = params.get("on_error")
        self.listening = False
        self.pool: [PoolData] = []

        self.read_timeout_id = None
        self.read_promise = None

        self.read_thread = None
        self._monitor_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()

        self.add_all_listeners()

    async def destroy(self):
        if self.read_promise:
            await self.read_promise

        self.stop_listening()
        self.remove_all_listeners()

        if self.on_close_callback:
            self.on_close_callback()

    def is_listening(self):
        return self.listening

    async def receive(self):
        if self.pool:
            return self.pool.pop(0).get("data")
        return None

    def peek(self):
        return self.pool.copy()

    def clear_read_interval(self):
        if self.read_timeout_id:
            self.read_timeout_id.cancel()
            self.read_timeout_id = None

    def set_read_interval(self):
        self.read_timeout_id = asyncio.create_task(self.on_read())

    def start_listening(self):
        self.listening = True
        self.set_read_interval()

    def stop_listening(self):
        self.clear_read_interval()
        self.listening = False

    def add_all_listeners(self) -> None:
        if not self._monitor_thread or not self._monitor_thread.is_alive():
            logger.debug("Starting device disconnect monitor thread.")
            self._monitor_thread = threading.Thread(
                target=self._run_device_monitor, daemon=True
            )
            self._monitor_thread.start()

    def remove_all_listeners(self) -> None:
        self._stop_event.set()
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=1.0)
            logger.debug("Device disconnect monitor thread stopped.")

    async def on_read(self):
        if not self.listening:
            self.clear_read_interval()
            return

        self.read_promise = asyncio.create_task(self._read_data())
        try:
            data = await self.read_promise
            if data:
                await self.on_data(data)
        except Exception as error:
            logger.error("Error while reading data from device")
            logger.error(error)
        finally:
            self.read_promise = None
            if self.listening:
                self.set_read_interval()

    async def _read_data(self):
        return await asyncio.to_thread(self._read_hid_data)

    def _read_hid_data(self):
        try:
            # hidapi Device.read() only accepts size parameter
            # No timeout parameter is supported - read is blocking
            return self.connection.read(64)
        except Exception as error:
            if self.on_error_callback:
                self.on_error_callback(error)
            return None

    async def on_data(self, data):
        if data and len(data) > 0:
            self.pool.append({"id": str(uuid.uuid4()), "data": bytearray(data)})

    async def on_close(self):
        self.stop_listening()
        self.remove_all_listeners()

        if self.on_close_callback:
            self.on_close_callback()

    def on_error(self, error: Exception):
        if self.on_error_callback:
            self.on_error_callback(error)

    def _run_device_monitor(self):
        while not self._stop_event.is_set():
            try:
                self._check_device_connection_sync()
            except Exception as e:
                logger.error(f"Error in device monitor: {e}")
            time.sleep(1)

    def _check_device_connection_sync(self):
        """Synchronous device connection check for use in thread."""
        try:
            import hid
            # Use synchronous hid.enumerate() directly
            all_hid_devices = hid.enumerate()
            
            # Check if our device is still connected
            is_device_connected = any(
                device_info.get("path") and 
                device_info.get("path").decode("utf-8") == self.device["path"]
                and device_info.get("vendor_id") == self.device.get("vendor_id")
                and device_info.get("product_id") == self.device.get("product_id")
                and device_info.get("serial_number") == self.device.get("serial")
                for device_info in all_hid_devices
            )

            if not is_device_connected:
                # Schedule async cleanup in the main event loop
                # We can't await here, so we'll just log and let the connection
                # error handling deal with it
                logger.warn("Device appears to be disconnected")
        except Exception as e:
            logger.error(f"Error checking device connection: {e}")
