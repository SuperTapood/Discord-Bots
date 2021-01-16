from discord.ext.commands import Cog


class JackCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        return

    @Cog.listener()
    async def on_member_join(self, member):
        await self.bot.send("stdout", f"Welcome to the family, {member.mention}.")
        return

    @Cog.listener()
    async def on_member_remove(self, member):
        await self.bot.send("stdout", f"Not leaving, are you {member.mention}?")
        return


def setup(bot):
    bot.add_cog(JackCog(bot))
    return
