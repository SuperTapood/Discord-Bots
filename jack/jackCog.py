from core import MasterCog


class JackCog(MasterCog):

    @MasterCog.listener()
    async def on_member_join(self, member):
        await self.bot.send("stdout", f"Welcome to the family, {member.mention}.")
        return

    # do not
    # @MasterCog.listener()
    # async def on_member_remove(self, member):
    #     await self.bot.send("stdout", f"Not leaving, are you {member.mention}?")
    #     return

    pass


def setup(bot):
    bot.add_cog(JackCog(bot))
    return
