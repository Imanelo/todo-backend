from fastapi import FastAPI
from app.routers import tasks

app = FastAPI(
    title="Task Tracker API",
    description="A lightweight REST API for managing tasks with in-memory storage.",
    version="1.0.0",
)

app.include_router(tasks.router)


@app.get("/", tags=["root"], summary="Root endpoint")
def read_root() -> dict[str, str]:
    return {
        "message": "Welcome to the Task Tracker API",
        "docs_url": "/docs",
    }


@app.get("/health", tags=["health"], summary="Health check")
def health_check() -> dict[str, str]:
    return {"status": "ok"}

