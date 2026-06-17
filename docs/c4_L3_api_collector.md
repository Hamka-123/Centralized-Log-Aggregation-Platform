```mermaid
C4Component
    title Level 3: API Collector Components

    Container_Boundary(api_collector, "API Collector") {
        Component(router, "API Router", "FastAPI Endpoints", "Entry point, handles HTTP requests")
        Component(model, "Log Model", "Pydantic", "Data contract and auto-validation")
        Component(service, "Log Service", "Business Logic", "Orchestration and decision making")
        Component(repo, "Log Repository", "Data Access Layer", "Database abstraction, SQL execution")
    }

    ContainerDb(db, "Database", "MariaDB", "Log storage")
    Person(user, "Client/Microservice", "Log source")

    %% Data flows
    Rel(user, router, "POST /logs", "HTTP JSON")
    Rel(router, model, "Validate", "Pydantic")
    Rel(router, service, "Delegate", "Business Logic")
    Rel(service, repo, "Save/Fetch", "Interface")
    Rel(repo, db, "SQL INSERT/SELECT", "SQL")

    %% Annotations
    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="1")