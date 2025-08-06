# Generated from manager.py
from dataclasses import dataclass
from typing import List, Optional
import betterproto
from .. import common
from .. import error

@dataclass
class SelectWalletIntiateRequest(betterproto.Message):
    pass




@dataclass
class SelectWalletResultResponse(betterproto.Message):
    wallet: "WalletItem" = betterproto.message_field(1)




@dataclass
class SelectWalletRequest(betterproto.Message):
    initiate: "SelectWalletIntiateRequest" = betterproto.message_field(
        1, group="request"
    )




@dataclass
class SelectWalletResponse(betterproto.Message):
    result: "SelectWalletResultResponse" = betterproto.message_field(
        1, group="response"
    )
    common_error: error.CommonError = betterproto.message_field(2, group="response")




