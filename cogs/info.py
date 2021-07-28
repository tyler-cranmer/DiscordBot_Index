import discord
from discord.ext import commands



class Info(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    
    async def activity(self, ctx, *, activity):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity))
        await ctx.send(f"Bot's activity changed to {activity}")


def setup(bot):
    bot.add_cog(Info(bot))