# Log Collector

The log collector is the ingestion edge of the platform.

## Responsibility

- implements the gRPC `LogService`
- accepts a client-streaming RPC of `LogEntry` messages
- optionally validates an API key from request metadata
- forwards each log to the processor over HTTP
- returns an `Ack` with the number of processed entries

## Files

- [app/server.py](app/server.py): gRPC server bootstrap
- [app/handler.py](app/handler.py): stream handler implementation
- [app/auth.py](app/auth.py): optional API key validation
- [requirements.txt](requirements.txt): Python dependencies
- [Dockerfile](Dockerfile): container build

## Request Flow

1. Client opens `StreamLogs`.
2. Collector validates the request if `LOG_COLLECTOR_API_KEY` is configured.
3. Collector reads streamed `LogEntry` messages one by one.
4. Collector POSTs each entry to `PROCESSOR_URL`.
5. Collector returns `Ack(status="OK:<count>")`.

## Runtime Configuration

- `PROCESSOR_URL`
  Downstream processor endpoint. Default: `http://processor:8001/logs`
- `LOG_COLLECTOR_API_KEY`
  Optional shared secret checked against `x-api-key` metadata

## Error Behavior

- processor transport failures are mapped to gRPC `UNAVAILABLE`
- unexpected collector failures are mapped to gRPC `INTERNAL`

## Logging

The service logs:

- startup
- stream acceptance
- each forwarded log entry
- downstream forwarding failures
- stream completion counts

## Testing

For local Kubernetes verification, port-forward the collector:

```bash
kubectl port-forward svc/log-collector 50051:50051 -n log-analytics
```

Then send sample scenarios:

```bash
make test-log
LOG_TEST_SCENARIO=payment_error make test-log
LOG_TEST_SCENARIO=search_error make test-log
make test-log-batch
```

Expected result:

- the client prints `OK:<count>`
- collector logs show stream acceptance and forwarding activity

Useful log check:

```bash
kubectl logs -n log-analytics deployment/log-collector --tail=100
```
