```mermaid
classDiagram
    %% API Layer (api/api_router.py)
    class APIRouter {
        +post_log(log: LogModel)
        +get_logs(service_name, level, limit)
        -service: LogService
    }

    %% Models (models/)
    class LogModel {
        <<pydantic>>
        +service_name: str
        +level: str
        +message: str
    }
    
    class ServiceModel {
        <<pydantic>>
        +service_name: str
        +description: str
    }

    %% Service Layer (services/log_service.py)
    class LogService {
        -repo: ILogRepository
        +create_log(log: LogModel)
        +list_logs(filters)
    }

    %% Repository Layer (repositories/)
    class ILogRepository {
        <<interface>>
        +save(log: LogModel)
        +find_all(filters)
    }

    class MariaDBLogRepository {
        +save(log: LogModel)
        +find_all(filters)
        -db_session: AsyncSession
    }

    %% Relationships
    APIRouter --> LogService : uses
    LogService --> ILogRepository : depends on (DIP)
    MariaDBLogRepository ..|> ILogRepository : implements
    
    APIRouter ..> LogModel : receives/validates
    LogService ..> LogModel : processes
    APIRouter ..> ServiceModel : manages

    %% Notes
    note for APIRouter "api_router.py: FastAPI Endpoints"
    note for LogService "log_service.py: Business logic"
    note for MariaDBLogRepository "log_repository.py: SQLAlchemy/AsyncIO"