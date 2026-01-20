"""Integration tests for the FastAPI endpoints."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestHealthEndpoint:
    """Tests for the health check endpoint."""

    def test_health_returns_ok(self, client):
        """Should return healthy status."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestRootEndpoint:
    """Tests for the root endpoint."""

    def test_root_returns_api_info(self, client):
        """Should return API information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Deep Research Agent API"
        assert "version" in data
        assert "docs" in data


class TestResearchStatusEndpoint:
    """Tests for the research status endpoint."""

    def test_status_returns_config(self, client):
        """Should return research configuration keys."""
        response = client.get("/api/v1/research/status")
        assert response.status_code == 200

        data = response.json()
        assert "max_iterations" in data
        assert "max_critique_loops" in data
        assert "reasoning_model" in data
        assert "search_mock_mode" in data


class TestResearchEndpoint:
    """Tests for the research execution endpoint."""

    def test_research_rejects_short_query(self, client):
        """Should reject queries that are too short."""
        response = client.post(
            "/api/v1/research",
            json={"query": "short"},
        )
        assert response.status_code == 422

    @patch("app.api.routes.build_research_graph")
    @patch("app.api.routes.create_initial_state")
    def test_research_returns_sse_stream(
        self,
        mock_create_state: MagicMock,
        mock_build_graph: MagicMock,
        client,
    ):
        """Should return SSE stream for valid research request."""
        async def mock_stream():
            yield {"strategist": {"plan": ["query1"]}}
            yield {"analyst": {"report_content": "Test report"}}

        mock_graph = MagicMock()
        mock_graph.astream = MagicMock(return_value=mock_stream())
        mock_build_graph.return_value = mock_graph
        mock_create_state.return_value = {"task": "test"}

        response = client.post(
            "/api/v1/research",
            json={"query": "What are the key trends in AI for 2025?"},
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
