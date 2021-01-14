# this class is the master class for all bots in the project

import discord

from exceptions import BotNotNamed, NoTokenFound
from data import Data
from discord import Intents

from discord.ext.commands import Bot


class Framework(Bot):
    def __init__(self, name=""):
        # a bit of variables so pycharm won't hate me
        self.token = ""
        self.guild = None
        self.name = name
        # reset all callbacks. might add defaults or smthg
        # or use dict.get(name, default=self.default_callback)
        self.callbacks = {}
        self.cmd_callbacks = {}
        # initialize Discord.Bot
        super().__init__(command_prefix="!",
                         owner_ids=Data.get_owners(),
                         intents=Intents.all())
        return

    def set_callback(self, name, callback):
        # this function is where the REAL magic happens
        if name not in self.callbacks:
            self.callbacks[name] = callback
        return

    def set_command_callback(self, cmd, callback):
        # this method is temporary maybe. I want to use both commands and plain message reading
        if cmd not in self.cmd_callbacks:
            self.cmd_callbacks[cmd] = callback
        return

    def load_token(self):
        # loads the token used by this specific bot
        try:
            assert self.name != ""
            with open(f"{self.name}.token", "r", encoding="utf-8") as file:
                self.token = file.read()
        except AssertionError:
            # if this is being raised, no name was given
            raise BotNotNamed()
        except FileNotFoundError:
            # if this is being raised, no token file was found
            raise NoTokenFound(self.name)
        return

    def setup(self):
        # blah blah yada yada
        pass

    def run(self):
        # this is the main function
        self.setup()
        self.load_token()
        # boot this bot up !
        super().run(self.token, reconnect=True)
        return

    # start of helper functions --------------------------------------------------

    async def set_presence(self, activity_type, name, **kwargs):
        # sets an activity for the bot
        # game and streaming are two special ones
        # the other ones will be harder to implement
        if activity_type == "game":
            activity = discord.Game(name=name, type=3)
            await self.change_presence(status=discord.Status.online, activity=activity)
        elif activity_type == "stream":
            activity = discord.Streaming(name=name, url=kwargs["url"])
            await self.change_presence(status=discord.Status.online, activity=activity)
        # todo: implement the other activities
        return

    async def send(self, channel, msg):
        # a quick nice helper function to send messages
        # todo: add a more complex channel system that will support several types
        channel = self.get_channel(Data.get_channel(channel))
        await channel.send(msg)
        return

    @staticmethod
    def extract_cmd(msg):
        # extract the command and the rest of it from a message
        msg = msg[1:].split(" ")
        cmd = msg[0]
        ctx = msg[1:]
        return cmd, "".join(ctx)

    # end of helper functions ----------------------------------------------------

    # start of callback functions ------------------------------------------------
    # these functions will, unless stated otherwise, attempt to call
    # callback functions when they are invoked

    async def on_connect(self):
        if "on_connect" in self.callbacks:
            await self.callbacks["on_connect"]()
        return

    async def on_disconnect(self):
        if "on_disconnect" in self.callbacks:
            await self.callbacks["on_disconnect"]()
        return

    async def on_ready(self):
        if "on_ready" in self.callbacks:
            await self.callbacks["on_ready"]()
        return

    async def on_message(self, message):
        # i don't want an infinite loop of the bot checking itself
        # or even check them
        if not message.author.bot:
            # if the message is a command
            if message.clean_content[0] == "!":
                cmd, ctx = self.extract_cmd(message.clean_content)
                if cmd in self.cmd_callbacks:
                    # invoke the command
                    await self.cmd_callbacks[cmd](ctx, message.channel)
                else:
                    # if the command doesn't exist, report it
                    await self.send("online log", f"Command {cmd} does not exist")
            elif "on_message" in self.callbacks:
                await self.callbacks["on_message"](message)
        return

    # end of callback functions -------------------------------------------------
