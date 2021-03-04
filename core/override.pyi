from typing import Callable


def override(interface_class: object) -> None:
    def overrider(method: Callable) -> None:
        ...

    return overrider
