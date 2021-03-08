import pickle
from time import time

from discord.ext.commands import command, Context

from core import MasterCog, Data


class UncleCog(MasterCog):
    data = {}
    path = "uncle/data.json"

    def __init__(self, bot):
        super().__init__(bot)
        self.data = self.read_data()
        return

    def read_data(self):
        # switched from json to pickle to support int dict keys
        try:
            with open(self.path, "rb") as handle:
                data = pickle.load(handle)
        except FileNotFoundError:
            self.write_data()
            data = self.read_data()
        return data

    def write_data(self):
        with open(self.path, "wb") as handle:
            pickle.dump(self.data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return

    def is_owner(self, arg):
        if type(arg) == Context:
            arg = arg.author.id
        else:
            raise NotImplementedError()
        return arg in Data.get_owners()

    @staticmethod
    def get_new_data():
        return {
            "money": 100,
            "dps": 0,
            "levels": [0, 0, 0, 0, 0, 0],
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
        data = await self.get_profile(ctx)
        if data is not None:
            fields = [
                (key, data[key], False) for key in data
            ]
            await self.bot.generate_send_embed(f"{ctx.author.display_name} stats",
                                               fields, ctx.channel)
        return

    def get_level(self, ctx, index):
        return self.data[str(ctx.author.id)]["levels"][index]

    @staticmethod
    def calculate_price(ctx, index):
        # i need to have some formula here
        return 0

    async def get_profile(self, ctx):
        if await self.assert_user(ctx):
            return self.data[ctx.author.id]
        else:
            return None

    @command(name="browse", aliases=["buy"])
    async def browse(self, ctx):
        data = await self.get_profile(ctx)
        if data is not None:
            fields = [
                (f"Mine {i}, Level {self.get_level(ctx, i)} -> {self.get_level(ctx, i)}",
                 f"{self.calculate_price(ctx, i)}$",
                 i % 2 == 1)
                for i in range(len(data["levels"]))
            ]
            await self.bot.generate_send_embed(f"Price catalog for {ctx.author.display_name}", fields, ctx.channel)
        return

    @command(name="data")
    async def get_data(self, ctx):
        if self.is_owner(ctx):
            if self.data == {}:
                await self.bot.send(ctx.channel, "No users found")
                return
            for player_id in self.data:
                info = self.data[player_id]
                fields = [
                    (key, f"{type(value)}: {value}", False)
                    for key, value in zip(info.keys(), info.values())
                ]
                await self.bot.generate_send_embed(f"{player_id} {type(player_id)} data", fields, ctx.channel)
        return

    # debug functions

    @command(name="create")
    async def create(self, ctx, profile_id):
        if self.is_owner(ctx):
            self.data[str(profile_id)] = self.get_new_data()
            self.write_data()
            await self.bot.send(ctx.channel, f"created profile for user {profile_id}")
        return

    @command(name="set_level", aliases=["setl"])
    async def set_level(self, ctx, index, level):
        if self.is_owner(ctx):
            self.data[str(ctx.author.id)]["levels"][int(index)] = int(level)
            await self.bot.send(ctx.channel, f"level {index} mine's level has been set to {level}")
        return

    @command(name="wipe", aliases=["reboot"])
    async def wipe(self, ctx):
        if self.is_owner(ctx):
            self.data = {
                profile: self.get_new_data()
                for profile in self.data
            }
            await self.bot.send(ctx.channel, "wiped data")
        return

    pass


def setup(bot):
    bot.add_cog(UncleCog(bot))
    return
