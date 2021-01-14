from discord import Embed

from framework import Framework
from random import randint
from data import Data


class Providence(Framework):
    # one liners that bots will use to report they are ready
    # the % will be replaced with the bots' name
    one_liners = [
        "A wild % appeared!",
        "% reporting for duty!",
        "% is up and running!",
        "% is as high as a kite!",
        "It's a me! %!",
        "% is as ready as they'll ever be!",
        "% thinks reading this is not the best use of time",
    ]

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

    async def help(self, bot, channel):
        """
        provides documentation about all of the commands available for a bot.
        This command takes an optional argument, the bot.
        outputs the help with the provided bot or all of them.
        """
        if bot == "":
            # if no bot is provided, display help for all bots
            await channel.send("No bots supplied. Documentation will be provided for all bots.")
            embeds = Data.get_help_embeds(self)
            for key in embeds:
                await channel.send(embed=embeds[key])
        elif bot not in Data.get_bots():
            # if the bot doesn't exist, tell the user
            await channel.send(f"bot '{bot}' not found!")
        else:
            # send out the embed for the proper bot
            await channel.send(Data.get_help_embeds(self)[bot])
        return

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
        chosen = self.one_liners.pop(randint(0, len(self.one_liners) - 1))
        await self.send("online log", chosen.replace("%", "Providence"))
        # boot up the rest of the boiz
        # empty for now.
        return
    pass
