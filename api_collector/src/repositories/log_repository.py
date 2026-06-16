import logging
import aiomysql
from .interfaces import IRepository

logger = logging.getLogger(__name__)

class MariaDBRepository(IRepository):
    # Теперь мы принимаем соединение (connection) вместо Session
    def __init__(self, connection: aiomysql.Connection):
        self.conn = connection

    async def save(self, data: dict):
        """Stores data in the database using pure SQL."""
        try:
            # Важно: В aiomysql используем %s, а не :param
            sql = """
                INSERT INTO logs (message, level, service_id) 
                VALUES (%s, %s, %s)
            """
            
            # Создаем курсор
            async with self.conn.cursor() as cursor:
                # Выполняем запрос
                await cursor.execute(sql, (data['message'], data['level'], data['service_id']))
                
            # autocommit=True у нас в конфиге, поэтому commit не нужен.
            # Если бы autocommit был False, нужно было бы писать: await self.conn.commit()
            
            logger.info(f"Log saved to database: {data.get('message')}")
            return True
            
        except Exception as e:
            # Если что-то пошло не так, логируем ошибку
            logger.error(f"Database error: {e}")
            # Здесь можно сделать await self.conn.rollback(), если нужно
            raise e