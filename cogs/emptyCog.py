from datetime import datetime
from typing import Optional

from discord import Member
from discord.ext.commands import Cog, command
from util.data import Data


class EmptyCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        # every bot has a help command so we need to remove it
        self.bot.remove_command("help")
        return
    pass


def setup(bot):
    bot.add_cog(EmptyCog(bot))
    return
