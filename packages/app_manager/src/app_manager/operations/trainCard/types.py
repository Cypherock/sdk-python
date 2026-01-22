from typing import Callable, Optional, Protocol
from app_manager.proto.generated.manager.train_card_pb2 import (
    TrainCardResult,
    TrainCardStatus,
)

# Re-export types
__all__ = ["TrainCardEventHandler", "ITrainCardParams"]

TrainCardEventHandler = Callable[[TrainCardStatus], None]


class ITrainCardParams(Protocol):
    onWallets: Callable[[TrainCardResult], bool]
    onEvent: Optional[TrainCardEventHandler]
