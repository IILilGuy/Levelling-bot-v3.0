from os import environ
from dotenv import load_dotenv
import aiosqlite

load_dotenv()

database = environ["DATABASE"]

async def create_table_if_not_exists():
    async with aiosqlite.connect(database) as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS levels (
            userId INTEGER PRIMARY KEY NOT NULL,
            exp INTEGER DEFAULT 0,
            lvl INTEGER DEFAULT 0,
            branch STRING 
        )""")
        await db.commit()

async def get_every_users():
    async with aiosqlite.connect(database) as db:
        async with db.execute("SELECT userId FROM levels") as cursor:
            data = await cursor.fetchall()
            return data

async def add_new_user(userId, branch):
    async with aiosqlite.connect(database) as db:
        await db.execute("INSERT INTO levels (userId, branch) VALUES (?,?)", (userId, branch))
        await db.commit()

async def remove_user(userId):
    async with aiosqlite.connect(database) as db:
        await db.execute(f"DELETE FROM levels WHERE userId = ?", (userId,))
        await db.commit()

async def add_exp(userId):
    async with aiosqlite.connect(database) as db:
        await db.execute("UPDATE levels SET exp = exp + 1 WHERE userId = ?", (userId,))
        await db.commit()

async def select_exp(userId):
    async with aiosqlite.connect(database) as db:
        async with db.execute("SELECT exp FROM levels WHERE userId = ?", (userId,)) as cursor:
            data = await cursor.fetchone()
            return data

async def lvl_up(level, userId):
    async with aiosqlite.connect(database) as db:
        await db.execute("UPDATE levels SET lvl = ? WHERE userId = ?", (level, userId))
        await db.commit()