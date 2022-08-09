from os import environ
from dotenv import load_dotenv
import aiosqlite

load_dotenv()

database = environ["DATABASE"]

async def count_users():
    async with aiosqlite.connect(database) as db:
        async with db.execute("SELECT Count() FROM levels") as cursor:
            data = await cursor.fetchone()
            return data

async def get_leaderboard_value(entries_per_page, current):
    async with aiosqlite.connect(database) as db:
        async with db.execute("SELECT userId, lvl FROM levels ORDER BY exp DESC LIMIT ? OFFSET ?", (entries_per_page, entries_per_page*(current-1),)) as cursor:
            data = await cursor.fetchall()
            return data

async def get_values():
    async with aiosqlite.connect(database) as db:
        async with db.execute("SELECT exp FROM levels") as cursor:
            data = await cursor.fetchall()
            return data

async def get_user_exp(userId):
    async with aiosqlite.connect(database) as db:
        async with db.execute("SELECT exp FROM levels WHERE userId = ?", (userId,)) as cursor:
            data = await cursor.fetchone()
            return data

async def get_user_lvl(userId):
    async with aiosqlite.connect(database) as db:
        async with db.execute("SELECT lvl FROM levels WHERE userId = ?", (userId,)) as cursor:
            data = await cursor.fetchone()
            return data

async def get_user_branch(userId):
    async with aiosqlite.connect(database) as db:
        async with db.execute("SELECT branch FROM levels WHERE userId = ?", (userId,)) as cursor:
            data = await cursor.fetchone()
            return data
