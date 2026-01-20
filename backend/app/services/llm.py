"""
LLM client initialization and configuration.

Provides factory functions for obtaining configured LangChain LLM instances.
"""

from functools import lru_cache

from langchain_openai import ChatOpenAI

from app.config import get_settings


@lru_cache
def get_reasoning_llm() -> ChatOpenAI:
    """
    Get the reasoning LLM instance.

    Used for complex tasks: Strategist, Analyst, Critic nodes.
    """
    settings = get_settings()
    return ChatOpenAI(
        model=settings.reasoning_model,
        temperature=0,
        api_key=settings.openai_api_key,
    )


@lru_cache
def get_fast_llm() -> ChatOpenAI:
    """
    Get the fast LLM instance.

    Used for simpler tasks: Curator node (fact extraction).
    """
    settings = get_settings()
    return ChatOpenAI(
        model=settings.fast_model,
        temperature=0,
        api_key=settings.openai_api_key,
    )
