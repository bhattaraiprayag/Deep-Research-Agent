"""
Research Agent Graph Construction.

Builds the LangGraph state machine that orchestrates the research workflow.
"""

import logging
from typing import Any

from langgraph.graph import END, StateGraph

from app.agent.edges import route_critic, route_strategist
from app.agent.nodes import (
    analyst_node,
    critic_node,
    curator_node,
    hunter_node,
    strategist_node,
)
from app.models.state import ResearchState

logger = logging.getLogger(__name__)


def build_research_graph() -> Any:
    """
    Build and compile the research agent graph.

    The graph follows this flow:
    Start -> Strategist -> [Hunter -> Curator -> Strategist]* -> Analyst -> [Critic -> Analyst]* -> End

    Returns:
        Compiled LangGraph ready for execution.
    """
    logger.info("Building research agent graph")

    workflow = StateGraph(ResearchState)

    workflow.add_node("strategist", strategist_node)
    workflow.add_node("hunter", hunter_node)
    workflow.add_node("curator", curator_node)
    workflow.add_node("analyst", analyst_node)
    workflow.add_node("critic", critic_node)

    workflow.set_entry_point("strategist")

    workflow.add_conditional_edges(
        "strategist",
        route_strategist,
        {
            "hunter": "hunter",
            "analyst": "analyst",
        },
    )

    workflow.add_edge("hunter", "curator")
    workflow.add_edge("curator", "strategist")
    workflow.add_edge("analyst", "critic")

    workflow.add_conditional_edges(
        "critic",
        route_critic,
        {
            "analyst": "analyst",
            "__end__": END,
        },
    )

    compiled = workflow.compile()
    logger.info("Research agent graph compiled successfully")

    return compiled


def create_initial_state(task: str) -> ResearchState:
    """
    Create the initial state for a research task.

    Args:
        task: The research query/task to investigate.

    Returns:
        Initialized ResearchState ready for graph execution.
    """
    return ResearchState(
        task=task,
        plan=[],
        gathered_facts=[],
        past_steps=[],
        temp_raw_results=[],
        iteration_count=0,
        critique_count=0,
        report_content="",
        critique_feedback="",
        is_approved=False,
    )
