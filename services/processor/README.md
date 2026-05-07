# Processor

The processor turns incoming collector payloads into Elasticsearch documents.

## Responsibility

- exposes `POST /logs`
- receives log payloads from the collector
- applies normalization in `pipeline.py`
- writes documents into Elasticsearch

## Files

- [app/processor.py](/Users/sreenityathatikunta/Documents/Projects/log-analytics-platform/services/processor/app/processor.py): FastAPI app and indexing logic
- [app/pipeline.py](/Users/sreenityathatikunta/Documents/Projects/log-analytics-platform/services/processor/app/pipeline.py): transformation logic
- [requirements.txt](/Users/sreenityathatikunta/Documents/Projects/log-analytics-platform/services/processor/requirements.txt): Python dependencies
- [Dockerfile](/Users/sreenityathatikunta/Documents/Projects/log-analytics-platform/services/processor/Dockerfile): container build

## Current Transformation

Input:

- `service_name`
- `level`
- `message`
- `timestamp`

Output document:

- `service`
- `level`
  Uppercased before indexing
- `message`
- `timestamp`

## Endpoints

- `GET /health`
  Returns `{"status":"ok"}`
- `POST /logs`
  Accepts a log payload and indexes it

## Runtime Configuration

- `ELASTICSEARCH_URL`
  Default: `http://elasticsearch:9200`
- `ELASTICSEARCH_INDEX`
  Default: `logs`

## Testing

The processor is usually verified indirectly through collector ingestion and query-service retrieval.

Send a sample log:

```bash
LOG_TEST_SCENARIO=payment_error make test-log
```

Then inspect processor logs:

```bash
kubectl logs -n log-analytics deployment/processor --tail=100
```

Expected behavior:

- the processor receives a `POST /logs`
- it normalizes the payload
- it indexes a document into the `logs` Elasticsearch index
