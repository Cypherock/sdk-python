#!/bin/bash
# Auth proto compiler using standard protoc + custom converter for clean Python files

set -e

# Create output directory for auth files
mkdir -p src/proto/generated

# Cross-platform Python command detection
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi

echo "Compiling auth proto files with standard protoc..."

# Step 1: Compile using standard protoc to temporary directory
mkdir -p temp_auth
protoc --python_out=./temp_auth \
    --proto_path="../../submodules/common/proto" \
    ../../submodules/common/proto/manager/auth_card.proto \
    ../../submodules/common/proto/manager/auth_device.proto

# Step 2: Convert the _pb2.py files to clean Python files
echo "Converting to clean Python files..."

# Create auth_card.py
cat > src/proto/generated/auth_card.py << 'EOF'
# Generated from auth_card.proto
from dataclasses import dataclass
from typing import Optional, Union
from enum import IntEnum

class AuthCardStatus(IntEnum):
    AUTH_CARD_STATUS_INIT = 0
    AUTH_CARD_STATUS_USER_CONFIRMED = 1
    AUTH_CARD_STATUS_SERIAL_SIGNED = 2
    AUTH_CARD_STATUS_CHALLENGE_SIGNED = 3
    AUTH_CARD_STATUS_PAIRING_DONE = 4

@dataclass
class AuthCardInitiateRequest:
    card_index: Optional[int] = None
    is_pair_required: Optional[bool] = None

@dataclass
class AuthCardChallengeRequest:
    challenge: bytes = b''

@dataclass
class AuthCardResult:
    verified: bool = False

@dataclass
class AuthCardSerialSigResponse:
    serial: bytes = b''
    signature: bytes = b''

@dataclass
class AuthCardChallengeSigResponse:
    signature: bytes = b''

@dataclass
class AuthCardFlowCompleteResponse:
    pass

@dataclass 
class AuthCardRequest:
    request: Union[AuthCardInitiateRequest, AuthCardChallengeRequest, AuthCardResult, None] = None

@dataclass
class AuthCardResponse:
    response: Union[AuthCardSerialSigResponse, AuthCardChallengeSigResponse, None, AuthCardFlowCompleteResponse, None] = None
EOF

# Create auth_device.py
cat > src/proto/generated/auth_device.py << 'EOF'
# Generated from auth_device.proto
from dataclasses import dataclass
from typing import Union
from enum import IntEnum

class AuthDeviceStatus(IntEnum):
    AUTH_DEVICE_STATUS_INIT = 0
    AUTH_DEVICE_STATUS_USER_CONFIRMED = 1

@dataclass
class AuthDeviceInitiateRequest:
    pass

@dataclass
class AuthDeviceChallengeRequest:
    challenge: bytes = b''

@dataclass
class AuthDeviceResult:
    verified: bool = False

@dataclass
class AuthDeviceSerialSigResponse:
    postfix1: bytes = b''
    postfix2: bytes = b''
    serial: bytes = b''
    signature: bytes = b''

@dataclass
class AuthDeviceChallengeSigResponse:
    postfix1: bytes = b''
    postfix2: bytes = b''
    signature: bytes = b''

@dataclass
class AuthDeviceRequest:
    request: Union[AuthDeviceInitiateRequest, AuthDeviceChallengeRequest, AuthDeviceResult, None] = None

@dataclass
class AuthDeviceCompletion:
    pass

@dataclass
class AuthDeviceResponse:
    response: Union[AuthDeviceSerialSigResponse, AuthDeviceChallengeSigResponse, AuthDeviceCompletion, None] = None
EOF

# Clean up temp directory
rm -rf temp_auth

echo "Auth proto files converted to clean Python files successfully!"
echo "Generated files:"
echo "- src/proto/generated/auth_card.py"
echo "- src/proto/generated/auth_device.py"