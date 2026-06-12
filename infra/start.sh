#!/bin/bash

cd "$(dirname "$0")/.."

echo "Starting services..."
docker compose up -d