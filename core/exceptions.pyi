# all of the custom exceptions that are being used in this project

class ActivityNotFound(Exception):
    # raised when an unknown activity is called

    __module__ = Exception.__module__

    def __init__(self, activity):
        self.activity = activity
        return

    def __str__(self):
        return f"Activity {self.activity} does not exist"

    pass


class BadCallback(Exception):
    __module__: str
    callback: str
    src: str
    reason: Exception

    def __init__(self, callback: str,
                 src: str, reason: Exception):
        ...

    def __str__(self) -> str:
        ...

    pass


class BotNotNamed(Exception):
    __module__: str

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


class NoTokenFound(Exception):
    __module__: str
    name: str

    def __init__(self, name: str):
        ...

    def __str__(self) -> str:
        ...

    pass


class OverrideError(Exception):
    __module__: str
    method: str
    class_name: str

    def __init__(self, method: str, class_name: str):
        ...

    def __str__(self) -> str:
        ...

    pass
