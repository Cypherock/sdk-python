# Generated from manager.py
from dataclasses import dataclass
from typing import List, Optional
import betterproto
from .. import common
from .. import error

class AuthDeviceStatus(betterproto.Enum):
    AUTH_DEVICE_STATUS_INIT = 0
    AUTH_DEVICE_STATUS_USER_CONFIRMED = 1




class OnboardingStep(betterproto.Enum):
    ONBOARDING_STEP_VIRGIN_DEVICE = 0
    ONBOARDING_STEP_DEVICE_AUTH = 1
    ONBOARDING_STEP_JOYSTICK_TRAINING = 2
    ONBOARDING_STEP_CARD_CHECKUP = 3
    ONBOARDING_STEP_CARD_AUTHENTICATION = 4
    ONBOARDING_STEP_COMPLETE = 5




@dataclass
class AuthDeviceInitiateRequest(betterproto.Message):
    pass




@dataclass
class AuthDeviceChallengeRequest(betterproto.Message):
    challenge: bytes = betterproto.bytes_field(1)




@dataclass
class AuthDeviceResult(betterproto.Message):
    verified: bool = betterproto.bool_field(1)




@dataclass
class AuthDeviceSerialSigResponse(betterproto.Message):
    postfix1: bytes = betterproto.bytes_field(1)
    postfix2: bytes = betterproto.bytes_field(2)
    serial: bytes = betterproto.bytes_field(3)
    signature: bytes = betterproto.bytes_field(4)




@dataclass
class AuthDeviceChallengeSigResponse(betterproto.Message):
    postfix1: bytes = betterproto.bytes_field(1)
    postfix2: bytes = betterproto.bytes_field(2)
    signature: bytes = betterproto.bytes_field(3)




@dataclass
class AuthDeviceRequest(betterproto.Message):
    initiate: "AuthDeviceInitiateRequest" = betterproto.message_field(
        1, group="request"
    )
    challenge: "AuthDeviceChallengeRequest" = betterproto.message_field(
        2, group="request"
    )
    result: "AuthDeviceResult" = betterproto.message_field(3, group="request")




@dataclass
class AuthDeviceResponse(betterproto.Message):
    serial_signature: "AuthDeviceSerialSigResponse" = betterproto.message_field(
        1, group="response"
    )
    challenge_signature: "AuthDeviceChallengeSigResponse" = betterproto.message_field(
        2, group="response"
    )
    flow_complete: "AuthDeviceCompletion" = betterproto.message_field(
        4, group="response"
    )
    common_error: error.CommonError = betterproto.message_field(3, group="response")




