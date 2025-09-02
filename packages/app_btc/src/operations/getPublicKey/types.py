from typing import Callable, Optional
from dataclasses import dataclass
from enum import IntEnum
from packages.app_btc.src.proto.generated.btc import GetPublicKeyIntiateRequest


class GetPublicKeyEvent(IntEnum):
    """Events that can occur during get public key operation."""
    INIT = 0
    CONFIRM = 1
    PASSPHRASE = 2
    PIN_CARD = 3
    VERIFY = 4


# Type alias for event handler
GetPublicKeyEventHandler = Callable[[GetPublicKeyEvent], None]

@dataclass
class GetPublicKeyParams(GetPublicKeyIntiateRequest):
    """Parameters for get public key operation. Extends GetPublicKeyIntiateRequest."""
    on_event: Optional[GetPublicKeyEventHandler] = None


@dataclass
class GetPublicKeyResult:
    """Result of get public key operation."""
    public_key: bytes
    address: str


