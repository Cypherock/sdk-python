# Generated manually due to optional fields
from dataclasses import dataclass, field
from typing import Optional
import betterproto

@dataclass
class AuthCardStatus(betterproto.Enum):
    AUTH_CARD_STATUS_INIT = 0
    AUTH_CARD_STATUS_USER_CONFIRMED = 1
    AUTH_CARD_STATUS_SERIAL_SIGNED = 2
    AUTH_CARD_STATUS_CHALLENGE_SIGNED = 3
    AUTH_CARD_STATUS_PAIRING_DONE = 4

@dataclass
class AuthCardInitiateRequest(betterproto.Message):
    card_index: Optional[int] = field(default=None)
    is_pair_required: Optional[bool] = field(default=None)

@dataclass
class AuthCardChallengeRequest(betterproto.Message):
    challenge: bytes = field(default=b'')

@dataclass
class AuthCardResult(betterproto.Message):
    verified: bool = field(default=False)

@dataclass
class AuthCardSerialSigResponse(betterproto.Message):
    serial: bytes = field(default=b'')
    signature: bytes = field(default=b'')

@dataclass
class AuthCardChallengeSigResponse(betterproto.Message):
    signature: bytes = field(default=b'')

@dataclass
class AuthCardFlowCompleteResponse(betterproto.Message):
    pass

@dataclass
class AuthCardRequest(betterproto.Message):
    initiate: Optional[AuthCardInitiateRequest] = field(default=None)
    challenge: Optional[AuthCardChallengeRequest] = field(default=None)
    result: Optional[AuthCardResult] = field(default=None)

@dataclass
class AuthCardResponse(betterproto.Message):
    serial_signature: Optional[AuthCardSerialSigResponse] = field(default=None)
    challenge_signature: Optional[AuthCardChallengeSigResponse] = field(default=None)
    common_error: Optional['error.CommonError'] = field(default=None)
    flow_complete: Optional[AuthCardFlowCompleteResponse] = field(default=None)
