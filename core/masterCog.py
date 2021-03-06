from discord.ext.commands import Cog
from discord.ext.commands import command


class MasterCog(Cog):
    def __init__(self, bot):
        """
        bind the bot to the cog and remove the bot's help command
        :param bot: Framework, the bot to be overridden
        """
        self.bot = bot
        self.bot.remove_command("help")
        return

    # empty functions to prevent exceptions when using commands
    # please do not use @override on them

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

    @command(name="init")
    async def init(self, ctx):
        pass

    @command(name="reset")
    async def reset(self, ctx):
        pass

    @command(name="browse")
    async def browse(self, ctx):
        pass

    pass
