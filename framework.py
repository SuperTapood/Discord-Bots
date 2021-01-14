import discord

from exceptions import BotNotNamed, NoTokenFound
from data import Data
from discord import Intents, Embed

from discord.ext.commands import Bot


class Framework(Bot):
    def __init__(self, name=""):
        self.token = ""
        self.guild = None
        self.name = name
        self.callbacks = {}
        self.cmd_callbacks = {}
        super().__init__(command_prefix="!",
                         owner_ids=Data.get_owners(),
                         intents=Intents.all())
        return

    def set_callback(self, name, callback):
        # this function is where the magic happens
        if name not in self.callbacks:
            self.callbacks[name] = callback
        return

    def set_command_callback(self, cmd, callback):
        if cmd not in self.cmd_callbacks:
            self.cmd_callbacks[cmd] = callback
        return

    def load_token(self):
        try:
            assert self.name != ""
            with open(f"{self.name}.token", "r", encoding="utf-8") as file:
                self.token = file.read()
        except AssertionError:
            raise BotNotNamed()
        except FileNotFoundError:
            raise NoTokenFound(self.name)
        return

    def setup(self):
        pass

    def run(self):
        self.setup()
        self.load_token()
        super().run(self.token, reconnect=True)
        return

    # start of helper functions --------------------------------------------------

    async def set_presence(self, activity_type, name, **kwargs):
        if activity_type == "game":
            activity = discord.Game(name=name, type=3)
            await self.change_presence(status=discord.Status.online, activity=activity)
        elif activity_type == "stream":
            activity = discord.Streaming(name=name, url=kwargs["url"])
            await self.change_presence(status=discord.Status.online, activity=activity)
        # todo: implement the other activities
        return

    async def send(self, channel, msg):
        channel = self.get_channel(Data.get_channel(channel))
        await channel.send(msg)
        return

    @staticmethod
    def extract_cmd(msg):
        msg = msg[1:].split(" ")
        cmd = msg[0]
        ctx = msg[1:]
        return cmd, "".join(ctx)

    # end of helper functions ----------------------------------------------------

    # start of callback functions ------------------------------------------------

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
        if not message.author.bot:
            if message.clean_content[0] == "!":
                cmd, ctx = self.extract_cmd(message.clean_content)
                if cmd in self.cmd_callbacks:
                    await self.cmd_callbacks[cmd](ctx, message.channel)
                else:
                    await self.send("online log", f"Command {cmd} does not exist")
            elif "on_message" in self.callbacks:
                await self.callbacks["on_message"](message)
        return

    # end of callback functions -------------------------------------------------
