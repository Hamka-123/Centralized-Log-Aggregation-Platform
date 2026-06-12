#!/bin/bash
cd "$(dirname "$0")/.."

echo "Redeploying project..."
docker compose down
docker compose build
docker compose up -d
