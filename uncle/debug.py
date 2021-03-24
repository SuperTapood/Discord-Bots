from discord.ext.commands import command

from core import MasterCog, Data


class Debug(MasterCog):
    @command(name="data")
    async def get_data(self, ctx):
        if self.is_owner(ctx):
            if self.data == {}:
                await ctx.send("No users found")
                return
            for player_id in self.data:
                info = self.data[player_id]
                fields = [
                    (key, f"{type(value)}: {value}", False)
                    for key, value in zip(info.keys(), info.values())
                ]
                await self.bot.generate_send_embed(f"{player_id} {type(player_id)} data", fields, ctx.channel)
        return

    @command(name="create")
    async def create(self, ctx, profile_id):
        if self.is_owner(ctx):
            self.data[str(profile_id)] = self.get_new_data()
            self.write_data()
            await ctx.send(f"created profile for user {profile_id}")
        self.write_data()
        return

    @command(name="set_level", aliases=["setl"])
    async def set_level(self, ctx, index, level):
        if self.is_owner(ctx):
            self.data[ctx.author.id]["levels"][int(index)] = int(level)
            await ctx.send(f"level {index} mine's level has been set to {level}")
        self.write_data()
        return

    @command(name="wipe", aliases=["reboot"])
    async def wipe(self, ctx):
        if self.is_owner(ctx):
            self.data = {
                profile: self.get_new_data()
                for profile in self.data
            }
            await ctx.send("wiped data")
        self.write_data()
        return

    @command(name="reset")
    async def reset(self, ctx):
        if ctx.author.id in Data.get_owners():
            self.data = {}
            self.write_data()
            await ctx.send("deleted profiles")
        self.write_data()
        return

    pass
