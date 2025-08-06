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

# Step 1: Compile all .proto files except auth_card.proto (which has optional fields)
protoc --python_betterproto_out=./src/proto/generated \
    --proto_path="../../submodules/common/proto" \
    ../../submodules/common/proto/manager/auth_device.proto \
    ../../submodules/common/proto/manager/common.proto \
    ../../submodules/common/proto/manager/core.proto \
    ../../submodules/common/proto/manager/firmware_update.proto \
    ../../submodules/common/proto/manager/get_device_info.proto \
    ../../submodules/common/proto/manager/get_logs.proto \
    ../../submodules/common/proto/manager/get_wallets.proto \
    ../../submodules/common/proto/manager/train_card.proto \
    ../../submodules/common/proto/manager/train_joystick.proto \
    ../../submodules/common/proto/manager/wallet_selector.proto

# Step 2: Create individual files by extracting from manager.py
mkdir -p ./src/proto/generated/manager

$PYTHON_CMD -c "
import re
import os

# Read the generated manager.py file
with open('./src/proto/generated/manager.py', 'r') as f:
    content = f.read()

# Define the files to create with their class patterns
files_to_create = {
    'auth_device.py': [
        'AuthDeviceStatus', 'OnboardingStep', 'AuthDeviceInitiateRequest', 
        'AuthDeviceChallengeRequest', 'AuthDeviceResult', 'AuthDeviceSerialSigResponse',
        'AuthDeviceChallengeSigResponse', 'AuthDeviceRequest', 'AuthDeviceResponse'
    ],
    'common.py': [
        'WalletItem', 'SupportedAppletItem'
    ],
    'core.py': [
        'Query', 'Result'
    ],
    'firmware.py': [
        'FirmwareUpdateError', 'FirmwareUpdateInitiateRequest', 'FirmwareUpdateConfirmedResponse',
        'FirmwareUpdateErrorResponse', 'FirmwareUpdateRequest', 'FirmwareUpdateResponse'
    ],
    'get_device_info.py': [
        'GetDeviceInfoIntiateRequest', 'GetDeviceInfoResultResponse', 'GetDeviceInfoRequest', 'GetDeviceInfoResponse'
    ],
    'get_logs.py': [
        'GetLogsStatus', 'GetLogsInitiateRequest', 'GetLogsFetchNextRequest', 'GetLogsDataResponse',
        'GetLogsErrorResponse', 'GetLogsRequest', 'GetLogsResponse'
    ],
    'get_wallets.py': [
        'GetWalletsIntiateRequest', 'GetWalletsResultResponse', 'GetWalletsRequest', 'GetWalletsResponse'
    ],
    'train_card.py': [
        'TrainCardStatus', 'ExistingWalletItem', 'TrainCardInitiate', 'TrainCardVerification',
        'TrainCardResult', 'TrainCardComplete', 'TrainCardRequest', 'TrainCardResponse'
    ],
    'train_joystick.py': [
        'TrainJoystickStatus', 'TrainJoystickInitiate', 'TrainJoystickRequest', 'TrainJoystickResult', 'TrainJoystickResponse'
    ],
    'wallet_selector.py': [
        'SelectWalletIntiateRequest', 'SelectWalletResultResponse', 'SelectWalletRequest', 'SelectWalletResponse'
    ]
}

# Create each file
for filename, classes in files_to_create.items():
    file_content = '''# Generated from manager.py
from dataclasses import dataclass
from typing import List, Optional
import betterproto
from .. import common
from .. import error

'''
    
    # Extract each class from the manager.py content
    for class_name in classes:
        # Find the class definition
        pattern = rf'(@dataclass\s*)?class {class_name}\(.*?\):(.*?)(?=@dataclass|class |$)'
        match = re.search(pattern, content, re.DOTALL)
        if match:
            class_def = match.group(0)
            file_content += class_def + '\n\n'
    
    # Write the file
    with open(f'./src/proto/generated/manager/{filename}', 'w') as f:
        f.write(file_content)

# Create auth_card.py manually (due to optional fields)
auth_card_content = '''# Generated manually due to optional fields
from dataclasses import dataclass, field
from typing import Optional
import betterproto

@dataclass
class AuthCardStatus(betterproto.Enum):
    AUTH_CARD_STATUS_INIT = 0
    AUTH_CARD_STATUS_USER_CONFIRMED = 1
    AUTH_CARD_STATUS_SERIAL_SIGNED = 2
    AUTH_CARD_STATUS_CHALLENGE_SIGNED = 3
    AUTH_CARD_STATUS_PAIRING_DONE = 4

@dataclass
class AuthCardInitiateRequest(betterproto.Message):
    card_index: Optional[int] = field(default=None)
    is_pair_required: Optional[bool] = field(default=None)

@dataclass
class AuthCardChallengeRequest(betterproto.Message):
    challenge: bytes = field(default=b'')

@dataclass
class AuthCardResult(betterproto.Message):
    verified: bool = field(default=False)

@dataclass
class AuthCardSerialSigResponse(betterproto.Message):
    serial: bytes = field(default=b'')
    signature: bytes = field(default=b'')

@dataclass
class AuthCardChallengeSigResponse(betterproto.Message):
    signature: bytes = field(default=b'')

@dataclass
class AuthCardFlowCompleteResponse(betterproto.Message):
    pass

@dataclass
class AuthCardRequest(betterproto.Message):
    initiate: Optional[AuthCardInitiateRequest] = field(default=None)
    challenge: Optional[AuthCardChallengeRequest] = field(default=None)
    result: Optional[AuthCardResult] = field(default=None)

@dataclass
class AuthCardResponse(betterproto.Message):
    serial_signature: Optional[AuthCardSerialSigResponse] = field(default=None)
    challenge_signature: Optional[AuthCardChallengeSigResponse] = field(default=None)
    common_error: Optional['error.CommonError'] = field(default=None)
    flow_complete: Optional[AuthCardFlowCompleteResponse] = field(default=None)
'''

with open('./src/proto/generated/manager/auth_card.py', 'w') as f:
    f.write(auth_card_content)

# Clean up the original manager.py
os.remove('./src/proto/generated/manager.py')
"

# Step 4: Extract and consolidate types (equivalent to extractTypes/index.js)
$PYTHON_CMD ../../scripts/extract_types/__init__.py ./src/proto/generated ./src/proto/generated/types.py