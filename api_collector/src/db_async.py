import aiomysql
from common.config import Config # Import the centralized Config class

# Configuration for the database pool using the Config class
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
    # Create the pool using the updated configuration
    db_pool = await aiomysql.create_pool(**db_config)
    print("Database pool initialized successfully.")

async def close_db_pool():
    """Closing the pool when the application stops."""
    global db_pool
    if db_pool:
        db_pool.close()
        await db_pool.wait_closed()
        print("Database pool closed.")

async def get_db():
    """Generator for obtaining a connection from the pool."""
    global db_pool
    async with db_pool.acquire() as conn:
        yield conn