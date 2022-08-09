import asyncio
import math
import sqlite3
import discord
from discord.ext import commands
from discord import option
from discord.commands import slash_command
from functions import getroles

class roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @slash_command(description="Ajoute un rôle en haut de la hiérarchie")
    @option("branch", description="Paradis ou Enfers ?", choices=["Paradis", "Enfers"])
    @option("role", description="Le rôle à ajouter en haut de la hiérarchie")
    async def add_role(self, ctx, branch: str, role: discord.Role):
        try:
            await getroles.add_role(branch, role.id)
            await ctx.respond(f"Le rôle {role.name} a été ajouté au sommet de la hiérarchie avec succès")
        except sqlite3.IntegrityError:
            await ctx.respond(f"Le rôle {role.name} existe déjà dans la base de données")

    @slash_command(description="Montre la hiérarchie des rôles")
    @option("branch", description="Paradis ou Enfers ?", choices=["Paradis", "Enfers"])
    async def roles_list(self, ctx, branch: str):
        if branch == "Paradis":
            table = "pRoles"
        if branch == "Enfers":
            table = "eRoles"
        
        previous_page = 0
        current = 1
        index = 1
        entries_per_page = 10

        await ctx.respond(f"Voici les rôles pour la branche : {branch}\nLes rôles sont montrés du plus petit au plus grand hiérarchiquement (1 = plus petit)")

        embed = discord.Embed(title=f"Roles Page {current}", description="", colour=discord.Colour.gold())
        msg = await ctx.send(embed=embed)

        nb_roles = await getroles.count_roles(table)
        nb_page=math.ceil(int(nb_roles)/int(entries_per_page))

        await msg.add_reaction("⬅️")
        await msg.add_reaction("➡️")

        while True:
            if current != previous_page:
                embed.title = f"Roles page {current}"
                embed.description = ""
                embed.set_footer(text=f"page {current}/{nb_page}")

                data = await getroles.get_roles_value(entries_per_page, current, table)
                index = entries_per_page*(current-1)
                
                
                for entry in data:
                    index += 1
                    roleId, rowid = entry

                    if roleId is not None:
                        role = discord.utils.get(ctx.guild.roles, id=roleId)
                        embed.description += f"{index}) {role.mention}\n"

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
                



def setup(bot: commands.Bot):
    bot.add_cog(roles(bot))