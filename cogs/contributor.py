import discord
from discord.ext import commands
import data 
   
class contributor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='submittalForm')
    async def submittalForm(self, ctx):
        await ctx.send('Hopefully This Works...')

    @commands.command(name='help')
    async def help(self, ctx):
        embed = discord.Embed(
            title = 'Submission Commands',
            description = 'List of commands for submittial bot',
            colour = discord.Colour.purple()
        )

        embed.add_field(name='!help', value= '- Brings up list of commands', inline = False)
        embed.add_field(name='!submittalForm', value= '- Brings up submittal form and instructions', inline = False)
        embed.add_field(name='!adminHelp (Administrator only)', value= '- Displays list of Admin controls', inline = False)
        embed.set_footer(text = 'If there is any problems with the bot, please contact {add contact}')
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(contributor(bot))
