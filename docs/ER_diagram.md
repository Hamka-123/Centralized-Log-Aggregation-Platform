```mermaid
erDiagram
    direction LR
    services ||--o{ logs : "generates"
    logs ||--o{ alerts : "triggers"

    services {
        int id PK "AUTO_INCREMENT"
        varchar(100) service_name "UNIQUE, NOT NULL"
        text description
    }

    logs {
        int id PK "AUTO_INCREMENT"
        int service_id FK
        varchar(10) level
        text message
        timestamp created_at
        tinyint processed "DEFAULT 0"
    }

    alerts {
        int id PK "AUTO_INCREMENT"
        int log_id FK
        varchar(50) status
        varchar(255) recipient
        timestamp sent_at
    }

```

Notes:
- Indexes implemented in `db/init.sql` for performance:
    - `idx_service_level (service_id, level)` — accelerate queries filtering by service and level.
    - `idx_created_at (created_at)` — used by retention/cleanup operations.
    - `idx_processed_level (processed, level)` — optimizes worker selection of unprocessed error logs.
- Alerts foreign key: `alerts.log_id` references `logs.id` with `ON DELETE CASCADE` (alerts are removed when the related log is deleted).
- Retention policy: stored procedure `sp_cleanup_logs()` removes logs older than 30 days; a scheduled event `purge_old_logs` calls it daily at ~03:00 (configured in `db/init.sql`).
