#!/bin/bash

cd "$(dirname "$0")/.."

echo "Stopping services..."
docker compose down