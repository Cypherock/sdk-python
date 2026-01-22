from typing import Callable, Optional
from app_manager.proto.generated.manager.train_joystick_pb2 import TrainJoystickStatus

# Re-export types
__all__ = ["TrainJoystickEventHandler"]

TrainJoystickEventHandler = Callable[[TrainJoystickStatus], None]
