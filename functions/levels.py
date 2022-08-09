import asyncio
import math
import discord
from functions import datastats
from database import levels_handler
from functions import getroles

async def add_new_user(userId, branch):
    await levels_handler.add_new_user(userId, branch)
    print(f"registered new user : {userId}\nbranch : {branch}")

async def check_if_in_database(userId):
    users = await levels_handler.get_every_users()
    for user in users:
        if userId == user[0]:
            in_database = True
            return in_database
        break

async def remove_user(userId):
    await levels_handler.remove_user(userId)

async def add_exp(userId, user, channel, guild):
    await levels_handler.add_exp(userId)
    await check_if_lvl_up(userId, user, channel, guild)

async def check_if_lvl_up(userId, user, channel, guild):
    exp = await levels_handler.select_exp(userId)
    if exp:
        level = math.sqrt(exp[0]) / 1

        if level.is_integer():
            await lvl_up(userId, user, level, channel, guild)

async def lvl_up(userId, user, level, channel, guild):
    await levels_handler.lvl_up(level, userId)

    msg = await channel.send(f"Bien joué {user.name}, tu viens de passer au niveau {int(level)} !")
    
    await check_if_has_role_to_assign(userId, channel, guild, user)
    
    await asyncio.sleep(3)
    await msg.delete()

    

async def check_if_has_role_to_assign(userId, channel, guild, user):
    lvl = await datastats.get_user_lvl(userId)
    
    if lvl != 0:
        if (lvl % 5 == 0):
            await assign_role(userId, channel, guild, user)
        else:
            return

async def assign_role(userId, channel, guild, user):
    branch = await datastats.get_user_branch(userId)

    if branch == "Paradis":
        table = "pRoles"
    if branch == "Enfers":
        table = "eRoles"

    every_roles = await getroles.get_database_roles(table)

    for entry in every_roles:
        role_id, id = entry
        role = discord.utils.get(guild.roles, id=role_id)

        if role in user.roles:
            next_role = await getroles.get_next_role(table, id)
            role_to_remove = role
            role_to_add = discord.utils.get(guild.roles, id = next_role)

            if role_to_remove != None and role_to_add != None:
                try:
                    await user.remove_roles(role_to_remove)
                    await user.add_roles(role_to_add)
                    msg = await channel.send(f"Bravo {user.name} ! Je t'ai donné le rôle {role_to_add.name} et je t'ai enlevé ton ancien rôle {role_to_remove.name} !")
                    await asyncio.sleep(3)
                    await msg.delete()

                except discord.errors.Forbidden:
                    await channel.send(f"Oups {user.mention}, il semblerait qu'il y ait un rôle assigné à ton level ({role_to_add.name}) mais je n'ai pas les permissions pour te le donner !")
                    await user.add_roles(role_to_remove)
            break
