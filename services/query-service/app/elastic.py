import os

from elasticsearch import Elasticsearch
from elasticsearch import NotFoundError

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://elasticsearch:9200")
ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX", "logs")

es = Elasticsearch(ELASTICSEARCH_URL)


def search_logs(service: str, level: str) -> dict:
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"service": service}},
                    {"match": {"level": level.upper()}},
                ]
            }
        }
    }
    try:
        response = es.search(index=ELASTICSEARCH_INDEX, body=query)
    except NotFoundError:
        return {
            "took": 0,
            "timed_out": False,
            "hits": {
                "total": {"value": 0, "relation": "eq"},
                "max_score": None,
                "hits": [],
            },
        }
    return response.body if hasattr(response, "body") else response
