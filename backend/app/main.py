from fastapi import FastAPI

from app.api.v1 import companies, users
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

app.include_router(companies.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "Club Mziya API is running"}
