"""
Custom Prometheus metrics for Deep Research Agent.

Defines application-specific metrics for monitoring agent performance,
LLM usage, search operations, and research quality.
"""

from prometheus_client import Counter, Gauge, Histogram, Info

# =============================================================================
# LLM Token & Cost Metrics
# =============================================================================

llm_tokens_total = Counter(
    "llm_tokens_total",
    "Total LLM tokens consumed",
    ["model", "type", "node"],  # labels: model, type (prompt/completion), node
)

llm_calls_total = Counter(
    "llm_calls_total",
    "Total LLM API calls",
    ["model", "node", "status"],  # labels: model, node, status (success/failure)
)

llm_call_duration_seconds = Histogram(
    "llm_call_duration_seconds",
    "LLM API call duration in seconds",
    ["model", "node"],
    buckets=[0.5, 1, 2, 5, 10, 20, 30, 60, 120],
)

# =============================================================================
# Node Execution Metrics
# =============================================================================

node_executions_total = Counter(
    "node_executions_total",
    "Total node executions",
    ["node"],
)

node_errors_total = Counter(
    "node_errors_total",
    "Total node errors",
    ["node", "error_type"],
)

node_execution_duration_seconds = Histogram(
    "node_execution_duration_seconds",
    "Node execution duration in seconds",
    ["node"],
    buckets=[0.1, 0.5, 1, 2, 5, 10, 20, 30, 60, 120, 300],
)

# =============================================================================
# Research Task Metrics
# =============================================================================

research_tasks_total = Counter(
    "research_tasks_total",
    "Total research tasks",
    ["status"],  # labels: status (started/completed/failed)
)

research_duration_seconds = Histogram(
    "research_duration_seconds",
    "Total research task duration in seconds",
    buckets=[10, 30, 60, 120, 180, 300, 600, 900, 1800],
)

research_iterations_total = Counter(
    "research_iterations_total",
    "Total research iterations",
)

research_iteration_count = Histogram(
    "research_iteration_count",
    "Number of iterations per research task",
    buckets=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
)

max_iterations_reached_total = Counter(
    "max_iterations_reached_total",
    "Times research hit max iterations limit",
)

# =============================================================================
# Critique & Quality Metrics
# =============================================================================

critique_decisions_total = Counter(
    "critique_decisions_total",
    "Total critique decisions",
    ["outcome", "attempt"],  # labels: outcome (approved/rejected), attempt (1,2,3...)
)

critique_loops_total = Counter(
    "critique_loops_total",
    "Total critique loop iterations",
)

# =============================================================================
# Search Metrics
# =============================================================================

search_requests_total = Counter(
    "search_requests_total",
    "Total search requests",
    ["status"],  # labels: status (success/failure)
)

search_latency_seconds = Histogram(
    "search_latency_seconds",
    "Search request latency in seconds",
    buckets=[0.1, 0.25, 0.5, 1, 2, 3, 5, 10],
)

search_results_total = Counter(
    "search_results_total",
    "Total search results returned",
)

search_results_filtered_total = Counter(
    "search_results_filtered_total",
    "Search results filtered due to low relevance",
)

search_mock_mode_active = Gauge(
    "search_mock_mode_active",
    "Whether search is running in mock mode (1=mock, 0=real)",
)

# =============================================================================
# Fact Extraction Metrics
# =============================================================================

curator_facts_extracted_total = Counter(
    "curator_facts_extracted_total",
    "Total facts extracted by Curator",
)

curator_facts_deduplicated_total = Counter(
    "curator_facts_deduplicated_total",
    "Facts deduplicated (already seen)",
)

# =============================================================================
# SSE Stream Metrics
# =============================================================================

active_sse_connections = Gauge(
    "active_sse_connections",
    "Currently active SSE connections",
)

sse_streams_started_total = Counter(
    "sse_streams_started_total",
    "Total SSE streams started",
)

sse_streams_completed_total = Counter(
    "sse_streams_completed_total",
    "Total SSE streams completed successfully",
)

sse_premature_closures_total = Counter(
    "sse_premature_closures_total",
    "SSE streams closed before completion",
)

sse_events_total = Counter(
    "sse_events_total",
    "Total SSE events sent",
    ["event_type"],
)

# =============================================================================
# Report Quality Metrics
# =============================================================================

report_facts_count = Histogram(
    "report_facts_count",
    "Number of facts per report",
    buckets=[1, 2, 5, 10, 15, 20, 30, 50],
)

report_sources_count = Histogram(
    "report_sources_count",
    "Number of unique sources per report",
    buckets=[1, 2, 3, 5, 8, 10, 15, 20],
)

report_length_chars = Histogram(
    "report_length_chars",
    "Report length in characters",
    buckets=[500, 1000, 2000, 3000, 5000, 8000, 10000, 15000, 20000],
)

# =============================================================================
# Application Info
# =============================================================================

app_info = Info(
    "deep_research_agent",
    "Deep Research Agent application information",
)


def set_app_info(version: str, reasoning_model: str, fast_model: str) -> None:
    """Set application info metrics."""
    app_info.info(
        {
            "version": version,
            "reasoning_model": reasoning_model,
            "fast_model": fast_model,
        }
    )
