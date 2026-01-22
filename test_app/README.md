# Cypherock SDK Test Application

This test application allows you to test the Cypherock SDK packages with actual firmware/hardware devices.

## Features

- **Device Discovery**: Automatically discover devices via HID, Serial Port, or WebUSB
- **ManagerApp Tests**: Test device management operations (get device info, wallets, logs, etc.)
- **BtcApp Tests**: Test Bitcoin operations (get public keys, xpubs, sign transactions)
- **Flexible Connection**: Support for multiple connection types with automatic fallback

## Usage

### Quick Start (Recommended)

**Important:** If `hidapi` is installed but Python can't find it, reinstall the Python package first:

```bash
poetry run pip install --force-reinstall --no-cache-dir hid
```

Then use the helper script which automatically sets library paths:

```bash
# List devices
./test_app/run.sh --list-devices

# Run tests
./test_app/run.sh --test manager-device-info
```

**Note:** The test app will work with any available connection type (HID, Serial, or WebUSB). If HID is unavailable, it will automatically try Serial or WebUSB.

### Direct Usage

If running directly, you may need to set library paths first (macOS):

```bash
# Set library path for macOS
export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH

# Then run commands
poetry run python test_app/main.py --list-devices
```

### List Available Devices

```bash
poetry run python test_app/main.py --list-devices
# Or use the helper script:
./test_app/run.sh --list-devices
```

### Run All Tests

```bash
poetry run python test_app/main.py --test all
```

### Run ManagerApp Tests

```bash
# Run all ManagerApp tests
poetry run python test_app/main.py --test manager-all

# Run specific ManagerApp tests
poetry run python test_app/main.py --test manager-device-info
poetry run python test_app/main.py --test manager-wallets
poetry run python test_app/main.py --test manager-logs
poetry run python test_app/main.py --test manager-sdk-version
```

### Run BtcApp Tests

```bash
# Run all BtcApp tests
poetry run python test_app/main.py --test btc-all

# Get public key for a specific path
poetry run python test_app/main.py --test btc-public-key --btc-path "m/84'/0'/0'/0/0"

# Get extended public keys
poetry run python test_app/main.py --test btc-xpubs --btc-paths "m/84'/0'/0'" "m/49'/0'/0'"

# Sign a transaction (requires transaction hex)
poetry run python test_app/main.py --test btc-sign-txn --txn-hex "0100000001..."
```

### Connection Options

```bash
# Use specific connection type
poetry run python test_app/main.py --test manager-device-info --connection hid
poetry run python test_app/main.py --test manager-device-info --connection serial
poetry run python test_app/main.py --test manager-device-info --connection webusb

# Use specific device index (if multiple devices are connected)
poetry run python test_app/main.py --test manager-device-info --device-index 1
```

## Available Tests

### ManagerApp Tests

- `manager-device-info`: Get device information
- `manager-wallets`: List all wallets on the device
- `manager-logs`: Get device logs
- `manager-select-wallet`: Select a wallet (may require user interaction)
- `manager-sdk-version`: Get SDK version and compatibility info
- `manager-all`: Run all ManagerApp tests

### BtcApp Tests

- `btc-public-key`: Get public key for a BIP32 path
- `btc-xpubs`: Get extended public keys for multiple paths
- `btc-sign-txn`: Sign a Bitcoin transaction
- `btc-all`: Run all BtcApp tests

## Examples

### Example 1: Quick Device Check

```bash
# List devices and check SDK version
poetry run python test_app/main.py --list-devices
poetry run python test_app/main.py --test manager-sdk-version
```

### Example 2: Test Bitcoin Operations

```bash
# Get public key for a native segwit address
poetry run python test_app/main.py --test btc-public-key --btc-path "m/84'/0'/0'/0/0"

# Get xpubs for different address types
poetry run python test_app/main.py --test btc-xpubs \
  --btc-paths "m/84'/0'/0'" "m/49'/0'/0'" "m/44'/0'/0'"
```

