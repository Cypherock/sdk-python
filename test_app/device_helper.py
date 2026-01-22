"""Helper module for device discovery and connection."""
import asyncio
from typing import List, Optional, Tuple, Any

from interfaces import IDevice, DeviceState, ConnectionTypeMap
from interfaces.errors.connection_error import DeviceConnectionError

# Try to import connection modules, handle missing dependencies gracefully
HID_AVAILABLE = False
HID_ERROR = None
SERIAL_AVAILABLE = False
SERIAL_ERROR = None
WEBUSB_AVAILABLE = False
WEBUSB_ERROR = None

try:
    from hw_hid import DeviceConnection as HIDDeviceConnection
    HID_AVAILABLE = True
except ImportError as e:
    HID_ERROR = str(e)

try:
    from hw_serialport import DeviceConnection as SerialDeviceConnection
    SERIAL_AVAILABLE = True
except ImportError as e:
    SERIAL_ERROR = str(e)

try:
    from hw_webusb import DeviceConnection as WebUSBDeviceConnection
    from hw_webusb.helpers.connection import create_port
    WEBUSB_AVAILABLE = True
except ImportError as e:
    WEBUSB_ERROR = str(e)


async def discover_devices() -> Tuple[List[IDevice], List[IDevice], bool]:
    """
    Discover all available devices across all connection types.

    Returns:
        Tuple of (hid_devices, serial_devices, webusb_available)
        Note: WebUSB doesn't support listing, so we just check if one is available
    """
    hid_devices = []
    serial_devices = []
    webusb_available = False

    if HID_AVAILABLE:
        try:
            hid_devices = await HIDDeviceConnection.list()
        except Exception as e:
            print(f"Error discovering HID devices: {e}")
    else:
        print(f"HID not available: {HID_ERROR or 'Library not installed'}")

    if SERIAL_AVAILABLE:
        try:
            serial_devices = await SerialDeviceConnection.list()
        except Exception as e:
            print(f"Error discovering Serial devices: {e}")
    else:
        print(f"Serial not available: {SERIAL_ERROR or 'Library not installed'}")

    if WEBUSB_AVAILABLE:
        try:
            # WebUSB doesn't have a list() method, so we try to create a port
            # to see if any device is available
            await create_port()
            webusb_available = True
        except Exception:
            webusb_available = False
    else:
        print(f"WebUSB not available: {WEBUSB_ERROR or 'Library not installed'}")

    return hid_devices, serial_devices, webusb_available


def print_devices(
    hid_devices: List[IDevice],
    serial_devices: List[IDevice],
    webusb_available: bool,
) -> None:
    """Print all discovered devices in a formatted way."""
    print("\n=== Discovered Devices ===\n")

    if hid_devices:
        print("HID Devices:")
        for i, device in enumerate(hid_devices, 1):
            print(
                f"  [{i}] {device.get('path', 'N/A')} - "
                f"State: {device.get('device_state', 'N/A')} - "
                f"Serial: {device.get('serial', 'N/A')}"
            )
    else:
        print("HID Devices: None found")

    if serial_devices:
        print("\nSerial Port Devices:")
        for i, device in enumerate(serial_devices, 1):
            print(
                f"  [{i}] {device.get('path', 'N/A')} - "
                f"State: {device.get('device_state', 'N/A')} - "
                f"Serial: {device.get('serial', 'N/A')}"
            )
    else:
        print("\nSerial Port Devices: None found")

    if webusb_available:
        print("\nWebUSB Devices: Available (1 device)")
    else:
        print("\nWebUSB Devices: None found")

    print()


