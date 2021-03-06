import json
from time import time

from discord.ext.commands import command

from core import MasterCog, Data


class UncleCog(MasterCog):
    data = {}
    path = "uncle/data.json"

    def __init__(self, bot):
        self.data = {}
        super().__init__(bot)
        return

    def read_data(self):
        try:
            with open(self.path, "r") as file:
                data = json.loads(file.read())
        except FileNotFoundError:
            self.write_data(append=False)
        return data

    def write_data(self, append=True):
        if append:
            new = self.data
            with open(self.path, "w") as file:
                file.write(json.dumps(new))
            self.data = new
        else:
            with open(self.path, "w") as file:
                file.write(json.dumps(self.data))
        return

    @staticmethod
    def get_new_data():
        return {
            "money": 100,
            "dps": 0,
            "levels": [0],
            "last": time()
        }

    @command(name="init")
    async def init(self, ctx):
        self.data[ctx.author.id] = self.get_new_data()
        self.write_data()
        await self.bot.send(ctx.channel, f"created profile for user {ctx.author.mention}")
        return

    @command(name="reset")
    async def reset(self, ctx):
        if ctx.author.id in Data.get_owners():
            self.data = {}
            self.write_data()
            await self.bot.send(ctx.channel, "deleted profiles")
        return

    async def assert_user(self, ctx):
        try:
            # basically self.data[ctx.author.id] but i don't want to store it
            # and don't want pycharm to annoy me
            self.data.__getitem__(ctx.author.id)
            return True
        except KeyError:
            await self.bot.send_bug_report("KeyError",
                                           name=ctx.author.display_name,
                                           key=ctx.author.id,
                                           data=self.data.keys())
            await self.bot.send(ctx.channel, f"user {ctx.author.display_name} does not exist "
                                             f"in the current context. Please use command !init first")
        return False

    @command(name="stats", aliases=["userstats", "stat"])
    async def stats(self, ctx):
        if await self.assert_user(ctx):
            data = self.data[ctx.author.id]
            fields = [
                (key, data[key], False) for key in data
            ]
            await self.bot.generate_send_embed(f"{ctx.author.display_name} stats",
                                               fields, ctx.channel)
        return

    pass


def setup(bot):
    bot.add_cog(UncleCog(bot))
    return
