graph TD
    subgraph Host [Docker Host]
        subgraph Network [Docker Bridge Network: app-network]
            API[api_collector]
            Worker[alerting_worker]
            DB[(db: MariaDB)]
        end
        
        subgraph Storage [Volumes]
            DB_Data[(db-data)]
        end
    end

    %% External Access
    Internet((External Sources / Client)) -->|HTTP: 8000| API

    %% Interactions
    API -->|SQL Query| DB
    Worker -->|SQL Query| DB
    
    %% Data Persistence
    DB -.->|Persistent Mount| DB_Data

    %% Management (Lifecycle)
    Scripts[Automation Scripts: build/start/redeploy] -.->|Orchestration| Host