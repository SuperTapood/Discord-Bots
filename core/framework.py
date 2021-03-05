# this class is the master class for all bots in the project
from datetime import datetime

import discord
from discord import Intents, Embed
from discord.ext.commands import Bot, CommandNotFound, ExtensionNotFound

from core import Data, BotNotNamed, NoTokenFound, ActivityNotFound, ExceptionNotFound
from tokens import get_token


class Framework(Bot):
    def __init__(self, name="", intents=Intents.all(), cmd_prefix="!"):
        """
        init the bot\n
        :param name: str, the name of the bot. Will be used to enforce cog naming
            and token regulations
        :param intents: optional str / Intents, the intents of the bot
        """
        # figure out intents
        if type(intents) != Intents:
            intents = getattr(Intents, intents)()
        # declaring variables early
        self.token = ""
        self.guild = None
        self.name = name
        # reset all callbacks
        self.callbacks = {}
        # initialize the master class
        super().__init__(command_prefix=cmd_prefix,
                         owner_ids=Data.get_owners(),
                         intents=intents)
        return

    async def default_callback(self, *args, **kwargs):
        """
        default callback for functions
        :param args: Any
        :param kwargs: Any
        :return:
        """
        pass

    def set_callback(self, name, callback):
        """
        set a callback for a function\n
        :param name: str, the function's name
        :param callback: any function, the function that will be called
        """
        # this function is where the REAL magic happens
        # jk, just allowing you to do whatever
        # please for the love of god don't override
        # the functions that use the callbacks
        if name not in self.callbacks:
            self.callbacks[name] = callback
        return

    def load_token(self):
        """
        load the bot's token
        """
        # loads the token used by this specific bot
        try:
            assert self.name != ""
            self.token = get_token(self.name)
        except AssertionError:
            # if this is being raised, no name was given
            raise BotNotNamed()
        except FileNotFoundError:
            # if this is being raised, no token file was found
            raise NoTokenFound(self.name)

    def setup(self):
        """
        load the bot's cog
        """
        try:
            self.load_extension(f"{self.name}.{self.name}Cog")
            print(f"{self.name.capitalize()} Cog loaded!")
        except ExtensionNotFound:
            print(f"{self.name.capitalize()} has no cog")
        return

    def run(self):
        """
        load the cog, the token and then boot the bot\n
        :return: self, for no reason at all
        """
        # this is the main function
        self.setup()
        self.load_token()
        # boot this bot up !
        super().run(self.token, reconnect=True)
        return self

    # start of helper functions --------------------------------------------------

    async def set_presence(self, activity_type, name, **kwargs):
        """
        set the bot's presence\n
        :param activity_type: str, name of the activity
        :param name: str, name of the activity itself
        :param kwargs: dict[str, Any], any other arguments
            that may be used
        """
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
            raise NotImplemented()
            # this doesn't appear to work...
            # noinspection PyUnreachableCode
            activity = discord.Activity(type=discord.ActivityType.custom, name=name)
            await self.change_presence(status=discord.Status.online, activity=activity)
        else:
            raise ActivityNotFound(activity_type)
        return

    async def send(self, channel, msg):
        """
        send a message to a channel\n
        :param channel: str/int/TextChannel, the channel.
            None TextChannel types will be casted to TextChannel.
        :param msg: str, the message to send
        """
        # a quick nice helper function to send messages
        if type(channel) == str:
            channel = self.get_channel(Data.get_channel(channel))
        elif type(channel) == int:
            channel = self.get_channel(channel)
        await channel.send(msg)
        return

    @staticmethod
    def extract_cmd(msg):
        """
        extract a command from a message\n
        :param msg: str, the message
        :return: tuple[str], the command and the context
        """
        msg = msg[1:].split(" ")
        cmd = msg[0]
        ctx = msg[1:]
        return cmd, "".join(ctx)

    @staticmethod
    def generate_embed(title, fields, colour=None, timestamp=datetime.utcnow(), thumbnail_url=None):
        """
        generate an embed using some defaults\n
        :param title: str, the title of the embed
        :param fields: list[tuple[str, str, bool]], all
            the fields to add to the embed ordered like this:
            (title, text, inline?)
        :param colour: optional color, the color of the embed
        :param timestamp: optional str, the timestamp
        :param thumbnail_url: optional str, the image to put in the thumbnail
        :return: Embed, the generated embed
        """
        if colour is not None:
            embed = Embed(title=title, colour=colour, timestamp=timestamp)
        else:
            embed = Embed(title=title, timestamp=timestamp)
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        if thumbnail_url is not None:
            embed.set_thumbnail(url=thumbnail_url)
        return embed

    async def send_bug_report(self, exc, **kwargs):  # sourcery skip
        """
        send a bug report to a channel\n
        :param exc: str, the reported exception
        :param kwargs: any arguments
        """
        # sourcery will be skipped bc this function will grow with more exceptions
        out = self.get_channel(Data.get_channel("bot bugs"))
        if exc == "MemberNotFound":
            msg = f"{exc}Error: could not find member '{kwargs['name']}' " \
                  f"in guild '{kwargs['guild']}'. Command was invoked by user {kwargs['author']}"
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
        """
        attempt to call the on_connect callback
        """
        await self.callbacks.get("on_connect", default=self.default_callback)()
        return

    async def on_disconnect(self):
        """
        attempt to call the on_disconnect callback
        """
        await self.callbacks.get("on_disconnect", default=self.default_callback)()
        return

    async def on_ready(self):
        """
        attempt to call the on_ready callback
        """
        await self.callbacks.get("on_ready", default=self.default_callback)()
        return

    async def on_message(self, message):
        """
        handles any sent messages. if the sent message is a command,
        discord will handle it on its own. else, the on_message callback will be
        invoked
        :param message: str, the message that was sent
        """
        # i don't want an infinite loop of the bot checking itself
        # or even check other bots
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
                await self.callbacks.get("on_message", default=self.default_callback)()
        return

    # end of callback functions -------------------------------------------------
