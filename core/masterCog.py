from discord.ext.commands import Cog, CommandNotFound


async def on_command_error(ctx, error):
    # handle any command errors
    if isinstance(error, CommandNotFound):
        return
    raise error


class MasterCog(Cog):
    def __init__(self, bot):
        """
        bind the bot to the cog and remove the bot's help command
        :param bot: Framework, the bot to be overridden
        """
        self.bot = bot

        # wrap the on_command error to handle
        # any command errors
        bot.event(on_command_error)

        self.bot.remove_command("help")
        return

    pass
