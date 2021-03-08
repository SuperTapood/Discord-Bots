from discord.ext.commands import Cog, Context

from core import Framework


async def on_command_error(ctx: Context, error: Exception):
    ...


class MasterCog(Cog):
    bot: Framework

    def __init__(self, bot: Framework):
        ...

    pass
