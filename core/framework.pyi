from datetime import datetime
from typing import Optional, Callable, Union, Any

from discord import Embed, TextChannel, Color, Message, Intents
from discord.ext.commands import Bot


class Framework(Bot):
    token: str
    guild: Optional[int]
    name: str
    callbacks: dict[str, Callable]
    prefix: str

    def __init__(self, name: Optional[str] = "", intents: Optional[Union[str, Intents]] = Intents.all(),
                 cmd_prefix: Optional[str] = "!") -> None:
        ...

    async def invoke_callback(self, callback: str, *args: Any, **kwargs: Any):
        ...

    def get_callbacks(self) -> dict[str, str]:
        ...

    def default_callback(self, *args: tuple[Any], **kwargs: dict[str, Any]):
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
                       timestamp: datetime = datetime.utcnow(),
                       thumbnail_url: str = None) -> Embed:
        ...

    async def generate_send_embed(self, title, fields, channel, colour=None, timestamp=datetime.utcnow(),
                                  thumbnail_url=None):
        ...

    async def send_bug_report(self, exc: str, **kwargs: Any) -> None:
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
