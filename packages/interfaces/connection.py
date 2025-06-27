from enum import Enum
from typing import List, Optional, Protocol, TypedDict, runtime_checkable

class ConnectionTypeMap(str, Enum):
    SERIAL_PORT = 'serial'
    HID = 'hid'
    WEBUSB = 'webusb'

class DeviceState(Enum):
    BOOTLOADER = 0
    INITIAL = 1
    MAIN = 2

class IDevice(TypedDict):
    path: str
    device_state: DeviceState
    vendor_id: int
    product_id: int
    serial: str
    type: str

class PoolData(TypedDict):
    id: str
    data: bytearray

@runtime_checkable
class IDeviceConnection(Protocol):
    async def get_connection_type(self) -> str:
        ...

    async def is_connected(self) -> bool:
        ...

    async def before_operation(self) -> None:
        ...

    async def after_operation(self) -> None:
        ...

    async def get_sequence_number(self) -> int:
        ...

    async def get_new_sequence_number(self) -> int:
        ...

    async def get_device_state(self) -> DeviceState:
        ...

    async def send(self, data: bytearray) -> None:
        ...

    async def receive(self) -> Optional[bytearray]:
        ...

    async def peek(self) -> List[PoolData]:
        ...

    async def destroy(self) -> None:
        ...
