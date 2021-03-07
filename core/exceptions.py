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
    # raised when a bad callback is being invoked

    __module__ = Exception.__module__

    def __init__(self, callback, src, reason):
        self.callback = callback
        self.src = src
        self.reason = reason
        return

    def __str__(self):
        return f"callback {self.callback} is not " \
               f"applicable to be a callback of {self.src} " \
               f"because {self.reason}"

    pass


class BotNotNamed(Exception):
    # raised when a bot isn't given a name

    __module__ = Exception.__module__

    def __str__(self):
        return "Framework can not access the name of this bot"

    pass


class ExceptionNotFound(Exception):
    # raised when an unknown exception is reported

    __module__ = Exception.__module__

    def __init__(self, exc):
        self.exc = exc
        return

    def __str__(self):
        return f"Exception {self.exc} does not exist and cannot be reported"

    pass


class NoTokenFound(Exception):
    # raised when the framework can't find the token of a bot

    __module__ = Exception.__module__

    def __init__(self, name):
        self.name = name
        return

    def __str__(self):
        return f"cannot find token file - {self.name}.token"

    pass


class OverrideError(Exception):
    # raised when a method cannot be overridden
    # useful for users who didn't spend a million billion
    # hours developing this project
    # kinda useful
    # kinda redundant

    __module__ = Exception.__module__

    def __init__(self, method, class_name):
        self.method = method
        self.class_name = class_name
        return

    def __str__(self):
        return f"method '{self.method}' does not exist in class '{self.class_name}'"

    pass
