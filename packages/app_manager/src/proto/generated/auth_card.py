# Generated from auth_card.proto
from dataclasses import dataclass
from typing import Optional, Union
from enum import IntEnum

class AuthCardStatus(IntEnum):
    AUTH_CARD_STATUS_INIT = 0
    AUTH_CARD_STATUS_USER_CONFIRMED = 1
    AUTH_CARD_STATUS_SERIAL_SIGNED = 2
    AUTH_CARD_STATUS_CHALLENGE_SIGNED = 3
    AUTH_CARD_STATUS_PAIRING_DONE = 4

@dataclass
class AuthCardInitiateRequest:
    card_index: Optional[int] = None
    is_pair_required: Optional[bool] = None

@dataclass
class AuthCardChallengeRequest:
    challenge: bytes = b''

@dataclass
class AuthCardResult:
    verified: bool = False

@dataclass
class AuthCardSerialSigResponse:
    serial: bytes = b''
    signature: bytes = b''

@dataclass
class AuthCardChallengeSigResponse:
    signature: bytes = b''

@dataclass
class AuthCardFlowCompleteResponse:
    pass

@dataclass 
class AuthCardRequest:
    request: Union[AuthCardInitiateRequest, AuthCardChallengeRequest, AuthCardResult, None] = None

@dataclass
class AuthCardResponse:
    response: Union[AuthCardSerialSigResponse, AuthCardChallengeSigResponse, None, AuthCardFlowCompleteResponse, None] = None
