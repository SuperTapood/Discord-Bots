# this class is the master class for all bots in the project
from datetime import datetime

import discord
from discord import Intents, Embed
from discord.ext.commands import Bot, CommandNotFound, ExtensionNotFound

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
        self.prefix = cmd_prefix
        # reset all callbacks
        self.callbacks = {}
        # initialize the master class
        super().__init__(command_prefix=cmd_prefix,
                         owner_ids=Data.get_owners(),
                         intents=intents)
        return

    @staticmethod
    def create_activity(activity_type, name, **kwargs):
        """
        set the bot's presence\n
        :param activity_type: str, name of the activity
        :param name: str, name of the activity itself
        :param kwargs: dict[str, Any], any other arguments
            that may be used
        :return: the created activity
        """
        if activity_type == "game":
            activity = discord.Game(name=name)
        elif activity_type == "stream":
            activity = discord.Streaming(name=name, url=kwargs["url"])
        elif activity_type == "listen":
            activity = discord.Activity(type=discord.ActivityType.listening, name=name)
        elif activity_type == "watch":
            activity = discord.Activity(type=discord.ActivityType.watching, name=name)
        elif activity_type == "custom":
            activity = discord.Activity(type=discord.ActivityType.custom, name=name)
        elif activity_type == "competing":
            activity = discord.Activity(type=discord.ActivityType.competing, name=name)
        else:
            raise ActivityNotFound(activity_type)
        return activity

    async def default_callback(self, *args, **kwargs):
        """
        default callback for functions\n
        :param args: Any
        :param kwargs: Any
        :return:
        """
        pass

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

    async def generate_send_embed(self, title, fields, channel, colour=None, timestamp=datetime.utcnow(),
                                  thumbnail_url=None):
        """
        generate an embed using some defaults\n
        :param title: str, the title of the embed
        :param fields: list[tuple[str, str, bool]], all
            the fields to add to the embed ordered like this:
            (title, text, inline?)
        :param channel: str, int, or TextChannel, the channel to send the embed to
        :param colour: optional color, the color of the embed
        :param timestamp: optional str, the timestamp
        :param thumbnail_url: optional str, the image to put in the thumbnail
        :return: Embed, the generated embed
        """
        embed = self.generate_embed(title, fields, colour, timestamp, thumbnail_url)
        if type(channel) == str:
            channel = self.get_channel(Data.get_channel(channel))
        elif type(channel) == int:
            channel = self.get_channel(channel)
        await channel.send(embed=embed)
        return

    def get_callbacks(self):
        """
        get all of the current callbacks because reasons
        """
        callbacks = ["on_connect",
                     "on_disconnect",
                     "on_ready",
                     "on_message"]
        return {
            c: self.callbacks.get(c, self.default_callback).__name__
            for c in callbacks
        }

    async def invoke_callback(self, callback, *args, **kwargs):
        """
        invoke a callback\n
        :param callback: str, the name of the function
        :param args: Any, the arguments to pass into the callback
        :param kwargs: Any, the keyword arguments to pass into the callback
        """
        # this is a tad complicated so pay attention
        # fetch the callback, or the default one if it doesn't exist
        callf = self.callbacks.get(callback, self.default_callback)
        # may raise TypeError if the callback is incompatible
        try:
            # a bit of figuring out what arguments we do or do not need
            # because lambda: --- cannot take args or kwargs even if
            # they are empty
            if args == ():
                if kwargs == {}:
                    await callf()
                else:
                    await callf(kwargs)
            else:
                if kwargs == {}:
                    await callf(args)
                else:
                    await callf(args, kwargs)
        except TypeError as e:
            raise BadCallback(callf, callback, e)
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
        return

    async def on_connect(self):
        """
        attempt to call the on_connect callback
        """
        await self.invoke_callback("on_connect")
        return

    async def on_disconnect(self):
        """
        attempt to call the on_disconnect callback
        """
        await self.invoke_callback("on_disconnect")
        return

    async def on_message(self, message):
        """
        handles any sent messages. if the sent message is a command,
        discord will handle it on its own. else, the on_message callback will be
        invoked\n
        :param message: str, the message that was sent
        """
        # i don't want an infinite loop of the bot checking itself
        # or even check other bots
        if not message.author.bot:
            # if the message is a command
            if message.clean_content[0] == self.prefix:
                # discord.py will handle this nonsense
                try:
                    await self.process_commands(message)  # may raise CommandNotFound
                # if the command wasn't found, it was either a mistake, or
                # a command for another bot :\
                # this may not even be necessary after the cog's error handling
                except CommandNotFound:
                    pass
            # invoke the callback if the message is not a command
            await self.invoke_callback("on_message", message)
        return

    async def on_ready(self):
        """
        attempt to call the on_ready callback
        """
        await self.invoke_callback("on_ready")
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

    async def send(self, channel, msg):
        """
        send a message to a channel\n
        :param channel: str/int/Context/TextChannel, the channel.
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

    async def send_bug_report(self, exc, **kwargs):  # sourcery skip
        """
        send a bug report to a channel\n
        :param exc: str, the reported exception
        :param kwargs: any arguments
        """
        # sourcery will be skipped bc this function will grow with more exceptions
        out = self.get_channel(Data.get_channel("bot bugs"))
        if exc == "MemberNotFound":
            msg = f"MemberNotFound: could not find member '{kwargs['name']}' " \
                  f"in guild '{kwargs['guild']}'. Command was invoked by user {kwargs['author']}"
        elif exc == "KeyError":
            msg = f"KeyError: member {kwargs['name']} (id {kwargs['key']}) does not exist in {kwargs['data']}"
        else:
            raise ExceptionNotFound(exc)
        await out.send(msg)
        return

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

    def set_callbacks(self, **kwargs):
        """
        set a callbacks for all functions\n
        :param kwargs: dict of str, callbacks for the functions
        """
        for name in ["on_connect",
                     "on_disconnect",
                     "on_ready",
                     "on_message"]:
            self.callbacks[name] = kwargs.pop(name, self.default_callback)
        return

    async def set_presence(self, activity):
        await self.change_presence(status=discord.Status.online, activity=activity)
        return

    def setup(self):
        """
        load the bot's cog. Used to enforce a naming standard but
        you can override it yourself if you feel like it
        """
        try:
            self.load_extension(f"{self.name}.{self.name}Cog")
            print(f"{self.name.capitalize()} Cog loaded!")
        except ExtensionNotFound:
            print(f"{self.name.capitalize()} has no cog")
        return

    pass
