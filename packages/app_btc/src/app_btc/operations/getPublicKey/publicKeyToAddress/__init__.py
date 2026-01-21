from typing import List
from ....utils import get_network_from_path, get_purpose_type
from bitcoinutils.keys import PublicKey as BitcoinPublicKey, P2shAddress
from bitcoinutils.setup import setup

def get_address_from_public_key(uncompressed_public_key: bytes, path: List[int]) -> str:
    """
    1. Get the purpose type from the derivation path
    2. Create the bitcoin public key object from the uncompressed public key
    3. Get the address from the public key based on the purpose type
    4. Assert that the address was generated successfully

    Args:
        uncompressed_public_key: Uncompressed public key as bytes (65 bytes)
        path: BIP32 derivation path as list of integers

    Returns:
        Bitcoin address as string

    Raises:
        AssertionError: If address could not be derived
    """

    network_config = get_network_from_path(path)
    network = "mainnet" if network_config.pub_key_hash == 0 else "testnet"
    setup(network)

    purpose_type = get_purpose_type(path)
    pubkey = BitcoinPublicKey(uncompressed_public_key.hex())

    if purpose_type == "legacy":
        address = pubkey.get_address()
    elif purpose_type == "segwit":
        address = pubkey.get_segwit_address()
    elif purpose_type == "nested_segwit":
        address = P2shAddress.from_script(pubkey.get_segwit_address().to_script_pub_key())
    elif purpose_type == "taproot":
        address = pubkey.get_taproot_address()
    else:
        raise ValueError(f"Unsupported purpose type: {purpose_type}")

    assert address, "Could not derive address"
    return address.to_string()
