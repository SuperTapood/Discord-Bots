from typing import Optional

from discord.ext.commands import command, Context

from core import MasterCog


class HouseCog(MasterCog):
    suits: dict[int, str]
    player: list[int]
    bot_cards: list[int]
    player_s: list[int]
    bot_s: list[int]
    deck: list[list[int]]
    player_skip: bool
    bot_skip: bool
    is_playing: bool

    def generate_deck(self) -> None:
        ...

    def deal(self, cards: list[int], signs: list[int], amount: int) -> None:
        ...

    def get_cards(self, cards: list[int], signs: list[int], is_bot: Optional[bool] = False) -> str:
        ...

    async def present_cards(self, ctx: Context) -> None:
        ...

    @command(name="bj")
    async def play_bj(self, ctx: Context) -> None:
        ...

    def bot_play(self) -> bool:
        ...

    @command(name="hit", aliases=["h"])
    async def hit(self, ctx: Context) -> None:
        ...

    @command(name="skip", aliases=["surrender", "s"])
    async def skip(self, ctx: Context) -> None:
        ...

    async def stop(self, ctx: Context) -> None:
        ...

    pass
