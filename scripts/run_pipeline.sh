#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

set -e

echo -e "${YELLOW}=== STAGE 1: Redeploy ===${NC}"
./scripts/redeploy.sh

echo -e "${YELLOW}=== STAGE 2: Infrastructure Validation ===${NC}"
./scripts/check_infra.sh

echo -e "${YELLOW}=== STAGE 3: Installing dependencies ===${NC}"
pip install -r api_collector/requirements.txt
pip install -r alerting_worker/requirements.txt
pip install -r tests/requirements.txt

echo -e "${YELLOW}=== STAGE 4: Log Health Check ===${NC}"
./scripts/verify_logs.sh

echo -e "${YELLOW}=== STAGE 5: Run application tests ===${NC}"
# Here we run the rest of the tests (all except for the infra)
KEEP_INFRA=true pytest -v ./tests/ --ignore=./tests/infra

echo -e "${GREEN}=== All pipelines passed successfully! ===${NC}"