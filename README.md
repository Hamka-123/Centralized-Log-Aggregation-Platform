# Centralized Log Aggregation Platform

An enterprise-grade system designed for collecting, storing, analyzing, and alerting on logs from various sources. The platform is built as a modular Python application with containerized microservices, featuring a REST API for log ingestion and an asynchronous worker for automated alerting.

---

## 📋 Overview

The **Centralized Log Aggregation Platform** provides:
- **Log Collection**: RESTful API for ingesting logs from multiple services
- **Log Storage**: Persistent MariaDB database with optimized schema
- **Alert Generation**: Automated detection and alerting for ERROR and CRITICAL level logs
- **Email Notifications**: SMTP-based alert delivery to administrators
- **Health Monitoring**: Built-in health check endpoints for container orchestration
- **Request Logging**: Automatic logging of every HTTP request with method, path, status code and duration
- **Graceful Shutdown**: Worker handles SIGTERM/SIGINT, waits for in-flight tasks before exiting
- **Modular Architecture**: Cleanly separated API Collector and Alerting Worker services

---

## 🏗️ System Architecture

The platform consists of three main services:

1. **API Collector** (FastAPI)
   - RESTful API service for log ingestion
   - Log filtering and retrieval endpoints
   - Health check endpoint
   - Database abstraction layer

2. **Alerting Worker** (Python Worker)
   - Background service for processing unalerted logs
   - Detects ERROR and CRITICAL level entries
   - Sends email notifications via SMTP
   - Marks processed alerts in the database

3. **Database** (MariaDB)
   - Persistent data storage
   - Optimized schema with indexes for high-volume queries
   - Support for multiple services and alert tracking

---

## 📁 Project Structure

```
Centralized-Log-Aggregation-Platform/
├── api_collector/          # FastAPI application for log collection
│   ├── src/
│   │   ├── main.py        # FastAPI app, lifespan, middleware wiring
│   │   ├── db_async.py    # Async connection pool (aiomysql)
│   │   ├── api/           # HTTP route handlers
│   │   ├── middleware/    # Request logging middleware
│   │   ├── models/        # Pydantic data contracts
│   │   ├── repositories/  # Data access layer (Repository Pattern)
│   │   └── services/      # Business logic
│   ├── Dockerfile
│   └── requirements.txt
│
├── alerting_worker/        # Background worker for alert generation
│   ├── src/
│   │   ├── main.py        # Worker entry point, dependency injection
│   │   ├── db_sync.py     # Synchronous DB connection with retry
│   │   ├── repositories/  # Data access layer
│   │   ├── services/      # Alert engine, business logic
│   │   ├── utils/         # SMTP client (Gateway pattern)
│   │   └── workers/       # Worker controller (ThreadPoolExecutor)
│   ├── Dockerfile
│   └── requirements.txt
│
├── common/                 # Shared modules
│   ├── config.py          # Environment config (12-factor)
│   └── logging_setup.py   # Centralized logging setup
│
├── db/                     # Database configuration
│   ├── init.sql          # Schema initialization script
│   └── Dockerfile        # MariaDB custom image
│
├── scripts/                # Utility scripts
│   ├── start.sh          # Start services
│   ├── stop.sh           # Stop services
│   ├── build.sh          # Build Docker images
│   ├── redeploy.sh       # Redeploy services
│   ├── run_pipeline.sh   # Full pipeline execution
│   ├── check_infra.sh    # Infrastructure validation
│   ├── wait-for-it.sh    # Service dependency waiting
│   └── debug_db.py       # Database debugging utility
│
├── tests/                  # Comprehensive test suite
│   ├── unit/             # Unit tests
│   ├── api/              # API integration tests
│   ├── integration/      # End-to-end tests
│   ├── infra/            # Infrastructure tests
│   ├── load_tests/       # Load testing (client swarm, reports)
│   └── README.md         # Testing documentation
│
├── docs/                   # Architecture and design documentation
│   ├── c4_L1.md          # C4 Context diagram
│   ├── c4_L2.md          # C4 Container diagram
│   ├── c4_L3_*.md        # C4 Component diagrams
│   ├── c4_L4_*.md        # C4 Code diagrams
│   ├── ER_diagram.md     # Entity-Relationship diagram
│   ├── data_flow.md      # Data flow documentation
│   └── infra.md          # Infrastructure documentation
│
├── docker-compose.yml      # Docker Compose orchestration
├── .env_template          # Environment variables template
└── TODO.md                # Implementation checklist
```

---

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose (recommended)
- Python 3.11+ (for local development)
- Git

### Setup Instructions

#### 1. Environment Configuration
Before launching, duplicate `.env_template` as `.env` and populate the required variables:

```bash
cp .env_template .env
```

#### 2. Deployment Methods

