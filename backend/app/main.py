from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from app.routes.path import router as path_router
from app.core.config import settings

app = FastAPI(
    title="PathForge API",
    description="Adaptive learning path generator powered by LangGraph + FAISS",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,  # ← from .env, not hardcoded
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(path_router, prefix="/api/v1", tags=["path"])


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "pathforge-api",
        "environment": settings.ENVIRONMENT
    }


@app.on_event("startup")
async def startup():
    logger.info(f"PathForge API started | env={settings.ENVIRONMENT}")
    logger.info(f"CORS origins: {settings.origins_list}")
    logger.info(f"FAISS index path: {settings.FAISS_INDEX_PATH}")