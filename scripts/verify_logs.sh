#!/bin/bash

# Configuration
LOG_DIR="./logs"
SERVICES=("api" "worker" "db")
MAX_AGE_MINUTES=5
MAX_SIZE_MB=50  # Max size allowed for any log file before truncation
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "--- Starting log verification in $LOG_DIR ---"

# Check if the logs directory exists
if [ ! -d "$LOG_DIR" ]; then
    echo -e "${RED}❌ ERROR: Directory $LOG_DIR not found.${NC}"
    exit 1
fi

SUCCESS=true

for service in "${SERVICES[@]}"; do
    if [ "$service" == "db" ]; then
        FILE="$LOG_DIR/db/db.log"
    else
        FILE="$LOG_DIR/$service.log"
    fi
    
    # 1. Check if the file exists
    if [ ! -f "$FILE" ]; then
        echo -e "${RED}❌ ERROR: File $FILE is missing.${NC}"
        SUCCESS=false
        continue
    fi
    
    # 2. Check file size and truncate if too large (prevent disk bloat)
    FILE_SIZE_BYTES=$(wc -c < "$FILE")
    MAX_SIZE_BYTES=$((MAX_SIZE_MB * 1024 * 1024))
    
    if [ "$FILE_SIZE_BYTES" -gt "$MAX_SIZE_BYTES" ]; then
        echo -e "${YELLOW}⚠️ WARNING: $FILE is too large ($((FILE_SIZE_BYTES/1024/1024))MB). Truncating...${NC}"
        truncate -s 0 "$FILE"
    elif [ "$FILE_SIZE_BYTES" -eq 0 ]; then
        echo -e "${RED}⚠️ WARNING: $FILE is empty.${NC}"
        SUCCESS=false
        continue
    fi
    
    # 3. Check for freshness (has it been updated in the last N minutes?)
    # Using 'find' with -mmin is compatible with standard Linux/macOS
    if [ -n "$(find "$FILE" -mmin +$MAX_AGE_MINUTES)" ]; then
        echo -e "${RED}❌ ERROR: Log $FILE is stale (not updated for over $MAX_AGE_MINUTES mins).${NC}"
        SUCCESS=false
        continue
    fi

    echo -e "${GREEN}✅ SUCCESS: $FILE is active and healthy.${NC}"
done

if [ "$SUCCESS" = true ]; then
    echo "--- Verification completed successfully! ---"
    exit 0
else
    echo "--- Verification failed. Check errors above. ---"
    exit 1
fi