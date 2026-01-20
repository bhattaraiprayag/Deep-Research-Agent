"""
FastAPI application entry point.

Configures and initializes the Deep Research Agent API server.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import get_settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler for startup/shutdown events."""
    settings = get_settings()
    logger.info("=" * 60)
    logger.info("Deep Research Agent - Starting Up")
    logger.info("=" * 60)
    logger.info(f"Reasoning Model: {settings.reasoning_model}")
    logger.info(f"Fast Model: {settings.fast_model}")
    logger.info(f"Max Iterations: {settings.max_iterations}")
    logger.info(f"Max Critique Loops: {settings.max_critique_loops}")
    logger.info(f"LangSmith Tracing: {settings.langsmith_tracing}")
    logger.info("=" * 60)

    yield

    logger.info("Deep Research Agent - Shutting Down")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    settings = get_settings()

    app = FastAPI(
        title="Deep Research Agent API",
        description=(
            "An AI-powered research agent that provides transparent, "
            "multi-step information gathering and synthesis with real-time "
            "reasoning visibility."
        ),
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router, prefix="/api/v1")

    @app.get("/", tags=["Root"])
    async def root() -> dict[str, str]:
        """Root endpoint with API information."""
        return {
            "name": "Deep Research Agent API",
            "version": "0.1.0",
            "docs": "/docs",
        }

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=True,
    )
