from typing import List, Dict, Any
from ..utils.bitcoinlib import get_bitcoin_py_lib
from ..utils.network import get_network_from_path, get_purpose_type
from util.utils.assert_utils import assert_condition
from bitcoinlib.encoding import convert_der_sig
from bitcoinlib.keys import Address
from util.utils.crypto import hex_to_uint8array
from bitcoinutils.setup import setup
from bitcoinutils.transactions import Transaction as UtilTransaction, TxInput, TxOutput, TxWitnessInput
from bitcoinutils.script import Script

def address_to_script_pub_key(address: str, derivation_path: List[int]) -> str:
    network = get_network_from_path(derivation_path)
    network_name = "bitcoin" if network.pub_key_hash == 0 else "testnet"

    addr_obj = Address.parse(address, network=network_name)

    if addr_obj.script_type == "p2wpkh":
        script_pubkey = f"0014{addr_obj.hash_bytes.hex()}"
    elif addr_obj.script_type == "p2sh-p2wpkh":
        script_pubkey = f"a914{addr_obj.hash_bytes.hex()}87"
    elif addr_obj.script_type == "p2pkh":
        script_pubkey = f"76a914{addr_obj.hash_bytes.hex()}88ac"
    elif addr_obj.script_type == "p2sh":
        script_pubkey = f"a914{addr_obj.hash_bytes.hex()}87"
    elif addr_obj.script_type == "p2tr":
        script_pubkey = f"5120{addr_obj.hash_bytes.hex()}"
    else:
        raise ValueError(f"Unsupported address type: {addr_obj.script_type}")

    return script_pubkey

def is_script_segwit(script: str) -> bool:
    return script.startswith("0014")

def is_script_nested_segwit(script: str) -> bool:
    return script.startswith("a914") and script.endswith("87") and len(script) == 46


def create_taproot_transaction(params: Dict[str, Any]) -> str:
    inputs = params["inputs"]
    outputs = params["outputs"]
    signatures = params["signatures"]
    derivation_path = params["derivation_path"]
    
    network = get_network_from_path(derivation_path)
    network_name = "mainnet" if network.pub_key_hash == 0 else "testnet"
    setup(network_name)

    txn_inputs = []
    for input_data in inputs:
        txn_inputs.append(TxInput(
            input_data.prev_txn_id,
            input_data.prev_index,
            sequence=str(input_data.sequence or "ffffffff")
        ))

    txn_outputs = []
    for output_data in outputs:
        txn_outputs.append(TxOutput(
            int(output_data.value),
            Script.from_raw(address_to_script_pub_key(output_data.address, derivation_path))
        ))

    txn = UtilTransaction(txn_inputs, txn_outputs, has_segwit=True)

    for signature in signatures:
        txn.witnesses.append(TxWitnessInput([signature[:128]]))

    return txn.serialize()


def create_signed_transaction(params: Dict[str, Any]) -> str:
    inputs = params["inputs"]
    outputs = params["outputs"]
    signatures = params["signatures"]
    derivation_path = params["derivation_path"]

    purpose_type = get_purpose_type(derivation_path)
    if purpose_type == "taproot":
        return create_taproot_transaction(params)

    network = get_network_from_path(derivation_path)
    network_name = "bitcoin" if network.pub_key_hash == 0 else "testnet"

    from bitcoinlib.transactions import Transaction, Input, Output, Key

    transaction = Transaction(network=network_name, version=2)

    for i, input_data in enumerate(inputs):
        if hasattr(input_data, "address"):
            address = input_data.address
            prev_txn_id = input_data.prev_txn_id
            prev_index = input_data.prev_index
            value = input_data.value
        else:
            address = input_data["address"]
            prev_txn_id = input_data["prevTxnId"]
            prev_index = input_data["prevIndex"]
            value = input_data["value"]

        script = address_to_script_pub_key(address, derivation_path)
        is_segwit = is_script_segwit(script)

        try:
            signature = signatures[i]

            pubkey = signature[-66:]
            k = Key(pubkey, compressed=True)

            der_length = int(signature[4:6], 16) * 2
            der_encoded = signature[2 : der_length + 6]
            der_bytes = bytes.fromhex(der_encoded)
            signature_hex = convert_der_sig(der_bytes, as_hex=True)
            signature_bytes = bytes.fromhex(signature_hex)
        except (ValueError, IndexError) as e:
            k = None
            signature_bytes = None


        # txn_input = {
        #     "prev_txid": prev_txn_id,
        #     "output_n": prev_index,
        #     "value": int(value),
        #     "address": address,
        # }

        # if is_segwit:
        #     txn_input["unlocking_script"] = ""
        #     txn_input["witness_type"] = "segwit"
        #     txn_input["script_type"] = "p2wpkh"
        # else:
            # if hasattr(input_data, "prev_txn"):
            #     prev_txn = input_data.prev_txn
            # else:
            #     prev_txn = input_data.get("prevTxn")
            # assert_condition(prev_txn, "prevTxn is required in input")
            # txn_input["unlocking_script"] = prev_txn
            # txn_input["script_type"] = "p2pkh"

        transaction.add_input(
            prev_txid=prev_txn_id,
            output_n=prev_index,
            value=int(value),
            address=address,
            keys=k.public_hex if k else None,
            signatures=signature_bytes if signature_bytes else None,
            witness_type="p2sh-segwit" if is_script_nested_segwit(script) else None
        )

    for output in outputs:
        if hasattr(output, "address"):
            address = output.address
            value = output.value
        else:
            address = output["address"]
            value = output["value"]

        transaction.add_output(address=address, value=int(value))

    # for i, signature in enumerate(signatures):
        # if not signature or signature == "":
        #     continue
        # if len(signature) < 6:
        #     continue

        # try:
        #     der_length = int(signature[4:6], 16) * 2
        #     der_encoded = signature[2 : der_length + 6]
        #     _ = bytes.fromhex(signature[-66:])
        #     der_bytes = bytes.fromhex(der_encoded)
        #     signature_hex = convert_der_sig(der_bytes, as_hex=True)
        # except (ValueError, IndexError) as e:
        #     continue

        # signature_bytes = bytes.fromhex(signature_hex)
        # _ = signature_bytes[:32]
        # _ = signature_bytes[32:64]
        # transaction.sign(signature_hex, i)
    return transaction.raw_hex()
