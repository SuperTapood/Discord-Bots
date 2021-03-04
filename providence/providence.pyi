from discord import Message

from core import Framework


class Providence(Framework):
    # one liners that bots will use to report they are ready
    # the % will be replaced with the bots' name

    def __init__(self) -> None:
        ...

    async def disconnected(self) -> None:
        ...

    @staticmethod
    async def message(msg: Message) -> None:
        ...

    async def ready(self) -> None:
        ...

    pass
