```mermaid
---
title: Data Flow Architecture
---

graph TD
    subgraph Sources["Log Sources"]
        Auth["Auth Service"]
        Billing["Billing Service"]
        Gateway["Gateway Service"]
    end

    subgraph API_System["API Collector"]
        API["POST /logs"]
        Val["Pydantic Validator"]
        Repo["Repository Layer"]
    end

    subgraph Storage["Database"]
        DB[("MariaDB")]
    end

    subgraph Alerting["Alerting Worker"]
        Worker["Alerting Worker"]
        SMTP["SMTP Server / Email"]
    end

    %% Data flows
    Auth -->|POST /logs| API
    Billing -->|POST /logs| API
    Gateway -->|POST /logs| API

    API --> Val
    Val --> Repo
    Repo --> DB

    Worker -.->|Poll / Check| DB
    Worker -->|Send Alert| SMTP