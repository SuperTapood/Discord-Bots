from datetime import datetime
from typing import Optional

from discord import Member
from discord.ext.commands import command

from core import MasterCog, Data


class ProvCog(MasterCog):
    @command(name="help")
    async def show_help(self, ctx, cmd: Optional[str]):
        """displays info on a command"""
        if cmd is None:
            # if no bot is provided, display help for all bots
            await ctx.send("No bots supplied. Documentation will be provided for all bots.")
            embeds = Data.get_help_embeds(self.bot)
            for key in embeds:
                await ctx.send(embed=embeds[key])
        elif cmd not in Data.get_bots():
            # if the bot doesn't exist, tell the user
            await ctx.send(f"bot '{cmd}' not found!")
        else:
            # send out the embed for the proper bot
            await ctx.send(embed=Data.get_help_embeds(self.bot)[cmd])
        return

    @command(name="userinfo", aliases=["info"])
    async def get_user_info(self, ctx, target: str = None):
        if target is None:
            target = ctx.author
        else:
            guild = ctx.guild
            member = guild.get_member_named(target)
            if member is None:
                await self.bot.send_bug_report("MemberNotFound", name=target, guild=guild, author=ctx.author)
                return
        # a hint as of why this may break
        assert type(target) == Member
        fields = [("ID", target.id, False),
                  ("Name", str(target), True),
                  ("Bot?", target.bot, True),
                  ("Top Role", target.top_role.mention, True)]

        embed = self.bot.generate_embed(title="User Information",
                                        colour=target.colour,
                                        timestamp=datetime.utcnow(),
                                        fields=fields,
                                        thumbnail_url=target.avatar_url)

        await ctx.send(embed=embed)
        return

    pass


def setup(bot):
    bot.add_cog(ProvCog(bot))
    return
