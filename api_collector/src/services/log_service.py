import logging

from ..models.log_model import LogModel
from ..repositories.log_repository import IRepository

logger = logging.getLogger(__name__)
class LogService:
    def __init__(self, repository: IRepository):
        self.repository = repository

    async def process_log(self, log: LogModel):
        if self.analyze_severity(log):
            logger.info(f"{log.level} LOG DETECTED: {log.message}")
        
        log_data = {
            "message": log.message,
            "level": log.level,
            "service_id": log.service_id
        }
        
        return await self.repository.save(log_data)

    def analyze_severity(self, log: LogModel) -> bool:
        return log.level in ["ERROR", "CRITICAL"]
    
    async def get_logs(self, service_name: str = None, level: str = None, limit: int = 100):
        return await self.repository.get_logs(service_name, level, limit)
    
    async def get_service_name(self, service_id: int):
        return await self.repository.get_service_name_by_id(service_id)

    async def create_service(self, service_name: str, description: str | None):
        return await self.repository.add_service(service_name, description)