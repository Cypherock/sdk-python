# Re-export types from generated files
from .generated.manager import (
    OnboardingStep,
    AuthDeviceStatus,
    AuthCardStatus,
    GetLogsStatus,
    TrainJoystickStatus,
    TrainCardStatus,
    FirmwareUpdateError,
)
from .generated.types import (
    WalletNotFound,
    WalletPartialState,
    CardError,
    UserRejection,
    DataFlow,
    SeedGenerationStatus,
)

# UpdateFirmwareStatus enum - used for status tracking during firmware update
# This is not in the proto files but is used internally
from enum import Enum


class UpdateFirmwareStatus(Enum):
    UPDATE_FIRMWARE_STATUS_USER_CONFIRMED = "UPDATE_FIRMWARE_STATUS_USER_CONFIRMED"


__all__ = [
    "OnboardingStep",
    "AuthDeviceStatus",
    "AuthCardStatus",
    "GetLogsStatus",
    "TrainJoystickStatus",
    "TrainCardStatus",
    "FirmwareUpdateError",
    "WalletNotFound",
    "WalletPartialState",
    "CardError",
    "UserRejection",
    "DataFlow",
    "SeedGenerationStatus",
    "UpdateFirmwareStatus",
]
