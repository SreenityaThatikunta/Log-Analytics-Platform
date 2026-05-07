# Query Service

The query service is the HTTP read interface for indexed logs.

## Responsibility

- exposes a search endpoint for clients and the frontend
- queries Elasticsearch using service and level filters
- returns Elasticsearch search output

## Files

- [app/main.py](/Users/sreenityathatikunta/Documents/Projects/log-analytics-platform/services/query-service/app/main.py): FastAPI app and middleware setup
- [app/routes.py](/Users/sreenityathatikunta/Documents/Projects/log-analytics-platform/services/query-service/app/routes.py): route definitions
- [app/elastic.py](/Users/sreenityathatikunta/Documents/Projects/log-analytics-platform/services/query-service/app/elastic.py): Elasticsearch query logic
- [requirements.txt](/Users/sreenityathatikunta/Documents/Projects/log-analytics-platform/services/query-service/requirements.txt): Python dependencies
- [Dockerfile](/Users/sreenityathatikunta/Documents/Projects/log-analytics-platform/services/query-service/Dockerfile): container build

## Endpoints

- `GET /health`
  Returns `{"status":"ok"}`
- `GET /logs?service=<name>&level=<level>`
  Searches the configured Elasticsearch index

## Current Query Shape

The service builds a boolean `must` query that matches:

- `service`
- `level`

`level` is uppercased before the search request.

## Current Behavior

- if the `logs` index does not exist, the service returns an empty result set instead of a 500
- CORS is enabled for local frontend usage

## Runtime Configuration

- `ELASTICSEARCH_URL`
- `ELASTICSEARCH_INDEX`

## Testing

Port-forward the query service:

```bash
kubectl port-forward svc/query-service 8000:8000 -n log-analytics
```

Health check:

```bash
curl "http://localhost:8000/health"
```

Sample validation queries:

```bash
curl "http://localhost:8000/logs?service=auth&level=error"
curl "http://localhost:8000/logs?service=auth&level=warn"
curl "http://localhost:8000/logs?service=payment&level=error"
curl "http://localhost:8000/logs?service=payment&level=info"
curl "http://localhost:8000/logs?service=checkout&level=info"
curl "http://localhost:8000/logs?service=search&level=error"
curl "http://localhost:8000/logs?service=inventory&level=warn"
```

Expected behavior:

- before ingestion, queries return zero hits
- after sending a matching sample log, the returned `hits` array contains indexed documents
