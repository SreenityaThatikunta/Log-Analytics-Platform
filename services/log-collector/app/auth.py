import os

import grpc


def validate_api_key(context: grpc.ServicerContext) -> None:
    expected = os.getenv("LOG_COLLECTOR_API_KEY")
    if not expected:
        return

    metadata = dict(context.invocation_metadata())
    if metadata.get("x-api-key") != expected:
        context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid API key")
