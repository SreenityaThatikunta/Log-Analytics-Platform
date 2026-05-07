# log-analytics-platform

`log-analytics-platform` is a small distributed log pipeline built as a set of focused services:

- a gRPC collector receives client log streams
- a processor transforms each log and indexes it into Elasticsearch
- a query service exposes HTTP search endpoints
- a React frontend provides a simple dashboard
- a Python SDK provides sample producers and test scenarios

## Project Flow

```text
Producer SDK -> gRPC Collector -> HTTP Processor -> Elasticsearch -> Query Service -> Frontend
```

## Repository Guide

- [proto/README.md](proto/README.md): gRPC contract and generated bindings
- [services/README.md](services/README.md): service overview and service-by-service links
- [sdk/python-client/README.md](sdk/python-client/README.md): SDK usage and test scenarios
- [infrastructure/README.md](infrastructure/README.md): Docker Compose and Kubernetes deployment layout
- [scripts/README.md](scripts/README.md): helper scripts and expected usage

## Run Locally with Docker Compose

Start the stack:

```bash
docker compose -f infrastructure/docker-compose.yml up --build
```

Local endpoints:

- frontend: `http://localhost:5173`
- query service: `http://localhost:8000`
- processor: `http://localhost:8001`
- Elasticsearch: `http://localhost:9200`
- collector gRPC: `localhost:50051`

Useful checks:

```bash
curl "http://localhost:8000/health"
make test-log
curl "http://localhost:8000/logs?service=auth&level=error"
```

Stop the stack:

```bash
docker compose -f infrastructure/docker-compose.yml down
```

## Run on Minikube

Build images into the Minikube Docker daemon:

```bash
eval $(minikube docker-env)
./scripts/build.sh
```

Deploy:

```bash
./scripts/deploy.sh
```

Verify:

```bash
kubectl get pods -n log-analytics
kubectl get svc -n log-analytics
kubectl get ingress -n log-analytics
```

Port-forward for testing:

Terminal 1:

```bash
kubectl port-forward svc/log-collector 50051:50051 -n log-analytics
```

Terminal 2:

```bash
kubectl port-forward svc/query-service 8000:8000 -n log-analytics
```

Terminal 3:

```bash
kubectl port-forward svc/frontend 5173:80 -n log-analytics
```

Then test:

```bash
make test-log
curl "http://localhost:8000/logs?service=auth&level=error"
```

## Current Status

Implemented and verified:

- gRPC ingestion
- processor indexing into Elasticsearch
- query API retrieval
- frontend search flow
- Docker Compose runtime
- Minikube deployment
- HPA metrics via Metrics Server

## Future Phase 4

Planned next-step improvements:

- add Kafka between collector and processor for buffering and backpressure handling
- add Redis for caching frequent query results
- improve service hardening with richer health checks and more structured logging
- add stronger auth controls for ingestion and query access
- add more automated tests and load testing
- expand the frontend beyond basic service and level filtering

For the full detailed documentation, use the folder READMEs linked above.
