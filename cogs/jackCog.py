from discord.ext.commands import Cog, command

from util.data import Data


class JackCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")
        return

    @Cog.listener()
    async def on_member_join(self, member):
        await self.bot.send("stdout", f"Welcome to the family, {member.mention}.")
        return

    @Cog.listener()
    async def on_member_remove(self, member):
        await self.bot.send("stdout", f"Not leaving, are you {member.mention}?")
        return

    @command(name="help")
    async def blank(self, *args, **kwargs):
        # a blank function so that discord won't raise an exception when
        # trying to invoke non existing commands
        pass

    @command(name="terminate", aliases=["kill"])
    async def stop(self, ctx, cmd):
        if ctx.author.id != Data.get_owners()[0]:
            ctx.send("Terminating...")
            quit()
        return


def setup(bot):
    bot.add_cog(JackCog(bot))
    return
