import pytest
import re
from packages.interfaces.__mocks__.connection import MockDeviceConnection
from packages.app_btc.src import BtcApp, set_bitcoin_lib
from .__helpers__ import clear_mocks, expect_mock_calls, setup_mocks
from .__fixtures__ import fixtures
import bitcoinlib


class TestBtcAppGetPublicKey:
    """Test BtcApp.getPublicKey functionality."""
    
    @pytest.fixture
    async def btc_app(self):
        """Create and cleanup BtcApp instance."""
        clear_mocks()
        
        connection = await MockDeviceConnection.create()
        btc_app = await BtcApp.create(connection)
        set_bitcoin_lib(bitcoinlib)
        
        yield btc_app
        
        await btc_app.destroy()
    
    @pytest.mark.asyncio
    async def test_should_be_able_to_get_public_key(self, btc_app):
        """Test valid getPublicKey operations."""
        for test_case in fixtures.valid:
            # Setup mocks for this test case
            on_event = setup_mocks(test_case)
            
            # Execute getPublicKey with test parameters
            output = await btc_app.get_public_key(
                **test_case.params,
                on_event=on_event,
            )
            
            # Verify output matches expected result
            assert output == test_case.output
            
            # Verify mock calls were as expected
            expect_mock_calls(test_case, on_event)
    
    @pytest.mark.asyncio
    async def test_should_throw_error_with_invalid_arguments(self, btc_app):
        """Test getPublicKey with invalid arguments."""
        for test_case in fixtures.invalid_args:
            setup_mocks(test_case)
            
            # Expect the operation to raise the specified error
            with pytest.raises(test_case.error_instance):
                await btc_app.get_public_key(test_case.params)
            
            # If there's a specific error message pattern, verify it
            if test_case.error_message:
                try:
                    await btc_app.get_public_key(test_case.params)
                except Exception as error:
                    if isinstance(test_case.error_message, re.Pattern):
                        assert test_case.error_message.search(str(error))
                    else:
                        assert test_case.error_message in str(error)
    
    @pytest.mark.asyncio
    async def test_should_throw_error_when_device_returns_invalid_data(self, btc_app):
        """Test getPublicKey when device returns invalid data."""
        for test_case in fixtures.invalid_data:
            setup_mocks(test_case)
            
            # Expect the operation to raise the specified error
            with pytest.raises(test_case.error_instance):
                await btc_app.get_public_key(test_case.params)
            
            # If there's a specific error message pattern, verify it
            if test_case.error_message:
                try:
                    await btc_app.get_public_key(test_case.params)
                except Exception as error:
                    if isinstance(test_case.error_message, re.Pattern):
                        assert test_case.error_message.search(str(error))
                    else:
                        assert test_case.error_message in str(error)
            
            # Verify mock calls were as expected
            expect_mock_calls(test_case, setup_mocks(test_case))
    
    @pytest.mark.asyncio
    async def test_should_throw_error_when_device_returns_error(self, btc_app):
        """Test getPublicKey when device returns errors."""
        for test_case in fixtures.error:
            setup_mocks(test_case)
            
            # Expect the operation to raise the specified error
            with pytest.raises(test_case.error_instance):
                await btc_app.get_public_key(test_case.params)
            
            # If there's a specific error message pattern, verify it
            if test_case.error_message:
                try:
                    await btc_app.get_public_key(test_case.params)
                except Exception as error:
                    if isinstance(test_case.error_message, re.Pattern):
                        assert test_case.error_message.search(str(error))
                    else:
                        assert test_case.error_message in str(error)
            
            # Verify mock calls were as expected
            expect_mock_calls(test_case, setup_mocks(test_case))


# Standalone test functions for pytest discovery
@pytest.fixture
async def mock_btc_app():
    """Standalone fixture for BtcApp."""
    clear_mocks()
    
    connection = await MockDeviceConnection.create()
    btc_app = await BtcApp.create(connection)
    set_bitcoin_lib(bitcoinlib)
    
    yield btc_app
    
    await btc_app.destroy()


@pytest.mark.asyncio
async def test_get_public_key_valid_cases(mock_btc_app):
    """Standalone test for valid getPublicKey cases."""
    for test_case in fixtures.valid:
        on_event = setup_mocks(test_case)
        
        output = await mock_btc_app.get_public_key(
            **test_case.params,
            on_event=on_event,
        )
        
        assert output == test_case.output
        expect_mock_calls(test_case, on_event)


@pytest.mark.asyncio
async def test_get_public_key_invalid_args(mock_btc_app):
    """Standalone test for invalid argument cases."""
    for test_case in fixtures.invalid_args:
        setup_mocks(test_case)
        
        with pytest.raises(test_case.error_instance):
            await mock_btc_app.get_public_key(test_case.params)


@pytest.mark.asyncio
async def test_get_public_key_invalid_data(mock_btc_app):
    """Standalone test for invalid data cases."""
    for test_case in fixtures.invalid_data:
        setup_mocks(test_case)
        
        with pytest.raises(test_case.error_instance):
            await mock_btc_app.get_public_key(test_case.params)


@pytest.mark.asyncio
async def test_get_public_key_device_errors(mock_btc_app):
    """Standalone test for device error cases."""
    for test_case in fixtures.error:
        setup_mocks(test_case)
        
        with pytest.raises(test_case.error_instance):
            await mock_btc_app.get_public_key(test_case.params)


__all__ = [
    'TestBtcAppGetPublicKey',
    'test_get_public_key_valid_cases',
    'test_get_public_key_invalid_args',
    'test_get_public_key_invalid_data',
    'test_get_public_key_device_errors',
    'mock_btc_app',
]
