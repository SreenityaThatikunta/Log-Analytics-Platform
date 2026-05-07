# Proto

This folder contains the shared gRPC contract for the ingestion pipeline.

## Files

- [log.proto](/Users/sreenityathatikunta/Documents/Projects/log-analytics-platform/proto/log.proto): source protobuf definition
- [log_pb2.py](/Users/sreenityathatikunta/Documents/Projects/log-analytics-platform/proto/log_pb2.py): generated protobuf Python messages
- [log_pb2_grpc.py](/Users/sreenityathatikunta/Documents/Projects/log-analytics-platform/proto/log_pb2_grpc.py): generated gRPC Python service bindings

## Contract

The package is `log`.

Service:

- `LogService`
  Client-streaming RPC `StreamLogs(stream LogEntry) returns (Ack)`

Messages:

- `LogEntry`
  `service_name`, `level`, `message`, `timestamp`
- `Ack`
  `status`

## Purpose

This contract is shared by:

- the log collector, which implements `LogService`
- the Python SDK, which constructs `LogEntry` messages and calls `StreamLogs`

## Regeneration

To regenerate Python bindings:

```bash
./scripts/generate_proto.sh
```

That script runs `grpc_tools.protoc` against `proto/log.proto`.

