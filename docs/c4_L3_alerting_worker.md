C4Component
    title C4 Level 3: Alerting Worker Components

    Container_Boundary(worker, "Alerting Worker") {
        Component(ctrl, "Worker Controller", "Orchestrator", "Manages lifecycle and threading")
        Component(fetcher, "Data Fetcher", "Data Access", "Fetches logs from database")
        Component(engine, "Alert Engine", "Logic", "Business logic and spam protection")
        Component(smtp, "SMTP Client", "Gateway", "Encapsulates email sending")
    }

    ContainerDb(db, "Database", "MariaDB")
    System_Ext(smtp_srv, "SMTP Server", "External mail service")

    Rel(ctrl, fetcher, "Initiates polling")
    Rel(ctrl, engine, "Passes logs for analysis")
    Rel(fetcher, db, "SELECT/UPDATE")
    Rel(engine, smtp, "Email sending trigger")
    Rel(smtp, smtp_srv, "SMTP Protocol")

    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="1")