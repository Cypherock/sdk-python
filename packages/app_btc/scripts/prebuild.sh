#!/bin/bash

set -e

# Ensure we're in the correct directory
cd "$(dirname "$0")/.."

rm -rf ./src/app_btc/proto/generated/*.py || true
rm -rf ./src/app_btc/proto/generated/btc || true

# Create output directory for generated files
mkdir -p src/app_btc/proto/generated

# Use poetry run python3 to ensure we use the root environment with standard protoc
PYTHON_CMD="poetry run python3"

protoc --python_out=./src/app_btc/proto/generated \
    --proto_path="../../submodules/common/proto" \
    ../../submodules/common/proto/btc/core.proto \
    ../../submodules/common/proto/btc/error.proto \
    ../../submodules/common/proto/btc/get_public_key.proto \
    ../../submodules/common/proto/btc/get_xpubs.proto \
    ../../submodules/common/proto/btc/sign_txn.proto \
    ../../submodules/common/proto/common.proto \
    ../../submodules/common/proto/error.proto

# Fix imports in generated files
$PYTHON_CMD ../../scripts/fix_proto_imports.py ./src/app_btc/proto/generated btc
