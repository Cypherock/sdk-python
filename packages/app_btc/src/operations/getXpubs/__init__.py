from typing import List
from packages.core.src.types import ISDK
from packages.util.utils import create_status_listener, create_logger_with_prefix
from packages.util.utils.assert_utils import assert_condition
from packages.app_btc.src.proto.generated.btc import GetXpubsStatus, GetXpubsResultResponse
from packages.app_btc.src.proto.generated.common import SeedGenerationStatus
from packages.app_btc.src.utils import (
    assert_or_throw_invalid_result,
    OperationHelper,
    logger as root_logger,
    configure_app_id,
    assert_derivation_path,
)
from .types import GetXpubsEvent, GetXpubsParams

# Re-export types
__all__ = ['get_xpubs', 'GetXpubsEvent', 'GetXpubsParams']

logger = create_logger_with_prefix(root_logger, 'GetXpubs')


async def get_xpubs(
    sdk: ISDK,
    params: GetXpubsParams,
) -> GetXpubsResultResponse:
    """
    Get extended public keys from device.
    Direct port of TypeScript getXpubs function.
    
    Args:
        sdk: SDK instance
        params: Parameters including wallet_id, derivation_paths, and optional on_event handler
        
    Returns:
        Result containing list of xpubs
        
    Raises:
        AssertionError: If parameters are invalid
    """
    assert_condition(params, 'Params should be defined')
    assert_condition(params.derivation_paths, 'DerivationPaths should be defined')
    assert_condition(params.wallet_id, 'WalletId should be defined')
    assert_condition(
        len(params.derivation_paths) > 0,
        'DerivationPaths should not be empty',
    )
    assert_condition(
        all(len(path.path) == 3 for path in params.derivation_paths),
        'DerivationPaths should be of depth 3',
    )
    
    # Validate each derivation path
    for item in params.derivation_paths:
        assert_derivation_path(item.path)

    await configure_app_id(
        sdk,
        [path.path for path in params.derivation_paths],
    )

    on_status, force_status_update = create_status_listener({
        'enums': GetXpubsEvent,
        'operationEnums': GetXpubsStatus,
        'seedGenerationEnums': SeedGenerationStatus,
        'onEvent': params.on_event,
        'logger': logger,
    })

    helper = OperationHelper(
        sdk=sdk,
        query_key='getXpubs',
        result_key='getXpubs',
        on_status=on_status,
    )

    await helper.send_query({
        'initiate': {
            'wallet_id': params.wallet_id,
            'derivation_paths': params.derivation_paths,
        }
    })

    xpubs: List[str] = []
    
    def has_more() -> bool:
        return len(xpubs) != len(params.derivation_paths)

    while has_more():
        result = await helper.wait_for_result()
        assert_or_throw_invalid_result(result.result)
        xpubs.extend(result.result.xpubs)
        force_status_update(GetXpubsEvent.PIN_CARD)
        
        if has_more():
            await helper.send_query({
                'fetch_next': {}
            })

    return GetXpubsResultResponse(xpubs=xpubs)



