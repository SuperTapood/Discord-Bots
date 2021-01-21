# this class is the master class for all bots in the project
from datetime import datetime

import discord

from util.exceptions import BotNotNamed, NoTokenFound, ActivityNotFound, ExceptionNotFound
from util.data import Data
from discord import Intents, Embed

from discord.ext.commands import Bot, CommandNotFound


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
            activity = discord.Game(name=name)
            await self.change_presence(status=discord.Status.online, activity=activity)
        elif activity_type == "stream":
            activity = discord.Streaming(name=name, url=kwargs["url"])
            await self.change_presence(status=discord.Status.online, activity=activity)
        elif activity_type == "listen":
            activity = discord.Activity(type=discord.ActivityType.listening, name=name)
            await self.change_presence(status=discord.Status.online, activity=activity)
        elif activity_type == "watch":
            activity = discord.Activity(type=discord.ActivityType.watching, name=name)
            await self.change_presence(status=discord.Status.online, activity=activity)
        elif activity_type == "custom":
            # this doesn't appear to work...
            activity = discord.Activity(type=discord.ActivityType.custom, name=name)
            await self.change_presence(status=discord.Status.online, activity=activity)
        else:
            raise ActivityNotFound(activity_type)
        return

    async def send(self, channel, msg):
        # a quick nice helper function to send messages
        if type(channel) == str:
            channel = self.get_channel(Data.get_channel(channel))
        elif type(channel) == int:
            channel = self.get_channel(channel)
        await channel.send(msg)
        return

    @staticmethod
    def extract_cmd(msg):
        # extract the command and the rest of it from a message
        msg = msg[1:].split(" ")
        cmd = msg[0]
        ctx = msg[1:]
        return cmd, "".join(ctx)

    @staticmethod
    def generate_embed(title, fields, colour=None, timestamp=datetime.utcnow(), thumbnail_url=None) -> Embed:
        if colour is not None:
            embed = Embed(title=title, colour=colour, timestamp=timestamp)
        else:
            embed = Embed(title=title, timestamp=timestamp)
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        if thumbnail_url is not None:
            embed.set_thumbnail(url=thumbnail_url)
        return embed

    async def send_bug_report(self, exc, **kwargs):
        # sourcery skip: remove-unnecessary-else, swap-if-else-branches
        out = self.get_channel(Data.get_channel("bot bugs"))
        if exc == "MemberNotFound":
            msg = f"{exc}Error: could not find member '{kwargs['name']}' " \
                  f"in guild '{kwargs['guild']}'. Command was invoked by user {kwargs['author'].mention}"
            cause = "I don't believe this is an actual bug, rather a user mistake. Please verify" \
                    f"the existence or non-existence of the user '{kwargs['name']}'"
        else:
            raise ExceptionNotFound(exc)
        await out.send(msg)
        await out.send(cause)

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
                # discord.py will handle this nonsense
                try:
                    await self.process_commands(message)  # may raise CommandNotFound
                except CommandNotFound:
                    pass
            elif "on_message" in self.callbacks:
                # invoke the callback if the message is not a command
                await self.callbacks["on_message"](message)
        return

    # end of callback functions -------------------------------------------------
