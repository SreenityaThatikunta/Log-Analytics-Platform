def process_log(log: dict) -> dict:
    return {
        "service": log["service_name"],
        "level": log["level"].upper(),
        "message": log["message"],
        "timestamp": log["timestamp"],
    }
