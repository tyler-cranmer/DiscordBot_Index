import discord
from discord.ext import commands, tasks

import json
import os

# from discord.ext import commands
# from datetime import datetime, time, timedelta
# import asyncio

# Check to see if the path exists in the config file. 
if os.path.exists(os.getcwd() + "/config.json"):
    with open("./config.json") as f:
        configData = json.load(f)

else:
    configTemplate = {"Token": "", "Prefix": "$"}

    with open(os.getcwd() + "/config.json", "w+") as f: #created the json file
        json.dump(configTemplate, f)


token =  configData["Token"]
prefix = configData["Prefix"]

bot = commands.Bot(command_prefix=prefix)

#enable different cogs while bots running 
# !loadclog filename
@bot.command()
async def loadcog(ctx, cog):
    bot.load_extension(f"cogs.{cog}")
    await ctx.send(f"{cog} file has been enabled.")

#disable different cogs while bots running
# !unloadclog filename
@bot.command()
async def unloadcog(ctx, cog):
    bot.unload_extension(f"cogs.{cog}") 
    await ctx.send(f"{cog} file has been disabled.")
       

#loop through files in directory to load cogs.
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")


bot.run(token)

# async def on_message(message):
#     if message.author == bot.user:
#         return
        
#     if message.content.startswith('$hooty'):
#         await message.channel.send('Hoot Hoot, im here!')
#         await message.channel.send('Please copy and past your information into the contribution form below. \n\nContribution Form: \n1. [Discord Username] \n2. [Working Group Association]\n3. [Contribution sheet link] \n')
        