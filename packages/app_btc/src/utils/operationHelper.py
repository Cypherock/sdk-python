from typing import List, Dict, Any, TypeVar, Generic, Optional
from packages.core.src.sdk import ISDK
from packages.interfaces.errors.app_error import DeviceAppError, DeviceAppErrorType
from packages.util.utils.create_status_listener import OnStatus
from packages.app_btc.src.proto.generated.btc import Query, Result
from packages.app_btc.src.proto.generated.common import ChunkPayload
from packages.app_btc.src.utils.assert_utils import assert_or_throw_invalid_result, parse_common_error

Q = TypeVar('Q')
R = TypeVar('R')


def decode_result(data: bytes) -> Result:
    """
    Decode result from device response.
    
    Args:
        data: Raw bytes from device
        
    Returns:
        Decoded result
        
    Raises:
        DeviceAppError: If decoding fails
    """
    try:
        return Result.FromString(data)
    except Exception:
        raise DeviceAppError(DeviceAppErrorType.INVALID_MSG_FROM_DEVICE)


def encode_query(query: Dict[str, Any]) -> bytes:
    """
    Encode query to send to device.
    
    Args:
        query: Query dictionary
        
    Returns:
        Encoded query bytes
    """
    query_obj = Query(**query)
    return query_obj.SerializeToString()


class OperationHelper(Generic[Q, R]):
    """
    Helper class for device operations with query/result pattern.
    """
    
    CHUNK_SIZE = 2048
    
    def __init__(self, sdk: ISDK, query_key: str, result_key: str, on_status: Optional[OnStatus] = None):
        """
        Initialize operation helper.
        
        Args:
            sdk: SDK instance
            query_key: Key for query type
            result_key: Key for result type
            on_status: Optional status callback
        """
        self.sdk = sdk
        self.query_key = query_key
        self.result_key = result_key
        self.on_status = on_status
    
    async def send_query(self, query: Dict[str, Any]) -> None:
        """
        Send query to device.
        
        Args:
            query: Query data
        """
        query_data = {self.query_key: query}
        encoded_query = encode_query(query_data)
        await self.sdk.send_query(encoded_query)
    
    async def wait_for_result(self) -> Any:
        """
        Wait for and decode result from device.
        
        Returns:
            Decoded result data
            
        Raises:
            DeviceAppError: If result is invalid or contains errors
        """
        result_data = await self.sdk.wait_for_result(on_status=self.on_status)
        result = decode_result(result_data)
        
        result_value = getattr(result, self.result_key, None)
        parse_common_error(getattr(result, 'common_error', None))
        assert_or_throw_invalid_result(result_value)
        parse_common_error(getattr(result_value, 'common_error', None))
        
        return result_value
    
    @staticmethod
    def split_into_chunks(data: bytes) -> List[bytes]:
        """
        Split data into chunks for transmission.
        
        Args:
            data: Data to split
            
        Returns:
            List of data chunks
        """
        chunks = []
        total_chunks = (len(data) + OperationHelper.CHUNK_SIZE - 1) // OperationHelper.CHUNK_SIZE
        
        for i in range(total_chunks):
            start = i * OperationHelper.CHUNK_SIZE
            end = min(start + OperationHelper.CHUNK_SIZE, len(data))
            chunk = data[start:end]
            chunks.append(chunk)
        
        return chunks
    
    async def send_in_chunks(self, data: bytes, query_key: str, result_key: str) -> None:
        """
        Send data in chunks to device.
        
        Args:
            data: Data to send
            query_key: Query key for chunk sending
            result_key: Result key for chunk acknowledgment
        """
        chunks = self.split_into_chunks(data)
        remaining_size = len(data)
        
        for i, chunk in enumerate(chunks):
            remaining_size -= len(chunk)
            
            chunk_payload = ChunkPayload(
                chunk=chunk,
                chunk_index=i,
                total_chunks=len(chunks),
                remaining_size=remaining_size,
            )
            
            await self.send_query({
                query_key: {
                    'chunk_payload': chunk_payload,
                },
            })
            
            result = await self.wait_for_result()
            result_data = getattr(result, result_key, None)
            assert_or_throw_invalid_result(result_data)
            
            chunk_ack = getattr(result_data, 'chunk_ack', None)
            assert_or_throw_invalid_result(chunk_ack)
            assert_or_throw_invalid_result(chunk_ack.chunk_index == i)






