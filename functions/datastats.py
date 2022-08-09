from database import levels_handler, stats_handler

async def count_users():
    data = await stats_handler.count_users()
    return data

async def get_leaderboard_value(entries_per_page, current):
    data = await stats_handler.get_leaderboard_value(entries_per_page, current)
    return data

async def get_guild_exp():
    data = await stats_handler.get_values()
    return data

async def get_user_exp(userId):
    data = await stats_handler.get_user_exp(userId)
    if data:
        return data[0]
    else:
        return data is None

async def get_user_lvl(userId):
    data = await stats_handler.get_user_lvl(userId)
    if data:
        return data[0]
    else:
        return data is None

async def get_user_branch(userId):
    data = await stats_handler.get_user_branch(userId)
    return data[0]