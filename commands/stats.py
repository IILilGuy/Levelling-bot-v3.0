import asyncio
import math
import discord
from discord import option
from discord.ext import commands
from discord.commands import slash_command
from functions import datastats

class stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Montre le leaderboard du serveur")
    async def leaderboard(self, ctx):

        previous_page = 0
        current = 1
        index = 1
        entries_per_page = 10

        ctx.respond("Voici le leaderboard:")

        embed = discord.Embed(title=f"Leaderboard Page {current}", colour=discord.Colour.gold())
        msg = await ctx.send(embed=embed)
        
        await msg.add_reaction("⬅️")
        await msg.add_reaction("➡️")

        nb_user = await datastats.count_users()
        nb_page = math.ceil(nb_user[0]/entries_per_page)

        while True:
            if current != previous_page:
                embed.title = f"Leaderboard Page {current}"
                embed.description = ""
                embed.set_footer(text=f"page {current}/{nb_page}")

                data = await datastats.get_leaderboard_value(entries_per_page, current)
                index = entries_per_page*(current-1)

                for entry in data:
                    index += 1
                    userId, lvl = entry
                    user = await self.bot.fetch_user(userId)
                    embed.description += f"{index}) {user.mention}: **level {lvl}**\n"

                await msg.edit(embed=embed)

            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author, timeout=60.0)

            except asyncio.exceptions.TimeoutError:
                await msg.clear_reactions()
            
            else:
                previous_page = current
                if reaction.emoji == "⬅️" and current !=1:
                    current -= 1
                if reaction.emoji == "➡️" and current != nb_page:
                    current += 1
                await msg.remove_reaction(reaction.emoji, ctx.author)


    @slash_command(description="Montre les stats de l'utilisateur donné.")
    @option("user",
            description="L'utilisateur dont je dois afficher les données. Par défaut: l'auteur de la commande",
            required=False)

    async def stats(self, ctx, user: discord.Member):
        if not user:
            user = ctx.author

        userId = user.id
        
        data = await datastats.get_user_exp(userId)
        
        if data is not True:
            exp = data

            guild_data = await datastats.get_guild_exp()
            lvl = math.sqrt(exp)//1
            rank = 1
            
            for value in guild_data:
                if exp < value[0]:
                    rank += 1

            current_lvl_exp = (1*(lvl))**2
            next_lvl_exp = (1*(lvl+1))**2

            lvl_percentage = ((exp-current_lvl_exp) /
                            (next_lvl_exp-current_lvl_exp)) * 100

            embed = discord.Embed(
            title=f"Stats for {user.name}", colour=discord.Colour.gold())
            embed.add_field(name="Level", value=int(lvl))
            embed.add_field(name="Exp", value=f"{exp}/{int(next_lvl_exp)}")
            embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}")
            embed.add_field(name="Level Progress", value=f"{round(lvl_percentage, 2)}%")

            await ctx.respond(embed=embed)
        else:
            embed=discord.Embed(title="Vous n'êtes pas dans la base de données", description="Utilisez la commande `/Register` pour commencer l'aventure !")
            await ctx.respond(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(stats(bot))