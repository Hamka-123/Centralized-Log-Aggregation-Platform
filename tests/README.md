# Project Testing

This directory contains automated tests for the "Centralized Log Aggregation Platform" project. Our goal is to ensure infrastructure stability and the correct operation of microservices.

## Directory Structure

- `/unit` — unit tests for the `api_collector` and `alerting_worker`
- `/api` — integration tests for the API (`api_collector`).
- `/integration` — integration tests
- `/infra` — smoke tests for validating Docker configuration and infrastructure scripts.

## Getting Started

### 1. Environment Setup

Before running the tests, make sure you have activated the virtual environment:

```bash
source venv/bin/activate
```

### 2. Installing Dependencies

Install the required testing libraries (pytest, requests, docker, etc.):

```bash
pip install -r tests/requirements.txt
```

## Infrastructure Testing

We have a dedicated script for smoke testing the infrastructure. It verifies that:

- **Configuration:** YAML files are linted and Docker Compose configs are valid.
- **Deployment:** Containers start successfully and reach a "healthy" state.
- **Connectivity:** The API responds correctly to health checks.

### Running Infrastructure Checks

Use the automation script from the project root:

```bash
./scripts/check_infra.sh
```

### Debugging with Infrastructure

By default, the infrastructure tests automatically shut down the containers after execution to keep your environment clean. If you want to keep the containers running for manual investigation or debugging, use the `KEEP_INFRA` environment variable:

```bash
KEEP_INFRA=true ./scripts/check_infra.sh
```

## Running Application Tests

### Basic Run

To run all application tests (API and Worker) from the project root:

```bash
pytest
```

### Running a Specific Module

To run only the API tests:

```bash
pytest tests/api/
```

### Verbose Output Mode

To see more detailed information about the tests being executed:

```bash
pytest -v
```

## Test Writing Guidelines

- File names must start with `test_` (for example, `test_api.py`).
- Function names must start with `test_`.
- Use `conftest.py` in the appropriate subdirectories for shared fixtures (for example, database connections).

Make sure all tests pass successfully before committing to the main branch!