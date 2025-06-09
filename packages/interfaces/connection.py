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
    deviceState: DeviceState
    vendorId: int
    productId: int
    serial: str
    type: str

class PoolData(TypedDict):
    id: str
    data: bytearray

@runtime_checkable
class IDeviceConnection(Protocol):
    async def getConnectionType(self) -> str:
        ...

    async def isConnected(self) -> bool:
        ...

    async def beforeOperation(self) -> None:
        ...

    async def afterOperation(self) -> None:
        ...

    async def getSequenceNumber(self) -> int:
        ...

    async def getNewSequenceNumber(self) -> int:
        ...

    async def getDeviceState(self) -> DeviceState:
        ...

    async def send(self, data: bytearray) -> None:
        ...

    async def receive(self) -> Optional[bytearray]:
        ...

    async def peek(self) -> List[PoolData]:
        ...

    async def destroy(self) -> None:
        ...
