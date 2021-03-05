from typing import Callable


def override(interface_class: object) -> Callable:
    def overrider(method: Callable) -> None:
        ...

    return overrider
