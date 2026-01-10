"""Test functions for ManagerApp operations."""
import json
from typing import Any

from app_manager import ManagerApp
from interfaces import IDeviceConnection


async def test_get_device_info(connection: IDeviceConnection) -> dict[str, Any]:
    """Test getting device information."""
    print("\n=== Testing get_device_info ===")
    try:
        app = await ManagerApp.create(connection)
        device_info = await app.get_device_info()
        print(f"Device Info: {json.dumps(device_info.__dict__ if hasattr(device_info, '__dict__') else str(device_info), indent=2, default=str)}")
        await app.destroy()
        return {"success": True, "data": device_info}
    except Exception as e:
        print(f"Error: {e}")
        return {"success": False, "error": str(e)}


async def test_get_wallets(connection: IDeviceConnection) -> dict[str, Any]:
    """Test getting wallets."""
    print("\n=== Testing get_wallets ===")
    try:
        app = await ManagerApp.create(connection)
        wallets = await app.get_wallets()
        print(f"Wallets: {json.dumps(wallets.__dict__ if hasattr(wallets, '__dict__') else str(wallets), indent=2, default=str)}")
        await app.destroy()
        return {"success": True, "data": wallets}
    except Exception as e:
        print(f"Error: {e}")
        return {"success": False, "error": str(e)}


async def test_get_logs(connection: IDeviceConnection) -> dict[str, Any]:
    """Test getting logs."""
    print("\n=== Testing get_logs ===")
    try:
        app = await ManagerApp.create(connection)

        def on_event(event):
            print(f"Log event: {event}")

        logs = await app.get_logs(on_event=on_event)
        print(f"Logs: {json.dumps(logs.__dict__ if hasattr(logs, '__dict__') else str(logs), indent=2, default=str)}")
        await app.destroy()
        return {"success": True, "data": logs}
    except Exception as e:
        print(f"Error: {e}")
        return {"success": False, "error": str(e)}


async def test_select_wallet(connection: IDeviceConnection) -> dict[str, Any]:
    """Test selecting a wallet."""
    print("\n=== Testing select_wallet ===")
    try:
        app = await ManagerApp.create(connection)
        result = await app.select_wallet()
        print(f"Select wallet result: {json.dumps(result.__dict__ if hasattr(result, '__dict__') else str(result), indent=2, default=str)}")
        await app.destroy()
        return {"success": True, "data": result}
    except Exception as e:
        print(f"Error: {e}")
        return {"success": False, "error": str(e)}


async def test_get_sdk_version(connection: IDeviceConnection) -> dict[str, Any]:
    """Test getting SDK version."""
    print("\n=== Testing get_sdk_version ===")
    try:
        app = await ManagerApp.create(connection)
        version = app.get_sdk_version()
        print(f"SDK Version: {version}")
        is_supported = app.is_supported()
        print(f"Is Supported: {is_supported}")
        await app.destroy()
        return {"success": True, "version": version, "is_supported": is_supported}
    except Exception as e:
        print(f"Error: {e}")
        return {"success": False, "error": str(e)}


async def run_all_manager_tests(connection: IDeviceConnection) -> dict[str, Any]:
    """Run all ManagerApp tests."""
    print("\n" + "=" * 50)
    print("Running All ManagerApp Tests")
    print("=" * 50)

    results = {}

    results["sdk_version"] = await test_get_sdk_version(connection)
    results["device_info"] = await test_get_device_info(connection)
    results["wallets"] = await test_get_wallets(connection)
    results["logs"] = await test_get_logs(connection)
    # Note: select_wallet might require user interaction, so we'll skip it in "all" tests
    # results["select_wallet"] = await test_select_wallet(connection)

    print("\n" + "=" * 50)
    print("ManagerApp Tests Summary")
    print("=" * 50)
    for test_name, result in results.items():
        status = "✓" if result.get("success") else "✗"
        print(f"{status} {test_name}: {result.get('success', False)}")

    return results

