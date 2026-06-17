import time
import pymysql
import logging
from common.config import Config

logger = logging.getLogger(__name__)

def get_db_connection():
    max_retries = 5
    retry_delay = 5 

    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to connect to DB (attempt {attempt + 1}/{max_retries})...")
            conn = pymysql.connect(
                host=Config.DB_HOST,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD,
                database=Config.DB_NAME,
                charset='utf8mb4',
                port=Config.DB_PORT,
                connect_timeout=5
            )
            logger.info("Database connection established successfully!")
            return conn
        except (pymysql.OperationalError, ConnectionRefusedError) as e:
            logger.warning(f"Connection failed: {e}. Retrying in {retry_delay}s...")
            time.sleep(retry_delay)
    
    raise Exception("Could not connect to database after multiple retries.")