from typing import Callable, Dict
from packages.interfaces.logger import LogCreator
from packages.util.utils.logger import create_default_console_logger, update_logger_object

logger_service_name = 'sdk-core'

logger: Dict[str, Callable] = {
    **create_default_console_logger(logger_service_name)
}

def update_logger(create_logger: LogCreator) -> None:
    update_logger_object({
        "currentLogger": logger,
        "newLogger": create_logger(logger_service_name)
    })

