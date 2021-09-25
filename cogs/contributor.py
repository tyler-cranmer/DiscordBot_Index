import discord
from discord.ext import commands 
import data 
   
class contributor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #submits google sheet to database
    #!submitForm {discordname} needs quotes for " name with spaces "
    @commands.command(name='submitForm')
    async def submitForm(self, ctx, arg):
        index_contributor = data.UserSheet(arg)
        submit = index_contributor.collectContributorSheet()
        await ctx.send(f'You have submitted {submit} contributions. Thank you for all the work you have done this month.')

    @submitForm.error
    async def submitForm_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Command failed. \n Please make sure to type: !submitForm "discord name"')
        
    #creates new contributor sheet
    #!newContributor {discordname} {gmail} needs quotes for " name with spaces "
    @commands.command(name='newContributor')
    async def newContributor(self, ctx, arg1, arg2):
        new_contributor = data.NewUser(arg1, arg2)
        URL = new_contributor.create_spread_sheet()
        await ctx.send('Your {} contribution sheet as been created. \n Please store this sheet in your GoogleDrive: {}'.format(arg1,URL))

    @newContributor.error
    async def newContributor_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Command failed. \n Please make sure to type: !newContributor "Discord name" "email"')

    @commands.command(name='help')
    async def help(self, ctx):
        embed = discord.Embed(
            title = 'Submission Commands',
            description = 'List of commands for submittial bot',
            colour = discord.Colour.purple()
        )

        embed.add_field(name='!newContributor', value= '- Creates new google work sheet. \n - Command syntax: !newContributor "discord name" "Gmail address"', inline = False)
        embed.add_field(name='!submitForm', value= '- Submits google sheet to database. \n - Command syntax: !submitForm "google sheet url"', inline = False)
        embed.add_field(name='!help', value= '- Brings up list of commands', inline = False)
        embed.add_field(name='!adminHelp (Administrator only)', value= '- Displays list of Admin controls', inline = False)
        embed.set_footer(text = 'If there is any problems with the bot, please contact {add contact}')
        
        await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if isinstance(error, commands.CommandError):
            await ctx.send('Command not found. Please type: !help or !adminHelp for a list of all commands.')


def setup(bot):
    bot.add_cog(contributor(bot))
