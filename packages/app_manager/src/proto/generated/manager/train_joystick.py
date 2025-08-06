# Generated from manager.py
from dataclasses import dataclass
from typing import List, Optional
import betterproto
from .. import common
from .. import error

class TrainJoystickStatus(betterproto.Enum):
    TRAIN_JOYSTICK_INIT = 0
    TRAIN_JOYSTICK_UP = 1
    TRAIN_JOYSTICK_RIGHT = 2
    TRAIN_JOYSTICK_DOWN = 3
    TRAIN_JOYSTICK_LEFT = 4
    TRAIN_JOYSTICK_CENTER = 5




@dataclass
class TrainJoystickInitiate(betterproto.Message):
    pass




@dataclass
class TrainJoystickRequest(betterproto.Message):
    initiate: "TrainJoystickInitiate" = betterproto.message_field(1, group="request")




@dataclass
class TrainJoystickResult(betterproto.Message):
    pass




@dataclass
class TrainJoystickResponse(betterproto.Message):
    result: "TrainJoystickResult" = betterproto.message_field(1, group="response")
    common_error: error.CommonError = betterproto.message_field(2, group="response")




