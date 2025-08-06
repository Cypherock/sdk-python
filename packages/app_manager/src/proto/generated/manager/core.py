# Generated from manager.py
from dataclasses import dataclass
from typing import List, Optional
import betterproto
from .. import common
from .. import error

@dataclass
class Query(betterproto.Message):
    get_device_info: "GetDeviceInfoRequest" = betterproto.message_field(
        1, group="request"
    )
    get_wallets: "GetWalletsRequest" = betterproto.message_field(2, group="request")
    auth_device: "AuthDeviceRequest" = betterproto.message_field(3, group="request")
    auth_card: "AuthCardRequest" = betterproto.message_field(4, group="request")
    get_logs: "GetLogsRequest" = betterproto.message_field(5, group="request")
    train_joystick: "TrainJoystickRequest" = betterproto.message_field(
        6, group="request"
    )
    train_card: "TrainCardRequest" = betterproto.message_field(7, group="request")
    firmware_update: "FirmwareUpdateRequest" = betterproto.message_field(
        8, group="request"
    )
    select_wallet: "SelectWalletRequest" = betterproto.message_field(9, group="request")




@dataclass
class Result(betterproto.Message):
    get_device_info: "GetDeviceInfoResponse" = betterproto.message_field(
        1, group="response"
    )
    get_wallets: "GetWalletsResponse" = betterproto.message_field(2, group="response")
    auth_device: "AuthDeviceResponse" = betterproto.message_field(3, group="response")
    auth_card: "AuthCardResponse" = betterproto.message_field(4, group="response")
    get_logs: "GetLogsResponse" = betterproto.message_field(5, group="response")
    train_joystick: "TrainJoystickResponse" = betterproto.message_field(
        6, group="response"
    )
    train_card: "TrainCardResponse" = betterproto.message_field(7, group="response")
    common_error: error.CommonError = betterproto.message_field(8, group="response")
    firmware_update: "FirmwareUpdateResponse" = betterproto.message_field(
        9, group="response"
    )
    select_wallet: "SelectWalletResponse" = betterproto.message_field(
        10, group="response"
    )

