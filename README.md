# log-analytics-platform

`log-analytics-platform` is a small distributed system for ingesting, transforming, indexing, and querying application logs. It is structured as a microservice-style project so each concern is isolated:

- producers send logs over gRPC
- the collector accepts the stream and forwards each log
- the processor normalizes data and writes it to Elasticsearch
- the query service exposes an HTTP API for searching logs
- the frontend provides a simple dashboard for querying the system

The project is intentionally staged in phases:

- Phase 1: core ingestion, processing, indexing, and querying
- Phase 2: containerized local development with Docker Compose and a frontend
- Phase 3: Kubernetes deployment with services, ingress, persistent storage, and autoscaling
- Phase 4: future hardening such as Kafka buffering, Redis caching, and deeper production concerns

## Architecture

The main flow is:

1. A producer uses the Python SDK and sends `LogEntry` messages to the gRPC collector.
2. The collector receives the stream on port `50051`.
3. For each log entry, the collector forwards a JSON payload to the processor over HTTP.
4. The processor transforms the payload into an Elasticsearch document and indexes it into the `logs` index.
5. The query service runs a filtered Elasticsearch query and returns the result over HTTP.
6. The frontend calls the query service and renders the returned log hits.

High-level topology:

```text
SDK / Producer
    |
    v
gRPC Log Collector
    |
    v
HTTP Processor
    |
    v
Elasticsearch
    |
    v
Query Service
    |
    v
Frontend
```

## Repository Layout

```text
proto/                                  Shared gRPC contract
services/log-collector/                 gRPC ingestion service
services/processor/                     HTTP transformation and indexing service
services/query-service/                 FastAPI query API
services/frontend/                      React/Vite dashboard
sdk/python-client/                      Sample client and producer SDK
infrastructure/docker-compose.yml       Local development stack
infrastructure/kubernetes/              Kubernetes manifests
scripts/build.sh                        Docker image build script
scripts/deploy.sh                       Kubernetes apply script
```

## Shared Contract

The shared contract is defined in [proto/log.proto](proto/log.proto).

It describes:

- `LogService`
- the client-streaming RPC `StreamLogs`
- `LogEntry`
- `Ack`

Current `LogEntry` shape:

- `service_name`: source service name
- `level`: log level such as `error`, `info`, `warn`
- `message`: log body
- `timestamp`: unix timestamp

The repo also includes generated Python gRPC bindings in `proto/log_pb2.py` and `proto/log_pb2_grpc.py`. The regeneration helper is [scripts/generate_proto.sh](scripts/generate_proto.sh).

## Services

### Log Collector

Path: `services/log-collector`

Role:

- accepts gRPC log streams on port `50051`
- optionally validates an API key if `LOG_COLLECTOR_API_KEY` is set
- forwards each log entry to the processor using `PROCESSOR_URL`
- returns a final `Ack` when the stream completes

Important behavior:

- logs stream start and completion
- logs each forwarded entry
- aborts with gRPC `UNAVAILABLE` if the processor cannot be reached
- aborts with gRPC `INTERNAL` for other stream-processing failures

What to expect:

- healthy collector pods listen on TCP `50051`
- when sending a sample log, the collector should return an `OK:<count>` response
- collector logs should show each forwarded record

### Processor

Path: `services/processor`

Role:

- exposes an HTTP endpoint at `POST /logs`
- receives collector-forwarded payloads
- applies normalization logic in `pipeline.py`
- writes documents into Elasticsearch

Current transformation:

- `service_name` becomes `service`
- `level` is normalized to uppercase
- `message` is passed through
- `timestamp` is passed through

Health:

- `GET /health` returns `{"status":"ok"}`

What to expect:

- processor pods listen on port `8001`
- successful ingest returns a response containing `result` and the indexed `document`

### Query Service

Path: `services/query-service`

Role:

- exposes `GET /logs?service=...&level=...`
- queries Elasticsearch for matching documents
- returns raw Elasticsearch search output

Health:

- `GET /health` returns `{"status":"ok"}`

Current behavior:

- if the `logs` index does not exist yet, the service returns an empty Elasticsearch-style result instead of failing
- CORS is enabled for the local frontend

What to expect:

- query-service pods listen on port `8000`
- before any ingestion, `/logs` returns zero hits
- after ingesting a test log, `/logs?service=auth&level=error` returns one or more hits

