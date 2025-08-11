from typing import Optional
from packages.interfaces import IDeviceConnection
from packages.core.src import sdk as core_sdk
from packages.core.src.types import ISDK

from . import operations
from .services import firmware_service
from .services.firmware import GetLatestFirmwareOptions


class ManagerApp:
    APPLET_ID = 1

    COMPATIBLE_VERSION = {
        'from': '1.0.0',
        'to': '2.0.0',
    }

    def __init__(self, sdk: ISDK):
        self._sdk = sdk

    @classmethod
    async def create(cls, connection: IDeviceConnection) -> 'ManagerApp':
        sdk = await core_sdk.SDK.create(connection, cls.APPLET_ID)
        return cls(sdk)

    def get_sdk_version(self) -> str:
        return self._sdk.get_version()

    def is_supported(self):
        return self._sdk.is_supported()

    async def get_device_info(self):
        return await self._sdk.run_operation(lambda: operations.get_device_info(self._sdk))

    async def get_wallets(self):
        return await self._sdk.run_operation(lambda: operations.get_wallets(self._sdk))

    async def select_wallet(self):
        return await self._sdk.run_operation(lambda: operations.select_wallet(self._sdk))

    async def destroy(self):
        return await self._sdk.destroy()

    async def abort(self):
        await self._sdk.send_abort()
    @classmethod
    async def get_latest_firmware(cls, params: Optional[GetLatestFirmwareOptions] = None):
        return await firmware_service.get_latest(params)

    async def update_firmware(self, params: operations.IUpdateFirmwareParams):
        return await self._sdk.run_operation(lambda: operations.update_firmware(self._sdk, params))