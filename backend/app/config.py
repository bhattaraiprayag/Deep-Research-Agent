"""
Configuration module for the Deep Research Agent.

Centralizes all environment variables and application settings using pydantic-settings.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # OpenAI Configuration
    openai_api_key: str

    # LangSmith Observability
    langsmith_tracing: bool = True
    langsmith_endpoint: str = "https://api.smith.langchain.com"
    langsmith_api_key: str = ""
    langsmith_project: str = "deep-research-agent"

    # Tavily Search API
    tavily_api_key: str

    # Agent Configuration
    max_iterations: int = 5
    max_critique_loops: int = 3
    reasoning_model: str = "gpt-4o"
    fast_model: str = "gpt-4o-mini"

    # Server Configuration
    backend_host: str = "0.0.0.0"  # noqa: S104
    backend_port: int = 8000

    # CORS Origins (comma-separated)
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        """Parse CORS origins into a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    """
    Get cached application settings.

    Uses LRU cache to ensure settings are loaded only once.
    """
    return Settings()