### Frontend

Path: `services/frontend`

Role:

- provides a minimal React/Vite dashboard
- queries the query service by `service` and `level`
- renders returned Elasticsearch hits

What to expect:

- the page shows filter inputs for service and level
- before ingestion, searches show an empty state
- after ingestion, matching logs appear as cards

### Python SDK

Path: `sdk/python-client`

Role:

- demonstrates how a producer would send logs to the collector
- contains a sample `send_logs()` function
- supports local testing through the `example.py` entrypoint

Default sample payload:

- `service_name="auth"`
- `level="error"`
- `message="token expired"`

Available built-in test scenarios:

- `auth_error`
  `service=auth`, `level=error`, `message="token expired"`
- `auth_warn`
  `service=auth`, `level=warn`, `message="refresh token nearing expiry"`
- `payment_error`
  `service=payment`, `level=error`, `message="card authorization failed"`
- `payment_info`
  `service=payment`, `level=info`, `message="refund request queued"`
- `checkout_info`
  `service=checkout`, `level=info`, `message="checkout session started"`
- `search_error`
  `service=search`, `level=error`, `message="elasticsearch query timeout"`
- `inventory_warn`
  `service=inventory`, `level=warn`, `message="low stock threshold reached"`
- `batch`
  Sends all of the scenarios above in a single gRPC stream

Validation queries for the built-in scenarios:

```bash
curl "http://localhost:8000/logs?service=auth&level=error"
curl "http://localhost:8000/logs?service=auth&level=warn"
curl "http://localhost:8000/logs?service=payment&level=error"
curl "http://localhost:8000/logs?service=payment&level=info"
curl "http://localhost:8000/logs?service=checkout&level=info"
curl "http://localhost:8000/logs?service=search&level=error"
curl "http://localhost:8000/logs?service=inventory&level=warn"
```

## Data Flow Details

The end-to-end flow currently verified in the cluster is:

1. `make test-log` sends a sample log through the Python client.
2. The client calls the collector over gRPC at `localhost:50051` when port-forwarded.
3. The collector forwards that log to the processor.
4. The processor indexes the transformed document into Elasticsearch under `logs`.
5. The query service returns the indexed hit from `GET /logs`.

Example indexed document observed in the running system:

```json
{
  "service": "auth",
  "level": "ERROR",
  "message": "token expired",
  "timestamp": 1778131235
}
```

## Running Locally with Docker Compose

This is the simplest full-stack local workflow.

Start the stack:

```bash
docker compose -f infrastructure/docker-compose.yml up --build
```

Services exposed locally:

- Elasticsearch: `http://localhost:9200`
- Processor: `http://localhost:8001`
- Query service: `http://localhost:8000`
- Frontend: `http://localhost:5173`
- Collector gRPC: `localhost:50051`

Useful checks:

```bash
curl "http://localhost:8000/health"
curl "http://localhost:8000/logs?service=auth&level=error"
make test-log
make test-log-batch
```

Stop the stack:

```bash
docker compose -f infrastructure/docker-compose.yml down
```

## Running on Minikube

The Kubernetes manifests in `infrastructure/kubernetes` are designed for a small single-node development cluster such as Minikube.

### Build Images into the Minikube Docker Daemon

```bash
eval $(minikube docker-env)
./scripts/build.sh
```

This is important. The Deployments use image names such as `log-collector:latest` and `query-service:latest`. If those images are not built into the same Docker environment the cluster can access, the pods will fail with `ImagePullBackOff`.

### Deploy

```bash
./scripts/deploy.sh
```

This script:

- checks that `kubectl` exists
- checks that a Kubernetes context is active
- checks that the API server is reachable
- applies the namespace manifest
- applies the manifest set via kustomize

### Verify

```bash
kubectl get pods -n log-analytics
kubectl get svc -n log-analytics
kubectl get ingress -n log-analytics
kubectl get hpa -n log-analytics
```

Expected healthy state:

- Elasticsearch pod: `Running`
- frontend, collector, processor, query-service pods: `Running`
- services created for all components
- ingress created for `log-analytics.local`

### Port-Forward for Testing

Use separate terminals:

Terminal 1:

```bash
kubectl port-forward svc/log-collector 50051:50051 -n log-analytics
```

Terminal 2:

```bash
kubectl port-forward svc/query-service 8000:8000 -n log-analytics
```

