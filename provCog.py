from datetime import datetime
from typing import Optional

from discord.ext.commands import Cog, command
from data import Data


class ProvCog(Cog):
    def __init__(self, bot):
        self.bot = bot
        # every bot has a help command so we need to remove it
        self.bot.remove_command("help")
        return

    @command(name="help", aliases=["info", "bot"])
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
            await ctx.send(Data.get_help_embeds(self.bot)[cmd])
        return

    @command(name="userinfo")
    async def get_user_info(self, ctx, target: Optional[str]):
        target = target or ctx.author

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
