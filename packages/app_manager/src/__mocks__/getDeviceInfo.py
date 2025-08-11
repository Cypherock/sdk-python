from unittest.mock import AsyncMock
from packages.app_manager.src.operations import getDeviceInfo

# Create mock function
get_device_info = AsyncMock()

# Mock the module
getDeviceInfo.get_device_info = get_device_info
