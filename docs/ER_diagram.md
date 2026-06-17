```mermaid
erDiagram
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