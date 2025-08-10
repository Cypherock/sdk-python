from dataclasses import dataclass
from typing import Optional, List
from enum import IntEnum

class SeedGenerationStatus(IntEnum):
    SEED_GENERATION_STATUS_INIT = 0
    SEED_GENERATION_STATUS_PASSPHRASE = 1
    SEED_GENERATION_STATUS_PIN_CARD = 2
    UNRECOGNIZED = -1

class WalletNotFound(IntEnum):
    WALLET_NOT_FOUND_UNKNOWN = 0
    WALLET_NOT_FOUND_ON_DEVICE = 1
    WALLET_NOT_FOUND_ON_CARD = 2
    UNRECOGNIZED = -1

class WalletPartialState(IntEnum):
    WALLET_PARTIAL_STATE_UNKNOWN = 0
    WALLET_PARTIAL_STATE_LOCKED = 1
    WALLET_PARTIAL_STATE_DELETE = 2
    WALLET_PARTIAL_STATE_UNVERIFIED = 3
    WALLET_PARTIAL_STATE_OUT_OF_SYNC = 4
    UNRECOGNIZED = -1

class CardError(IntEnum):
    """Error logged locally on device but spcific case unknown"""
    CARD_ERROR_UNKNOWN = 0
    """Error occured as card is not paired."""
    CARD_ERROR_NOT_PAIRED = 1
    """Incompatible applet version"""
    CARD_ERROR_SW_INCOMPATIBLE_APPLET = 3
    """Null pointer exception"""
    CARD_ERROR_SW_NULL_POINTER_EXCEPTION = 4
    """Operation failed on card (Tx Exp)"""
    CARD_ERROR_SW_TRANSACTION_EXCEPTION = 5
    """Tapped card family id mismatch"""
    CARD_ERROR_SW_FILE_INVALID = 6
    """Security conditions not satisfied, i.e. pairing session invalid"""
    CARD_ERROR_SW_SECURITY_CONDITIONS_NOT_SATISFIED = 7
    """Wrong card sequence"""
    CARD_ERROR_SW_CONDITIONS_NOT_SATISFIED = 8
    """Invalid APDU length"""
    CARD_ERROR_SW_WRONG_DATA = 9
    """Curropted card"""
    CARD_ERROR_SW_FILE_NOT_FOUND = 10
    """Wallet does not exist on device"""
    CARD_ERROR_SW_RECORD_NOT_FOUND = 11
    """Card is full"""
    CARD_ERROR_SW_FILE_FULL = 12
    """Incorrect pin intered"""
    CARD_ERROR_SW_CORRECT_LENGTH_00 = 13
    """Apllet unknown error"""
    CARD_ERROR_SW_INVALID_INS = 14
    """Card pairing to device missing"""
    CARD_ERROR_SW_NOT_PAIRED = 15
    """Operation failed on card (Crypto Exp)"""
    CARD_ERROR_SW_CRYPTO_EXCEPTION = 16
    """Locked wallet status word, POW meaning proof of word"""
    CARD_ERROR_POW_SW_WALLET_LOCKED = 17
    """Card health critical, migration required"""
    CARD_ERROR_SW_INS_BLOCKED = 18
    """Operation failed on card (Out of boundary)"""
    CARD_ERROR_SW_OUT_OF_BOUNDARY = 19
    UNRECOGNIZED = -1

class UserRejection(IntEnum):
    USER_REJECTION_UNKNOWN = 0
    USER_REJECTION_CONFIRMATION = 1
    UNRECOGNIZED = -1

