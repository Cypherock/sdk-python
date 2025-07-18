from dataclasses import dataclass
from typing import List, Optional
import betterproto


class SeedGenerationStatus(betterproto.Enum):
    SEED_GENERATION_STATUS_INIT = 0
    SEED_GENERATION_STATUS_PASSPHRASE = 1
    SEED_GENERATION_STATUS_PIN_CARD = 2
    UNRECOGNIZED = -1


class DeviceWaitingOn(betterproto.Enum):
    DEVICE_WAITING_ON_NULL = 0
    DEVICE_WAITING_ON_IDLE = 1
    DEVICE_WAITING_ON_BUSY_IP_CARD = 2
    DEVICE_WAITING_ON_BUSY_IP_KEY = 3
    UNRECOGNIZED = -1


class DeviceIdleState(betterproto.Enum):
    DEVICE_IDLE_STATE_NULL = 0
    DEVICE_IDLE_STATE_IDLE = 1
    DEVICE_IDLE_STATE_USB = 2
    DEVICE_IDLE_STATE_DEVICE = 3
    UNRECOGNIZED = -1


class CmdState(betterproto.Enum):
    CMD_STATE_NONE = 0
    CMD_STATE_RECEIVING = 1
    CMD_STATE_RECEIVED = 2
    CMD_STATE_EXECUTING = 3
    CMD_STATE_DONE = 4
    CMD_STATE_FAILED = 5
    CMD_STATE_INVALID_CMD = 6
    UNRECOGNIZED = -1


class ErrorType(betterproto.Enum):
    NO_ERROR = 0
    UNKNOWN_APP = 1
    INVALID_MSG = 2
    APP_NOT_ACTIVE = 3
    APP_TIMEOUT_OCCURRED = 4
    DEVICE_SESSION_INVALID = 5
    UNRECOGNIZED = -1


class WalletNotFound(betterproto.Enum):
    WALLET_NOT_FOUND_UNKNOWN = 0
    WALLET_NOT_FOUND_ON_DEVICE = 1
    WALLET_NOT_FOUND_ON_CARD = 2
    UNRECOGNIZED = -1


class WalletPartialState(betterproto.Enum):
    WALLET_PARTIAL_STATE_UNKNOWN = 0
    WALLET_PARTIAL_STATE_LOCKED = 1
    WALLET_PARTIAL_STATE_DELETE = 2
    WALLET_PARTIAL_STATE_UNVERIFIED = 3
    WALLET_PARTIAL_STATE_OUT_OF_SYNC = 4
    UNRECOGNIZED = -1


class CardError(betterproto.Enum):
    CARD_ERROR_UNKNOWN = 0
    CARD_ERROR_NOT_PAIRED = 1
    CARD_ERROR_SW_INCOMPATIBLE_APPLET = 3
    CARD_ERROR_SW_NULL_POINTER_EXCEPTION = 4
    CARD_ERROR_SW_TRANSACTION_EXCEPTION = 5
    CARD_ERROR_SW_FILE_INVALID = 6
    CARD_ERROR_SW_SECURITY_CONDITIONS_NOT_SATISFIED = 7
    CARD_ERROR_SW_CONDITIONS_NOT_SATISFIED = 8
    CARD_ERROR_SW_WRONG_DATA = 9
    CARD_ERROR_SW_FILE_NOT_FOUND = 10
    CARD_ERROR_SW_RECORD_NOT_FOUND = 11
    CARD_ERROR_SW_FILE_FULL = 12
    CARD_ERROR_SW_CORRECT_LENGTH_00 = 13
    CARD_ERROR_SW_INVALID_INS = 14
    CARD_ERROR_SW_NOT_PAIRED = 15
    CARD_ERROR_SW_CRYPTO_EXCEPTION = 16
    CARD_ERROR_POW_SW_WALLET_LOCKED = 17
    CARD_ERROR_SW_INS_BLOCKED = 18
    CARD_ERROR_SW_OUT_OF_BOUNDARY = 19
    UNRECOGNIZED = -1



