"""
Critic Node - The Reviewer.

Reviews the Analyst's report for accuracy, citation quality, and task alignment.
"""

import logging
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from app.agent.nodes.schemas import CritiqueOutput
from app.models.state import ResearchState
from app.services.llm import get_reasoning_llm_with_metrics

logger = logging.getLogger(__name__)

CRITIC_SYSTEM_PROMPT = """You are a Research Quality Critic. Your role is to rigorously review research reports.

Evaluation Criteria:
1. Factual Accuracy: Are all claims supported by the provided context?
2. Citation Quality: Are sources properly cited for each claim?
3. Task Alignment: Does the report fully answer the user's research question?
4. Completeness: Are there significant gaps in coverage?
5. Clarity: Is the report well-structured and clear?

Decision Guidelines:
- Set approved=True only if all criteria are satisfactorily met
- If rejecting, provide specific, actionable feedback
- Point to exact issues: missing citations, unsupported claims, gaps
- Be constructive but thorough

Output JSON with 'approved' (bool) and 'feedback' (str).
"""


def _format_verification_context(state: ResearchState) -> str:
    """Format gathered facts for verification."""
    gathered = state.get("gathered_facts", [])
    if not gathered:
        return "No context provided."

    return "\n".join([f"- {f['content']} ({f['source']})" for f in gathered])


def critic_node(state: ResearchState) -> dict[str, Any]:
    """
    Review and critique the research report.

    Verifies factual claims against gathered evidence and
    checks citation accuracy.

    Args:
        state: Current research state with report content.

    Returns:
        Updated state with critique feedback and approval status.
    """
    report = state.get("report_content", "")
    task = state["task"]
    critique_count = state.get("critique_count", 0)

    logger.info(f"[Critic] Reviewing report (attempt {critique_count + 1})")

    context_block = _format_verification_context(state)

    user_message = f"""Task: {task}

Available Context/Evidence:
{context_block}

Report Draft to Review:
{report}"""

    llm = get_reasoning_llm_with_metrics(node="critic")
    structured_llm = llm.with_structured_output(CritiqueOutput)

    response = structured_llm.invoke(
        [
            SystemMessage(content=CRITIC_SYSTEM_PROMPT),
            HumanMessage(content=user_message),
        ]
    )

    result = {
        "critique_feedback": response.feedback,
        "critique_count": critique_count + 1,
        "is_approved": response.approved,
    }

    if response.approved:
        logger.info("[Critic] Report approved")
    else:
        logger.info(f"[Critic] Report rejected: {response.feedback[:100]}...")

    return result
