from sqlite3 import IntegrityError
import discord
from discord.ext import commands
from discord import option
from discord.commands import slash_command
from discord.utils import get
from functions import getroles, levels

class register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(description="Enregistre toi et commence l'aventure")
    @option("branch", description="Paradis ou Enfers ?", choices=["Paradis", "Enfers"])
    async def register(self, ctx, branch: str):
        if branch == "Paradis":
            table = "pRoles"
        if branch == "Enfers":
            table = "eRoles"
        
        roleId = await getroles.get_first_role(table)
        first_role = discord.utils.get(ctx.guild.roles, id=roleId[0])
        user = ctx.author

        try:
            await levels.add_new_user(ctx.author.id, branch)
            await user.add_roles(first_role)
            await ctx.respond(f"Vous avez été enregistré dans la base de données avec succès. Votre branche : {branch}")
        
        except IntegrityError:
            await ctx.respond(f"{ctx.author.name}, vous êtes déjà présent dans la base de données")

        except discord.errors.Forbidden:
            await ctx.respond(f"{ctx.author.name}, je n'ai pas pu vous enregistrer car je n'ai pas la permission de vous donner le premier rôle.")

    @slash_command(description="Retire toi de la base de données et arrête l'aventure")
    async def unregister(self, ctx):
        await levels.remove_user(ctx.author.id)
        await ctx.respond(f"{ctx.author.name}, vous avez été retiré de la base de données avec succès")
        # Eventuellement rajouter le retrait des rôles de la base de données

def setup(bot: commands.Bot):
    bot.add_cog(register(bot))