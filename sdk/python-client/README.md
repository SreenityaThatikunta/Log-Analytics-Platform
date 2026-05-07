# Python Client SDK

This folder provides a simple sample producer for the gRPC collector.

## Files

- [client.py](client.py): gRPC client helpers and built-in scenarios
- [example.py](example.py): CLI-style entrypoint used by the `Makefile`

## Main Functions

- `send_logs(...)`
  Sends one or more `LogEntry` messages over gRPC
- `build_scenario_log(name)`
  Builds a named sample log
- `list_scenarios()`
  Returns the available scenario names

## Built-in Test Scenarios

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
  Sends all scenarios in one stream

## Environment Variables

- `LOG_COLLECTOR_ADDRESS`
  Collector address. Default: `localhost:50051`
- `LOG_TEST_SCENARIO`
  Scenario name consumed by `example.py`

## Common Commands

List available scenarios:

```bash
make test-log-list
```

Send the default scenario:

```bash
make test-log
```

Send a named scenario:

```bash
LOG_TEST_SCENARIO=payment_error make test-log
LOG_TEST_SCENARIO=inventory_warn make test-log
```

Send all scenarios:

```bash
make test-log-batch
```

## Validation Queries

```bash
curl "http://localhost:8000/logs?service=auth&level=error"
curl "http://localhost:8000/logs?service=auth&level=warn"
curl "http://localhost:8000/logs?service=payment&level=error"
curl "http://localhost:8000/logs?service=payment&level=info"
curl "http://localhost:8000/logs?service=checkout&level=info"
curl "http://localhost:8000/logs?service=search&level=error"
curl "http://localhost:8000/logs?service=inventory&level=warn"
```

## Port-Forward Requirement

When testing against Kubernetes, `make test-log` only works while the collector port-forward is active:

```bash
kubectl port-forward svc/log-collector 50051:50051 -n log-analytics
```
