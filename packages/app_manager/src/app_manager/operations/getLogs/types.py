from typing import Callable
from app_manager.proto.generated.manager.get_logs_pb2 import GetLogsStatus
from .error import GetLogsError, GetLogsErrorType

# Re-export error types
__all__ = ["GetLogsError", "GetLogsErrorType", "GetLogsEventHandler"]

GetLogsEventHandler = Callable[[GetLogsStatus], None]
