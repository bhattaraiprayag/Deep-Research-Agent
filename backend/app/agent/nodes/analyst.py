"""
Analyst Node - The Writer.

Synthesizes gathered facts into a comprehensive Markdown report.
"""

import logging
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from app.models.state import ResearchState
from app.services.llm import get_reasoning_llm

logger = logging.getLogger(__name__)

ANALYST_SYSTEM_PROMPT = """You are a Senior Research Analyst. Your role is to synthesize research findings into a comprehensive report.

Guidelines:
1. Write in clear, professional Markdown format
2. Structure the report with appropriate headings and sections
3. Strictly cite sources using [Source URL] format for every claim
4. Include an Executive Summary at the beginning
5. Organize findings by theme or relevance
6. End with Key Takeaways or Conclusions
7. If you received critique feedback, address those specific issues immediately

Report Structure:
- Executive Summary
- Key Findings (organized by theme)
- Analysis & Insights
- Conclusions & Recommendations
- Sources

Important: Every factual claim must be attributed to its source.
"""


def _format_context_block(state: ResearchState) -> str:
    """Format gathered facts into a numbered context block."""
    gathered = state.get("gathered_facts", [])
    if not gathered:
        return "No facts available."

    lines = []
    for idx, item in enumerate(gathered, 1):
        lines.append(f"[{idx}] {item['content']} (Source: {item['source']})")

    return "\n".join(lines)


def analyst_node(state: ResearchState) -> dict[str, Any]:
    """
    Synthesize gathered facts into a research report.

    Addresses any feedback from previous critique if present.

    Args:
        state: Current research state with gathered facts.

    Returns:
        Updated state with report content.
    """
    task = state["task"]
    critique = state.get("critique_feedback", "")

    logger.info("[Analyst] Synthesizing research report")

    context_block = _format_context_block(state)

    user_content = f"""Task: {task}

Research Context:
{context_block}"""

    if critique:
        user_content += f"""

CRITICAL FEEDBACK FROM PREVIOUS DRAFT:
{critique}

Address these issues in your revised report."""
        logger.info("[Analyst] Addressing critique feedback")

    llm = get_reasoning_llm()
    response = llm.invoke([
        SystemMessage(content=ANALYST_SYSTEM_PROMPT),
        HumanMessage(content=user_content),
    ])

    report = response.content if isinstance(response.content, str) else str(response.content)
    logger.info(f"[Analyst] Generated report ({len(report)} chars)")

    return {"report_content": report}
