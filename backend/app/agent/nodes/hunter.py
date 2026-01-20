"""
Hunter Node - The Executor.

Executes search queries asynchronously and filters results by relevance.
"""

import logging
from typing import Any

from app.models.state import RawSearchResult, ResearchState, StepLog
from app.services.search import get_search_service

logger = logging.getLogger(__name__)


async def hunter_node(state: ResearchState) -> dict[str, Any]:
    """
    Execute search queries and gather raw results.

    Performs parallel searches, filters by relevance score,
    and deduplicates by URL.

    Args:
        state: Current research state containing the search plan.

    Returns:
        Updated state with raw results and step logs.
    """
    plan = state.get("plan", [])
    if not plan:
        return {
            "temp_raw_results": [],
            "past_steps": [],
            "iteration_count": state.get("iteration_count", 0) + 1,
        }

    current_facts = state.get("gathered_facts", [])
    existing_urls = {item["source"] for item in current_facts}

    logger.info(f"[Hunter] Executing {len(plan)} queries in parallel")

    search_service = get_search_service()
    results_by_query = await search_service.search_batch(plan)

    raw_results_batch: list[RawSearchResult] = []
    step_logs: list[StepLog] = []

    for query, results in results_by_query.items():
        if not results:
            step_logs.append(StepLog(query=query, outcome="No relevant results found"))
            logger.debug(f"[Hunter] Query '{query[:50]}...': No results")
            continue

        count_new = 0
        for res in results:
            url = res["url"]
            if url in existing_urls:
                continue

            raw_results_batch.append(res)
            existing_urls.add(url)
            count_new += 1

        outcome = f"Found {count_new} new sources"
        step_logs.append(StepLog(query=query, outcome=outcome))
        logger.debug(f"[Hunter] Query '{query[:50]}...': {outcome}")

    logger.info(f"[Hunter] Collected {len(raw_results_batch)} new sources total")

    return {
        "temp_raw_results": raw_results_batch,
        "past_steps": step_logs,
        "iteration_count": state.get("iteration_count", 0) + 1,
    }
