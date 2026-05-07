# Services

This folder contains the application services that make up the runtime system.

## Services

- [log-collector/README.md](log-collector/README.md): gRPC ingestion service
- [processor/README.md](processor/README.md): transformation and Elasticsearch indexing service
- [query-service/README.md](query-service/README.md): FastAPI query API
- [frontend/README.md](frontend/README.md): React/Vite dashboard

## Runtime Roles

- `log-collector`
  Accepts gRPC log streams and forwards each entry to the processor
- `processor`
  Normalizes log payloads and indexes them into Elasticsearch
- `query-service`
  Queries Elasticsearch and returns filtered log results
- `frontend`
  Lets a user search logs by service and level from the browser

## Expected Ports

- collector: `50051`
- processor: `8001`
- query-service: `8000`
- frontend: `5173` in development, exposed behind service port `80` in Kubernetes

## Sample Test Flow

For Kubernetes verification, keep these port-forwards active:

```bash
kubectl port-forward svc/log-collector 50051:50051 -n log-analytics
kubectl port-forward svc/query-service 8000:8000 -n log-analytics
kubectl port-forward svc/frontend 5173:80 -n log-analytics
```

Send sample logs:

```bash
make test-log
LOG_TEST_SCENARIO=payment_error make test-log
LOG_TEST_SCENARIO=inventory_warn make test-log
make test-log-batch
```

Validate through the query API:

```bash
curl "http://localhost:8000/logs?service=auth&level=error"
curl "http://localhost:8000/logs?service=payment&level=error"
curl "http://localhost:8000/logs?service=inventory&level=warn"
```
