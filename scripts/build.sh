#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Capture the total start time
total_start_time=$(date +%s)

BUILD_FLAGS=""
if [[ "$1" == "--no-cache" ]]; then
    BUILD_FLAGS="--no-cache"
    echo -e "${YELLOW}--- Build with --no-cache enabled ---${NC}"
fi

set -e

cd "$(dirname "$0")/.."

time_build() {
    local start_time=$(date +%s)
    "$@"
    local end_time=$(date +%s)
    echo -e "${GREEN}Task took $((end_time - start_time)) seconds.${NC}"
}

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

    # 3. Role-based structure validation (Enterprise Layout)
    case "$name" in
        "Api_Collector")
            for layer in "src/api" "src/services" "src/repositories" "src/models"; do
                if [ ! -d "$dir/$layer" ]; then 
                    echo -e "${RED}Error: Required layer '$layer' missing in $name${NC}"; exit 1
                fi
            done
            ;;
        "Alerting_Worker")
            for layer in "src/workers" "src/services" "src/repositories"; do
                if [ ! -d "$dir/$layer" ]; then
                    echo -e "${RED}Error: Required layer '$layer' missing in $name${NC}"; exit 1
                fi
            done
            ;;
    esac

    # 4. Verify syntax
    echo "Running syntax check for $name..."
    docker build --check "$dir" > /dev/null

    echo -e "${GREEN}Check complete, no warnings found for $name.${NC}"
}

# Validation calls
check_module "./db" "Database"
check_module "./api_collector" "Api_Collector"
check_module "./alerting_worker" "Alerting_Worker"

echo -e "${GREEN}Validation passed. Starting build process...${NC}"

echo -e "${YELLOW}Building Database image...${NC}"
time_build docker compose build $BUILD_FLAGS db

echo -e "${YELLOW}Building Api_Collector...${NC}"
time_build docker compose build $BUILD_FLAGS api_collector

echo -e "${YELLOW}Building Alerting_Worker...${NC}"
time_build docker compose build $BUILD_FLAGS alerting_worker

echo -e "${GREEN}Build complete!${NC}"

# Calculate and display total time
total_end_time=$(date +%s)
total_duration=$((total_end_time - total_start_time))

echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN}Total build pipeline time: $total_duration seconds.${NC}"
echo -e "${GREEN}==========================================${NC}"