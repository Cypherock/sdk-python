import pytest
from packages.interfaces.__mocks__.connection import MockDeviceConnection
from packages.app_btc.src.__mocks__ import sdk as sdk_mocks
from packages.app_btc.src import BtcApp


class TestBtcAppCreate:
    """Test BtcApp.create functionality."""
    
    @pytest.fixture
    async def connection(self):
        """Create and cleanup mock device connection."""
        connection = await MockDeviceConnection.create()
        sdk_mocks.reset_mocks()
        yield connection
        await connection.destroy()
    
    @pytest.mark.asyncio
    async def test_should_be_able_to_create_btc_app_instance(self, connection):
        """Test that BtcApp can be created with a mock connection."""
        # Create BtcApp instance
        btc_app = await BtcApp.create(connection)
        
        # Verify the app was created
        assert btc_app is not None
        assert isinstance(btc_app, BtcApp)
        
        # Verify SDK.create was called once
        assert sdk_mocks.create.call_count == 1
        
        # Verify SDK.create was called with the connection
        create_call_args = sdk_mocks.create.call_args_list[-1]
        assert connection in create_call_args[0]  # Check positional args


# Standalone test functions for pytest discovery
@pytest.fixture
async def mock_connection():
    """Standalone fixture for mock connection."""
    connection = await MockDeviceConnection.create()
    sdk_mocks.reset_mocks()
    yield connection
    await connection.destroy()


@pytest.mark.asyncio
async def test_btc_app_create_standalone(mock_connection):
    """Standalone test for BtcApp creation."""
    btc_app = await BtcApp.create(mock_connection)
    
    assert btc_app is not None
    assert isinstance(btc_app, BtcApp)
    assert sdk_mocks.create.call_count == 1
    
    # Verify connection was passed to SDK.create
    create_call_args = sdk_mocks.create.call_args_list[-1]
    assert mock_connection in create_call_args[0]


__all__ = [
    'TestBtcAppCreate',
    'test_btc_app_create_standalone',
    'mock_connection',
]
