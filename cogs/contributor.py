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
        if len(submit[1]) > 0:
            await ctx.send(f'The formating of Column A of your google sheet is causing an error. Your submission was not recorded. \n Column A, Row: {submit[1][0]} need to be fixed. Please see video on how to properly fill out google sheet.') 
        elif submit[0] == 0:
            await ctx.send(f'You have submitted {submit[0]} contributions.')
            await ctx.send(f'If you tried to submit more than {submit[0]} contributions, please make sure to fill every google sheet cell with info for each contribution.  \n\n Please fix google sheet and rerun submission command.')
        elif submit[0] == 1:
            await ctx.send(f'You have submitted {submit[0]} contribution. If you need to submit additional contributions at a later time, please clear your google sheet of the already submitted contributions and fill in the additional work only. Thank you for all the work you have done this month.')
        else:
            await ctx.send(f'You have submitted {submit[0]} contributions. If you need to submit additional contributions at a later time, please clear your google sheet of the already submitted contributions and fill in the additional work only. Thank you for all the work you have done this month.')

    @submitForm.error
    async def submitForm_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Command failed. \n Please make sure to type: !submitForm "url-of-google-sheet"')
        
    #creates new contributor sheet
    #!newContributor {discordname} {gmail} needs quotes for " name with spaces "
    @commands.command(name='newContributor')
    async def newContributor(self, ctx):
        new_contributor = data.NewUser()
        URL = new_contributor.create_spread_sheet()
        await ctx.send('Here is the monthly contribution sheet. There are 2 steps before you will be able to submit your work. \n\n 1. Please make a copy of this google sheet and store in your GoogleDrive \n 2. Share access of your google sheet with this email address: \n\n indexcontribution@indexbot-324117.iam.gserviceaccount.com \n\n {}'.format(URL))

    @newContributor.error
    async def newContributor_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Command failed. \n Please make sure to type: !newContributor')

    @commands.command(name='help')
    async def help(self, ctx):
        embed = discord.Embed(
            title = 'Submission Commands',
            description = 'List of commands for submittial bot',
            colour = discord.Colour.purple()
        )

        embed.add_field(name='!newContributor', value= '- Creates new google work sheet. \n - Command syntax: !newContributor', inline = False)
        embed.add_field(name='!submitForm (google sheet url)', value= '- Submits google sheet to database. \n - Command syntax: !submitForm (google sheet url) with no brackets', inline = False)
        embed.add_field(name='!help', value= '- Brings up list of commands', inline = False)
        embed.add_field(name='!adminHelp (Administrator only)', value= '- Displays list of Admin controls', inline = False)
        embed.set_footer(text = 'If there are any problems with the bot, please DM TeeWhy')
        
        await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        if isinstance(error, commands.CommandError):
            await ctx.send('Command not found. Please type: !help or !adminHelp for a list of all commands.')


def setup(bot):
    bot.add_cog(contributor(bot))
