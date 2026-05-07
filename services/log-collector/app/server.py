from concurrent import futures
import logging
from pathlib import Path
import sys

import grpc

ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from proto.log_pb2_grpc import add_LogServiceServicer_to_server
from handler import LogService


def serve() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_LogServiceServicer_to_server(LogService(), server)
    server.add_insecure_port("[::]:50051")
    logging.getLogger(__name__).info("Starting log collector on port 50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
