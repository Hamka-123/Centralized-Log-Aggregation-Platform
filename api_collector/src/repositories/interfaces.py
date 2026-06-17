from abc import ABC, abstractmethod

class IRepository(ABC):
    @abstractmethod
    async def save(self, entity):
        pass

    @abstractmethod
    async def get_logs(self, service_name: str, level: str, limit: int):
        pass

class IServiceRepository(ABC):
    @abstractmethod
    async def add_service(self, service_name: str, description: str | None) -> int:
        pass

    @abstractmethod
    async def get_service_name_by_id(self, service_id: int) -> str | None:
        pass