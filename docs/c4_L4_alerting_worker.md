```mermaid
classDiagram
    %% Classes and their responsibilities
    class WorkerLoop {
        -repo: LogRepository
        -alertEngine: AlertEngine
        +start() void
        -run_loop() void
    }

    class LogRepository {
        +fetch_unprocessed_logs() List~Log~
        +mark_as_processed(ids: List) void
    }

    class AlertEngine {
        -notifier: INotificationClient
        +analyze_and_alert(logs: List~Log~) void
        -should_alert(log: Log) bool
    }

    class INotificationClient {
        <<interface>>
        +send(subject: str, body: str) void
    }

    class SMTPClient {
        -config: dict
        +send(subject: str, body: str) void
    }

    %% Relationships
    WorkerLoop --> LogRepository : uses (DI)
    WorkerLoop --> AlertEngine : uses (DI)
    AlertEngine --> INotificationClient : composition
    SMTPClient ..|> INotificationClient : implements

    %% Explanations for relationships
    note for WorkerLoop "Manages timing and lifecycle"
    note for AlertEngine "Business logic for filtering and decision making"
    note for SMTPClient "Implements email sending via SMTP protocol"