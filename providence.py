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
        return

    async def disconnected(self):
        # what the bot will do when disconnected
        await self.send("online log", "disconnected")
        return

    async def message(self, msg):
        # the on_message callback
        if not msg.author.bot:
            content = msg.clean_content
            if "69" in content or "420" in content:
                await msg.channel.send("nice")
        return

    @override(Framework)
    def setup(self):
        self.load_extension("cogs.provCog")
        print("ProvCog loaded")
        return

    async def ready(self):
        # a callback for when the bot is ready
        print("READY!")
        # sets presence for the bot
        await self.set_presence("game", "with you peasants")
        # announce thyself
        chosen = Data.get_one_liner()
        # this starts to get annoying while testing
        await self.send("online log", chosen.replace("%", "Providence"))
        return
    pass


Providence().run()
