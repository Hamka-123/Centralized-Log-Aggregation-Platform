#!/bin/bash

cd "$(dirname "$0")/.."

echo "Building Database image..."
docker build -t centralized-log-db ./db

echo "Building Api_Collector..."
docker build -t api-collector ./api_collector

echo "Building Alerting_Worker..."
docker build -t alerting-worker ./alerting_worker

echo "Build complete!"