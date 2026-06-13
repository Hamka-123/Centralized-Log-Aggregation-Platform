# Centralized Log Aggregation Platform
An enterprise system designed for collecting, storing, and initially analyzing logs from various sources. The system is developed as a modular Python application integrated into a containerized environment.

## Full documentation
https://docs.google.com/document/d/1ZYanmctLJ1nQAkrA3QUProKJxsqcL_bCVbXhCCZKYlA/edit?usp=sharing 

---
## Project Startup 
### Backend Setup
Before launching, duplicate `.env_template` as `.env` and populate the `DB_*` (database) and `SMTP_*` (email alerts) environment variables with your credentials.

### Methods
1. Recommended method (for development and local execution)
We use docker compose because it automatically handles network configuration, service dependencies, and environment variables, ensuring a seamless and reliable setup.

```Bash
docker compose up -d --build
```
2. Manual build (CI/CD / Production)
For specific image build stages or for educational purposes, you can use the scripts located in the `infra/` directory:

```Bash
./infra/build.sh
.infra/redeploy.sh
.infra/start.sh
.infra/stop.sh
```
