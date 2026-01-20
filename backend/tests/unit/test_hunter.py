"""Unit tests for the Hunter node."""

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.agent.nodes.hunter import hunter_node


class TestHunterNode:
    """Tests for the Hunter node function."""

    @pytest.mark.asyncio
    async def test_returns_empty_results_with_no_plan(self):
        """Should return empty results when plan is empty."""
        state = {
            "plan": [],
            "gathered_facts": [],
            "iteration_count": 0,
        }

        result = await hunter_node(state)

        assert result["temp_raw_results"] == []
        assert result["past_steps"] == []
        assert result["iteration_count"] == 1

    @pytest.mark.asyncio
    @patch("app.agent.nodes.hunter.get_search_service")
    async def test_executes_searches_and_returns_results(
        self,
        mock_get_search: MagicMock,
        sample_raw_results: list[dict[str, Any]],
    ):
        """Should execute searches and return filtered results."""
        mock_search = MagicMock()
        mock_search.search_batch = AsyncMock(
            return_value={
                "AI PM skills 2025": sample_raw_results,
            }
        )
        mock_get_search.return_value = mock_search

        state = {
            "plan": ["AI PM skills 2025"],
            "gathered_facts": [],
            "iteration_count": 0,
        }

        result = await hunter_node(state)

        assert len(result["temp_raw_results"]) == 2
        assert len(result["past_steps"]) == 1
        assert "Found 2 new sources" in result["past_steps"][0]["outcome"]
        assert result["iteration_count"] == 1

    @pytest.mark.asyncio
    @patch("app.agent.nodes.hunter.get_search_service")
    async def test_deduplicates_by_url(
        self,
        mock_get_search: MagicMock,
        sample_raw_results: list[dict[str, Any]],
    ):
        """Should skip URLs that already exist in gathered facts."""
        mock_search = MagicMock()
        mock_search.search_batch = AsyncMock(
            return_value={
                "query1": sample_raw_results,
            }
        )
        mock_get_search.return_value = mock_search

        existing_fact = {
            "content": "Existing content",
            "source": sample_raw_results[0]["url"],
            "relevance_score": 0.9,
        }

        state = {
            "plan": ["query1"],
            "gathered_facts": [existing_fact],
            "iteration_count": 0,
        }

        result = await hunter_node(state)

        assert len(result["temp_raw_results"]) == 1
        assert result["temp_raw_results"][0]["url"] == sample_raw_results[1]["url"]

    @pytest.mark.asyncio
    @patch("app.agent.nodes.hunter.get_search_service")
    async def test_logs_no_results_found(
        self,
        mock_get_search: MagicMock,
    ):
        """Should log when no results are found for a query."""
        mock_search = MagicMock()
        mock_search.search_batch = AsyncMock(
            return_value={
                "obscure query": [],
            }
        )
        mock_get_search.return_value = mock_search

        state = {
            "plan": ["obscure query"],
            "gathered_facts": [],
            "iteration_count": 0,
        }

        result = await hunter_node(state)

        assert result["past_steps"][0]["outcome"] == "No relevant results found"
