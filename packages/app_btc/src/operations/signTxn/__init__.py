import copy
from typing import List
from packages.core.src.types import ISDK
from packages.util.utils import (
    create_logger_with_prefix,
    create_status_listener,
    hex_to_uint8_array,
    uint8_array_to_hex,
)
from packages.util.utils.assert_utils import assert_condition
from packages.app_btc.src.proto.generated.btc import SignTxnStatus
from packages.app_btc.src.proto.generated.common import SeedGenerationStatus
from packages.app_btc.src.utils import (
    assert_or_throw_invalid_result,
    OperationHelper,
    logger as root_logger,
    get_coin_type_from_path,
    configure_app_id,
    AppFeatures,
    address_to_script_pub_key,
    create_signed_transaction,
)
from packages.app_btc.src.services.transaction import get_raw_txn_hash
from .helpers import assert_sign_txn_params
from .types import SignTxnParams, SignTxnResult, SignTxnEvent

# Re-export types
__all__ = ['sign_txn', 'SignTxnEvent', 'SignTxnParams', 'SignTxnResult']

logger = create_logger_with_prefix(root_logger, 'SignTxn')

# Default parameters for transaction signing
SIGN_TXN_DEFAULT_PARAMS = {
    'version': 2,
    'locktime': 0,
    'hashtype': 1,
    'input': {
        'sequence': 0xffffffff,
    },
}


async def sign_txn(
    sdk: ISDK,
    params: SignTxnParams,
) -> SignTxnResult:
    """
    Sign Bitcoin transaction on device.
    Direct port of TypeScript signTxn function.
    
    Args:
        sdk: SDK instance
        params: Parameters including wallet_id, derivation_path, txn data, and optional on_event handler
        
    Returns:
        Result containing signatures and signed_transaction
        
    Raises:
        AssertionError: If parameters are invalid
    """
    assert_sign_txn_params(params)
    logger.info('Started')

    await configure_app_id(sdk, [params.derivation_path])
    await sdk.check_feature_support_compatibility([AppFeatures.INPUT_IN_CHUNKS])

    on_status, force_status_update = create_status_listener({
        'enums': SignTxnEvent,
        'operationEnums': SignTxnStatus,
        'seedGenerationEnums': SeedGenerationStatus,
        'onEvent': params.on_event,
        'logger': logger,
    })

    helper = OperationHelper(
        sdk=sdk,
        query_key='signTxn',
        result_key='signTxn',
        on_status=on_status,
    )

    await helper.send_query({
        'initiate': {
            'wallet_id': params.wallet_id,
            'derivation_path': params.derivation_path,
        }
    })

    result = await helper.wait_for_result()
    assert_or_throw_invalid_result(result.confirmation)
    force_status_update(SignTxnEvent.CONFIRM)

    await helper.send_query({
        'meta': {
            'version': SIGN_TXN_DEFAULT_PARAMS['version'],
            'locktime': params.txn.locktime or SIGN_TXN_DEFAULT_PARAMS['locktime'],
            'input_count': len(params.txn.inputs),
            'output_count': len(params.txn.outputs),
            'sighash': params.txn.hash_type or SIGN_TXN_DEFAULT_PARAMS['hashtype'],
        }
    })
    result = await helper.wait_for_result()
    assert_or_throw_invalid_result(result.meta_accepted)

    # Duplicate locally and fill `prev_txn` if missing; we need completed inputs for preparing signed transaction
    inputs = copy.deepcopy(params.txn.inputs)
    
    for i, input_data in enumerate(params.txn.inputs):
        # Device needs transaction hash which is reversed byte order of the transaction id
        prev_txn_hash = bytes.fromhex(input_data.prev_txn_id)[::-1].hex()
        
        prev_txn = (
            input_data.prev_txn or
            await get_raw_txn_hash({
                'hash': input_data.prev_txn_id,
                'coin_type': get_coin_type_from_path(params.derivation_path),
            })
        )
        inputs[i].prev_txn = prev_txn

        await helper.send_query({
            'input': {
                'prev_txn_hash': hex_to_uint8_array(prev_txn_hash),
                'prev_output_index': input_data.prev_index,
                'script_pub_key': hex_to_uint8_array(
                    address_to_script_pub_key(input_data.address, params.derivation_path)
                ),
                'value': input_data.value,
                'sequence': input_data.sequence or SIGN_TXN_DEFAULT_PARAMS['input']['sequence'],
                'change_index': input_data.change_index,
                'address_index': input_data.address_index,
            }
        })
        result = await helper.wait_for_result()
        assert_or_throw_invalid_result(result.input_accepted)

        await helper.send_in_chunks(
            hex_to_uint8_array(prev_txn),
            'prev_txn_chunk',
            'prev_txn_chunk_accepted',
        )

    for output in params.txn.outputs:
        await helper.send_query({
            'output': {
                'script_pub_key': hex_to_uint8_array(
                    address_to_script_pub_key(output.address, params.derivation_path)
                ),
                'value': output.value,
                'is_change': output.is_change,
                'changes_index': output.address_index,
            }
        })
        result = await helper.wait_for_result()
        assert_or_throw_invalid_result(result.output_accepted)

    signatures: List[str] = []

    for i in range(len(params.txn.inputs)):
        await helper.send_query({
            'signature': {
                'index': i,
            }
        })

        result = await helper.wait_for_result()
        assert_or_throw_invalid_result(result.signature)

        signatures.append(uint8_array_to_hex(result.signature.signature))

    force_status_update(SignTxnEvent.PIN_CARD)
    signed_transaction = create_signed_transaction({
        'inputs': inputs,
        'outputs': params.txn.outputs,
        'signatures': signatures,
        'derivation_path': params.derivation_path,
    })

    logger.info('Completed')
    return SignTxnResult(
        signed_transaction=signed_transaction,
        signatures=signatures,
    )
