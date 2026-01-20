"""
Server-Sent Events (SSE) models for real-time streaming.

Defines structured event types for frontend consumption.
"""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class EventType(str, Enum):
    """Types of events emitted during research execution."""

    # Node lifecycle events
    NODE_START = "node_start"
    NODE_END = "node_end"

    # Agent activity events
    PLANNING = "planning"
    SEARCHING = "searching"
    EXTRACTING = "extracting"
    WRITING = "writing"
    CRITIQUING = "critiquing"

    # Data events
    QUERIES_GENERATED = "queries_generated"
    FACTS_EXTRACTED = "facts_extracted"
    REPORT_CHUNK = "report_chunk"
    REPORT_COMPLETE = "report_complete"

    # Status events
    STATUS_UPDATE = "status_update"
    ERROR = "error"
    COMPLETE = "complete"


class ResearchEvent(BaseModel):
    """Structured event for SSE streaming."""

    event_type: EventType = Field(..., description="Type of the event")
    node: str | None = Field(default=None, description="Current node name")
    data: dict[str, Any] = Field(default_factory=dict, description="Event payload")
    message: str | None = Field(default=None, description="Human-readable message")

    def to_sse(self) -> str:
        """Format as SSE event string."""
        return f"event: {self.event_type.value}\ndata: {self.model_dump_json()}\n\n"
