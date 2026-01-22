"""
Strategist Node - The Planner.

Analyzes gathered facts and plans the next research steps by
identifying knowledge gaps and generating targeted search queries.
"""

import json
import logging
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from app.agent.nodes.schemas import StrategistOutput
from app.config import get_settings
from app.models.state import ResearchState
from app.services.llm import get_reasoning_llm

logger = logging.getLogger(__name__)

STRATEGIST_SYSTEM_PROMPT = """You are a Senior Research Strategist. Your role is to plan research for user tasks.

Guidelines:
1. Analyze the Task and Current Knowledge carefully.
2. Identify specific knowledge gaps that need to be filled.
3. Generate up to 3 targeted, specific search queries.
4. If sufficient information exists to write a comprehensive report, set is_complete=True.
5. Learn from Past Steps to avoid redundant or previously failed queries.
6. Focus on different angles and perspectives of the topic.

Search Query Tips:
- Be specific and targeted
- Include relevant years, names, or technical terms
- Avoid overly broad queries
- Consider different aspects: technical, business, societal impacts
"""


def _compress_context(state: ResearchState) -> str:
    """Compress gathered facts into a summary for token efficiency."""
    gathered = state.get("gathered_facts", [])
    if not gathered:
        return "No facts gathered yet."

    summaries = []
    for item in gathered:
        content_preview = item["content"][:200]
        summaries.append(f"- {content_preview}... (Source: {item['source']})")

    return "\n".join(summaries)


def _format_past_steps(state: ResearchState) -> str:
    """Format past steps log for context."""
    past_steps = state.get("past_steps", [])
    if not past_steps:
        return "No previous steps."
    return json.dumps(past_steps, default=str)


def strategist_node(state: ResearchState) -> dict[str, Any]:
    """
    Plan the next research steps.

    Reflects on gathered facts and past steps to generate targeted
    search queries or signal completion.

    Args:
        state: Current research state.

    Returns:
        Updated state with new plan and iteration count.
    """
    settings = get_settings()
    task = state["task"]
    iteration = state.get("iteration_count", 0)

    logger.info(f"[Strategist] Iteration {iteration}/{settings.max_iterations}")

    if iteration >= settings.max_iterations:
        logger.info("[Strategist] Max iterations reached. Moving to synthesis.")
        return {"plan": [], "iteration_count": iteration}

    context_summary = _compress_context(state)
    past_steps_log = _format_past_steps(state)

    user_message = f"""Task: {task}

Current Knowledge Summary:
{context_summary}

Past Steps Log:
{past_steps_log}

Iteration: {iteration}/{settings.max_iterations}"""

    llm = get_reasoning_llm()
    structured_llm = llm.with_structured_output(StrategistOutput)

    response = structured_llm.invoke(
        [
            SystemMessage(content=STRATEGIST_SYSTEM_PROMPT),
            HumanMessage(content=user_message),
        ]
    )

    if response.is_complete:
        logger.info("[Strategist] Sufficient information gathered. Moving to synthesis.")
        return {"plan": [], "iteration_count": iteration}

    logger.info(f"[Strategist] Generated {len(response.search_queries)} queries")
    for i, query in enumerate(response.search_queries, 1):
        logger.debug(f"  Query {i}: {query}")

    return {
        "plan": response.search_queries,
        "iteration_count": iteration,
    }
