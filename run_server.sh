#!/usr/bin/env bash
set -euo pipefail

PORT=${PORT:-1337}

pids=$(lsof -ti tcp:"$PORT" 2>/dev/null || true)
if [[ -n "$pids" ]]; then
  echo "Killing processes on port $PORT..."
  echo "$pids" | xargs kill -9
fi

echo "Starting server on port $PORT..."
node server.js
