import logging

import aiomysql
from common.config import Config 

logger = logging.getLogger(__name__)

db_config = {
    'host': Config.DB_HOST,
    'port': Config.DB_PORT,
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'db': Config.DB_NAME,
    'autocommit': True  
}

db_pool = None

async def init_db_pool():
    """Initializing the connection pool when the application starts."""
    global db_pool
    db_pool = await aiomysql.create_pool(**db_config)
    logger.info("Database pool initialized successfully.")

async def close_db_pool():
    """Closing the pool when the application stops."""
    global db_pool
    if db_pool:
        db_pool.close()
        await db_pool.wait_closed()
        logger.info("Database pool closed.")

async def get_db():
    """Generator for obtaining a connection from the pool."""
    global db_pool
    async with db_pool.acquire() as conn:
        yield conn