from datetime import datetime
from typing import Optional, Callable, Union, Any

from discord import Embed, TextChannel, Color, Message
from discord.ext.commands import Bot


class Framework(Bot):
    token: str
    guild: Optional[int]
    name: str
    callbacks: dict[str, Callable]

    def __init__(self, name: Optional[str] = "") -> None:
        ...

    def set_callback(self, name: str, callback: Callable) -> None:
        ...

    def load_token(self) -> None:
        ...

    def setup(self) -> None:
        ...

    def run(self) -> None:
        ...

    # start of helper functions --------------------------------------------------

    async def set_presence(self, activity_type: str, name: str, **kwargs: Optional[dict[str, Any]]):
        ...

    async def send(self, channel: Union[str, int, TextChannel], msg: str):
        ...

    @staticmethod
    def extract_cmd(msg: str) -> tuple[str]:
        ...

    @staticmethod
    def generate_embed(title: str, fields: list[tuple[str, str, bool]], colour: Color = None,
                       timestamp: str = datetime.utcnow(),
                       thumbnail_url: str = None) -> Embed:
        ...

    async def send_bug_report(self, exc: str, **kwargs: dict[str, Any]) -> None:
        ...

    # end of helper functions ----------------------------------------------------

    # start of callback functions ------------------------------------------------

    async def on_connect(self) -> None:
        ...

    async def on_disconnect(self) -> None:
        ...

    async def on_ready(self) -> None:
        ...

    async def on_message(self, message: Message) -> None:
        ...

    # end of callback functions -------------------------------------------------
