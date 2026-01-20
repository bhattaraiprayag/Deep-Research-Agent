# Quick Start Guide

This guide covers getting the Deep Research Agent up and running quickly.

## Prerequisites

- **Docker Desktop** (v24.0+) with Docker Compose
- **API Keys**:
  - OpenAI API key (required)
  - Tavily API key (required)
  - LangSmith API key (optional, for tracing)

## Option 1: Docker Compose (Recommended)

### Step 1: Clone and Configure

```bash
# Navigate to the project
cd Deep-Research-Agent

# Create environment file
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
OPENAI_API_KEY=sk-your-openai-key-here
TAVILY_API_KEY=tvly-your-tavily-key-here

# Optional: LangSmith tracing
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=ls-your-langsmith-key-here
LANGSMITH_PROJECT=deep-research-agent
```

### Step 2: Build and Run

```bash
docker compose up --build
```

Wait for both services to start. You'll see:
```
deep-research-backend   | INFO:     Uvicorn running on http://0.0.0.0:8000
deep-research-frontend  | nginx -g daemon off
```

### Step 3: Access the Application

Open your browser to: **http://localhost:3000**

Enter a research query (minimum 10 characters) and press Enter or click the send button.

---

## Option 2: Local Development

### Backend Setup

```powershell
cd backend

# Create virtual environment with uv
uv venv

# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Install dependencies
uv sync --dev

# Create .env in backend folder
cp ../.env.example .env
# Edit .env with your API keys

# Run development server
uv run uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

Open a new terminal:

```powershell
cd frontend

# Install dependencies
npm install

# Run development server (with API proxy)
npm run dev
```

Access at: **http://localhost:5173**

---

## Verification

### Health Check

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{"status": "healthy", "version": "0.1.0"}
```

### Agent Status

```bash
curl http://localhost:8000/api/v1/research/status
```

Expected response:
```json
{
  "max_iterations": 5,
  "max_critique_loops": 3,
  "reasoning_model": "gpt-4o",
  "fast_model": "gpt-4o-mini",
  "search_mock_mode": false
}
```

If `search_mock_mode` is `true`, your Tavily API key is not configured correctly.

---

## Troubleshooting

### Docker Build Fails

**Error**: `failed to solve: ... network error`

**Solution**: Check your internet connection and Docker Desktop is running.

---

**Error**: `OPENAI_API_KEY not set`

**Solution**: Ensure your `.env` file exists in the project root and contains valid API keys.

---

### Backend Health Check Fails

**Error**: Container reports unhealthy

**Solution**: 
1. Check logs: `docker compose logs backend`
2. Verify API keys are correct
3. Ensure no firewall is blocking port 8000

---

### Frontend Cannot Connect to Backend

**Error**: Network errors in browser console

**Solution**:
1. Ensure backend is running: `docker compose ps`
2. Check backend logs: `docker compose logs backend`
3. For local development, verify the Vite proxy is configured in `vite.config.ts`

---

### SSE Stream Disconnects

**Error**: Research stops mid-process

**Solution**:
- This may occur with long-running research. The nginx configuration has extended timeouts.
- Check backend logs for any errors.
- Reduce `MAX_ITERATIONS` in `.env` for faster completion.

---

## Running Tests

### Backend Tests

```bash
cd backend
uv run pytest tests/ -v
```

With coverage:
```bash
uv run pytest tests/ --cov=app --cov-report=html
```

---

## Stopping the Application

```bash
# Stop containers
docker compose down

# Stop and remove volumes
docker compose down -v
```

---

## Next Steps

- Read [ARCHITECTURE.md](./ARCHITECTURE.md) for technical design details
- Configure LangSmith for observability and debugging
- Customize the agent behavior via environment variables
