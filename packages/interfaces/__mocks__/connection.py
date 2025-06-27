import uuid
from typing import List, Optional, Callable

from packages.interfaces.connection import (
    ConnectionTypeMap,
    DeviceState,
    PoolData
)
from packages.interfaces.errors.connection_error import (
    DeviceConnectionError,
    DeviceConnectionErrorType
)

class MockDeviceConnection:
    def __init__(self):
        self.is_connection_open = False
        self.is_destroyed = False
        self.sequence_number = 0
        self.pool: List[PoolData] = []
        self.device_state = DeviceState.MAIN
        self.connection_type = ConnectionTypeMap.SERIAL_PORT.value
        self.on_data: Optional[Callable[[bytes], None]] = None

    def configure_device(self, device_state: DeviceState, connection_type: str) -> None:
        self.device_state = device_state
        self.connection_type = connection_type

    def configure_listeners(self, on_data: Callable[[bytes], None]) -> None:
        self.on_data = on_data

    def remove_listeners(self) -> None:
        self.on_data = None

    @classmethod
    async def create(cls) -> 'MockDeviceConnection':
        return cls()

    async def get_connection_type(self) -> str:
        return self.connection_type

    async def is_connected(self) -> bool:
        return not self.is_destroyed

    async def before_operation(self) -> None:
        self.is_connection_open = True

    async def after_operation(self) -> None:
        self.is_connection_open = False

    async def get_sequence_number(self) -> int:
        return self.sequence_number

    async def get_new_sequence_number(self) -> int:
        self.sequence_number += 1
        return self.sequence_number

    async def get_device_state(self) -> DeviceState:
        return self.device_state

    async def destroy(self) -> None:
        self.is_destroyed = True
        self.is_connection_open = False

    async def send(self, data: bytes) -> None:
        if not self.is_connection_open:
            raise DeviceConnectionError(DeviceConnectionErrorType.CONNECTION_CLOSED)

        if self.on_data:
            self.on_data(data)

    async def mock_device_send(self, data: bytes) -> None:
        self.pool.append({"id": str(uuid.uuid4()), "data": data})

    async def receive(self) -> Optional[bytes]:
        if not self.pool:
            return None
        return self.pool.pop(0).get("data")

    async def peek(self) -> List[PoolData]:
        return self.pool.copy()