"""
FastAPI dependency injection functions.

Provides common dependencies for route handlers.
"""

from typing import Annotated, Any

from fastapi import Depends

from app.agent.graph import build_research_graph
from app.config import Settings, get_settings
from app.services.llm import get_fast_llm, get_reasoning_llm
from app.services.search import SearchService, get_search_service


SettingsDep = Annotated[Settings, Depends(get_settings)]
SearchServiceDep = Annotated[SearchService, Depends(get_search_service)]


def get_research_graph() -> Any:
    """Get the compiled research graph."""
    return build_research_graph()


ResearchGraphDep = Annotated[Any, Depends(get_research_graph)]
