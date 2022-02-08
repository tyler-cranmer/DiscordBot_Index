import discord
from discord.ext import commands
import json
import os
import datetime
from data.database import DB
from data.sheets import MasterControls


# Check to see if the path exists in the config file. 
if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {"Token": "", "Prefix": "!"}

    with open(os.getcwd() + "/config.json", "w+") as f: #created the json file
        json.dump(configTemplate, f)


token =  configData["Token"]
prefix = configData["Prefix"]

db_name = configData["database_name"]

# turn off messages from guilds, so you only get messages from DM channels
my_intents = discord.Intents.default()
my_intents.guild_messages = False 
# optionally turn on members or presences here if you need them
bot = commands.Bot(command_prefix=prefix, intents=my_intents)
bot.remove_command('help') 




if __name__ == '__main__':

    DB.create(db_name)

    @bot.event
    async def on_ready():
        date = datetime.datetime.now()
        print(f'Hooty and the bot is ready. {date}')
        await bot.change_presence(activity= discord.Activity(type=discord.ActivityType.custom, name='for Submissions || !help'))
        bot.load_extension("cogs.events")
        bot.load_extension("cogs.admin")


    bot.run(token)