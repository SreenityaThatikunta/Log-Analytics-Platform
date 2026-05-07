from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import router

app = FastAPI(title="query-service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://frontend:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


@app.get("/health")
def healthcheck() -> dict:
    return {"status": "ok"}
