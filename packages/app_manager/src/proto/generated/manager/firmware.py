# Generated from manager.py
from dataclasses import dataclass
from typing import List, Optional
import betterproto
from .. import common
from .. import error

class FirmwareUpdateError(betterproto.Enum):
    FIRMWARE_UPDATE_ERROR_UNKNOWN = 0
    FIRMWARE_UPDATE_ERROR_VERSION_NOT_ALLOWED = 1




@dataclass
class FirmwareUpdateInitiateRequest(betterproto.Message):
    version: common.Version = betterproto.message_field(1)




@dataclass
class FirmwareUpdateConfirmedResponse(betterproto.Message):
    pass




@dataclass
class FirmwareUpdateErrorResponse(betterproto.Message):
    error: "FirmwareUpdateError" = betterproto.enum_field(1)




@dataclass
class FirmwareUpdateRequest(betterproto.Message):
    initiate: "FirmwareUpdateInitiateRequest" = betterproto.message_field(
        1, group="request"
    )




@dataclass
class FirmwareUpdateResponse(betterproto.Message):
    confirmed: "FirmwareUpdateConfirmedResponse" = betterproto.message_field(
        1, group="response"
    )
    common_error: error.CommonError = betterproto.message_field(2, group="response")
    error: "FirmwareUpdateErrorResponse" = betterproto.message_field(
        3, group="response"
    )




