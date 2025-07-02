import hid
import asyncio
from typing import Dict, List, Any, Optional, cast

from packages.interfaces import (
    DeviceState,
    IDevice,
    ConnectionTypeMap
)

def format_device_info(device: Dict[str, Any]) -> Optional[IDevice]:
    vendor_id = device.get('vendor_id')
    product_id = device.get('product_id')
    serial_number = device.get('serial_number')

    if (
            device.get('path') and
            vendor_id == 0x3503 and
            product_id == 0x0103 and
            serial_number
    ):
        return cast(IDevice, {
            'path': device['path'].decode('utf-8'),
            'deviceState': DeviceState.MAIN,
            'vendorId': vendor_id,
            'productId': product_id,
            'serial': serial_number,
            'type': ConnectionTypeMap.HID,
        })

    return None


async def get_available_devices() -> List[IDevice]:
    device_list: List[IDevice] = []
    all_hid_devices = await asyncio.to_thread(hid.enumerate)

    for port_param in all_hid_devices:
        device = format_device_info(port_param)
        if device:
            device_list.append(device)

    return device_list