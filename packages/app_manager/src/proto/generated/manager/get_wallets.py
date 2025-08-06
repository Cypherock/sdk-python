# Generated from manager.py
from dataclasses import dataclass
from typing import List, Optional
import betterproto
from .. import common
from .. import error

@dataclass
class GetWalletsIntiateRequest(betterproto.Message):
    pass




@dataclass
class GetWalletsResultResponse(betterproto.Message):
    wallet_list: List["WalletItem"] = betterproto.message_field(1)




@dataclass
class GetWalletsRequest(betterproto.Message):
    initiate: "GetWalletsIntiateRequest" = betterproto.message_field(1, group="request")




@dataclass
class GetWalletsResponse(betterproto.Message):
    result: "GetWalletsResultResponse" = betterproto.message_field(1, group="response")
    common_error: error.CommonError = betterproto.message_field(2, group="response")