### Example 3: Full Test Suite

```bash
# Run all tests with automatic device detection
poetry run python test_app/main.py --test all
```

## Requirements

- A Cypherock X1 hardware device connected via HID, Serial Port, or WebUSB
- Python 3.11+
- All SDK dependencies installed (run `make setup`)

### System Dependencies

**macOS:**
```bash
brew install hidapi libusb
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install libhidapi-dev libusb-1.0-0-dev
```

**Windows:**
- Install libusb and hidapi libraries manually or via package manager

## Troubleshooting

### No devices found

- Ensure the device is connected and powered on
- Check that the device is not in use by another application
- Try different connection types: `--connection hid`, `--connection serial`, or `--connection webusb`

### Permission errors (Linux)

You may need to add udev rules for USB devices:

```bash
# Create udev rule for Cypherock devices
sudo nano /etc/udev/rules.d/99-cypherock.rules
```

Add:
```
SUBSYSTEM=="usb", ATTR{idVendor}=="3503", MODE="0666"
```

Then reload:
```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### Missing system libraries

If you see errors like "Unable to load libhidapi", install the required system libraries:

**macOS:**
```bash
brew install hidapi libusb
# After installing, reinstall the Python hid package:
poetry run pip install --force-reinstall --no-cache-dir hid
```

**Linux:**
```bash
sudo apt-get install libhidapi-dev libusb-1.0-0-dev
# After installing, reinstall the Python hid package:
poetry run pip install --force-reinstall --no-cache-dir hid
```

**Note:** If `hidapi` is already installed but Python still can't find it, try:

1. **Use the helper script** (easiest):
   ```bash
   ./test_app/run.sh --list-devices
   ```

2. **Set library path manually** (macOS):
   ```bash
   export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH
   poetry run python test_app/main.py --list-devices
   ```

3. **Reinstall the Python `hid` package**:
   ```bash
   poetry run pip install --force-reinstall --no-cache-dir hid
   ```

4. **Restart your terminal/Python environment** after installing system libraries

### HID Connection Errors

If you see errors like `module 'hid' has no attribute 'device'` when trying to connect via HID:

This usually means the Python `hid` package (hidapi) is not properly installed or is missing required methods. Try:

1. **Reinstall the hid package**:
   ```bash
   poetry run pip install --force-reinstall --no-cache-dir hid
   ```

2. **Verify the system library is installed**:
   ```bash
   brew install hidapi  # macOS
   # or
   sudo apt-get install libhidapi-dev  # Linux
   ```

3. **Try using WebUSB instead** (if available):
   ```bash
   ./test_app/run.sh --test manager-device-info --connection webusb
   ```

4. **Check if devices are discoverable**:
   ```bash
   ./test_app/run.sh --list-devices
   ```
   If devices are listed but connection fails, the issue is with the HID library installation.

### USB Permission Errors (WebUSB)

If you see errors like `[Errno 13] Access denied (insufficient permissions)` when using WebUSB:

**macOS:**
1. **Recommended:** Use HID connection instead (better permission handling):
   ```bash
   ./test_app/run.sh --test manager-device-info --connection hid
   ```

2. **Alternative:** Run with sudo (not recommended for development):
   ```bash
   sudo ./test_app/run.sh --test manager-device-info --connection webusb
   ```

3. **Alternative:** Ensure libusb is properly installed:
   ```bash
   brew install libusb
   # Then try again
   ```

**Linux:**
Create a udev rule (see "Linux USB Permissions" section above).

**Note:** HID connection typically has better permission handling and is recommended over WebUSB when available.

### Connection errors

- Try disconnecting and reconnecting the device
- Check if the device is in bootloader mode (some operations may not work)
- Use `--list-devices` to verify the device is detected
- If a specific connection type fails, try another: `--connection hid`, `--connection serial`, or `--connection webusb`

