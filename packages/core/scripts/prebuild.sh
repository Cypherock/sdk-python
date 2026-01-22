#!/bin/bash
# Python SDK proto compiler using standard protoc

set -e

# Ensure we're in the correct directory
cd "$(dirname "$0")/.."

rm -rf ./src/core/encoders/proto/generated/*.py || true

# Create output directory for generated files
mkdir -p src/core/encoders/proto/generated

# Use poetry run python3 to ensure we use the root environment with standard protoc
PYTHON_CMD="poetry run python3"

# Compile .proto files using standard protoc
protoc --python_out=./src/core/encoders/proto/generated \
    --proto_path="../../submodules/common/proto" \
    ../../submodules/common/proto/common.proto \
    ../../submodules/common/proto/core.proto \
    ../../submodules/common/proto/error.proto \
    ../../submodules/common/proto/session.proto \
    ../../submodules/common/proto/version.proto

# Fix imports in generated files
$PYTHON_CMD ../../scripts/fix_proto_imports.py ./src/core/encoders/proto/generated core
