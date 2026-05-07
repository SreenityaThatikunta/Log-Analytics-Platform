"""Minimal generated gRPC module for log.proto."""

import grpc

from proto import log_pb2 as log__pb2


class LogServiceStub:
    def __init__(self, channel: grpc.Channel) -> None:
        self.StreamLogs = channel.stream_unary(
            "/log.LogService/StreamLogs",
            request_serializer=log__pb2.LogEntry.SerializeToString,
            response_deserializer=log__pb2.Ack.FromString,
        )


class LogServiceServicer:
    def StreamLogs(self, request_iterator, context):
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented")
        raise NotImplementedError("Method not implemented")


def add_LogServiceServicer_to_server(servicer, server) -> None:
    rpc_method_handlers = {
        "StreamLogs": grpc.stream_unary_rpc_method_handler(
            servicer.StreamLogs,
            request_deserializer=log__pb2.LogEntry.FromString,
            response_serializer=log__pb2.Ack.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "log.LogService", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


__all__ = [
    "LogServiceServicer",
    "LogServiceStub",
    "add_LogServiceServicer_to_server",
]
