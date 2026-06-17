```mermaid
graph TD
    subgraph "Producer Layer"
        Client[API Client] -->|1. HTTP POST| Collector[API Collector]
        Collector -->|2. INSERT logs<br/>processed=0| DB_Logs[(MariaDB: logs)]
    end

    subgraph "Queue & Persistence"
        DB_Logs
    end

    subgraph "Consumer Layer (Multi-threaded)"
        Worker[Alerting Worker ThreadPool] -->|3. SELECT logs<br/>WHERE processed=0| DB_Logs
        Worker -->|4. UPDATE logs<br/>SET processed=1| DB_Logs
        Worker -->|5. Send Email| SMTP[SMTP Server]
        Worker -->|6. INSERT alerts| DB_Alerts[(MariaDB: alerts)]
    end

    style DB_Logs fill:#f9f,stroke:#333,stroke-width:2px
    style Worker fill:#bbf,stroke:#333,stroke-width:2px