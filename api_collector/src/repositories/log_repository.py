import logging
import aiomysql
from .interfaces import IRepository, IServiceRepository

logger = logging.getLogger(__name__)

class MariaDBRepository(IRepository, IServiceRepository):
    def __init__(self, connection: aiomysql.Connection):
        self.conn = connection

    async def save(self, data: dict):
        """Stores data in the database using pure SQL."""
        try:
            sql = """
                INSERT INTO logs (message, level, service_id) 
                VALUES (%s, %s, %s)
            """
            
            async with self.conn.cursor() as cursor:
                await cursor.execute(sql, (data['message'], data['level'], data['service_id']))
                
            # autocommit=True is in our config, so commit isn't needed.
            # If autocommit were False, we'd have to write: await self.conn.commit()
            
            logger.info(f"Log saved to database: {data.get('message')}")
            return True
            
        except Exception as e:
            logger.error(f"Database error: {e}")
            # Here can do await self.connection.rollback() if needed
            raise e
    
    async def get_logs(self, service_name: str = None, level: str = None, limit: int = 100):
        """Fetches logs with optional filtering."""
        # Use JOIN to get service name by ID
        query = """
            SELECT l.message, l.level, s.service_name 
            FROM logs l 
            JOIN services s ON l.service_id = s.id 
            WHERE 1=1
        """
        params = []

        if service_name:
            query += " AND s.service_name = %s"
            params.append(service_name)
        
        if level:
            query += " AND l.level = %s"
            params.append(level)
        
        query += " LIMIT %s"
        params.append(limit)

        async with self.conn.cursor(aiomysql.cursors.DictCursor) as cursor:
            await cursor.execute(query, params)
            return await cursor.fetchall()

    async def get_service_name_by_id(self, service_id: int):
        query = "SELECT service_name FROM services WHERE id = %s"
        async with self.conn.cursor(aiomysql.cursors.DictCursor) as cursor:
            await cursor.execute(query, (service_id,))
            result = await cursor.fetchone()
            return result['service_name'] if result else None
        
    async def add_service(self, service_name: str, description: str | None):
        query = "INSERT INTO services (service_name, description) VALUES (%s, %s)"
        
        async with self.conn.cursor() as cursor:
            await cursor.execute(query, (service_name, description))
            await self.conn.commit()
            return cursor.lastrowid