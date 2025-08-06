# Generated from manager.py
from dataclasses import dataclass
from typing import List, Optional
import betterproto
from .. import common
from .. import error

@dataclass
class WalletItem(betterproto.Message):
    id: bytes = betterproto.bytes_field(1)
    name: str = betterproto.string_field(2)
    has_pin: bool = betterproto.bool_field(3)
    has_passphrase: bool = betterproto.bool_field(4)
    # This field determines whether the particular wallet is in usable state It
    # does not indicate why the wallet is not usable.
    is_valid: bool = betterproto.bool_field(5)




@dataclass
class SupportedAppletItem(betterproto.Message):
    id: int = betterproto.uint32_field(1)
    version: common.Version = betterproto.message_field(2)




