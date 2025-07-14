#!/bin/bash
# Python SDK proto compiler using betterproto (equivalent to TypeScript version)

set -e

# Create output directory
mkdir -p src/encoders/proto/generated

# Cross-platform Python command detection (same logic as TypeScript version)
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi

# Step 1: Compile .proto files using betterproto (equivalent to protoc + ts-proto)
protoc --python_betterproto_out=./src/encoders/proto/generated \
    --proto_path="../../submodules/common/proto" \
    ../../submodules/common/proto/common.proto \
    ../../submodules/common/proto/core.proto \
    ../../submodules/common/proto/error.proto \
    ../../submodules/common/proto/session.proto \
    ../../submodules/common/proto/version.proto

# Step 2: Extract and consolidate types (equivalent to extractTypes/index.js)
$PYTHON_CMD ../../scripts/extract_types/__init__.py ./src/encoders/proto/generated ./src/encoders/proto/generated/types.py
