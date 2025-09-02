from typing import List, Dict, Any
from packages.app_btc.src.utils.bitcoinlib import get_bitcoin_py_lib

def address_to_script_pub_key(address: str, derivation_path: List[int]) -> str:
    bitcoin_py_lib = get_bitcoin_py_lib()
    network = 'bitcoin' if derivation_path[1] == 0 else 'testnet'

    from bitcoinlib.scripts import Script
    script = Script.parse_address(address)
    return script.raw.hex()


def is_script_segwit(script: str) -> bool:
    return script.startswith('0014')

def create_signed_transaction(params: Dict[str, Any]) -> str:
    inputs = params['inputs']
    outputs = params['outputs']
    signatures = params['signatures']
    derivation_path = params['derivation_path']

    bitcoin_py_lib = get_bitcoin_py_lib()
    network = 'bitcoin' if derivation_path[1] == 0 else 'testnet'

    from bitcoinlib.transactions import Transaction

    transaction = Transaction(network=network)

    for input_data in inputs:
        script = address_to_script_pub_key(input_data['address'], derivation_path)
        is_segwit = is_script_segwit(script)

        txn_input = {
            'prev_txid': input_data['prevTxnId'],
            'output_n': input_data['prevIndex'],
            'value': int(input_data['value'])
        }

        if is_segwit:
            txn_input['witness'] = True
        else:
            assert input_data.get('prevTxn'), 'prevTxn is required in input'
            txn_input['unlocking_script'] = input_data['prevTxn']

        transaction.add_input(**txn_input)

    for output in outputs:
        transaction.add_output(
            address=output['address'],
            value=int(output['value'])
        )

    for i, signature in enumerate(signatures):
        der_length = int(signature[4:6], 16) * 2
        der_encoded = signature[2:der_length + 6]
        public_key = bytes.fromhex(signature[-66:])

        der_bytes = bytes.fromhex(der_encoded)

        r_length = der_bytes[3]
        r = der_bytes[4:4 + r_length]
        s_start = 4 + r_length + 2
        s_length = der_bytes[s_start - 1]
        s = der_bytes[s_start:s_start + s_length]

        r_value = r[-32:] if len(r) > 32 else b'\x00' * (32 - len(r)) + r
        s_value = s[-32:] if len(s) > 32 else b'\x00' * (32 - len(s)) + s

        signature_bytes = r_value + s_value

        transaction.sign(signature_bytes, i, public_key)

    return transaction.raw_hex()