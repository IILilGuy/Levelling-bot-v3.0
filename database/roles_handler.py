from os import environ
from dotenv import load_dotenv
import aiosqlite

load_dotenv()

database = environ["DATABASE"]

async def create_table_if_not_exists():
    async with aiosqlite.connect(database) as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS eRoles (
            roleId INTEGER,
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )""")
        await db.execute("""CREATE TABLE IF NOT EXISTS pRoles (
            roleId INTEGER,
            id INTEGER PRIMARY KEY AUTOINCREMENT

        )""")
        await db.commit()

async def add_role(branch, roleId):
    async with aiosqlite.connect(database) as db:
        if branch == "Enfers":
            table = "eRoles"
        if branch == "Paradis":
            table = "pRoles"
        else:
            print("error: branch invalid")
        
        await db.execute(f"INSERT INTO {table} (roleId) VALUES (?)", (roleId,))
        await db.commit()

async def count_roles(table):
    async with aiosqlite.connect(database) as db:
        async with db.execute(f"SELECT count(*) FROM {table}") as cursor:
            data = await cursor.fetchone()
            return data[0]

async def get_roles_value(entries_per_page, current, table):
    async with aiosqlite.connect(database) as db:
        async with db.execute(f"SELECT roleId, id FROM {table} ORDER BY id LIMIT ? OFFSET ? ", (entries_per_page, entries_per_page*(current-1),)) as cursor:
            data = await cursor.fetchall()
            return data

async def get_database_roles(table):
    async with aiosqlite.connect(database) as db:
        async with db.execute(f"SELECT roleId, id FROM {table}") as cursor:
            data = await cursor.fetchall()
            return data

async def get_next_role(table, id):
    async with aiosqlite.connect(database) as db:
        async with db.execute(f"SELECT roleId FROM {table} WHERE id = ?", (id+1,)) as cursor:
            data = await cursor.fetchone()
            return data

async def get_first_role(table):
    async with aiosqlite.connect(database) as db:
        async with db.execute(f"SELECT roleId, id FROM {table}") as cursor:
            data = await cursor.fetchall()
            return data
