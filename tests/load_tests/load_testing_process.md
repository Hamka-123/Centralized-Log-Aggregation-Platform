# Load Testing Process

## Overview

Load testing is orchestrated by a Python script (`tests/load_tests/client_simulator/load_test.py`). It spins up the full infrastructure stack, launches N simulated clients, collects performance metrics, and generates an HTML report.

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│                 load_test.py                    │
│  (orchestrator: brings up infra, collects stats)│
└──────────┬──────────────────────┬───────────────┘
           │                      │
           ▼                      ▼
   ┌──────────────-┐     ┌──────────────────┐
   │ Docker Compose│     │       N ×        │
   │ (api_collector│     │  log-client      │
   │  db, worker,  │     │  (simulator.py)  │
   │  mailhog)     │     └────────┬─────────┘
   └──────┬───────-┘              │
          │                       │
          ▼                       ▼
   ┌─────────────────────────────────────┐
   │       docker stats (CPU/RAM)        │
   │       MySQL KPI queries             │
   └─────────────────────────────────────┘
```

---

## Components

### 1. Orchestrator — `load_test.py`

The main entrypoint that:
- Parses CLI arguments
- Starts infrastructure via `docker compose up`
- Captures `docker stats` at three stages: baseline, peak load, recovery
- Launches N clients with Docker Compose scaling: `--scale log-client=N`
- Waits 60 seconds for the load to accumulate
- Runs SQL queries against MySQL for KPI metrics
- Generates an HTML report
- Optionally tears down the infrastructure

**Runtime options:**

| Flag | Description |
|------|-------------|
| `--clients N` | Number of concurrent clients (default: 10) |
| `--mailhog` | Redirect SMTP traffic to a local MailHog (safe mode) |
| `--no-smtp` | Completely disable email delivery |
| `--cleanup` | Remove all infrastructure (`down -v`) after the test |

**Examples:**
```bash
# Safe test with 1 client — for alert debugging
python tests/load_tests/client_simulator/load_test.py --mailhog --clients 1

# High-load database performance test with 100 clients, no email interference
python tests/load_tests/client_simulator/load_test.py --clients 100 --no-smtp
```

### 2. Client Simulator — `simulator.py`

Runs inside each `log-client` Docker container. It performs:
1. **Service registration** — POSTs to `/api/services/register` with a unique name in the format `{service_type}-{REPLICA_INDEX}-{hostname}`
2. **Log sending** — continuously POSTs to `/api/logs` at ~10 messages per second
3. Identifies itself via `SERVICE_TYPE` and `REPLICA_INDEX` environment variables (set by Docker Compose when scaling)

### 3. SQL KPI — `kpi_report.sql`

Queries executed against MySQL after the test:
- **Total logs** processed in the last 2 minutes
- **Distribution by service** (`service_id`, `count`)
- **Processing status** — how many logs were processed vs. pending

### 4. HTML Report — `report_template.html`

Template with a `{content}` placeholder, populated with:
- `docker stats` tables at each stage (CPU, Memory)
- SQL query results
- Test timestamp

Reports are saved to `tests/load_tests/client_simulator/reports/{timestamp}/report.html`

---

## Test Lifecycle

```
 1. Setup
    ├── Build images (docker compose build)
    └── Start infrastructure (db, api_collector, worker, optionally mailhog)

 2. Baseline metrics
    └── docker stats — record CPU/RAM before load

 3. Launch clients
    ├── docker compose rm -f log-client (remove stale containers)
    └── docker compose up -d --scale log-client=N

 4. Load period (60 seconds)
    ├── Each client: ~10 logs/sec → API Collector
    ├── API Collector → MySQL
    └── Alerting Worker reads logs and fires alerts

 5. Peak metrics
    └── docker stats — record CPU/RAM under load

 6. KPI collection
    └── MySQL queries (kpi_report.sql)

 7. Cleanup clients
    └── docker compose rm -f log-client

 8. Recovery metrics (after 30 seconds)
    └── docker stats — record CPU/RAM after load subsides

 9. Report generation
    ├── Inject metrics into HTML template
    └── Save to reports/{timestamp}/report.html

10. (Optional) Full teardown
    └── docker compose down -v
```

---

## Safety and Warnings

- **Real email delivery**: if `alert_engine` is configured to send an email for every ERROR-level log, a load test may spam the target mailbox or get blocked by the SMTP provider.
- **MailHog**: with `--mailhog`, SMTP traffic is redirected to a local MailHog instance at `localhost:8025` — completely safe for debugging.
- **Docker resources**: for tests with >50 clients, at least 4 GB RAM is recommended.

---

## Directory Structure

```
tests/load_tests/client_simulator/
├── Dockerfile              # Image for log-client (python:3.11-slim + requests)
├── simulator.py            # Client simulator logic
├── load_test.py            # Orchestrator (recommended entrypoint)
├── load_test.sh            # Shell-based orchestrator (alternative)
├── kpi_report.sql          # SQL queries for database KPIs
├── report_template.html    # HTML report template
├── README.md               # Documentation
└── reports/                # Stored reports
    └── {timestamp}/
        └── report.html
```

---

## Key Features

1. **Client scaling** via Docker Compose `--scale` — no need to manually launch N processes; each container gets a unique `REPLICA_INDEX`.
2. **Three metric snapshots** (before / during / after) — clearly shows the infrastructure's response to load.
3. **SQL KPI** provides quantitative throughput metrics (total logs, logs per service).
4. **Flexible SMTP configuration** — alerts can be tested safely, or email can be disabled entirely for pure DB performance tests.
5. **Two entrypoints** — Python (`load_test.py`) and Shell (`load_test.sh`) — choose whichever fits the environment.
