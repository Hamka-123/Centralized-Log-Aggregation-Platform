# Project Testing

This directory contains the testing suite for the **Centralized Log Aggregation Platform**. We use an **integration-first** approach where `pytest` orchestrates the infrastructure (Docker containers) to ensure real-world verification of API endpoints, worker behavior, infrastructure readiness, and database integrity.

## Directory Structure

```text
tests/
├── unit/             # Unit tests for api_collector and alerting_worker
├── api/              # API integration tests for api_collector
├── integration/      # End-to-end integration tests (API → Database flow)
├── infra/            # Infrastructure smoke tests
└── conftest.py       # Shared fixtures for Docker orchestration and database sessions
```
---

## Getting Started

### 1. Environment Setup

Ensure your virtual environment is active:

```bash
source venv/bin/activate
```

### 2. Installing Dependencies

Install the required testing libraries:

```bash
pip install -r tests/requirements.txt
```

---

## Infrastructure Strategy

The test suite utilizes a fixture-based orchestration approach. Shared fixtures in `conftest.py` automatically manage the Docker lifecycle for integration tests.

### Lifecycle

1. **Setup** – Before tests start, pytest triggers:

   ```bash
   docker compose up -d
   ```

2. **Health Checks** – The suite verifies that the API and supporting services are responsive before executing test functions.

3. **Teardown** – By default, containers are stopped and removed after test execution to ensure a clean environment.

---

## Infrastructure Testing

Infrastructure smoke tests validate the deployment environment before application-level tests run.

The infrastructure checks verify:

* **Configuration** – Docker Compose files are valid and YAML configuration is correctly structured.
* **Deployment** – Containers start successfully and reach a healthy state.
* **Connectivity** – The API responds correctly to health-check requests.
* **Service Availability** – Required dependencies are reachable and operational.

### Running Infrastructure Checks

Execute the validation script from the project root:

```bash
./scripts/check_infra.sh
```

---

## The KEEP_INFRA Workflow (Recommended for Development)

To speed up development and avoid repeatedly starting and stopping containers, you can keep the infrastructure running after test execution.

### Infrastructure Debugging Mode

```bash
KEEP_INFRA=true ./scripts/check_infra.sh
```

### Integration Test Persistence Mode

```bash
KEEP_INFRA=true pytest -v tests/integration/test_api_db.py
```

### Important Notes

When using `KEEP_INFRA=true`:

* Containers remain running after test completion.
* Database state is preserved for manual inspection.
* You can connect to services for debugging purposes.

If application code changes, rebuild or restart containers before rerunning tests:

```bash
docker compose up -d --build
```

---

## Running Application Tests

### Run All Tests

Execute the complete test suite:

```bash
pytest
```

### Verbose Mode

Display detailed test execution information:

```bash
pytest -v
```

### Run API Tests Only

```bash
pytest tests/api/
```

### Run Integration Tests Only

```bash
pytest tests/integration/
```

### Run Unit Tests Only

```bash
pytest tests/unit/
```

### Run Infrastructure Tests Only

```bash
pytest tests/infra/
```

---

## Database Verification

Integration tests utilize the `db_session` fixture to connect directly to the live MariaDB container.

### Requirements

Ensure your `.env` file contains valid test credentials and connection settings.

### Features

The `db_session` fixture automatically:

* Creates database connections.
* Provides transactional access for assertions.
* Cleans up resources after test execution.

### Example

```python
def test_log_persistence(db_session):
    ...
```

---

## Test Writing Guidelines

### Naming Conventions

Files must start with:

```text
test_*.py
```

Examples:

```text
test_api.py
test_worker.py
test_auth.py
```

Functions must also start with:

```python
def test_user_login():
    ...
```

### Fixtures

Use `conftest.py` for shared setup and teardown logic.

Examples:

* Database sessions
* Docker orchestration
* API clients
* Test data factories

Request fixtures explicitly in test functions:

```python
def test_create_log(db_session):
    ...
```

### API Testing

Use the `requests` library to interact with the running API.

Validate:

* HTTP status codes
* Response payloads
* Side effects in the database

Example:

```python
response = requests.post("/logs", json=payload)

assert response.status_code == 201
```

---

## Troubleshooting

If tests fail to connect to the API or database:

### Verify Containers

```bash
docker compose ps
```

Ensure all required containers show as **Up** and healthy.

### Verify Configuration

Check that:

* Values in `.env` are correct.
* Exposed ports match Docker Compose settings.
* Database credentials are valid.

### Rebuild Containers

If running with `KEEP_INFRA=true`, ensure the latest application code has been deployed:

```bash
docker compose up -d --build
```

---

## Tips for Success

### Keep Tests Isolated

Each test should:

* Prepare its own data, or
* Depend on a deterministic database state.

Avoid reliance on execution order.

### Fail Fast

Use verbose mode for easier debugging:

```bash
pytest -v
```

### Verify Both API and Persistence

Whenever possible:

1. Validate the API response.
2. Verify that the expected state exists in the database.

This ensures complete end-to-end coverage of the platform's behavior.

---
# Logging & Debugging

The platform uses centralized logging. During testing, log outputs are a primary tool for diagnosing failures.

## Log Location

All logs are written to the `./logs` directory on the host machine.

When running tests with Docker orchestration, ensure this directory is accessible.

### Log Files

- **api.log** — API activity and request/response cycles.
- **worker.log** — Background task processing and alert engine activity.

## Enabling Verbose Logs in Tests

`pytest` captures standard output by default. To display logging output directly in the console during test execution, use the `--log-cli-level` flag.

### Show INFO-Level Logs

```bash
pytest --log-cli-level=INFO
```

### Show DEBUG-Level Logs

Useful for deep troubleshooting:

```bash
pytest --log-cli-level=DEBUG
```

## Pre-Commit Checklist

Before merging or committing changes:

* All unit tests pass.
* All API tests pass.
* All integration tests pass.
* Infrastructure checks succeed.
* No failing assertions remain.
* Docker containers start successfully in a clean environment.

Always ensure the complete test suite passes before merging into the main branch.
