# TODO — Centralized Log Aggregation Platform

A concise step-by-step implementation checklist aligned with the requirements and system design (C4 / ER diagrams).

---

## ✅ MUST HAVE (2 weeks — course requirements compliance)

### 1. Infrastructure & orchestration
- [x] Prepare `docker-compose.yml` with services: `db`, `api_collector`, `alerting_worker`.
- [x] Use the official `mariadb` image and mount `db/init.sql` into `/docker-entrypoint-initdb.d/`.
- [x] Add volumes for persistence (`db-data`).

### 2. Database
- [x] Complete `db/init.sql`: tables `services`, `logs`, `alerts` with constraints and indexes.
- [x] Retention Policy

### 3. Api_Collector (FastAPI) — basic implementation
- [x] Implement `POST /logs` — accept and persist logs (basic validation).
- [x] Implement `GET /logs` — support filtering by `service_name`, `level`, `limit`.
- [x] Implement `/health` endpoint.

### 4. Alerting_Worker — core functionality
- [x] Implement the worker: DB connection, fetch unprocessed entries (ERROR/CRITICAL).
- [x] Basic SMTP integration: send email, handle errors.
- [x] Mark entries as alerted (table `alerts`).
- [x] Configure via environment variables and polling interval.

### 5. Containerization
- [x] Complete `Dockerfile` for `Api_Collector` and `Alerting_Worker` (python:3.11-slim).
- [x] Add `HEALTHCHECK` to Dockerfiles.
- [x] Add `.dockerignore`.

### 6. Configuration
- [x] Keep `.env_template` tracked; add `.env` to `.gitignore` for local overrides.
- [x] Document required environment variables (DB_*, SMTP_*).

### 7. Logging
- [x] Add `logging` configuration to API and worker (console, INFO level minimum).

### 8. Infrastructure scripts
- [x] Ensure `infra/start.sh`, `stop.sh`, `build.sh` work correctly.

### 9. Documentation
- [x] README: how to run locally, key endpoints.
- [x] Link to C4 / ER diagrams in `docs/`.

### 10. Release
- [x] First functional commit with clear message.
- [x] Tag as `v1.0` or `v1.0.0-alpha`.

---

## 🎁 NICE TO HAVE (future enhancements)

### Extended logging & monitoring
- [ ] Structured logs (JSON format).
- [ ] Metrics export (Prometheus endpoint).
- [x] Request/response logging for API.

### Tests & validation
- [x] Unit tests for worker and API logic (pytest).
- [x] Integration/smoke tests: `docker compose up` + smoke requests.
- [ ] Testcontainers for real DB testing.
- [x] Infrastructure and script testing (linting, smoke testing)
- [x] start clients

### CI / CD
- [ ] GitHub Actions pipeline: lint (ruff), type checks (mypy), unit tests.
- [ ] Automated Docker image builds and registry pushes.
- [x] Shell CI pipeline
- [x] Smoke tests in pipeline.

### Security & optimization
- [x] Minimize DB user privileges (separate app user).
- [ ] Non-root user in containers.
- [ ] Run `pip-audit` / `safety` and fix vulnerabilities.
- [ ] Production: Vault / SecretsManager integration.

### Feature enhancements
- [ ] Retries and throttling for SMTP.
- [ ] Advanced log filtering (time range, regex).
- [ ] Pagination for GET /logs.
- [ ] Batch insert for logs (if high volume).
  
### Examples & tooling
- [ ] curl / Postman collection for API.
- [ ] Docker Compose overrides for dev and prod environments.
- [ ] Database migrations (Alembic or custom scripts).
- [ ] Add the maintenance_logs audit table and record the deletion history within the cleanup procedure.

### Documentation
- [ ] CHANGELOG.md with versioning.
- [ ] Sequence flow diagrams in `docs/`.
- [ ] Deployment guide (for simple hosting or Kubernetes).
- [ ] Contributing guide.

### Frontend
- [x] Swagger UI
- [ ] Service status dashboard


---

**Green line (2 weeks):** Must Have items deliver a working MVP that meets course requirements.  
**Blue line (future):** Nice to Have items improve scalability, reliability, and DevOps maturity.

