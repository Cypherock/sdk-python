import pytest
from packages.interfaces.__mocks__.connection import MockDeviceConnection
from packages.app_manager.src.__mocks__ import sdk as sdk_mocks
from packages.app_manager.src import ManagerApp

@pytest.fixture
async def connection():
    connection = await MockDeviceConnection.create()
    yield connection
    await connection.destroy()

@pytest.fixture(autouse=True)
def setup():
    sdk_mocks.create.reset_mock()

@pytest.mark.asyncio
async def test_should_be_able_to_create_manager_app_instance(connection):
    await ManagerApp.create(connection)
    
    assert sdk_mocks.create.call_count == 1
    assert connection in sdk_mocks.create.call_args[0]