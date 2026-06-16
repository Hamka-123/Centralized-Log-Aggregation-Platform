from ..models.log_model import LogModel
from ..repositories.log_repository import IRepository

class LogService:
    def __init__(self, repository: IRepository):
        self.repo = repository

    async def process_log(self, log: LogModel):
        if self.analyze_severity(log):
            print(f"CRITICAL LOG DETECTED: {log.message}")
        
        log_data = {
            "message": log.message,
            "level": log.level,
            "service_id": log.service_id
        }
        
        # ДОБАВИЛИ await
        # Именно здесь, если забыть log_data, будет ошибка missing argument
        return await self.repo.save(log_data)

    def analyze_severity(self, log: LogModel) -> bool:
        return log.level in ["ERROR", "CRITICAL"]
    
    async def get_logs(self, service_name: str = None, level: str = None, limit: int = 100):
        return await self.repo.get_logs(service_name, level, limit)
    
    async def get_service_name(self, service_id: int):
        return await self.repo.get_service_name_by_id(service_id)