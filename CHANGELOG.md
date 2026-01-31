# Changelog

All notable changes to the Deep Research Agent project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-01-31

### Added
- **Production-Grade Monitoring Infrastructure**: Complete overhaul of Prometheus + Grafana setup
- **Grafana Auto-Provisioning**: Dashboards and datasources are automatically configured on startup
- **10 Pre-Configured Dashboards**:
  - 🎯 Agent Execution Overview (P0) - Command center for real-time health
  - 🧠 LLM Token & Cost Economics (P0) - Token tracking and cost estimation
  - 🔄 Loop Dynamics & Iteration Analytics (P1) - Research loop analysis
  - 📊 Node-Level Performance Breakdown (P1) - Per-node latency and errors
  - 🔍 Tavily Search Performance (P2) - Search API monitoring
  - ✅ Quality Assurance Pipeline (P2) - Critic node outcomes
  - 📡 SSE Stream Health (P2) - Real-time streaming health
  - 🏗️ Infrastructure & Resource Utilization (P3) - Container-level metrics
  - 🕐 End-to-End Research Timing (P3) - Phase breakdown and SLA
  - 📈 Business Intelligence & Usage Analytics (P3) - Usage analytics and growth
- **Custom Prometheus Metrics** (`app/metrics.py`):
  - LLM metrics: `llm_tokens_total`, `llm_calls_total`, `llm_call_duration_seconds`
  - Node metrics: `node_executions_total`, `node_execution_duration_seconds`
  - Research metrics: `research_tasks_total`, `research_duration_seconds`, `research_iterations_total`
  - Critique metrics: `critique_decisions_total`, `critique_loops_total`
  - Search metrics: `search_requests_total`, `search_latency_seconds`, `search_results_total`
  - SSE metrics: `sse_streams_started_total`, `sse_events_total`, `active_sse_connections`
  - Report quality: `report_facts_count`, `report_sources_count`, `report_length_chars`

### Changed
- **Directory Structure**: Moved `/prometheus` folder to `/monitoring/prometheus`
- **Docker Compose**: Updated Grafana service with provisioning volumes and environment variables
- **Documentation**: Updated ARCHITECTURE.md and QUICKSTART.md with new monitoring structure
- **LLM Service**: Added `get_reasoning_llm_with_metrics()` and `get_fast_llm_with_metrics()` for per-node tracking
- **Search Service**: Integrated metrics for request rate, latency, and result counts
- **Streaming Module**: Added SSE connection and event tracking
- **All Agent Nodes**: Updated to use metrics-enabled LLM functions
- **App Version**: Bumped to 0.2.0

### Removed
- **Old Prometheus Folder**: Deleted `/prometheus` folder (now in `/monitoring/prometheus`)

## [0.1.1] - 2026-01-22


### Added
- **CI/CD Pipeline**: GitHub Actions workflow for automated testing, linting, and Docker builds
- **Pre-commit Hooks**: Enforces code quality (ruff, mypy, prettier) and security (private key detection) locally
- **Production Server**: Replaced `uvicorn` with `gunicorn` (using `UvicornWorker`) for better concurrency
- **Security Hardening**:
  - Added `flake8-bandit` (S) to ruff config for security analysis
  - Added `Content-Security-Policy` and other security headers to Nginx
  - Switched to `hashlib.sha256` for fact deduplication
- **Documentation**: Added `CONTRIBUTING.md` guide for developers

### Changed
- **Dependencies**: Updated `pyproject.toml` and `package.json` with strict linting/formatting tools
- **Docker Optimization**: Reduced frontend build context size significantly using `.dockerignore`
- **Type Safety**: Relaxed `mypy` strictness slightly to accommodate existing codebase while preventing new errors

## [0.1.0] - 2026-01-20

### Added

#### Backend
- **FastAPI Application**: Production-ready API server with SSE streaming support
- **LangGraph Agent**: Five-node research agent (Strategist, Hunter, Curator, Analyst, Critic)
- **Modular Architecture**: Clean separation of concerns with dedicated modules for:
  - `agent/nodes/` - Individual node implementations
  - `agent/edges.py` - Conditional routing logic
  - `agent/graph.py` - Graph construction
  - `services/` - LLM and search service wrappers
  - `models/` - Pydantic schemas and TypedDicts
  - `api/` - FastAPI routes and streaming utilities
- **Configuration Management**: Pydantic-settings based configuration from environment variables
- **Tavily Integration**: Deep search capability with quality filtering and mock mode
- **LangSmith Integration**: Optional observability and tracing support
- **Dual LLM Strategy**: gpt-4o for reasoning, gpt-4o-mini for extraction
- **Unit Tests**: Comprehensive test coverage for nodes and edge routing
- **Integration Tests**: API endpoint testing with TestClient

#### Frontend
- **React 19 + TypeScript**: Modern frontend stack with strict typing
- **Vite Build System**: Fast development and optimized production builds
- **Tailwind CSS**: Utility-first styling with custom design tokens
- **Split-Pane Layout**: Real-time reasoning visibility alongside report output
- **SSE Integration**: Custom `useResearch` hook for event stream processing
- **Component Library**:
  - `ReasoningPane` - Live reasoning log with node icons and timestamps
  - `ReportPane` - Markdown rendering with copy/download actions
  - `InputBar` - Query input with validation and loading states
  - `StatusIndicator` - Animated status display with stats
  - `Layout` - Responsive split-pane container
- **Dark Theme**: Premium dark aesthetic with glassmorphism effects
- **Animations**: Micro-animations for enhanced user experience

#### Infrastructure
- **Docker Compose**: Multi-container orchestration with networking
- **Backend Dockerfile**: Multi-stage build with uv for dependencies
- **Frontend Dockerfile**: Multi-stage build with nginx for production
- **Nginx Configuration**: SPA routing, API proxy, gzip, and SSE support
- **Health Checks**: Container health monitoring for both services

#### Documentation
- **README.md**: Project overview and quick reference
- **QUICKSTART.md**: Step-by-step setup guide with troubleshooting
- **ARCHITECTURE.md**: Technical design decisions and production considerations
- **CHANGELOG.md**: Version history (this file)

### Technical Decisions
- Used `uv` for Python package management instead of pip/poetry
- Chose SSE over WebSockets for simpler unidirectional streaming
- Implemented atomic fact extraction to prevent context window pollution
- Added critique loop with bounded retries for quality assurance
- Separated reasoning and fast models for cost optimization

### Reference Implementation
- Based on `sample/researcher-v2.py` single-script implementation
- Fully modularized and production-ready architecture
- Enhanced with SSE streaming and web interface

---

## [Unreleased]

### Planned
- User authentication and rate limiting
- Research history persistence
- Multi-modal research support
- Export to PDF/DOCX
- Collaborative research sessions
