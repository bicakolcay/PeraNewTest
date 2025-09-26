from fastapi import FastAPI

from .api.v1.campaigns import router as campaigns_router

app = FastAPI(title="Campaign Manager API")


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Basic health check endpoint."""
    return {"status": "ok"}


app.include_router(campaigns_router, prefix="/api/v1/campaigns", tags=["campaigns"])
