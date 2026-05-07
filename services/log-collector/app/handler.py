import logging
import os
from pathlib import Path
import sys

import requests
from requests import RequestException

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import grpc

from auth import validate_api_key
from proto.log_pb2 import Ack
from proto.log_pb2_grpc import LogServiceServicer


PROCESSOR_URL = os.getenv("PROCESSOR_URL", "http://processor:8001/logs")
logger = logging.getLogger(__name__)


class LogService(LogServiceServicer):
    def StreamLogs(self, request_iterator, context):
        validate_api_key(context)

        count = 0
        logger.info("Accepted new log stream")

        try:
            for log in request_iterator:
                payload = {
                    "service_name": log.service_name,
                    "level": log.level,
                    "message": log.message,
                    "timestamp": log.timestamp,
                }
                logger.info(
                    "Forwarding log entry",
                    extra={
                        "service_name": log.service_name,
                        "level": log.level,
                        "timestamp": log.timestamp,
                    },
                )
                response = requests.post(PROCESSOR_URL, json=payload, timeout=5)
                response.raise_for_status()
                count += 1
        except RequestException as exc:
            logger.exception("Processor request failed")
            context.abort(
                grpc.StatusCode.UNAVAILABLE,
                f"Failed to forward logs to processor: {exc}",
            )
        except Exception as exc:
            logger.exception("Collector stream processing failed")
            context.abort(
                grpc.StatusCode.INTERNAL,
                f"Collector failed while processing stream: {exc}",
            )

        logger.info("Completed log stream with %s entries", count)
        return Ack(status=f"OK:{count}")
