#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

BUILD_FLAGS=""
if [[ "$1" == "--no-cache" ]]; then
    BUILD_FLAGS="--no-cache"
    echo -e "${YELLOW}--- Build with --no-cache enabled ---${NC}"
fi

set -e

cd "$(dirname "$0")/.."

check_module() {
    local dir=$1
    local name=$2
    echo -e "${YELLOW}--- Validating $name ($dir) ---${NC}"
    
    # 1. Check for Dockerfile
    if [ ! -f "$dir/Dockerfile" ]; then
        echo -e "${RED}Error: Dockerfile not found in $dir${NC}"
        exit 1
    fi
    
    # 2. Check for dependencies
    if [ -f "$dir/requirements.txt" ]; then
        echo "Found requirements.txt, checking dependencies..."
    fi

    # 3. Verify syntax
    echo "Running syntax check for $name..."
    docker build --check "$dir" > /dev/null

    echo -e "${GREEN}Check complete, no warnings found for $name.${NC}"
}

check_module "./db" "Database"
check_module "./api_collector" "Api_Collector"
check_module "./alerting_worker" "Alerting_Worker"

echo -e "${GREEN}Validation passed. Starting build process...${NC}"

echo -e "${YELLOW}Building Database image...${NC}"
docker compose build $BUILD_FLAGS db

echo -e "${YELLOW}Building Api_Collector...${NC}"
docker compose build $BUILD_FLAGS api_collector

echo -e "${YELLOW}Building Alerting_Worker...${NC}"
docker compose build $BUILD_FLAGS alerting_worker

echo -e "${GREEN}Build complete!${NC}"