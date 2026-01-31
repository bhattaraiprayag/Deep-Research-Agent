"""Unit tests for the Strategist node."""

from typing import Any
from unittest.mock import MagicMock, patch

from app.agent.nodes.strategist import _compress_context, strategist_node


class TestCompressContext:
    """Tests for context compression utility."""

    def test_empty_facts_returns_placeholder(self):
        """Should return placeholder text when no facts exist."""
        state = {"gathered_facts": []}
        result = _compress_context(state)
        assert result == "No facts gathered yet."

    def test_truncates_long_facts(self):
        """Should truncate fact content to 200 characters."""
        long_fact = {
            "content": "A" * 300,
            "source": "https://example.com",
            "relevance_score": 0.9,
        }
        state = {"gathered_facts": [long_fact]}
        result = _compress_context(state)
        assert "..." in result
        # The truncated content should be around 200 chars (before "...")
        content_part = result.split("...")[0].split("- ")[1]
        assert len(content_part) <= 210  # Allow small buffer due to formatting

    def test_includes_sources(self, sample_facts: list[dict[str, Any]]):
        """Should include source URLs in compressed context."""
        state = {"gathered_facts": sample_facts}
        result = _compress_context(state)
        assert "example.com/article1" in result
        assert "example.com/article2" in result


class TestStrategistNode:
    """Tests for the Strategist node function."""

    @patch("app.agent.nodes.strategist.get_settings")
    @patch("app.agent.nodes.strategist.get_reasoning_llm_with_metrics")
    def test_returns_empty_plan_at_max_iterations(
        self,
        mock_llm: MagicMock,
        mock_settings: MagicMock,
    ):
        """Should return empty plan when max iterations reached."""
        mock_settings.return_value.max_iterations = 3

        state = {
            "task": "Test task",
            "gathered_facts": [],
            "past_steps": [],
            "iteration_count": 3,
        }

        result = strategist_node(state)

        assert result["plan"] == []
        assert result["iteration_count"] == 3
        mock_llm.assert_not_called()

    @patch("app.agent.nodes.strategist.get_settings")
    @patch("app.agent.nodes.strategist.get_reasoning_llm_with_metrics")
    def test_generates_queries_when_incomplete(
        self,
        mock_llm: MagicMock,
        mock_settings: MagicMock,
    ):
        """Should generate search queries when research is incomplete."""
        mock_settings.return_value.max_iterations = 5

        mock_response = MagicMock()
        mock_response.search_queries = ["query 1", "query 2"]
        mock_response.is_complete = False

        mock_structured_llm = MagicMock()
        mock_structured_llm.invoke.return_value = mock_response
        mock_llm.return_value.with_structured_output.return_value = mock_structured_llm

        state = {
            "task": "Test task",
            "gathered_facts": [],
            "past_steps": [],
            "iteration_count": 0,
        }

        result = strategist_node(state)

        assert result["plan"] == ["query 1", "query 2"]
        assert result["iteration_count"] == 0

    @patch("app.agent.nodes.strategist.get_settings")
    @patch("app.agent.nodes.strategist.get_reasoning_llm_with_metrics")
    def test_returns_empty_plan_when_complete(
        self,
        mock_llm: MagicMock,
        mock_settings: MagicMock,
    ):
        """Should return empty plan when is_complete is True."""
        mock_settings.return_value.max_iterations = 5

        mock_response = MagicMock()
        mock_response.search_queries = []
        mock_response.is_complete = True

        mock_structured_llm = MagicMock()
        mock_structured_llm.invoke.return_value = mock_response
        mock_llm.return_value.with_structured_output.return_value = mock_structured_llm

        state = {
            "task": "Test task",
            "gathered_facts": [{"content": "Some fact", "source": "url", "relevance_score": 0.9}],
            "past_steps": [],
            "iteration_count": 2,
        }

        result = strategist_node(state)

        assert result["plan"] == []
