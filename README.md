# Deep Research Agent

A production-grade AI-powered research agent that performs exhaustive, multi-step information gathering and synthesis with **real-time reasoning visibility**.

## Overview

The Deep Research Agent addresses a fundamental challenge with traditional LLM interfaces: the "black box" problem. Users often struggle to trust AI-generated research because they cannot observe the reasoning process. This application provides **transparency by design**, streaming the agent's thought process—its planning, searching, fact extraction, and synthesis—to users in real-time.

### Key Features

- **Transparent Reasoning**: Watch the agent's decision-making process unfold in real-time
- **Deep Search**: Multi-iteration search with Tavily API for comprehensive coverage
- **Fact Curation**: Automatic extraction and deduplication of atomic facts
- **Quality Review**: Built-in critique loop for accuracy verification
- **Cited Reports**: Structured Markdown reports with source citations
- **Modern UI**: Split-pane interface with live updates
- **Engineering Rigor**: Full CI/CD pipeline, strict type checking, and security hardening

## Architecture

The system follows a Plan-and-Execute architecture with five specialized nodes:

```
┌──────────────┐     ┌────────┐     ┌─────────┐
│  Strategist  │────▶│ Hunter │────▶│ Curator │
│  (Planner)   │     │(Search)│     │(Extract)│
└──────┬───────┘     └────────┘     └────┬────┘
       │                                 │
       │◀────────────────────────────────┘
       │
       ▼
┌──────────────┐     ┌─────────┐
│   Analyst    │────▶│  Critic │────▶ END
│   (Write)    │◀────│(Review) │
└──────────────┘     └─────────┘
```

## Project Structure

```
Deep-Research-Agent/
├── backend/                   # FastAPI backend
│   ├── app/
│   │   ├── agent/            # LangGraph agent implementation
│   │   │   ├── nodes/        # Individual node implementations
│   │   │   ├── edges.py      # Routing logic
│   │   │   └── graph.py      # Graph construction
│   │   ├── api/              # FastAPI routes and streaming
│   │   ├── models/           # Pydantic models and types
│   │   ├── services/         # LLM and search services
│   │   ├── config.py         # Settings management
│   │   └── main.py           # Application entry point
│   ├── tests/                # Unit and integration tests
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/                  # React/Vite frontend
│   ├── src/
│   │   ├── components/       # UI components
│   │   ├── hooks/            # Custom React hooks
│   │   └── types/            # TypeScript definitions
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
├── .env.example
└── README.md
```

## Technology Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | React 19, TypeScript, Vite, Tailwind CSS, Lucide Icons |
| **Backend** | FastAPI, Python 3.12, Pydantic, Gunicorn |
| **Agent Framework** | LangChain, LangGraph |
| **Search** | Tavily API |
| **Observability** | LangSmith |
| **CI/CD** | GitHub Actions, Pre-commit |
| **Code Quality** | Ruff, Mypy, Prettier, ESLint |
| **Package Manager** | uv (Python), npm (Node.js) |
| **Containerization** | Docker, Docker Compose |

## Quick Start

See [QUICKSTART.md](./QUICKSTART.md) for detailed setup instructions.

### Prerequisites

- Docker and Docker Compose
- OpenAI API key
- Tavily API key
- (Optional) LangSmith API key for tracing

### Running with Docker

```bash
# Clone and navigate
cd Deep-Research-Agent

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Build and run
docker compose up --build
```

Access the application at `http://localhost:3000`

## Development

### Backend Development

```bash
cd backend

# Create virtual environment with uv
uv venv
uv sync --dev

# Activate environment
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate   # Linux/macOS

# Run development server
uv run uvicorn app.main:app --reload

# Run tests
uv run pytest tests/ -v
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
# Build for production
npm run build

# Run linting and formatting
npm run lint
npm run format
```

## Quality Assurance

This project enforces high engineering standards through:

- **Pre-commit Hooks**: Automatically checks code before every commit.
  - Trailing whitespace & end-of-file fixes
  - `ruff` for Python linting and formatting
  - `mypy` for static type checking
  - `prettier` for frontend consistency
  - `detect-private-key` for security
- **CI/CD Pipeline**: GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push:
  - Backend: Linting, Type Checking, Testing (with coverage), Docker Build
  - Frontend: Linting, Type Checking, Formatting, Docker Build

## Configuration

All configuration is managed through environment variables. See `.env.example` for available options:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | (required) |
| `TAVILY_API_KEY` | Tavily search API key | (required) |
| `MAX_ITERATIONS` | Maximum research iterations | 5 |
| `MAX_CRITIQUE_LOOPS` | Maximum revision attempts | 3 |
| `REASONING_MODEL` | Model for complex reasoning | gpt-4o |
| `FAST_MODEL` | Model for fact extraction | gpt-4o-mini |

## API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/health` | Health check |
| `POST` | `/api/v1/research` | Execute research (SSE stream) |
| `GET` | `/api/v1/research/status` | Get agent configuration |

### SSE Event Types

The research endpoint streams events with the following types:

- `node_start` / `node_end`: Node lifecycle events
- `queries_generated`: Search queries from Strategist
- `facts_extracted`: Facts from Curator
- `report_chunk`: Report content from Analyst
- `complete`: Research finished
- `error`: Error occurred

## License

MIT License - See LICENSE file for details.
