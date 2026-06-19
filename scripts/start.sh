#!/bin/bash

cd "$(dirname "$0")/.."

echo "--- Starting Redeployment Pipeline ---"
docker compose up -d db api_collector alerting_worker