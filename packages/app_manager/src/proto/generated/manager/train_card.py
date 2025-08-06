# Generated from manager.py
from dataclasses import dataclass
from typing import List, Optional
import betterproto
from .. import common
from .. import error

class TrainCardStatus(betterproto.Enum):
    TRAIN_CARD_STATUS_INIT = 0
    TRAIN_CARD_STATUS_CARD_TAPPED = 1




@dataclass
class ExistingWalletItem(betterproto.Message):
    id: bytes = betterproto.bytes_field(1)
    name: str = betterproto.string_field(2)




@dataclass
class TrainCardInitiate(betterproto.Message):
    pass




@dataclass
class TrainCardVerification(betterproto.Message):
    self_created: bool = betterproto.bool_field(1)




@dataclass
class TrainCardResult(betterproto.Message):
    wallet_list: List["ExistingWalletItem"] = betterproto.message_field(1)
    card_paired: bool = betterproto.bool_field(2)




@dataclass
class TrainCardComplete(betterproto.Message):
    pass




@dataclass
class TrainCardRequest(betterproto.Message):
    initiate: "TrainCardInitiate" = betterproto.message_field(1, group="request")
    wallet_verify: "TrainCardVerification" = betterproto.message_field(
        2, group="request"
    )




@dataclass
class TrainCardResponse(betterproto.Message):
    result: "TrainCardResult" = betterproto.message_field(1, group="response")
    flow_complete: "TrainCardComplete" = betterproto.message_field(2, group="response")
    common_error: error.CommonError = betterproto.message_field(3, group="response")




