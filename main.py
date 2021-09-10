import discord
from discord.ext import commands
import json
import os
import sqlite3
import data 

# from discord.ext import commands
# from datetime import datetime, time, timedelta
# import asyncio

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


# turn off messages from guilds, so you only get messages from DM channels
my_intents = discord.Intents.default()
my_intents.guild_messages = False 
# optionally turn on members or presences here if you need them
bot = commands.Bot(command_prefix=prefix, intents=my_intents)
bot.remove_command('help') 




if __name__ == '__main__':

    db = 'index_contribution.db'
    # data.DB.create(db)
    # m = data.MasterControls()
    # m.collectAllOwlIDs()



    @bot.event
    async def on_ready():
        print('Hooty and the bot is ready.')
        await bot.change_presence(activity= discord.Game(name=f"{prefix} - prefix"))
        bot.load_extension("cogs.events")
        bot.load_extension("cogs.admin")


    bot.run(token)