class UserRejection(betterproto.Enum):
    USER_REJECTION_UNKNOWN = 0
    USER_REJECTION_CONFIRMATION = 1
    UNRECOGNIZED = -1


class DataFlow(betterproto.Enum):
    DATA_FLOW_DECODING_FAILED = 0
    DATA_FLOW_INVALID_QUERY = 1
    DATA_FLOW_FIELD_MISSING = 2
    DATA_FLOW_INVALID_REQUEST = 3
    DATA_FLOW_INACTIVITY_TIMEOUT = 4
    DATA_FLOW_INVALID_DATA = 5
    DATA_FLOW_QUERY_NOT_ALLOWED = 6
    UNRECOGNIZED = -1


@dataclass
class ICommand:
    applet_id: int


@dataclass
class IErrorCmd:
    applet_id: int
    type: ErrorType


@dataclass
class IAppVersionIntiateRequest:
    pass


@dataclass
class IAppVersionRequest:
    initiate: Optional[IAppVersionIntiateRequest] = None


@dataclass
class IVersion:
    major: int
    minor: int
    patch: int


@dataclass
class IAppVersionItem:
    id: int
    version: Optional[IVersion] = None


@dataclass
class IAppVersionResultResponse:
    app_versions: List[IAppVersionItem]


@dataclass
class ICommonError:
    unknown_error: Optional[int] = None
    corrupt_data: Optional[DataFlow] = None
    device_setup_required: Optional[int] = None
    wallet_not_found: Optional[WalletNotFound] = None
    wallet_partial_state: Optional[WalletPartialState] = None
    card_error: Optional[CardError] = None
    user_rejection: Optional[UserRejection] = None


@dataclass
class IAppVersionResponse:
    result: Optional[IAppVersionResultResponse] = None
    common_error: Optional[ICommonError] = None


@dataclass
class IAppVersionCmd:
    request: Optional[IAppVersionRequest] = None
    response: Optional[IAppVersionResponse] = None


@dataclass
class ISessionStartInitiateRequest:
    pass


@dataclass
class ISessionStartBeginRequest:
    session_random_public: bytes
    session_age: int
    signature: bytes
    device_id: bytes


@dataclass
class ISessionStartRequest:
    initiate: Optional[ISessionStartInitiateRequest] = None
    start: Optional[ISessionStartBeginRequest] = None


@dataclass
class ISessionStartInitiateResultResponse:
    device_random_public: bytes
    device_id: bytes
    signature: bytes
    postfix1: bytes
    postfix2: bytes
    key_index: int


@dataclass
class ISessionStartAckResponse:
    pass


@dataclass
class ISessionStartResponse:
    confirmation_initiate: Optional[ISessionStartInitiateResultResponse] = None
    confirmation_start: Optional[ISessionStartAckResponse] = None
    common_error: Optional[ICommonError] = None


@dataclass
class ISessionStartCmd:
    request: Optional[ISessionStartRequest] = None
    response: Optional[ISessionStartResponse] = None


@dataclass
class ISessionCloseClearRequest:
    pass


@dataclass
class ISessionCloseRequest:
    clear: Optional[ISessionCloseClearRequest] = None


@dataclass
class ISessionCloseClearResponse:
    pass


@dataclass
class ISessionCloseResponse:
    clear: Optional[ISessionCloseClearResponse] = None
    common_error: Optional[ICommonError] = None


@dataclass
class ISessionCloseCmd:
    request: Optional[ISessionCloseRequest] = None
    response: Optional[ISessionCloseResponse] = None


@dataclass
class IMsg:
    cmd: Optional[ICommand] = None
    error: Optional[IErrorCmd] = None
    app_version: Optional[IAppVersionCmd] = None
    session_start: Optional[ISessionStartCmd] = None
    session_close: Optional[ISessionCloseCmd] = None




