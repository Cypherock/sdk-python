# Generated from manager.py
from dataclasses import dataclass
from typing import List, Optional
import betterproto
from .. import common
from .. import error

@dataclass
class GetDeviceInfoIntiateRequest(betterproto.Message):
    pass




@dataclass
class GetDeviceInfoResultResponse(betterproto.Message):
    device_serial: bytes = betterproto.bytes_field(1)
    firmware_version: common.Version = betterproto.message_field(2)
    is_authenticated: bool = betterproto.bool_field(3)
    applet_list: List["SupportedAppletItem"] = betterproto.message_field(4)
    is_initial: bool = betterproto.bool_field(5)
    onboarding_step: "OnboardingStep" = betterproto.enum_field(6)




@dataclass
class GetDeviceInfoRequest(betterproto.Message):
    initiate: "GetDeviceInfoIntiateRequest" = betterproto.message_field(
        1, group="request"
    )




@dataclass
class GetDeviceInfoResponse(betterproto.Message):
    result: "GetDeviceInfoResultResponse" = betterproto.message_field(
        1, group="response"
    )
    common_error: error.CommonError = betterproto.message_field(2, group="response")




