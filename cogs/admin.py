import discord
from discord.ext import commands
import json

# Opens Json File to check for Admin Id
with open("./config.json") as f:
    configData = json.load(f)

AdminId = configData["Admin"]

#sets the admin owner of the bot.
def is_owner():
    async def predicate(ctx):
        return ctx.author.id == AdminId
    return commands.check(predicate)


class Admin(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    #Activates the bot to accept submissions
    @commands.command(name='activate')
    @is_owner()
    async def activate(self, ctx):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='for Submissions'))
        self.bot.unload_extension(f"cogs.events") 
        self.bot.load_extension(f"cogs.contributor")
        await ctx.send(f"Hooty is now taking in Contribution submissions")


    # Deactivates the Bot
    @commands.command(name='deactivate')
    @is_owner()
    async def deactivate(self, ctx):
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Closed for Submissions'))
        self.bot.unload_extension(f"cogs.contributor")
        self.bot.load_extension(f"cogs.events") 
        await ctx.send(f"Hooty is no longer taking in Contribution submissions")

    #enable different cogs while bots running 
    # !loadclog classname
    @commands.command(name='loadcog')
    @is_owner()
    async def loadcog(self, ctx, cog):
        self.bot.load_extension(f"cogs.{cog}")
        await ctx.send(f"{cog} file has been enabled.")

    #disable different cogs while bots running
    # !unloadcog {classname} 
    @commands.command(name='unloadcog')
    @is_owner()
    async def unloadcog(self, ctx, cog):
        self.bot.unload_extension(f"cogs.{cog}") 
        await ctx.send(f"{cog} file has been disabled.")


    #Admin Help Command
    @commands.command(name='adminHelp')
    @is_owner()
    async def adminHelp(self, ctx):

        embed = discord.Embed(
            title = 'Admin Bot Commands',
            description = 'List of commands only for the Administrator',
            colour = discord.Colour.blue()
        )

        embed.add_field(name='!activate', value= '- Activates bot for Submissions', inline = False)
        embed.add_field(name='!deactivate', value= '- Dectivates bot for Submissions', inline = False)
        embed.add_field(name='!adminHelp', value= '- Displays list of Admin controls', inline = False)
        embed.add_field(name='!loadcog className', value= '- Enables different class functions', inline = False)
        embed.add_field(name='!unloadcog className', value= '- Disables different class functions', inline = False)
        embed.set_footer(text = 'If there is any problems with the bot, please contact {add contact}')
        
        await ctx.send(embed=embed)

    #Throws Error if non admin tries to access adminHelp command.
    @adminHelp.error
    async def adminHelp_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send('Your account does not have Admin privlages. If you are trying to submit contribution documents, please type !help for a list of commands to assist you. ')

def setup(bot):
    bot.add_cog(Admin(bot))