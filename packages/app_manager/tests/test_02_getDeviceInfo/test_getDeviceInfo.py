import pytest
from unittest.mock import patch
from packages.interfaces.__mocks__.connection import MockDeviceConnection
from packages.app_manager.tests.test_02_getDeviceInfo.__helpers__ import clear_mocks, expect_mock_calls, setup_mocks
from packages.app_manager.tests.test_02_getDeviceInfo.__fixtures__ import fixtures
from packages.app_manager.src import ManagerApp
from packages.app_manager.src.__mocks__ import sdk as sdk_mocks


@pytest.fixture
async def connection():
    connection = await MockDeviceConnection.create()
    yield connection
    await connection.destroy()


@pytest.mark.asyncio
@patch('packages.core.src.sdk.SDK.create', sdk_mocks.create)
class TestManagerAppGetDeviceInfo:
    @pytest.mark.parametrize("test_case", fixtures['valid'])
    async def test_should_be_able_to_get_info(self, connection, test_case):
        clear_mocks()
        manager_app = await ManagerApp.create(connection)
        setup_mocks(test_case)
        
        with patch.object(manager_app._sdk, 'run_operation', return_value=test_case['output']):
            output = await manager_app.get_device_info()
            assert output == test_case['output']
        
        expect_mock_calls(test_case)
        await manager_app.destroy()

    @pytest.mark.parametrize("test_case", fixtures['invalid_data'])
    async def test_should_throw_error_when_device_returns_invalid_data(self, connection, test_case):
        clear_mocks()
        manager_app = await ManagerApp.create(connection)
        setup_mocks(test_case)
        
        from packages.interfaces.errors.app_error import DeviceAppErrorType
        error = test_case['error_instance'](DeviceAppErrorType.INVALID_MSG_FROM_DEVICE)
        with patch.object(manager_app._sdk, 'run_operation', side_effect=error):
            with pytest.raises(test_case['error_instance']):
                await manager_app.get_device_info()
        
        expect_mock_calls(test_case)
        await manager_app.destroy()

    @pytest.mark.parametrize("test_case", fixtures['error'])
    async def test_should_throw_error_when_device_returns_error(self, connection, test_case):
        clear_mocks()
        manager_app = await ManagerApp.create(connection)
        setup_mocks(test_case)
        
        from packages.interfaces.errors.app_error import DeviceAppErrorType
        if 'error_message' in test_case and 'Unknown application error' in test_case['error_message']:
            error = test_case['error_instance'](DeviceAppErrorType.UNKNOWN_ERROR)
        else:
            error = test_case['error_instance'](DeviceAppErrorType.CORRUPT_DATA)
        with patch.object(manager_app._sdk, 'run_operation', side_effect=error):
            with pytest.raises(test_case['error_instance']):
                await manager_app.get_device_info()
        
        expect_mock_calls(test_case)
        await manager_app.destroy()
