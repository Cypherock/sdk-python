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
