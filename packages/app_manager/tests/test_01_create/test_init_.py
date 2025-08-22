import pytest
from unittest.mock import patch
from packages.interfaces.__mocks__.connection import MockDeviceConnection
from packages.app_manager.src.__mocks__ import sdk as sdk_mocks
from packages.app_manager.src import ManagerApp

@pytest.fixture
async def connection():
    connection = await MockDeviceConnection.create()
    yield connection
    await connection.destroy()

@pytest.mark.asyncio
async def test_should_be_able_to_create_manager_app_instance(connection):
    with patch('packages.core.src.sdk.SDK.create', sdk_mocks.create):
        await ManagerApp.create(connection)