**Method 1: Docker Compose (Recommended for Development)**

The recommended way using Docker Compose, which automatically handles networking, service dependencies, and environment variables:

```bash
docker compose up -d --build db api_collector alerting_worker
```

**Method 2: Manual Build (CI/CD / Production)**

For specific image build stages or production deployments, use the provided scripts:

```bash
# Build images
./scripts/build.sh

# Start services
./scripts/start.sh

# Stop services
./scripts/stop.sh

# Full redeploy with cleaning cache
./scripts/redeploy.sh

# Run full pipeline with tests
./scripts/run_pipeline.sh
```

#### 3. Verify Deployment

Check service health:

```bash
# API Collector health
curl http://localhost:8000/health

# Check logs
docker compose logs -f api_collector
docker compose logs -f alerting_worker
docker compose logs -f db
```

---

## 📡 API Documentation

### Base URL
```
http://localhost:8000/docs
```

### Endpoints

#### Health Check
```http
GET /health
```

#### Register a Service
```http
POST /api/services/register
Content-Type: application/json

{
  "service_name": "my-service",
  "description": "My microservice"
}
```

#### Get Service Name
```http
GET /api/services/{service_id}
```

#### Submit Log Entry
```http
POST /api/logs
Content-Type: application/json

{
  "service_id": 1,
  "level": "ERROR",
  "message": "Connection timeout"
}
```

#### Retrieve Logs
```http
GET /api/logs?service_name=my-service&level=ERROR&limit=100
```
---

## ⚙️ Configuration

### Logging Configuration

The application uses Python's standard logging with both console and file output:

```python
# Log Levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
# Minimum level: INFO
# Format: [timestamp] [level] [logger_name]: message
```

---

## 🧪 Testing

The project includes a comprehensive test suite with multiple layers:

- **Unit Tests**: Individual component testing
- **API Integration Tests**: REST endpoint validation
- **End-to-End Tests**: Complete workflow validation
- **Infrastructure Tests**: Docker and service readiness checks

For detailed testing documentation, setup instructions, and usage examples, see [tests/README.md](tests/README.md).

For load testing with multiple concurrent clients, MailHog integration, and performance reporting, see [tests/load_tests/client_simulator/README.md](tests/load_tests/client_simulator/README.md).

Quick test run:
```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Run all tests
pytest tests/ -v

# Run specific test category
pytest tests/unit/ -v
pytest tests/api/ -v
pytest tests/integration/ -v
```

---

## 📊 Architecture Diagrams

Detailed architecture documentation is available in the `docs/` directory:

- **[C4 Model - Level 1](docs/c4_L1.md)** - System Context
- **[C4 Model - Level 2](docs/c4_L2.md)** - Container Architecture
- **[C4 Model - Level 3](docs/c4_L3_api_collector.md)** - API Collector Components
- **[C4 Model - Level 3](docs/c4_L3_alerting_worker.md)** - Alerting Worker Components
- **[Entity-Relationship Diagram](docs/ER_diagram.md)** - Database Schema
- **[Data Flow](docs/data_flow.md)** - System Data Flow
- **[Infrastructure](docs/infra.md)** - Infrastructure Setup

---

## 📚 Additional Documentation

- **[Full Project Documentation](https://docs.google.com/document/d/1ZYanmctLJ1nQAkrA3QUProKJxsqcL_bCVbXhCCZKYlA/edit?usp=sharing)** - Comprehensive design document
- **[Implementation Checklist](TODO.md)** - Feature implementation status
- **[Testing Guide](tests/README.md)** - Detailed testing strategy and execution

---

## 🛠️ Development

### Local Development Setup

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r api_collector/requirements.txt
pip install -r alerting_worker/requirements.txt
pip install -r tests/requirements.txt
```

### Running Services Locally

```bash
# Terminal 1: API Collector
cd api_collector
python -m src.main

# Terminal 2: Alerting Worker
cd alerting_worker
python -m src.main

# Terminal 3: MariaDB (or use Docker)
docker run -d -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root mariadb:latest
```

---

## 📝 Logs and Monitoring

The API Collector includes a `RequestLoggingMiddleware` that logs every incoming HTTP request:

```
2026-06-19 10:58:00 - api_collector - INFO - --> POST /api/logs
2026-06-19 10:58:00 - api_collector - INFO - <-- POST /api/logs — 201 (12ms)
```

The Alerting Worker supports graceful shutdown — it catches SIGTERM (from Docker) and finishes processing in-flight alerts before exiting.

All services produce structured logs to stdout/stderr and are captured by Docker:

```bash
# View API Collector logs
docker compose logs -f api_collector

# View Alerting Worker logs
docker compose logs -f alerting_worker

# View Database logs
docker compose logs -f db

# Follow all logs
docker compose logs -f
```
