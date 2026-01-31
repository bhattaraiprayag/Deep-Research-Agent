"""
FastAPI application entry point.

Configures and initializes the Deep Research Agent API server.
"""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.routes import router
from app.config import get_settings
from app.metrics import set_app_info

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

APP_VERSION = "0.2.0"


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan handler for startup/shutdown events."""
    settings = get_settings()

    # Set app info metrics
    set_app_info(
        version=APP_VERSION,
        reasoning_model=settings.reasoning_model,
        fast_model=settings.fast_model,
    )

    logger.info("=" * 60)
    logger.info("Deep Research Agent - Starting Up")
    logger.info("=" * 60)
    logger.info(f"Version: {APP_VERSION}")
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
        version=APP_VERSION,
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

    Instrumentator().instrument(app).expose(app)

    @app.get("/", tags=["Root"])
    async def root() -> dict[str, str]:
        """Root endpoint with API information."""
        return {
            "name": "Deep Research Agent API",
            "version": APP_VERSION,
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
