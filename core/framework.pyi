# this class is the master class for all bots in the project
from datetime import datetime
from typing import Any, Union, Callable, Optional

from discord import Intents, TextChannel, Color, Message
from discord.ext.commands import Bot, Context

from core import *


class Framework(Bot):
    token: str
    guild: Optional[int]
    name: str
    prefix: str
    callbacks: dict[str, Callable]

    def __init__(self, name: str = "", intents: Union[Intents, str] = Intents.all(), cmd_prefix: str = "!"):
        ...

    async def default_callback(self, *args: Any, **kwargs: Any):
        ...

    @staticmethod
    def extract_cmd(msg: str) -> tuple[str]:
        ...

    @staticmethod
    def generate_embed(title: str, fields: list[tuple[str, str, bool]],
                       colour: Color = None, timestamp: datetime = datetime.utcnow(),
                       thumbnail_url: str = None):
        ...

    async def generate_send_embed(self, title: str, fields: list[tuple[str, str, bool]],
                                  channel: Union[str, int, Context, TextChannel],
                                  colour: Color = None, timestamp: datetime = datetime.utcnow(),
                                  thumbnail_url: str = None):
        ...

    def get_callbacks(self) -> dict[str, str]:
        ...

    async def invoke_callback(self, callback: str, *args: Any, **kwargs: Any):
        ...

    def load_token(self):
        ...

    async def on_connect(self):
        ...

    async def on_disconnect(self):
        ...

    async def on_message(self, message: Message):
        ...

    async def on_ready(self):
        ...

    def run(self) -> Framework:
        ...

    async def send(self, channel: Union[str, int, Context, TextChannel],
                   msg: str):
        ...

    async def send_bug_report(self, exc: str, **kwargs: Any):  # sourcery skip
        ...

    def set_callback(self, name: str, callback: Callable):
        ...

    async def set_presence(self, activity_type: str, name: str, **kwargs: Any):
        ...

    def setup(self):
        ...

    pass
