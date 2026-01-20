"""
Conditional edge routing logic for the research graph.

Defines functions that determine graph transitions based on state.
"""

import logging
from typing import Literal

from app.config import get_settings
from app.models.state import ResearchState

logger = logging.getLogger(__name__)


def route_strategist(state: ResearchState) -> Literal["hunter", "analyst"]:
    """
    Route from Strategist to next node.

    Args:
        state: Current research state.

    Returns:
        "hunter" if there are queries to execute, "analyst" otherwise.
    """
    plan = state.get("plan", [])

    if not plan:
        logger.debug("[Edge] Strategist -> Analyst (no more queries)")
        return "analyst"

    logger.debug(f"[Edge] Strategist -> Hunter ({len(plan)} queries)")
    return "hunter"


def route_critic(state: ResearchState) -> Literal["analyst", "__end__"]:
    """
    Route from Critic to next node.

    Args:
        state: Current research state with critique results.

    Returns:
        "__end__" if approved or max loops reached, "analyst" to revise.
    """
    settings = get_settings()
    critique_count = state.get("critique_count", 0)
    is_approved = state.get("is_approved", False)
    feedback = state.get("critique_feedback", "")

    if critique_count >= settings.max_critique_loops:
        logger.info("[Edge] Critic -> END (max critique loops reached)")
        return "__end__"

    if is_approved:
        logger.info("[Edge] Critic -> END (report approved)")
        return "__end__"

    if "No critical issues" in feedback or len(feedback) < 10:
        logger.info("[Edge] Critic -> END (feedback indicates approval)")
        return "__end__"

    logger.info(f"[Edge] Critic -> Analyst (revision needed, attempt {critique_count})")
    return "analyst"
