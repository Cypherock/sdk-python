# # Re-export types from generated files
# from .generated.manager import (
#     OnboardingStep,
#     AuthDeviceStatus,
#     AuthCardStatus,
#     GetLogsStatus,
#     TrainJoystickStatus,
#     TrainCardStatus,
#     FirmwareUpdateError,
# )
# from .generated.types import (
#     WalletNotFound,
#     WalletPartialState,
#     CardError,
#     UserRejection,
#     DataFlow,
#     SeedGenerationStatus,
# )

# Re-export types from generated types.py
from .generated.types import *

# UpdateFirmwareStatus enum - used for status tracking during firmware update
# This is not in the proto files but is used internally
from enum import Enum

# change this TS code to python code
# export enum UpdateFirmwareStatus {
#   UPDATE_FIRMWARE_STATUS_INIT = 0,
#   UPDATE_FIRMWARE_STATUS_USER_CONFIRMED = 1,
#   UNRECOGNIZED = -1,
# }

class UpdateFirmwareStatus(Enum):
    UPDATE_FIRMWARE_STATUS_INIT = 0
    UPDATE_FIRMWARE_STATUS_USER_CONFIRMED = 1
    UNRECOGNIZED = -1



# class UpdateFirmwareStatus(Enum):
#     UPDATE_FIRMWARE_STATUS_USER_CONFIRMED = "UPDATE_FIRMWARE_STATUS_USER_CONFIRMED"


# __all__ = [
#     "OnboardingStep",
#     "AuthDeviceStatus",
#     "AuthCardStatus",
#     "GetLogsStatus",
#     "TrainJoystickStatus",
#     "TrainCardStatus",
#     "FirmwareUpdateError",
#     "WalletNotFound",
#     "WalletPartialState",
#     "CardError",
#     "UserRejection",
#     "DataFlow",
#     "SeedGenerationStatus",
#     "UpdateFirmwareStatus",
# ]


__all__ = list(globals().get('__all__', [])) + ["UpdateFirmwareStatus"]