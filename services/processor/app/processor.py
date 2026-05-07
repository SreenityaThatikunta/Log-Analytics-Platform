import os

from elasticsearch import Elasticsearch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from pipeline import process_log

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://elasticsearch:9200")
ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX", "logs")

app = FastAPI(title="processor")
es = Elasticsearch(ELASTICSEARCH_URL)


class LogPayload(BaseModel):
    service_name: str
    level: str
    message: str
    timestamp: int


def handle_log(log: dict) -> dict:
    doc = process_log(log)
    response = es.index(index=ELASTICSEARCH_INDEX, document=doc)
    body = response.body if hasattr(response, "body") else response
    return {"result": body.get("result", "created"), "document": doc}


@app.get("/health")
def healthcheck() -> dict:
    return {"status": "ok"}


@app.post("/logs")
def ingest_log(log: LogPayload) -> dict:
    try:
        return handle_log(log.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
