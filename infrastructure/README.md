# Infrastructure

This folder contains the runtime deployment definitions for local and Kubernetes environments.

## Contents

- [docker-compose.yml](/Users/sreenityathatikunta/Documents/Projects/log-analytics-platform/infrastructure/docker-compose.yml): local multi-container development stack
- [kubernetes/README.md](kubernetes/README.md): detailed Kubernetes resource documentation

## Local Runtime

Use Docker Compose for the fastest full-stack local run:

```bash
docker compose -f infrastructure/docker-compose.yml up --build
```

This starts:

- Elasticsearch
- processor
- log-collector
- query-service
- frontend

## Kubernetes Runtime

Use the manifests in `infrastructure/kubernetes` together with `./scripts/build.sh` and `./scripts/deploy.sh`.

