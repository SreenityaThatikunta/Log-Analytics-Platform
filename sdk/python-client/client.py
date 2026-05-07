from pathlib import Path
import sys
import time

import grpc

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from proto.log_pb2 import LogEntry
from proto.log_pb2_grpc import LogServiceStub


SAMPLE_SCENARIOS = {
    "auth_error": {
        "service_name": "auth",
        "level": "error",
        "message": "token expired",
    },
    "auth_warn": {
        "service_name": "auth",
        "level": "warn",
        "message": "refresh token nearing expiry",
    },
    "payment_error": {
        "service_name": "payment",
        "level": "error",
        "message": "card authorization failed",
    },
    "payment_info": {
        "service_name": "payment",
        "level": "info",
        "message": "refund request queued",
    },
    "checkout_info": {
        "service_name": "checkout",
        "level": "info",
        "message": "checkout session started",
    },
    "search_error": {
        "service_name": "search",
        "level": "error",
        "message": "elasticsearch query timeout",
    },
    "inventory_warn": {
        "service_name": "inventory",
        "level": "warn",
        "message": "low stock threshold reached",
    },
}


def build_log_entry(service_name: str, level: str, message: str, timestamp: int | None = None) -> LogEntry:
    return LogEntry(
        service_name=service_name,
        level=level,
        message=message,
        timestamp=timestamp or int(time.time()),
    )


def build_scenario_log(name: str) -> LogEntry:
    scenario = SAMPLE_SCENARIOS[name]
    return build_log_entry(**scenario)


def list_scenarios() -> list[str]:
    return sorted(SAMPLE_SCENARIOS)


def send_logs(entries: list[LogEntry] | None = None, address: str = "localhost:50051") -> str:
    channel = grpc.insecure_channel(address)
    stub = LogServiceStub(channel)
    log_entries = entries or [build_scenario_log("auth_error")]

    def generator():
        for entry in log_entries:
            yield entry

    ack = stub.StreamLogs(generator())
    return ack.status
