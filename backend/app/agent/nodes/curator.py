"""
Curator Node - The Distiller.

Extracts atomic facts from raw search results using a fast LLM.
Prevents context window pollution through summarization.
"""

import asyncio
import hashlib
import logging
from typing import Any

from langchain_core.messages import SystemMessage

from app.agent.nodes.schemas import CuratorOutput
from app.models.state import Fact, RawSearchResult, ResearchState
from app.services.llm import get_fast_llm

logger = logging.getLogger(__name__)


def _create_extraction_prompt(task: str, content: str) -> str:
    """Generate the fact extraction prompt."""
    return f"""Analyze the following text regarding the user task: '{task}'.

Extract key facts, statistics, insights, or findings. Rules:
1. Each fact should be atomic (single piece of information)
2. Include specific numbers, dates, or names when available
3. Discard promotional content or fluff
4. If the text is irrelevant to the task, set is_relevant=False

Text:
{content}"""


async def _extract_facts_from_item(
    task: str,
    item: RawSearchResult,
) -> list[Fact]:
    """Extract facts from a single search result."""
    prompt = _create_extraction_prompt(task, item["content"])

    try:
        llm = get_fast_llm()
        structured_llm = llm.with_structured_output(CuratorOutput)
        response = await structured_llm.ainvoke([SystemMessage(content=prompt)])

        if response.is_relevant and response.facts:
            return [
                Fact(
                    content=fact,
                    source=item["url"],
                    relevance_score=item["score"],
                )
                for fact in response.facts
            ]
    except Exception as e:
        logger.warning(f"[Curator] Extraction error: {e}")

    return []


def _deduplicate_facts(
    new_facts: list[Fact],
    existing_facts: list[Fact],
) -> list[Fact]:
    """Remove duplicate facts based on content hash."""
    seen_hashes: set[str] = set()

    for existing in existing_facts:
        h = hashlib.md5(existing["content"].encode()).hexdigest()
        seen_hashes.add(h)

    unique_facts: list[Fact] = []
    for fact in new_facts:
        h = hashlib.md5(fact["content"].encode()).hexdigest()
        if h not in seen_hashes:
            unique_facts.append(fact)
            seen_hashes.add(h)

    return unique_facts


async def curator_node(state: ResearchState) -> dict[str, Any]:
    """
    Extract and deduplicate facts from raw search results.

    Uses a fast LLM to distill raw content into atomic facts,
    preventing context window pollution.

    Args:
        state: Current research state with raw results buffer.

    Returns:
        Updated state with new gathered facts and cleared buffer.
    """
    raw_results = state.get("temp_raw_results", [])

    if not raw_results:
        logger.info("[Curator] No raw results to process")
        return {"gathered_facts": [], "temp_raw_results": []}

    task = state["task"]
    logger.info(f"[Curator] Processing {len(raw_results)} raw sources")

    extraction_tasks = [
        _extract_facts_from_item(task, item)
        for item in raw_results
    ]
    extraction_results = await asyncio.gather(*extraction_tasks)

    all_new_facts: list[Fact] = []
    for facts in extraction_results:
        all_new_facts.extend(facts)

    existing_facts = state.get("gathered_facts", [])
    unique_facts = _deduplicate_facts(all_new_facts, existing_facts)

    logger.info(
        f"[Curator] Extracted {len(all_new_facts)} facts, "
        f"{len(unique_facts)} unique after deduplication"
    )

    return {
        "gathered_facts": unique_facts,
        "temp_raw_results": [],
    }
