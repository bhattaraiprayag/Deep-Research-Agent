# Contributing to Deep Research Agent

Thank you for your interest in contributing! This guide helps you set up your environment and submit quality code.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [uv](https://github.com/astral-sh/uv) (for Python 3.12+)
- [Node.js](https://nodejs.org/) (v20+)

## Initial Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd Deep-Research-Agent
    ```

2.  **Install Pre-commit hooks:**
    This ensures code quality checks run automatically before you commit.
    ```bash
    pip install pre-commit  # Or use: uv tool install pre-commit
    pre-commit install
    ```

3.  **Backend Setup:**
    ```bash
    cd backend
    uv sync
    ```

4.  **Frontend Setup:**
    ```bash
    cd frontend
    npm ci
    ```

## Development Workflow

### Backend

-   **Run locally:**
    ```bash
    cd backend
    uv run uvicorn app.main:app --reload
    ```
-   **Run tests:**
    ```bash
    uv run pytest
    ```
-   **Lint & Format:**
    ```bash
    uv run ruff check . --fix
    uv run ruff format .
    ```

### Frontend

-   **Run locally:**
    ```bash
    cd frontend
    npm run dev
    ```
-   **Lint:**
    ```bash
    npm run lint
    ```
-   **Format:**
    ```bash
    npm run format
    ```

## Docker

To run the full stack using Docker:

```bash
docker-compose up --build
```

## Pull Request Process

1.  Ensure all CI checks pass.
2.  Update documentation if you change functionality.
3.  Add tests for new features.
