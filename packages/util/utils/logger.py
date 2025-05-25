from typing import Any, Dict, Optional
import datetime
from packages.interfaces.logger import ILogger
from config import config

# Log level priority mapping
log_level_priority = {
    "error": 0,
    "warn": 1,
    "info": 2,
    "verbose": 3,
    "debug": 4
}

def do_log(level: str) -> bool:
    """
    Determine if a log message should be output based on configured log level.
    """
    current_priority = log_level_priority.get(level)
    allowed_priority = log_level_priority.get(config.get("LOG_LEVEL", "info"), 2)

    if current_priority is None:
        return False

    return allowed_priority >= current_priority


def create_default_meta(service: str, meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create default metadata for log messages.
    """
    result = {
        "service": service,
        "timestamp": datetime.datetime.now()
    }

    if meta is not None:
        result.update(meta)

    return result


def create_default_console_logger(service: str) -> Dict[str, Any]:
    def info_logger(message: Any, meta: Optional[Dict[str, Any]] = None) -> None:
        if do_log("info"):
            print("INFO:", message, create_default_meta(service, meta))

    def debug_logger(message: Any, meta: Optional[Dict[str, Any]] = None) -> None:
        if do_log("debug"):
            print("DEBUG:", message, create_default_meta(service, meta))

    def verbose_logger(message: Any, meta: Optional[Dict[str, Any]] = None) -> None:
        if do_log("verbose"):
            print("VERBOSE:", message, create_default_meta(service, meta))

    def warn_logger(message: Any, meta: Optional[Dict[str, Any]] = None) -> None:
        if do_log("warn"):
            print("WARN:", message, create_default_meta(service, meta))

    def error_logger(message: Any, meta: Optional[Dict[str, Any]] = None) -> None:
        if do_log("error"):
            print("ERROR:", message, create_default_meta(service, meta))

    return {
        "info": info_logger,
        "debug": debug_logger,
        "verbose": verbose_logger,
        "warn": warn_logger,
        "error": error_logger
    }


def update_logger_object(params: Dict[str, Any]) -> None:
    """
    Update logger object with new logger methods.
    """
    new_logger = params.get("newLogger")
    current_logger = params.get("currentLogger")

    if new_logger and current_logger:
        for key in new_logger:
            if key in new_logger:
                def create_logger_wrapper(key_name):
                    def wrapper(message: Any, meta: Optional[Dict[str, Any]] = None) -> None:
                        new_message = message
                        new_meta = meta

                        # Handle JSON serialization if available
                        if message and isinstance(message, object) and hasattr(message, 'to_json'):
                            new_message = message.to_json()

                        if meta and isinstance(meta, object) and hasattr(meta, 'to_json'):
                            new_meta = meta.to_json()

                        new_logger[key_name](new_message, new_meta)

                    return wrapper

                current_logger[key] = create_logger_wrapper(key)


def create_logger_with_prefix(logger: ILogger, name: str) -> ILogger:
    new_logger = {key: value for key, value in logger.items()}

    for key in new_logger:
        def create_prefixed_logger(key_name):
            def prefixed_logger(message: Any, meta: Optional[Dict[str, Any]] = None) -> None:
                new_meta = meta or {}
                new_meta["component"] = name

                if isinstance(message, str):
                    logger[key_name](f"{name}: {message}", new_meta)
                else:
                    logger[key_name](message, new_meta)

            return prefixed_logger

        new_logger[key] = create_prefixed_logger(key)

    return new_logger
