from os import environ
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()

bot_token = environ["TOKEN"]

bot = commands.Bot()

bot.load_extension('events.onReady')
bot.load_extension('events.onMessage')
bot.load_extension('commands.register')
bot.load_extension('commands.stats')
bot.load_extension('commands.roles')

bot.run(bot_token)