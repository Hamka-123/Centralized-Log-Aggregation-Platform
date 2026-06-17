import os
import aiomysql
from dotenv import load_dotenv

load_dotenv()

db_config = {
    'host': os.getenv("DB_HOST"),
    'port': int(os.getenv("DB_PORT", "3306")),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'db': os.getenv("DB_NAME"),
    'autocommit': True  
}

db_pool = None

async def init_db_pool():
    """Initializing the connection pool when the application starts."""
    global db_pool
    db_pool = await aiomysql.create_pool(**db_config)

async def close_db_pool():
    """Closing the pool when the application stops."""
    global db_pool
    if db_pool:
        db_pool.close()
        await db_pool.wait_closed()

async def get_db():
    """
    A generator for obtaining a connection from the pool.
    """
    global db_pool
    async with db_pool.acquire() as conn:
        yield conn