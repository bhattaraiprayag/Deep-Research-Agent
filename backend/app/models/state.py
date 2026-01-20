"""
State models for the Deep Research Agent.

Defines the core data structures used throughout the LangGraph workflow.
"""

from typing import Annotated, TypedDict

import operator


class StepLog(TypedDict):
    """Structured log of a single research step."""

    query: str
    outcome: str


class Fact(TypedDict):
    """Atomic unit of information extracted from raw sources."""

    content: str
    source: str
    relevance_score: float


class RawSearchResult(TypedDict):
    """Temporary container for raw search data before curation."""

    title: str
    content: str
    url: str
    score: float


class ResearchState(TypedDict):
    """
    Global state for the LangGraph workflow.

    This state is passed between nodes and accumulates information
    throughout the research process.
    """

    # Input
    task: str

    # Planning
    plan: list[str]

    # Accumulators (use operator.add for merging)
    gathered_facts: Annotated[list[Fact], operator.add]
    past_steps: Annotated[list[StepLog], operator.add]

    # Temporary buffers
    temp_raw_results: list[RawSearchResult]

    # Control flow
    iteration_count: int
    critique_count: int

    # Outputs
    report_content: str
    critique_feedback: str

    # Internal flags
    is_approved: bool
