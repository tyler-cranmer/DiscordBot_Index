import discord
from discord.ext import commands



class Admin(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def activity(self, ctx, *, arg):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=arg))
        await ctx.send(f"Bot's activityz changed to {arg}")
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def activate(self, ctx):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='for Submissions'))
        await ctx.send(f"Hooty is now taking in Contribution submissions")


    # #enable different cogs while bots running 
    # # !loadclog filename
    # @commands.command()
    # async def loadcog(self, ctx, cog):
    #     self.bot.load_extension(f"cogs.{cog}")
    #     await ctx.send(f"{cog} file has been enabled.")

    # #disable different cogs while bots running
    # # !unloadcog {filename} w/out .py
    # @commands.command()
    # async def unloadcog(self, ctx, cog):
    #     self.bot.unload_extension(f"cogs.{cog}") 
    #     await ctx.send(f"{cog} file has been disabled.")




    @commands.command()
    async def test(self, ctx):
        await ctx.send(f"Test was successful")

def setup(bot):
    bot.add_cog(Admin(bot))