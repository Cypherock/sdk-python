# Generated from manager.py
from dataclasses import dataclass
from typing import List, Optional
import betterproto
from .. import common
from .. import error

class GetLogsStatus(betterproto.Enum):
    GET_LOGS_STATUS_INIT = 0
    GET_LOGS_STATUS_USER_CONFIRMED = 1




@dataclass
class GetLogsInitiateRequest(betterproto.Message):
    pass




@dataclass
class GetLogsFetchNextRequest(betterproto.Message):
    pass




@dataclass
class GetLogsDataResponse(betterproto.Message):
    data: bytes = betterproto.bytes_field(1)
    has_more: bool = betterproto.bool_field(2)




@dataclass
class GetLogsErrorResponse(betterproto.Message):
    logs_disabled: bool = betterproto.bool_field(1)




@dataclass
class GetLogsRequest(betterproto.Message):
    initiate: "GetLogsInitiateRequest" = betterproto.message_field(1, group="request")
    fetch_next: "GetLogsFetchNextRequest" = betterproto.message_field(
        2, group="request"
    )




@dataclass
class GetLogsResponse(betterproto.Message):
    logs: "GetLogsDataResponse" = betterproto.message_field(1, group="response")
    common_error: error.CommonError = betterproto.message_field(2, group="response")
    error: "GetLogsErrorResponse" = betterproto.message_field(3, group="response")