Then test:

```bash
curl "http://localhost:8000/health"
curl "http://localhost:8000/logs?service=auth&level=error"
make test-log
make test-log-batch
curl "http://localhost:8000/logs?service=auth&level=error"
```

To see the available named scenarios:

```bash
make test-log-list
```

To send a specific scenario:

```bash
LOG_TEST_SCENARIO=payment_error make test-log
LOG_TEST_SCENARIO=inventory_warn make test-log
LOG_TEST_SCENARIO=checkout_info make test-log
```

Then validate the matching results:

```bash
curl "http://localhost:8000/logs?service=payment&level=error"
curl "http://localhost:8000/logs?service=inventory&level=warn"
curl "http://localhost:8000/logs?service=checkout&level=info"
```

### Metrics Server and HPA

HPA depends on Metrics Server. If `kubectl get hpa -n log-analytics` shows `cpu: <unknown>`, enable Metrics Server:

```bash
minikube addons enable metrics-server
```

Once it is ready:

```bash
kubectl top pods -n log-analytics
kubectl top nodes
```

In the verified cluster state, metrics are available and `kubectl top` returns live CPU and memory usage for all pods and the Minikube node.

## Kubernetes Resources

Phase 3 includes:

- Namespace: `log-analytics`
- ConfigMap for shared runtime configuration
- Elasticsearch StatefulSet with a PersistentVolumeClaim
- ClusterIP Services for all internal components
- Deployments for frontend, collector, processor, and query service
- Ingress for frontend and query API routing
- HPAs for collector and query service

### Ingress Routing

Current ingress host:

- `log-analytics.local`

Current routes:

- `/api/...` -> query-service
- `/` -> frontend

This assumes an ingress controller such as NGINX is installed in the cluster.

## Configuration

Important environment variables:

- `PROCESSOR_URL`
  Used by the collector to forward incoming logs
- `ELASTICSEARCH_URL`
  Used by processor and query service to connect to Elasticsearch
- `ELASTICSEARCH_INDEX`
  Defaults to `logs`
- `VITE_QUERY_API_URL`
  Used by the frontend to query the API
- `LOG_COLLECTOR_API_KEY`
  Optional API key validation for collector requests
- `LOG_COLLECTOR_ADDRESS`
  Used by `make test-log` and the Python example client

## Make Targets

Current `Makefile` targets:

- `build-images`
  Builds all Docker images
- `compose-up`
  Starts the Docker Compose stack
- `compose-down`
  Stops the Docker Compose stack
- `k8s-deploy`
  Applies Kubernetes manifests
- `k8s-dry-run`
  Runs a local `kubectl` dry-run against the kustomize bundle
- `test-log`
  Sends a sample log through the Python SDK to the collector
- `test-log-batch`
  Sends all built-in sample scenarios in a single stream
- `test-log-list`
  Prints the available built-in sample scenarios

## Operational Expectations

What to expect when the system is healthy:

- `/health` on the query service returns `{"status":"ok"}`
- `GET /logs` returns zero hits before data exists
- sending a sample log through the SDK results in one indexed Elasticsearch document
- querying by `service=auth&level=error` returns that document
- collector logs show stream acceptance and forwarding
- processor logs should show indexing activity when traffic arrives
- HPA metrics show real CPU values once Metrics Server is working

What to expect when things fail:

- if images are not available to Minikube, pods show `ImagePullBackOff`
- if Metrics Server is unavailable, HPA shows `cpu: <unknown>`
- if the query service cannot find the `logs` index yet, it returns an empty result, not a 500
- if the processor is unavailable, the collector aborts the gRPC call with `UNAVAILABLE`

## Current Project Status

The project has been implemented and verified through:

- gRPC ingestion
- HTTP forwarding to the processor
- Elasticsearch indexing
- HTTP query retrieval
- Docker Compose local runtime
- Kubernetes deployment on Minikube
- live metrics from Metrics Server
- end-to-end sample log validation

## Next Logical Improvements

Reasonable next steps from here:

- add Kafka between collector and processor for buffering and backpressure handling
- add Redis for query caching
- add health endpoints to the collector itself
- add structured JSON logging across all services
- add authentication and authorization for query access
- add tests for collector, processor, and query-service behavior
- make the frontend richer with pagination, timestamps, and result summaries
