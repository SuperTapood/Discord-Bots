from discord.ext.commands import Cog
from discord.ext.commands import command


class MasterCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")
        return

    @command(name="bj")
    async def play_bj(self, ctx):
        pass

    @command(name="hit", aliases=["h"])
    async def hit(self, ctx):
        pass

    @command(name="skip", aliases=["surrender", "s"])
    async def skip(self, ctx):
        pass

    @command(name="help", aliases=["info"])
    async def show_help(self, ctx, cmd=None):
        pass

    @command(name="userinfo")
    async def get_user_info(self, ctx, target=None):
        pass

    pass
