import discord
from discord.ext import commands
from database import levels_handler, roles_handler

class onReady(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await levels_handler.create_table_if_not_exists()
        await roles_handler.create_table_if_not_exists()
        print('ready')

def setup(bot: commands.Bot):
    bot.add_cog(onReady(bot))