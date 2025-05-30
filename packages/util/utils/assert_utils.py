from typing import TypeVar, Union, Optional
T = TypeVar('T')
def assert_condition(condition: Optional[T], error: Union[str, Exception]) -> None:
    if condition is None or condition is False:
        if isinstance(error, str):
            raise AssertionError(f"AssertionError: {error}")
        else:
            raise error
