"""
Pydantic models for structured LLM outputs.

Used with LangChain's with_structured_output for type-safe responses.
"""

from pydantic import BaseModel, Field


class StrategistOutput(BaseModel):
    """Structured output from the Strategist node."""

    search_queries: list[str] = Field(
        description="List of targeted search queries to fill knowledge gaps."
    )
    is_complete: bool = Field(
        description="True if sufficient information has been gathered to write the report."
    )


class CuratorOutput(BaseModel):
    """Structured output from the Curator node."""

    facts: list[str] = Field(description="List of atomic facts extracted from the text.")
    is_relevant: bool = Field(
        description="True if the content is relevant to the user's research task."
    )


class CritiqueOutput(BaseModel):
    """Structured output from the Critic node."""

    approved: bool = Field(
        description="True if the report is accurate, well-cited, and answers the task."
    )
    feedback: str = Field(
        description="Specific instructions for improvement if rejected, or confirmation if approved."
    )
