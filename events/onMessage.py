import discord
from discord.ext import commands
from functions import levels

class onMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        if not message.author.bot:
            
            in_database = await levels.check_if_in_database(message.author.id)
            
            if in_database is True:
                channel = message.channel
                user = message.author
                guild = message.guild
                await levels.add_exp(message.author.id, user, channel, guild)
            
def setup(bot: commands.Bot):
    bot.add_cog(onMessage(bot))