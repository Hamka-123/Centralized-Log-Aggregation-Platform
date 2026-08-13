# Centralized Log Aggregation Platform

A modular centralized logging and alerting platform for collecting, storing, processing, and monitoring logs from multiple services.

The project combines a REST API, background alerting worker, persistent storage, containerized infrastructure, automated testing, and operational tooling.

**[View the project presentation →](https://docs.google.com/presentation/d/1B59gownHOBTjBwzCm44b97DK2W8WGQQBjBd0s5iSMgQ/edit?slide=id.p1)**

---

## 🚀 What It Does

- Collects logs from multiple services through a REST API
- Validates and stores log entries in MariaDB
- Detects `ERROR` and `CRITICAL` events
- Sends automated email alerts through SMTP
- Provides health checks and operational logging
- Runs API and background processing as separate services
- Supports graceful worker shutdown
- Includes automated testing and load-testing capabilities
- Provides Docker-based local deployment and infrastructure validation

---

## 🏗️ Architecture

```text
                  ┌─────────────────────┐
                  │   Source Services   │
                  │                     │
                  │ Auth / Billing /     │
                  │ Gateway / Other     │
                  └──────────┬──────────┘
                             │
                             │ POST /api/logs
                             ▼
                  ┌─────────────────────┐
                  │    API Collector    │
                  │       FastAPI       │
                  └──────────┬──────────┘
                             │
                             │ Store logs
                             ▼
                  ┌─────────────────────┐
                  │       MariaDB       │
                  └──────────┬──────────┘
                             │
                             │ Process logs
                             ▼
                  ┌─────────────────────┐
                  │   Alerting Worker   │
                  │      Python         │
                  └──────────┬──────────┘
                             │
                             │ Email alerts
                             ▼
                  ┌─────────────────────┐
                  │     SMTP Server     │
                  └─────────────────────┘
````

The system is intentionally split into independently deployable components:

* **API Collector** — asynchronous FastAPI service responsible for log ingestion and retrieval
* **Alerting Worker** — background service responsible for detecting alertable logs and sending notifications
* **MariaDB** — persistent storage for services, logs, and alert state

Detailed architecture and design decisions are documented in [`docs/`](docs/).

---

## 🛠️ Technology Stack

### Application

* Python 3.11+
* FastAPI
* Pydantic
* aiomysql

### Infrastructure

* Docker
* Docker Compose
* Bash
* Linux

### Database

* MariaDB
* SQL
* Indexed relational schema

### Testing

* pytest
* Unit testing
* API testing
* Integration testing
* Infrastructure testing
* Load testing

### Engineering Practices

* Layered architecture
* Repository Pattern
* Service Layer
* Gateway Pattern
* Dependency Injection
* Graceful shutdown
* Health checks
* Environment-based configuration
* Infrastructure validation

---

## 🚀 Quick Start

### Prerequisites

* Docker
* Docker Compose
* Git

### Start the Platform

Create the environment configuration:

```bash
cp .env_template .env
```

Start all services:

```bash
docker compose up -d --build
```

Check service status:

```bash
docker compose ps
```

Verify the API:

```bash
curl http://localhost:8000/health
```

API documentation:

```text
http://localhost:8000/docs
```

View logs:

```bash
docker compose logs -f
```

Stop the platform:

```bash
docker compose down
```

---

## 🧪 Testing

The project uses a layered testing approach covering application logic, API behavior, service integration, infrastructure, and performance.

```text
Unit
  ↓
API
  ↓
Integration
  ↓
Infrastructure
  ↓
Load Testing
```

Install test dependencies:

```bash
pip install -r tests/requirements.txt
```

Run the test suite:

```bash
pytest tests/ -v
```

Detailed testing strategy and execution instructions are available in the [`tests/README.md`](tests/README.md).

For performance testing, see the [Load Testing Guide](tests/load_tests/client_simulator/README.md).

---

## 📚 Documentation

### Architecture

* [C4 Level 1 — System Context](docs/c4_L1.md)
* [C4 Level 2 — Container Architecture](docs/c4_L2.md)
* [C4 Level 3 — API Collector](docs/c4_L3_api_collector.md)
* [C4 Level 3 — Alerting Worker](docs/c4_L3_alerting_worker.md)
* [Entity-Relationship Diagram](docs/ER_diagram.md)
* [Data Flow](docs/data_flow.md)
* [Infrastructure](docs/infra.md)

### Project Documentation

* [Project Presentation](https://docs.google.com/presentation/d/1B59gownHOBTjBwzCm44b97DK2W8WGQQBjBd0s5iSMgQ/edit?slide=id.p1)
* [Full Project Documentation](https://docs.google.com/document/d/1ZYanmctLJ1nQAkrA3QUProKJxsqcL_bCVbXhCCZKYlA/edit?usp=sharing)
* [Testing Guide](tests/README.md)
* [Load Testing Guide](tests/load_tests/client_simulator/README.md)
* [Implementation Checklist](TODO.md)

---

## 📁 Repository Structure

```text
Centralized-Log-Aggregation-Platform/
│
├── api_collector/        # FastAPI log ingestion service
├── alerting_worker/      # Background alerting service
├── common/               # Shared configuration and logging
├── db/                   # Database initialization
├── scripts/              # Operational and infrastructure scripts
├── tests/                # Automated and load tests
├── docs/                 # Architecture and design documentation
│
├── docker-compose.yml
├── .env_template
└── TODO.md
```

---

## 🔄 Engineering Approach

The project explores the complete engineering lifecycle around a small distributed system:

**Design → Build → Containerize → Test → Operate → Investigate → Improve**

The focus is not only on implementing the application itself, but on combining application architecture, infrastructure, testing, automation, and operational practices into one reproducible engineering environment.

```
