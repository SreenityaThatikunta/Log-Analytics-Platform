from fastapi import APIRouter

from elastic import search_logs

router = APIRouter()


@router.get("/logs")
def get_logs(service: str, level: str) -> dict:
    return search_logs(service, level)
