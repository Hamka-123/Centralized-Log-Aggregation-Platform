#!/bin/bash

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

set -e

echo -e "${YELLOW}--- 0. Preparing environment ---${NC}"
# Install dependencies (if not yet present)
pip install -q --upgrade pip
pip install -q yamllint -r ./tests/requirements.txt

# 1. Check the configs
echo -e "${YELLOW}--- 1. Running YAML Lint ---${NC}"
yamllint docker-compose.yml

echo -e "${YELLOW}--- 2. Validating Docker Compose Config ---${NC}"
docker compose config --quiet

#2. Run infrastructure tests
echo -e "${YELLOW}--- 3. Running Smoke Tests ---${NC}"
KEEP_INFRA=true pytest ./tests/infra

echo -e "${GREEN}--- Infrastructure checks passed successfully! ---${NC}"