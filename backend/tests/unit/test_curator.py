"""Unit tests for the Curator node."""

from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.agent.nodes.curator import curator_node, _deduplicate_facts


class TestDeduplicateFacts:
    """Tests for fact deduplication utility."""

    def test_removes_duplicate_facts(self):
        """Should remove facts with identical content."""
        new_facts = [
            {"content": "Fact A", "source": "url1", "relevance_score": 0.9},
            {"content": "Fact A", "source": "url2", "relevance_score": 0.8},
            {"content": "Fact B", "source": "url3", "relevance_score": 0.85},
        ]
        existing_facts: list[Any] = []

        result = _deduplicate_facts(new_facts, existing_facts)

        assert len(result) == 2
        contents = [f["content"] for f in result]
        assert "Fact A" in contents
        assert "Fact B" in contents

    def test_excludes_existing_facts(self, sample_facts: list[dict[str, Any]]):
        """Should exclude facts that already exist."""
        new_facts = [
            sample_facts[0],
            {"content": "New fact", "source": "url_new", "relevance_score": 0.9},
        ]

        result = _deduplicate_facts(new_facts, sample_facts)

        assert len(result) == 1
        assert result[0]["content"] == "New fact"

    def test_handles_empty_inputs(self):
        """Should handle empty new facts list."""
        result = _deduplicate_facts([], [])
        assert result == []


class TestCuratorNode:
    """Tests for the Curator node function."""

    @pytest.mark.asyncio
    async def test_returns_empty_when_no_raw_results(self):
        """Should return empty facts when no raw results exist."""
        state = {
            "task": "Test task",
            "temp_raw_results": [],
            "gathered_facts": [],
        }

        result = await curator_node(state)

        assert result["gathered_facts"] == []
        assert result["temp_raw_results"] == []

    @pytest.mark.asyncio
    @patch("app.agent.nodes.curator.get_fast_llm")
    async def test_extracts_facts_from_raw_results(
        self,
        mock_llm: MagicMock,
        sample_raw_results: list[dict[str, Any]],
    ):
        """Should extract facts from raw search results."""
        mock_response = MagicMock()
        mock_response.facts = ["Extracted fact 1", "Extracted fact 2"]
        mock_response.is_relevant = True

        mock_structured_llm = MagicMock()
        mock_structured_llm.ainvoke = AsyncMock(return_value=mock_response)
        mock_llm.return_value.with_structured_output.return_value = mock_structured_llm

        state = {
            "task": "Test task",
            "temp_raw_results": sample_raw_results[:1],
            "gathered_facts": [],
        }

        result = await curator_node(state)

        assert len(result["gathered_facts"]) == 2
        assert result["temp_raw_results"] == []

    @pytest.mark.asyncio
    @patch("app.agent.nodes.curator.get_fast_llm")
    async def test_filters_irrelevant_results(
        self,
        mock_llm: MagicMock,
        sample_raw_results: list[dict[str, Any]],
    ):
        """Should skip irrelevant content."""
        mock_response = MagicMock()
        mock_response.facts = []
        mock_response.is_relevant = False

        mock_structured_llm = MagicMock()
        mock_structured_llm.ainvoke = AsyncMock(return_value=mock_response)
        mock_llm.return_value.with_structured_output.return_value = mock_structured_llm

        state = {
            "task": "Test task",
            "temp_raw_results": sample_raw_results,
            "gathered_facts": [],
        }

        result = await curator_node(state)

        assert result["gathered_facts"] == []
