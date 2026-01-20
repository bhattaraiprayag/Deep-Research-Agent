"""
FastAPI route definitions.

Defines all API endpoints for the Deep Research Agent.
"""

import logging
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.agent.graph import build_research_graph, create_initial_state
from app.api.streaming import stream_research_events
from app.models.schemas import ErrorResponse, HealthResponse, ResearchRequest

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    tags=["System"],
    summary="Health check endpoint",
)
async def health_check() -> HealthResponse:
    """Check if the service is healthy and return version info."""
    return HealthResponse(status="healthy", version="0.1.0")


@router.post(
    "/research",
    tags=["Research"],
    summary="Execute a research task with SSE streaming",
    responses={
        200: {"description": "SSE stream of research events"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal error"},
    },
)
async def execute_research(request: ResearchRequest) -> StreamingResponse:
    """
    Execute a deep research task and stream results via SSE.

    The response is a Server-Sent Events stream containing:
    - Node lifecycle events (start/end)
    - Search query generation updates
    - Fact extraction progress
    - Report content chunks
    - Completion status

    The frontend can use these events to update the reasoning pane
    and report pane in real-time.
    """
    logger.info(f"Starting research for query: {request.query[:100]}...")

    try:
        graph = build_research_graph()
        initial_state = create_initial_state(request.query)

        return StreamingResponse(
            stream_research_events(graph, initial_state),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            },
        )

    except Exception as e:
        logger.exception("Failed to initialize research")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start research: {str(e)}",
        ) from e


@router.get(
    "/research/status",
    tags=["Research"],
    summary="Get current research capabilities",
)
async def get_research_status() -> dict[str, Any]:
    """Get information about the research agent's current capabilities."""
    from app.config import get_settings
    from app.services.search import get_search_service

    settings = get_settings()
    search_service = get_search_service()

    return {
        "max_iterations": settings.max_iterations,
        "max_critique_loops": settings.max_critique_loops,
        "reasoning_model": settings.reasoning_model,
        "fast_model": settings.fast_model,
        "search_mock_mode": search_service.is_mock_mode,
    }
