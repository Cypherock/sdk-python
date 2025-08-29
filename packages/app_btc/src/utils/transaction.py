from typing import List, Dict, Any
from bitcointx.core import CTransaction, CTxOut, COutPoint
from bitcointx.core.psbt import PartiallySignedTransaction as PSBT
from bitcointx.core.script import CScript
from bitcointx.wallet import CBitcoinAddress, P2PKHCoinAddress
from cryptography.hazmat.primitives.asymmetric.utils import decode_dss_signature
from packages.util.utils.assert_utils import assert_condition
from packages.app_btc.src.utils.network import get_network_from_path

def address_to_script_pub_key(address: str, derivation_path: List[int]) -> str:
    """
    Convert address to script public key.
    Automatically detects P2PKH / P2SH / P2WPKH formats.
    """
    get_network_from_path(derivation_path)
    addr = CBitcoinAddress(address)
    return addr.to_scriptPubKey().hex()


def is_script_segwit(script: str) -> bool:
    """
    Check if script is a segwit script (starts with OP_0 + 20-byte hash).
    """
    return script.startswith("0014")


class CustomSigner:
    def __init__(self, public_key: bytes, signature_data: str):
        self.public_key = public_key
        self.signature_data = signature_data
        self._decoded_signature = None

    def _decode_signature(self) -> tuple:
        """
        Decode DER-encoded ECDSA signature into (r, s).
        Equivalent to bip66.decode.
        """
        if self._decoded_signature is None:
            der_length = int(self.signature_data[4:6], 16) * 2
            der_encoded = self.signature_data[2:der_length + 6]

            r, s = decode_dss_signature(bytes.fromhex(der_encoded))
            self._decoded_signature = (r, s)

        return self._decoded_signature

    def sign(self, _hash_to_sign: bytes) -> bytes:
        """
        Return pre-computed r||s signature (64 bytes).
        """
        r, s = self._decode_signature()

        r_bytes = r.to_bytes(32, "big")
        s_bytes = s.to_bytes(32, "big")

        return r_bytes + s_bytes


def create_signed_transaction(
    inputs: List[Dict[str, Any]],
    outputs: List[Dict[str, Any]],
    signatures: List[str],
    derivation_path: List[int]
) -> str:
    network = get_network_from_path(derivation_path)

    psbt = PSBT()

    # Add inputs
    for i, input_data in enumerate(inputs):
        script = address_to_script_pub_key(input_data["address"], derivation_path)
        is_segwit = is_script_segwit(script)

        outpoint = COutPoint(
            hash=bytes.fromhex(input_data["prev_txn_id"]),
            n=input_data["prev_index"]
        )

        if is_segwit:
            witness_utxo = CTxOut(
                nValue=int(input_data["value"]),
                scriptPubKey=CScript(bytes.fromhex(script))
            )
            psbt.add_input(outpoint, witness_utxo=witness_utxo)
        else:
            assert_condition(input_data.get("prev_txn"), "prevTxn is required in input")
            non_witness_utxo = CTransaction.deserialize(bytes.fromhex(input_data["prev_txn"]))
            psbt.add_input(outpoint, non_witness_utxo=non_witness_utxo)

    # Add outputs
    for output in outputs:
        output_txout = CTxOut(
            nValue=int(output["value"]),
            scriptPubKey=P2PKHCoinAddress.from_string(
                output["address"], network=network
            ).to_scriptPubKey()
        )
        psbt.add_output(output_txout)

    # Sign inputs with custom pre-computed signatures
    for i, signature in enumerate(signatures):
        public_key = bytes.fromhex(signature[-66:])
        signer = CustomSigner(public_key, signature)
        psbt.sign_with(signer, input_index=i)

    # Finalize and extract
    psbt.finalize()
    return psbt.tx.serialize().hex()
