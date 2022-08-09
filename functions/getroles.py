from commands.roles import roles
from database import roles_handler

async def add_role(branch, roleId):
    await roles_handler.add_role(branch, roleId)

async def count_roles(table):
    data = await roles_handler.count_roles(table)
    return data

async def get_roles_value(entries_per_page, current, table):
    data = await roles_handler.get_roles_value(entries_per_page, current, table)
    return data

async def get_database_roles(table):
    data = await roles_handler.get_database_roles(table)
    return data

async def get_next_role(table, id):
    data = await roles_handler.get_next_role(table, id)
    return data[0]

async def get_first_role(table):
    data = await roles_handler.get_first_role(table)
    first_role = min(data)
    return first_role
