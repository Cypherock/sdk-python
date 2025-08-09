#!/bin/bash
# App Manager proto compiler using betterproto (equivalent to TypeScript version)

set -e

# Clean up existing generated files
rm -rf ./src/proto/generated/*.py || true
rm -rf ./src/proto/generated/manager || true

# Create output directory
mkdir -p src/proto/generated

# Cross-platform Python command detection (same logic as TypeScript version)
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi

# Step 1: Compile .proto files using betterproto (equivalent to protoc + ts-proto)
# Exclude auth_card.proto and auth_device.proto
protoc --python_betterproto_out=./src/proto/generated \
    --proto_path="../../submodules/common/proto" \
    ../../submodules/common/proto/manager/common.proto \
    ../../submodules/common/proto/manager/core.proto \
    ../../submodules/common/proto/manager/firmware_update.proto \
    ../../submodules/common/proto/manager/get_device_info.proto \
    ../../submodules/common/proto/manager/get_logs.proto \
    ../../submodules/common/proto/manager/get_wallets.proto \
    ../../submodules/common/proto/manager/train_card.proto \
    ../../submodules/common/proto/manager/train_joystick.proto \
    ../../submodules/common/proto/manager/wallet_selector.proto

# Step 2: Extract and consolidate types (equivalent to extractTypes/index.js)
$PYTHON_CMD ../../scripts/extract_types/__init__.py ./src/proto/generated ./src/proto/generated/types.py