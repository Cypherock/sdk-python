from typing import Any, Callable, Dict, Protocol, TypeVar, Union, runtime_checkable

LogMethod = Callable[[Any, Dict[str, Any]], None]

@runtime_checkable
class ILogger(Protocol):
    def info(self, message: Any, meta: Dict[str, Any] = None) -> None:
        ...

    def error(self, message: Any, meta: Dict[str, Any] = None) -> None:
        ...

    def warn(self, message: Any, meta: Dict[str, Any] = None) -> None:
        ...

    def debug(self, message: Any, meta: Dict[str, Any] = None) -> None:
        ...

    def verbose(self, message: Any, meta: Dict[str, Any] = None) -> None:
        ...

LogLevel = Union['info', 'error', 'warn', 'debug', 'verbose']

LogWithServiceAndMethod = Callable[[str, LogLevel, Any, Dict[str, Any]], None]

T = TypeVar('T', bound=ILogger)
LogCreator = Callable[[str], T]
