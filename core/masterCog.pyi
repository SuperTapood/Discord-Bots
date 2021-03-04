from typing import Optional

from discord.ext.commands import Cog, Context
from discord.ext.commands import command

from core.framework import Framework


class MasterCog(Cog):
    bot: Framework

    def __init__(self, bot: Framework) -> None:
        ...

    @command(name="bj")
    async def play_bj(self, ctx: Context) -> None:
        pass

    @command(name="hit", aliases=["h"])
    async def hit(self, ctx: Context) -> None:
        pass

    @command(name="skip", aliases=["surrender", "s"])
    async def skip(self, ctx: Context) -> None:
        pass

    @command(name="help", aliases=["info"])
    async def show_help(self, ctx: Context, cmd: Optional[str] = None) -> None:
        pass

    @command(name="userinfo")
    async def get_user_info(self, ctx: Context, target: Optional[str] = None) -> None:
        pass

    pass
