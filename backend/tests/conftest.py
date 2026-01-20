"""
Pytest configuration and shared fixtures.

Provides common fixtures for unit and integration tests.
"""

import os
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

os.environ.setdefault("OPENAI_API_KEY", "test-api-key")
os.environ.setdefault("TAVILY_API_KEY", "test-tavily-key")


@pytest.fixture
def sample_task() -> str:
    """Sample research task for testing."""
    return "What are the key trends in AI product management for 2025?"


@pytest.fixture
def mock_settings() -> MagicMock:
    """Mocked settings object."""
    settings = MagicMock()
    settings.openai_api_key = "test-key"
    settings.tavily_api_key = "test-tavily-key"
    settings.max_iterations = 3
    settings.max_critique_loops = 2
    settings.reasoning_model = "gpt-4o"
    settings.fast_model = "gpt-4o-mini"
    settings.cors_origin_list = ["http://localhost:3000"]
    return settings


@pytest.fixture
def sample_facts() -> list[dict[str, Any]]:
    """Sample gathered facts for testing."""
    return [
        {
            "content": "AI Product Managers need to understand ML lifecycle management.",
            "source": "https://example.com/article1",
            "relevance_score": 0.9,
        },
        {
            "content": "Cross-functional collaboration is essential for AI PM roles.",
            "source": "https://example.com/article2",
            "relevance_score": 0.85,
        },
    ]


@pytest.fixture
def sample_research_state(sample_task: str) -> dict[str, Any]:
    """Sample research state for testing."""
    return {
        "task": sample_task,
        "plan": [],
        "gathered_facts": [],
        "past_steps": [],
        "temp_raw_results": [],
        "iteration_count": 0,
        "critique_count": 0,
        "report_content": "",
        "critique_feedback": "",
        "is_approved": False,
    }


@pytest.fixture
def sample_raw_results() -> list[dict[str, Any]]:
    """Sample raw search results for testing."""
    return [
        {
            "title": "AI PM Trends 2025",
            "content": "Key skills for AI PMs include understanding model evaluation, "
                       "data pipelines, and stakeholder communication.",
            "url": "https://example.com/ai-pm-trends",
            "score": 0.92,
        },
        {
            "title": "Future of Product Management",
            "content": "Product managers working with AI need to bridge the gap between "
                       "technical teams and business stakeholders.",
            "url": "https://example.com/future-pm",
            "score": 0.88,
        },
    ]


@pytest.fixture
def mock_llm_response():
    """Factory for mocking LLM responses."""
    def _create_mock(content: str | dict[str, Any]):
        mock = MagicMock()
        if isinstance(content, dict):
            for key, value in content.items():
                setattr(mock, key, value)
        else:
            mock.content = content
        return mock
    return _create_mock
