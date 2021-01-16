from discord import Embed

from util.framework import Framework
from util.override import override
from util.data import Data


class Providence(Framework):
    # one liners that bots will use to report they are ready
    # the % will be replaced with the bots' name

    def __init__(self):
        # initialize the superclass first
        super().__init__("providence")
        # set all of the callbacks for the super class
        self.set_callback("on_disconnect", self.disconnected)
        self.set_callback("on_ready", self.ready)
        self.set_callback("on_message", self.message)
        self.set_command_callback("help", self.help)
        return

    async def disconnected(self):
        # what the bot will do when disconnected
        await self.send("online log", "disconnected")
        return

    async def message(self, msg):
        # the on_message callback
        if not msg.author.bot:
            content = msg.clean_content
            if "69" in content:
                await self.send(msg.channel, "nice")
        return

    @override(Framework)
    def setup(self):
        self.load_extension("provCog")
        print("ProvCog loaded")

    # these are the command placeholders bc i could not be bothered to move this
    # somewhere else. Also moving this will require a redo of the entire help command
    # and i can't be asked

    async def help(self, bot, channel):
        """
        provides documentation about all of the commands available for a bot.
        This command takes an optional argument, the bot.
        outputs the help with the provided bot or all of them.
        """
        pass

    def get_embed(self) -> Embed:
        # the embed method for the help command
        # returns an embed with the info
        embed = Embed(title="Help with the providence bot")
        fields = [("!Help", self.help.__doc__, False)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        return embed

    async def ready(self):
        # a callback for when the bot is ready
        print("READY!")
        # sets presence for the bot
        await self.set_presence("game", "with you peasants")
        # announce thyself
        chosen = Data.get_one_liner()
        # this starts to get annoying while testing
        # await self.send("online log", chosen.replace("%", "Providence"))
        return

    pass
