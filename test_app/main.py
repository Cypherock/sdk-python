#!/usr/bin/env python3
"""Main entry point for the Cypherock SDK test application."""
import argparse
import asyncio
import sys

from device_helper import discover_devices, print_devices, create_connection
from tests_manager import (
    test_get_device_info,
    test_get_wallets,
    test_get_logs,
    test_select_wallet,
    test_get_sdk_version,
    run_all_manager_tests,
)
from tests_btc import (
    test_get_public_key,
    test_get_xpubs,
    test_sign_txn,
    run_all_btc_tests,
)


async def main():
    """Main function to run the test application."""
    parser = argparse.ArgumentParser(
        description="Cypherock SDK Test Application - Test packages with actual firmware"
    )
    parser.add_argument(
        "--connection",
        choices=["auto", "hid", "serial", "webusb"],
        default="auto",
        help="Connection type to use (default: auto)",
    )
    parser.add_argument(
        "--device-index",
        type=int,
        default=0,
        help="Device index to connect to (default: 0)",
    )
    parser.add_argument(
        "--list-devices",
        action="store_true",
        help="List all available devices and exit",
    )

    # Test selection
    parser.add_argument(
        "--test",
        choices=[
            "all",
            "manager-all",
            "btc-all",
            "manager-device-info",
            "manager-wallets",
            "manager-logs",
            "manager-select-wallet",
            "manager-sdk-version",
            "btc-public-key",
            "btc-xpubs",
            "btc-sign-txn",
        ],
        help="Specific test to run",
    )

    # BTC-specific arguments
    parser.add_argument(
        "--btc-path",
        type=str,
        default="m/84'/0'/0'/0/0",
        help="BIP32 path for BTC operations (default: m/84'/0'/0'/0/0)",
    )
    parser.add_argument(
        "--btc-paths",
        nargs="+",
        help="Multiple BIP32 paths for get_xpubs (e.g., --btc-paths \"m/84'/0'/0'\" \"m/49'/0'/0'\")",
    )
    parser.add_argument(
        "--txn-hex",
        type=str,
        help="Transaction hex for sign_txn test",
    )

    args = parser.parse_args()

    # List devices if requested
    if args.list_devices:
        print("Discovering devices...")
        hid_devices, serial_devices, webusb_available = await discover_devices()
        print_devices(hid_devices, serial_devices, webusb_available)
        return

    # If no test specified, show help
    if not args.test:
        parser.print_help()
        print("\nUse --list-devices to see available devices")
        return

    # Create connection
    print(f"Connecting via {args.connection} (device index: {args.device_index})...")
    try:
        connection, conn_type = await create_connection(
            connection_type=args.connection, device_index=args.device_index
        )
        print(f"Connected via {conn_type}")
    except Exception as e:
        print(f"Failed to connect: {e}")
        sys.exit(1)

    try:
        # Run the selected test
        if args.test == "all":
            print("\n" + "=" * 70)
            print("Running All Tests")
            print("=" * 70)
            manager_results = await run_all_manager_tests(connection)
            btc_results = await run_all_btc_tests(connection)
            print("\n" + "=" * 70)
            print("All Tests Complete")
            print("=" * 70)

        elif args.test == "manager-all":
            await run_all_manager_tests(connection)

        elif args.test == "btc-all":
            await run_all_btc_tests(connection)

        elif args.test == "manager-device-info":
            await test_get_device_info(connection)

        elif args.test == "manager-wallets":
            await test_get_wallets(connection)

        elif args.test == "manager-logs":
            await test_get_logs(connection)

        elif args.test == "manager-select-wallet":
            await test_select_wallet(connection)

        elif args.test == "manager-sdk-version":
            await test_get_sdk_version(connection)

        elif args.test == "btc-public-key":
            await test_get_public_key(connection, args.btc_path)

        elif args.test == "btc-xpubs":
            paths = args.btc_paths if args.btc_paths else None
            await test_get_xpubs(connection, paths)

        elif args.test == "btc-sign-txn":
            if not args.txn_hex:
                print("Error: --txn-hex is required for sign_txn test")
                sys.exit(1)
            await test_sign_txn(connection, args.txn_hex)

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\n\nError during test execution: {e}")
        import traceback

        traceback.print_exc()
    finally:
        # Cleanup
        try:
            await connection.destroy()
            print("\nConnection closed")
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(main())

