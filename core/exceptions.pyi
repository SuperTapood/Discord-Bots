from typing import Any


class OverrideError(Exception):
    __module__: str
    method: str
    class_name: str

    def __init__(self, method: str, class_name: str) -> None:
        ...

    def __str__(self) -> str:
        ...

    pass


class BotNotNamed(Exception):
    __module__: str

    def __str__(self) -> str:
        ...

    pass


class NoTokenFound(Exception):
    __module__: str
    name: str

    def __init__(self, name: str) -> None:
        ...

    def __str__(self) -> str:
        ...

    pass


class ActivityNotFound(Exception):
    __module__: str
    activity: str

    def __init__(self, activity: str):
        ...

    def __str__(self) -> str:
        ...

    pass


class ExceptionNotFound(Exception):
    __module__: str
    exc: str

    def __init__(self, exc: str):
        ...

    def __str__(self) -> str:
        ...

    pass


class BadCallback(Exception):
    # raised when a bad callback is being invoked

    __module__: str
    callback: str
    src: str
    reason: Any

    def __init__(self, callback: str, src: str, reason: Any):
        ...

    def __str__(self) -> str:
        ...

    pass
