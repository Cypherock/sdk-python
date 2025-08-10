from enum import IntEnum

class UpdateFirmwareStatus(IntEnum):
    UPDATE_FIRMWARE_STATUS_INIT = 0
    UPDATE_FIRMWARE_STATUS_USER_CONFIRMED = 1
    UNRECOGNIZED = -1


