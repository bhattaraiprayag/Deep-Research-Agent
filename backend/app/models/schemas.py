"""
API request/response schemas for the Deep Research Agent.

Uses Pydantic models for validation and serialization.
"""

from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    """Request body for initiating a research task."""

    query: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="The research query to investigate",
        examples=["What are the emerging skills needed for AI Product Managers in 2025?"],
    )


class ResearchResponse(BaseModel):
    """Final response containing the research report."""

    task: str = Field(..., description="The original research query")
    report: str = Field(..., description="The synthesized research report in Markdown")
    facts_count: int = Field(..., description="Number of facts gathered during research")
    sources_count: int = Field(..., description="Number of unique sources cited")
    iterations: int = Field(..., description="Number of research iterations performed")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(default="healthy", description="Service health status")
    version: str = Field(default="0.1.0", description="API version")


class ErrorResponse(BaseModel):
    """Standardized error response."""

    error: str = Field(..., description="Error message")
    detail: str | None = Field(default=None, description="Additional error details")
