"""
LLM client initialization and configuration.

Provides factory functions for obtaining configured LangChain LLM instances
with Prometheus metrics integration.
"""

import time
from functools import lru_cache
from typing import Any

from langchain_core.callbacks import BaseCallbackHandler
from langchain_openai import ChatOpenAI

from app.config import get_settings
from app.metrics import (
    llm_call_duration_seconds,
    llm_calls_total,
    llm_tokens_total,
)


class MetricsCallbackHandler(BaseCallbackHandler):
    """Callback handler for tracking LLM metrics."""

    def __init__(self, model: str, node: str = "unknown") -> None:
        self.model = model
        self.node = node
        self._start_time: float | None = None

    def on_llm_start(self, *_args: Any, **_kwargs: Any) -> None:
        """Record LLM call start time."""
        self._start_time = time.perf_counter()

    def on_llm_end(self, response: Any, **_kwargs: Any) -> None:
        """Record LLM call metrics on completion."""
        if self._start_time:
            duration = time.perf_counter() - self._start_time
            llm_call_duration_seconds.labels(
                model=self.model,
                node=self.node,
            ).observe(duration)

        llm_calls_total.labels(
            model=self.model,
            node=self.node,
            status="success",
        ).inc()

        # Extract token usage if available
        if hasattr(response, "llm_output") and response.llm_output:
            token_usage = response.llm_output.get("token_usage", {})
            if token_usage:
                prompt_tokens = token_usage.get("prompt_tokens", 0)
                completion_tokens = token_usage.get("completion_tokens", 0)

                llm_tokens_total.labels(
                    model=self.model,
                    type="prompt",
                    node=self.node,
                ).inc(prompt_tokens)

                llm_tokens_total.labels(
                    model=self.model,
                    type="completion",
                    node=self.node,
                ).inc(completion_tokens)

    def on_llm_error(self, _error: Exception, **_kwargs: Any) -> None:  # type: ignore[override]
        """Record LLM call error."""
        llm_calls_total.labels(
            model=self.model,
            node=self.node,
            status="failure",
        ).inc()


def get_reasoning_llm_with_metrics(node: str = "unknown") -> ChatOpenAI:
    """
    Get a reasoning LLM instance with metrics tracking.

    Args:
        node: Name of the node using this LLM for labeling.

    Returns:
        ChatOpenAI instance with metrics callback.
    """
    settings = get_settings()
    return ChatOpenAI(
        model=settings.reasoning_model,
        temperature=0,
        api_key=settings.openai_api_key,
        callbacks=[MetricsCallbackHandler(settings.reasoning_model, node)],
    )


def get_fast_llm_with_metrics(node: str = "unknown") -> ChatOpenAI:
    """
    Get a fast LLM instance with metrics tracking.

    Args:
        node: Name of the node using this LLM for labeling.

    Returns:
        ChatOpenAI instance with metrics callback.
    """
    settings = get_settings()
    return ChatOpenAI(
        model=settings.fast_model,
        temperature=0,
        api_key=settings.openai_api_key,
        callbacks=[MetricsCallbackHandler(settings.fast_model, node)],
    )


@lru_cache
def get_reasoning_llm() -> ChatOpenAI:
    """
    Get the reasoning LLM instance (legacy, without per-node metrics).

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
    Get the fast LLM instance (legacy, without per-node metrics).

    Used for simpler tasks: Curator node (fact extraction).
    """
    settings = get_settings()
    return ChatOpenAI(
        model=settings.fast_model,
        temperature=0,
        api_key=settings.openai_api_key,
    )
