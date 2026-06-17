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
│   │   ├── main.py        # FastAPI app and route definitions
│   │   ├── database.py    # Database connection and session management
│   │   ├── models/        # Data models
│   │   ├── repositories/  # Data access layer
│   │   ├── services/      # Business logic
│   │   ├── api/           # API route handlers
│   │   ├── logs/          # Logging configuration
│   │   └── utils/         # Utility functions
│   ├── Dockerfile
│   └── requirements.txt
│
├── alerting_worker/        # Async worker for alert generation
│   ├── src/
│   │   ├── main.py        # Worker entry point
│   │   ├── models/        # Data models
│   │   ├── repositories/  # Data access layer
│   │   ├── services/      # Alert engine and SMTP client
│   │   ├── utils/         # Utility functions
│   │   └── workers/       # Worker controller
│   ├── Dockerfile
│   └── requirements.txt
│
├── db/                     # Database configuration
│   ├── init.sql          # Schema initialization script
│   └── Dockerfile        # MariaDB custom image
│
├── config/                 # Application configuration
│   ├── settings.py        # Environment settings
│   ├── logging_config.py  # Logging configuration
│   └── constants.py       # Application constants
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

Edit `.env` with your credentials:
- `DB_HOST`: Database host (default: `db`)
- `DB_PORT`: Database port (default: `3306`)
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password
- `DB_NAME`: Database name
- `SMTP_SERVER`: SMTP server address (e.g., `smtp.gmail.com`)
- `SMTP_PORT`: SMTP port (e.g., `587`)
- `SMTP_USER`: Email address for sending alerts
- `SMTP_PASSWORD`: SMTP password or app-specific token

#### 2. Deployment Methods

**Method 1: Docker Compose (Recommended for Development)**

The recommended way using Docker Compose, which automatically handles networking, service dependencies, and environment variables:

```bash
docker compose up -d --build
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

# Full redeploy
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

Response:
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

#### Submit Log Entry
```http
POST /logs
Content-Type: application/json
```

Request body:
```json
{
  "message": "Application started successfully",
  "level": "INFO",
  "service_name": "api_service",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

#### Retrieve Logs
```http
GET /logs?service_name=api_service&level=ERROR&limit=100
```

Query parameters:
- `service_name` (optional): Filter by service
- `level` (optional): Filter by log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `limit` (optional): Maximum number of results (default: 100)

Response:
```json
{
  "logs": [
    {
      "id": 1,
      "message": "Error occurred",
      "level": "ERROR",
      "service_name": "api_service",
      "timestamp": "2024-01-01T12:00:00Z"
    }
  ],
  "total": 1
}
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

---

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check database connectivity
python scripts/debug_db.py

# View database logs
docker compose logs db
```

### API Not Responding
```bash
# Check API health
curl http://localhost:8000/health

# Check API logs
docker compose logs api_collector
```

### Worker Not Processing Alerts
```bash
# Check worker logs
docker compose logs alerting_worker

# Verify database has ERROR/CRITICAL logs
curl http://localhost:8000/logs?level=ERROR
```

