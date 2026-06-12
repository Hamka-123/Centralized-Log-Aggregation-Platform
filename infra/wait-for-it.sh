#!/bin/bash
# wait-for-it.sh: waits for a service to be available
# Usage: ./wait-for-it.sh HOST:PORT -- command to run

set -e

host="$1"
shift
cmd="$@"

echo "Waiting for ${host}..."

while ! nc -z ${host%:*} ${host#*:} 2>/dev/null; do
  echo "  ... waiting"
  sleep 1
done

echo "${host} is up - executing command"
exec $cmd
