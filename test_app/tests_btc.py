"""Test functions for BtcApp operations."""
import json
from typing import Any

from app_btc import BtcApp
from app_btc.operations import GetPublicKeyParams, GetXpubsParams, SignTxnParams
from interfaces import IDeviceConnection


async def test_get_public_key(connection: IDeviceConnection, path: str = "m/84'/0'/0'/0/0") -> dict[str, Any]:
    """Test getting public key."""
    print("\n=== Testing get_public_key ===")
    print(f"Path: {path}")
    try:
        app = await BtcApp.create(connection)
        params = GetPublicKeyParams(path=path)
        result = await app.get_public_key(params)
        print(f"Public Key: {json.dumps(result.__dict__ if hasattr(result, '__dict__') else str(result), indent=2, default=str)}")
        await app.destroy()
        return {"success": True, "data": result}
    except Exception as e:
        print(f"Error: {e}")
        return {"success": False, "error": str(e)}


async def test_get_xpubs(connection: IDeviceConnection, paths: list[str] = None) -> dict[str, Any]:
    """Test getting extended public keys."""
    print("\n=== Testing get_xpubs ===")
    if paths is None:
        paths = ["m/84'/0'/0'", "m/49'/0'/0'", "m/44'/0'/0'"]
    print(f"Paths: {paths}")
    try:
        app = await BtcApp.create(connection)
        params = GetXpubsParams(paths=paths)
        result = await app.get_xpubs(params)
        print(f"Xpubs: {json.dumps(result.__dict__ if hasattr(result, '__dict__') else str(result), indent=2, default=str)}")
        await app.destroy()
        return {"success": True, "data": result}
    except Exception as e:
        print(f"Error: {e}")
        return {"success": False, "error": str(e)}


async def test_sign_txn(connection: IDeviceConnection, txn_hex: str = None) -> dict[str, Any]:
    """Test signing a transaction."""
    print("\n=== Testing sign_txn ===")
    print("Note: This requires a valid transaction hex. Using placeholder.")
    try:
        if not txn_hex:
            print("No transaction hex provided. Skipping sign_txn test.")
            return {"success": False, "error": "No transaction hex provided"}

        app = await BtcApp.create(connection)
        params = SignTxnParams(txn=txn_hex)
        result = await app.sign_txn(params)
        print(f"Signed Transaction: {json.dumps(result.__dict__ if hasattr(result, '__dict__') else str(result), indent=2, default=str)}")
        await app.destroy()
        return {"success": True, "data": result}
    except Exception as e:
        print(f"Error: {e}")
        return {"success": False, "error": str(e)}


async def run_all_btc_tests(connection: IDeviceConnection) -> dict[str, Any]:
    """Run all BtcApp tests."""
    print("\n" + "=" * 50)
    print("Running All BtcApp Tests")
    print("=" * 50)

    results = {}

    # Test get_public_key with a standard path
    results["get_public_key"] = await test_get_public_key(connection, "m/84'/0'/0'/0/0")

    # Test get_xpubs with standard paths
    results["get_xpubs"] = await test_get_xpubs(connection)

    # Note: sign_txn requires a valid transaction, so we'll skip it in "all" tests
    # results["sign_txn"] = await test_sign_txn(connection, txn_hex)

    print("\n" + "=" * 50)
    print("BtcApp Tests Summary")
    print("=" * 50)
    for test_name, result in results.items():
        status = "✓" if result.get("success") else "✗"
        print(f"{status} {test_name}: {result.get('success', False)}")

    return results

