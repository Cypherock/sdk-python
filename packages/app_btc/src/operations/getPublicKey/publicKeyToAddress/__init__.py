from typing import List, Dict, Callable
from enum import Enum
from coincurve import PublicKey
from bitcoinlib.keys import HDKey

class PurposeType(Enum):
    SEGWIT = "segwit"
    LEGACY = "legacy"

def get_purpose_type(path: List[int]) -> PurposeType:
    if len(path) > 0:
        purpose = path[0]
        if purpose == 84:
            return PurposeType.SEGWIT
        elif purpose == 44:
            return PurposeType.LEGACY
    return PurposeType.LEGACY

def get_network_from_path(path: List[int]) -> str:
    if len(path) > 1:
        coin_type = path[1]
        if coin_type == 0:
            return "bitcoin"
        elif coin_type == 1:
            return "testnet"
    return "bitcoin"

def get_payments_function(path: List[int]) -> Callable:
    def p2wpkh_payment(pubkey: bytes, network: str) -> Dict[str, str]:
        hd_key = HDKey(pubkey, network=network)
        address = hd_key.address(encoding='bech32')
        return {"address": address}

    def p2pkh_payment(pubkey: bytes, network: str) -> Dict[str, str]:
        hd_key = HDKey(pubkey, network=network)
        address = hd_key.address(encoding='base58')
        return {"address": address}

    payment_function_map: Dict[PurposeType, Callable] = {
        PurposeType.SEGWIT: p2wpkh_payment,
        PurposeType.LEGACY: p2pkh_payment,
    }

    purpose = get_purpose_type(path)
    return payment_function_map[purpose]

def get_address_from_public_key(uncompressed_public_key: bytes, path: List[int]) -> str:
    """
    1. Compress the uncompressed public key using secp256k1
    2. Get the appropriate payment function based on the path
    3. Generate the address using the payment function
    4. Assert that the address was generated successfully

    Args:
        uncompressed_public_key: Uncompressed public key as bytes (65 bytes)
        path: BIP32 derivation path as list of integers

    Returns:
        Bitcoin address as string

    Raises:
        AssertionError: If address could not be derived
    """
    compressed_public_key = PublicKey(uncompressed_public_key).format(compressed=True)
    payments_function = get_payments_function(path)
    network = get_network_from_path(path)
    result = payments_function(compressed_public_key, network)
    address = result["address"]

    assert address, "Could not derive address"
    return address