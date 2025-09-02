from typing import Callable, Optional
from dataclasses import dataclass
from enum import IntEnum
from packages.app_btc.src.proto.generated.btc import GetXpubsIntiateRequest


class GetXpubsEvent(IntEnum):
    """Events that can occur during get xpubs operation."""
    INIT = 0
    CONFIRM = 1
    PASSPHRASE = 2
    PIN_CARD = 3


# Type alias for event handler
GetXpubsEventHandler = Callable[[GetXpubsEvent], None]


@dataclass
class GetXpubsParams(GetXpubsIntiateRequest):
    """Parameters for get xpubs operation. Extends GetXpubsIntiateRequest."""
    on_event: Optional[GetXpubsEventHandler] = None
