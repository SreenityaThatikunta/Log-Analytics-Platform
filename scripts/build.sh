#!/usr/bin/env bash

set -euo pipefail

docker build -f services/log-collector/Dockerfile -t log-collector:latest .
docker build -f services/processor/Dockerfile -t processor:latest .
docker build -f services/query-service/Dockerfile -t query-service:latest .
docker build -f services/frontend/Dockerfile -t frontend:latest .