class DataFlow(IntEnum):
    """protobuf decoding by nanopb api failed"""
    DATA_FLOW_DECODING_FAILED = 0
    """
    query received is: invalid or is of different app_function (eg. device
    auth in between get logs)
    """
    DATA_FLOW_INVALID_QUERY = 1
    """protobuf `optional` fields when checked on receiving end was absent."""
    DATA_FLOW_FIELD_MISSING = 2
    """
    Wrong request is received in app_function. could be at start of flow
    or in-between the flow
    """
    DATA_FLOW_INVALID_REQUEST = 3
    """inactivity during wait-for-data from host. In-between a flow"""
    DATA_FLOW_INACTIVITY_TIMEOUT = 4
    """
    when the flow specific data validity fails. could be at start of flow
    or in-between the flow
    """
    DATA_FLOW_INVALID_DATA = 5
    """
    query received is: when app in unserviceable state (eg. export wallet
    request before on-boarding, export wallet request on unauthenticated
    device on main
    """
    DATA_FLOW_QUERY_NOT_ALLOWED = 6
    UNRECOGNIZED = -1

class AuthCardStatus(IntEnum):
    AUTH_CARD_STATUS_INIT = 0
    AUTH_CARD_STATUS_USER_CONFIRMED = 1
    AUTH_CARD_STATUS_SERIAL_SIGNED = 2
    AUTH_CARD_STATUS_CHALLENGE_SIGNED = 3
    AUTH_CARD_STATUS_PAIRING_DONE = 4
    UNRECOGNIZED = -1

class AuthDeviceStatus(IntEnum):
    AUTH_DEVICE_STATUS_INIT = 0
    AUTH_DEVICE_STATUS_USER_CONFIRMED = 1
    UNRECOGNIZED = -1

class FirmwareUpdateError(IntEnum):
    FIRMWARE_UPDATE_ERROR_UNKNOWN = 0
    FIRMWARE_UPDATE_ERROR_VERSION_NOT_ALLOWED = 1
    UNRECOGNIZED = -1

class OnboardingStep(IntEnum):
    ONBOARDING_STEP_VIRGIN_DEVICE = 0
    ONBOARDING_STEP_DEVICE_AUTH = 1
    ONBOARDING_STEP_JOYSTICK_TRAINING = 2
    ONBOARDING_STEP_CARD_CHECKUP = 3
    ONBOARDING_STEP_CARD_AUTHENTICATION = 4
    ONBOARDING_STEP_COMPLETE = 5
    UNRECOGNIZED = -1

class GetLogsStatus(IntEnum):
    GET_LOGS_STATUS_INIT = 0
    GET_LOGS_STATUS_USER_CONFIRMED = 1
    UNRECOGNIZED = -1

class TrainCardStatus(IntEnum):
    TRAIN_CARD_STATUS_INIT = 0
    TRAIN_CARD_STATUS_CARD_TAPPED = 1
    UNRECOGNIZED = -1

class TrainJoystickStatus(IntEnum):
    TRAIN_JOYSTICK_INIT = 0
    TRAIN_JOYSTICK_UP = 1
    TRAIN_JOYSTICK_RIGHT = 2
    TRAIN_JOYSTICK_DOWN = 3
    TRAIN_JOYSTICK_LEFT = 4
    TRAIN_JOYSTICK_CENTER = 5
    UNRECOGNIZED = -1

class UpdateFirmwareStatus(IntEnum):
    UPDATE_FIRMWARE_STATUS_INIT = 0
    UPDATE_FIRMWARE_STATUS_USER_CONFIRMED = 1
    UNRECOGNIZED = -1

@dataclass
class IAuthCardInitiateRequest:
    card_index: Optional[int] = None
    """
    true: allow pair card: 3 card taps (false 3rd beep if already paired)
    false, undefined: do not pair card: 2 card taps
    """
    is_pair_required: Optional[bool] = None

@dataclass
class IAuthCardChallengeRequest:
    challenge: bytes

@dataclass
class IAuthCardResult:
    verified: bool

@dataclass
class IAuthCardRequest:
    initiate: Optional['IAuthCardInitiateRequest'] = None
    challenge: Optional['IAuthCardChallengeRequest'] = None
    result: Optional['IAuthCardResult'] = None

@dataclass
class IAuthCardSerialSigResponse:
    serial: bytes
    signature: bytes

