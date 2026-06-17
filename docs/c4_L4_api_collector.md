```mermaid
classDiagram
    %% Classes and their roles
    class LogController {
        -service: LogService
        +create_log(log: LogModel)
    }

    class LogModel {
        <<pydantic>>
        +service_name: str
        +level: str
        +message: str
    }

    class LogService {
        -repo: IRepository
        +process_log(log: LogModel)
        -analyze_severity(log: LogModel)
    }

    class IRepository {
        <<interface>>
        +save(log: LogModel)
    }

    class MariaDBRepository {
        +save(log: LogModel)
    }

    %% Relationships
    LogController --> LogService : uses (DI)
    LogController --> LogModel : validates
    LogService --> IRepository : composition / uses (DIP)
    MariaDBRepository ..|> IRepository : implements

    %% Explanatory notes
    note for LogController "Thin controller: HTTP and validation only"
    note for LogService "Business logic: classification and decision making"
    note for IRepository "Abstraction: hides database details (Repository Pattern)"