async def create_connection(
    connection_type: str = "auto",
    device_index: int = 0,
) -> Tuple[Any, str]:
    """
    Create a connection to a device.

    Args:
        connection_type: Type of connection ('hid', 'serial', 'webusb', or 'auto')
        device_index: Index of device to connect to (0-based)

    Returns:
        Tuple of (connection, connection_type_string)
    """
    hid_devices, serial_devices, webusb_available = await discover_devices()

    connection = None
    conn_type = None

    if connection_type == "auto":
        # Try HID first, then Serial, then WebUSB
        if HID_AVAILABLE and hid_devices:
            connection_type = "hid"
        elif SERIAL_AVAILABLE and serial_devices:
            connection_type = "serial"
        elif WEBUSB_AVAILABLE and webusb_available:
            connection_type = "webusb"
        else:
            available_types = []
            if HID_AVAILABLE:
                available_types.append("HID")
            if SERIAL_AVAILABLE:
                available_types.append("Serial")
            if WEBUSB_AVAILABLE:
                available_types.append("WebUSB")
            if not available_types:
                raise DeviceConnectionError(
                    "No connection types available. Please install required system libraries:\n"
                    "  macOS: brew install hidapi libusb\n"
                    "  Linux: sudo apt-get install libhidapi-dev libusb-1.0-0-dev"
                )
            raise DeviceConnectionError("No devices found")

    if connection_type == "hid":
        if not HID_AVAILABLE:
            error_msg = HID_ERROR or "Library not installed"
            raise DeviceConnectionError(
                f"HID connection not available. Error: {error_msg}\n"
                "Install system library: brew install hidapi (macOS) or sudo apt-get install libhidapi-dev (Linux)"
            )
        if not hid_devices or device_index >= len(hid_devices):
            raise DeviceConnectionError(
                f"No HID device at index {device_index}. Found {len(hid_devices)} devices."
            )
        device = hid_devices[device_index]
        connection = await HIDDeviceConnection.connect(device)
        conn_type = ConnectionTypeMap.HID.value

    elif connection_type == "serial":
        if not SERIAL_AVAILABLE:
            error_msg = SERIAL_ERROR or "Library not installed"
            raise DeviceConnectionError(
                f"Serial connection not available. Error: {error_msg}"
            )
        if not serial_devices or device_index >= len(serial_devices):
            raise DeviceConnectionError(
                f"No Serial device at index {device_index}. Found {len(serial_devices)} devices."
            )
        device = serial_devices[device_index]
        connection = await SerialDeviceConnection.connect(device)
        conn_type = ConnectionTypeMap.SERIAL_PORT.value

    elif connection_type == "webusb":
        if not WEBUSB_AVAILABLE:
            error_msg = WEBUSB_ERROR or "Library not installed"
            raise DeviceConnectionError(
                f"WebUSB connection not available. Error: {error_msg}\n"
                "Install system library: brew install libusb (macOS) or sudo apt-get install libusb-1.0-0-dev (Linux)"
            )
        if not webusb_available:
            raise DeviceConnectionError("No WebUSB device available")
        # WebUSB uses create() which finds the first available device
        try:
            connection = await WebUSBDeviceConnection.create()
            conn_type = ConnectionTypeMap.WEBUSB.value
        except Exception as e:
            error_msg = str(e)
            # Check for permission errors
            if "Access denied" in error_msg or "insufficient permissions" in error_msg.lower() or "errno 13" in error_msg.lower():
                raise DeviceConnectionError(
                    f"WebUSB permission denied: {error_msg}\n\n"
                    "To fix USB permissions on macOS:\n"
                    "  1. Try using HID connection instead: --connection hid\n"
                    "  2. Or run with sudo (not recommended): sudo ./test_app/run.sh ...\n"
                    "  3. Or install libusb with proper permissions:\n"
                    "     brew install libusb\n"
                    "     Then try running again.\n\n"
                    "Note: HID connection typically has better permission handling."
                )
            raise DeviceConnectionError(f"Failed to create WebUSB connection: {error_msg}")

    else:
        raise ValueError(f"Invalid connection type: {connection_type}")

    if not connection:
        raise DeviceConnectionError("Failed to create connection")

    return connection, conn_type