@dataclass
class IAuthCardChallengeSigResponse:
    signature: bytes

@dataclass
class ICommonError:
    """***** Protocol specific errors ******"""
    unknown_error: Optional[int] = None
    corrupt_data: Optional[DataFlow] = None
    """The user needs to complete device setup"""
    device_setup_required: Optional[int] = None
    """The specified wallet does not exist"""
    wallet_not_found: Optional[WalletNotFound] = None
    """The specified wallet is in partial state"""
    wallet_partial_state: Optional[WalletPartialState] = None
    """
    ***** User action errors ******
    Card Error
    """
    card_error: Optional[CardError] = None
    """User rejection error"""
    user_rejection: Optional[UserRejection] = None

@dataclass
class IAuthCardFlowCompleteResponse:
    pass

@dataclass
class IAuthCardResponse:
    serial_signature: Optional[IAuthCardSerialSigResponse] = None
    challenge_signature: Optional[IAuthCardChallengeSigResponse] = None
    common_error: Optional[ICommonError] = None
    flow_complete: Optional[IAuthCardFlowCompleteResponse] = None

@dataclass
class IAuthDeviceInitiateRequest:
    pass

@dataclass
class IAuthDeviceChallengeRequest:
    challenge: bytes

@dataclass
class IAuthDeviceResult:
    verified: bool

@dataclass
class IAuthDeviceRequest:
    initiate: Optional[IAuthDeviceInitiateRequest] = None
    challenge: Optional[IAuthDeviceChallengeRequest] = None
    result: Optional[IAuthDeviceResult] = None

@dataclass
class IAuthDeviceSerialSigResponse:
    postfix1: bytes
    postfix2: bytes
    serial: bytes
    signature: bytes

@dataclass
class IAuthDeviceChallengeSigResponse:
    postfix1: bytes
    postfix2: bytes
    signature: bytes

@dataclass
class IAuthDeviceCompletion:
    pass

@dataclass
class IAuthDeviceResponse:
    serial_signature: Optional[IAuthDeviceSerialSigResponse] = None
    challenge_signature: Optional[IAuthDeviceChallengeSigResponse] = None
    flow_complete: Optional[IAuthDeviceCompletion] = None
    common_error: Optional[ICommonError] = None

@dataclass
class IGetDeviceInfoIntiateRequest:
    pass

@dataclass
class IGetDeviceInfoRequest:
    initiate: Optional[IGetDeviceInfoIntiateRequest] = None

@dataclass
class IGetWalletsIntiateRequest:
    pass

@dataclass
class IGetWalletsRequest:
    initiate: Optional[IGetWalletsIntiateRequest] = None

@dataclass
class IGetLogsInitiateRequest:
    pass

@dataclass
class IGetLogsFetchNextRequest:
    pass

@dataclass
class IGetLogsRequest:
    initiate: Optional[IGetLogsInitiateRequest] = None
    fetch_next: Optional[IGetLogsFetchNextRequest] = None

@dataclass
class ITrainJoystickInitiate:
    pass

@dataclass
class ITrainJoystickRequest:
    initiate: Optional[ITrainJoystickInitiate] = None

@dataclass
class ITrainCardInitiate:
    pass

@dataclass
class ITrainCardVerification:
    self_created: bool

@dataclass
class ITrainCardRequest:
    initiate: Optional[ITrainCardInitiate] = None
    wallet_verify: Optional[ITrainCardVerification] = None

@dataclass
class IVersion:
    major: int
    minor: int
    patch: int

@dataclass
class IFirmwareUpdateInitiateRequest:
    version: Optional[IVersion] = None

@dataclass
class IFirmwareUpdateRequest:
    initiate: Optional[IFirmwareUpdateInitiateRequest] = None

@dataclass
class ISelectWalletIntiateRequest:
    pass

@dataclass
class ISelectWalletRequest:
    initiate: Optional[ISelectWalletIntiateRequest] = None

