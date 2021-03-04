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

    def __init__(self, exc: str):
        ...

    def __str__(self) -> str:
        ...

    pass
