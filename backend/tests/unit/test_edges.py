"""Unit tests for edge routing functions."""

from unittest.mock import patch

from app.agent.edges import route_critic, route_strategist


class TestRouteStrategist:
    """Tests for strategist routing logic."""

    def test_routes_to_hunter_when_plan_exists(self):
        """Should route to hunter when there are search queries."""
        state = {"plan": ["query1", "query2"]}
        result = route_strategist(state)
        assert result == "hunter"

    def test_routes_to_analyst_when_plan_empty(self):
        """Should route to analyst when plan is empty."""
        state = {"plan": []}
        result = route_strategist(state)
        assert result == "analyst"

    def test_routes_to_analyst_when_plan_missing(self):
        """Should route to analyst when plan key is missing."""
        state = {}
        result = route_strategist(state)
        assert result == "analyst"


class TestRouteCritic:
    """Tests for critic routing logic."""

    @patch("app.agent.edges.get_settings")
    def test_routes_to_end_when_approved(self, mock_settings):
        """Should route to end when report is approved."""
        mock_settings.return_value.max_critique_loops = 3

        state = {
            "critique_count": 1,
            "is_approved": True,
            "critique_feedback": "Looks good!",
        }
        result = route_critic(state)
        assert result == "__end__"

    @patch("app.agent.edges.get_settings")
    def test_routes_to_end_at_max_loops(self, mock_settings):
        """Should route to end when max critique loops reached."""
        mock_settings.return_value.max_critique_loops = 2

        state = {
            "critique_count": 2,
            "is_approved": False,
            "critique_feedback": "Needs improvement",
        }
        result = route_critic(state)
        assert result == "__end__"

    @patch("app.agent.edges.get_settings")
    def test_routes_to_analyst_when_rejected(self, mock_settings):
        """Should route to analyst when report needs revision."""
        mock_settings.return_value.max_critique_loops = 3

        state = {
            "critique_count": 1,
            "is_approved": False,
            "critique_feedback": "Missing citations for claims in section 2.",
        }
        result = route_critic(state)
        assert result == "analyst"

    @patch("app.agent.edges.get_settings")
    def test_routes_to_end_on_minimal_feedback(self, mock_settings):
        """Should route to end when feedback indicates approval."""
        mock_settings.return_value.max_critique_loops = 3

        state = {
            "critique_count": 1,
            "is_approved": False,
            "critique_feedback": "OK",
        }
        result = route_critic(state)
        assert result == "__end__"
