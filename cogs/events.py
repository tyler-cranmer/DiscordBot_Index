import discord
from discord.ext import commands

#This class is turned on while the bot is NOT accepting submission.
class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.startswith('!help'):
            await message.channel.send('Submissions for this month are currently closed. Please check back with me during the last week of every month for instructions to submit your contribution form.')


def setup(bot):
    bot.add_cog(Events(bot))