@dataclass
class IQuery:
    get_device_info: Optional[IGetDeviceInfoRequest] = None
    get_wallets: Optional[IGetWalletsRequest] = None
    auth_device: Optional[IAuthDeviceRequest] = None
    auth_card: Optional[IAuthCardRequest] = None
    get_logs: Optional[IGetLogsRequest] = None
    train_joystick: Optional[ITrainJoystickRequest] = None
    train_card: Optional[ITrainCardRequest] = None
    firmware_update: Optional[IFirmwareUpdateRequest] = None
    select_wallet: Optional[ISelectWalletRequest] = None

@dataclass
class ISupportedAppletItem:
    id: int
    version: Optional[IVersion] = None

@dataclass
class IGetDeviceInfoResultResponse:
    device_serial: bytes
    is_authenticated: bool
    applet_list: List[ISupportedAppletItem]
    is_initial: bool
    onboarding_step: OnboardingStep
    firmware_version: Optional[IVersion] = None

@dataclass
class IGetDeviceInfoResponse:
    result: Optional[IGetDeviceInfoResultResponse] = None
    common_error: Optional[ICommonError] = None

@dataclass
class IWalletItem:
    id: bytes
    name: str
    has_pin: bool
    has_passphrase: bool
    """
    This field determines whether the particular wallet is in usable state
    It does not indicate why the wallet is not usable.
    """
    is_valid: bool

@dataclass
class IGetWalletsResultResponse:
    wallet_list: List[IWalletItem]

@dataclass
class IGetWalletsResponse:
    result: Optional[IGetWalletsResultResponse] = None
    common_error: Optional[ICommonError] = None

@dataclass
class IGetLogsDataResponse:
    data: bytes
    has_more: bool

@dataclass
class IGetLogsErrorResponse:
    logs_disabled: bool

@dataclass
class IGetLogsResponse:
    logs: Optional[IGetLogsDataResponse] = None
    common_error: Optional[ICommonError] = None
    error: Optional[IGetLogsErrorResponse] = None

@dataclass
class ITrainJoystickResult:
    pass

@dataclass
class ITrainJoystickResponse:
    result: Optional[ITrainJoystickResult] = None
    common_error: Optional[ICommonError] = None

@dataclass
class IExistingWalletItem:
    id: bytes
    name: str

@dataclass
class ITrainCardResult:
    wallet_list: List[IExistingWalletItem]
    card_paired: bool

@dataclass
class ITrainCardComplete:
    pass

@dataclass
class ITrainCardResponse:
    result: Optional[ITrainCardResult] = None
    flow_complete: Optional[ITrainCardComplete] = None
    common_error: Optional[ICommonError] = None

@dataclass
class IFirmwareUpdateConfirmedResponse:
    pass

@dataclass
class IFirmwareUpdateErrorResponse:
    error: FirmwareUpdateError

@dataclass
class IFirmwareUpdateResponse:
    confirmed: Optional[IFirmwareUpdateConfirmedResponse] = None
    common_error: Optional[ICommonError] = None
    error: Optional[IFirmwareUpdateErrorResponse] = None

@dataclass
class ISelectWalletResultResponse:
    wallet: Optional[IWalletItem] = None

@dataclass
class ISelectWalletResponse:
    result: Optional[ISelectWalletResultResponse] = None
    common_error: Optional[ICommonError] = None

@dataclass
class IResult:
    get_device_info: Optional[IGetDeviceInfoResponse] = None
    get_wallets: Optional[IGetWalletsResponse] = None
    auth_device: Optional[IAuthDeviceResponse] = None
    auth_card: Optional[IAuthCardResponse] = None
    get_logs: Optional[IGetLogsResponse] = None
    train_joystick: Optional[ITrainJoystickResponse] = None
    train_card: Optional[ITrainCardResponse] = None
    common_error: Optional[ICommonError] = None
    firmware_update: Optional[IFirmwareUpdateResponse] = None
    select_wallet: Optional[ISelectWalletResponse] = None


