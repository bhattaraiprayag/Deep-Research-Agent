"""
SSE streaming utilities.

Provides functions to stream research events to the frontend.
"""

import json
import logging
from collections.abc import AsyncGenerator
from typing import Any

from app.models.events import EventType, ResearchEvent

logger = logging.getLogger(__name__)


def format_sse_event(event: ResearchEvent) -> str:
    """Format a ResearchEvent as an SSE string."""
    return f"event: {event.event_type.value}\ndata: {event.model_dump_json()}\n\n"


def create_event(
    event_type: EventType,
    node: str | None = None,
    data: dict[str, Any] | None = None,
    message: str | None = None,
) -> str:
    """Create and format an SSE event."""
    event = ResearchEvent(
        event_type=event_type,
        node=node,
        data=data or {},
        message=message,
    )
    return format_sse_event(event)


async def stream_research_events(
    graph: Any,
    initial_state: dict[str, Any],
) -> AsyncGenerator[str, None]:
    """
    Stream research execution events via SSE.

    Args:
        graph: Compiled LangGraph.
        initial_state: Initial research state.

    Yields:
        SSE-formatted event strings.
    """
    yield create_event(
        EventType.STATUS_UPDATE,
        message="Starting research...",
        data={"status": "starting"},
    )

    final_report = ""
    facts_count = 0
    sources: set[str] = set()

    try:
        async for event in graph.astream(initial_state):
            for node_name, node_output in event.items():
                yield create_event(
                    EventType.NODE_START,
                    node=node_name,
                    message=f"Executing {node_name}",
                )

                if node_name == "strategist":
                    plan = node_output.get("plan", [])
                    if plan:
                        yield create_event(
                            EventType.QUERIES_GENERATED,
                            node=node_name,
                            data={"queries": plan},
                            message=f"Generated {len(plan)} search queries",
                        )
                    else:
                        yield create_event(
                            EventType.PLANNING,
                            node=node_name,
                            message="Research planning complete, moving to synthesis",
                        )

                elif node_name == "hunter":
                    steps = node_output.get("past_steps", [])
                    yield create_event(
                        EventType.SEARCHING,
                        node=node_name,
                        data={"steps": steps},
                        message=f"Completed {len(steps)} searches",
                    )

                elif node_name == "curator":
                    new_facts = node_output.get("gathered_facts", [])
                    facts_count += len(new_facts)
                    for fact in new_facts:
                        sources.add(fact.get("source", ""))

                    yield create_event(
                        EventType.FACTS_EXTRACTED,
                        node=node_name,
                        data={
                            "new_facts_count": len(new_facts),
                            "total_facts": facts_count,
                        },
                        message=f"Extracted {len(new_facts)} new facts",
                    )

                elif node_name == "analyst":
                    report = node_output.get("report_content", "")
                    if report:
                        final_report = report
                        yield create_event(
                            EventType.REPORT_CHUNK,
                            node=node_name,
                            data={"content": report},
                            message="Report generated",
                        )

                elif node_name == "critic":
                    is_approved = node_output.get("is_approved", False)
                    feedback = node_output.get("critique_feedback", "")
                    yield create_event(
                        EventType.CRITIQUING,
                        node=node_name,
                        data={
                            "approved": is_approved,
                            "feedback": feedback[:200] if feedback else "",
                        },
                        message="Approved" if is_approved else "Revision requested",
                    )

                yield create_event(
                    EventType.NODE_END,
                    node=node_name,
                    message=f"Completed {node_name}",
                )

        yield create_event(
            EventType.REPORT_COMPLETE,
            data={
                "report": final_report,
                "facts_count": facts_count,
                "sources_count": len(sources),
            },
            message="Research complete",
        )

        yield create_event(
            EventType.COMPLETE,
            data={"status": "complete"},
            message="Research finished successfully",
        )

    except Exception as e:
        logger.exception("Error during research execution")
        yield create_event(
            EventType.ERROR,
            data={"error": str(e)},
            message=f"Research failed: {str(e)}",
        )
