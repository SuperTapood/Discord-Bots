from typing import Optional

from discord.ext.commands import command, Context

from core import MasterCog


class ProvCog(MasterCog):
    @command(name="help", aliases=["info"])
    async def show_help(self, ctx: Context, cmd: Optional[str]) -> None:
        ...

    @command(name="userinfo")
    async def get_user_info(self, ctx: Context, target: str = None) -> None:
        ...

    pass
