from typing import Callable, Optional, Protocol
from packages.interfaces import IDevice, IDeviceConnection
from packages.app_manager.src.proto.generated.types import IVersion, UpdateFirmwareStatus

# Re-export types
__all__ = ['GetDevices', 'CreateDeviceConnection', 'UpdateFirmwareEventHandler', 'IUpdateFirmwareParams']

GetDevices = Callable[[], list[IDevice]]

CreateDeviceConnection = Callable[[IDevice], IDeviceConnection]

UpdateFirmwareEventHandler = Callable[[UpdateFirmwareStatus], None]


class IUpdateFirmwareParams(Protocol):
    firmware: Optional[bytes]
    version: Optional[IVersion]
    allowPrerelease: Optional[bool]
    createConnection: CreateDeviceConnection
    getDevices: GetDevices
    onProgress: Optional[Callable[[int], None]]
    onEvent: Optional[UpdateFirmwareEventHandler]
