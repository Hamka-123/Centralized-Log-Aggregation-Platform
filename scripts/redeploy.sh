#!/bin/bash

YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

cd "$(dirname "$0")/.." || exit

printf "${YELLOW}===================\nRedeploying project pipeline\n===================${NC}\n"

echo -e "${GREEN}--- Rebuild containers..."
./infra/build.sh

echo -e "${YELLOW}--- Stopping containers..."
docker compose down

echo -e "${YELLOW}--- Starting containers..."
docker compose up -d

echo -e "${GREEN}--- Deployment finished successfully! ---${NC}"
docker compose ps
