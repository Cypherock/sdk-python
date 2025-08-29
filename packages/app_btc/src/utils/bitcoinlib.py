from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import bitcointx

_bitcoin_lib: Optional['bitcointx'] = None


def get_bitcoin_lib() -> 'bitcointx':
    """
    Get the configured bitcointx instance.
    
    Returns:
        The bitcointx module
        
    Raises:
        RuntimeError: If bitcointx has not been set
    """
    if _bitcoin_lib is None:
        raise RuntimeError('bitcointx has not been set yet')
    return _bitcoin_lib


def set_bitcoin_lib(bitcoin_library: 'bitcointx') -> None:
    """
    Set the bitcointx library to use.
    
    Args:
        bitcoin_library: The bitcointx module to use
    """
    global _bitcoin_lib
    _bitcoin_lib = bitcoin_library

