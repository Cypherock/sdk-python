from typing import Callable, Optional, Protocol
from packages.app_manager.src.proto.generated.types import ITrainCardResult, TrainCardStatus

# Re-export types
__all__ = ['TrainCardEventHandler', 'ITrainCardParams']

TrainCardEventHandler = Callable[[TrainCardStatus], None]


class ITrainCardParams(Protocol):
    onWallets: Callable[[ITrainCardResult], bool]
    onEvent: Optional[TrainCardEventHandler]
