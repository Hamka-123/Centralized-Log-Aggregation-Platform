# Centralized Log Aggregation: Load Testing Guide

This project includes infrastructure for log collection and a load-testing tool.

## ⚠️ Important Warning: Real Email Delivery

By default, the script is configured to send notifications through the real SMTP server specified in your configuration.

**Risk:** If `alert_engine` is configured to send an email for every `ERROR`-level log, you may spam the target mailbox or get blocked by your SMTP provider.

## 🚀 Quick Start

The load-testing tool is located at:

```text
tests/load_tests/client_simulator/load_test.py
```

### Run the test in safe mode (recommended)

```bash
python tests/load_tests/client_simulator/load_test.py --mailhog
```

### Run the test with real email delivery

```bash
python tests/load_tests/client_simulator/load_test.py
```

## 🛠 Runtime Options

| Flag          | Description                                                           |
| ------------- | --------------------------------------------------------------------- |
| `--clients N` | Run the test with `N` concurrent clients (e.g., `--clients 50`).      |
| `--mailhog`   | Redirect SMTP traffic to a local MailHog instance (port 8025).        |
| `--no-smtp`   | Completely disable email delivery (ideal for DB performance testing). |
| `--cleanup`   | Remove all infrastructure (`down -v`) after the test completes.       |

## 📋 Usage Scenarios

### 1. Testing with MailHog (Alert Debugging)

Use this option to verify email generation without the risk of spamming:

```bash
python tests/load_tests/client_simulator/load_test.py --mailhog --clients 1
```

MailHog UI is available at:

```text
http://localhost:8025
```

### 2. High-Load Database Performance Testing

To test the system under high load (e.g., 100 clients) without email interference:

```bash
python tests/load_tests/client_simulator/load_test.py --clients 100 --no-smtp
```

## ⚙️ Technical Details

### Scalability

Clients are launched dynamically using Docker Compose scaling:

```text
--scale log-client=N
```

### Identification

Each client receives a unique `REPLICA_INDEX` through environment variables, allowing for precise log source tracking in the database.

### Reporting

After the test completes, an HTML report is generated in:

```text
tests/load_tests/client_simulator/reports/
```

The report includes:

* Resource consumption metrics (CPU/RAM)
* Database performance metrics (calculated via `kpi_report.sql`)

## 🧹 Infrastructure Management

### Full Reset

To completely remove all services, including the database and API:

```bash
docker compose down -v
```

## Troubleshooting

If you encounter errors, ensure that your `common/config.py` contains valid credentials and that Docker has sufficient resources (at least **4 GB RAM** recommended for large load tests).
