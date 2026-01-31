"""
Tavily search service wrapper.

Provides an abstraction layer over the Tavily API with
quality filtering, mock mode for testing, and Prometheus metrics.
"""

import asyncio
import logging
import time
from functools import lru_cache

from tavily import TavilyClient

from app.config import get_settings
from app.metrics import (
    search_latency_seconds,
    search_mock_mode_active,
    search_requests_total,
    search_results_filtered_total,
    search_results_total,
)
from app.models.state import RawSearchResult

logger = logging.getLogger(__name__)


class SearchService:
    """Wrapper service for Tavily search API with metrics."""

    MIN_RELEVANCE_SCORE = 0.6

    def __init__(self, api_key: str | None = None) -> None:
        """
        Initialize the search service.

        Args:
            api_key: Tavily API key. If None, mock mode is enabled.
        """
        self._client: TavilyClient | None = None
        self._mock_mode = False

        if api_key:
            try:
                self._client = TavilyClient(api_key=api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize Tavily client: {e}. Using mock mode.")
                self._mock_mode = True
        else:
            logger.info("No Tavily API key provided. Mock mode enabled.")
            self._mock_mode = True

        # Set mock mode metric
        search_mock_mode_active.set(1 if self.is_mock_mode else 0)

    @property
    def is_mock_mode(self) -> bool:
        """Check if running in mock mode."""
        return self._mock_mode or self._client is None

    async def search(self, query: str, max_results: int = 5) -> list[RawSearchResult]:
        """
        Perform a search query.

        Args:
            query: The search query string.
            max_results: Maximum number of results to return.

        Returns:
            List of raw search results passing the quality gate.
        """
        start_time = time.perf_counter()

        if self.is_mock_mode:
            results = self._mock_search(query)
            search_requests_total.labels(status="success").inc()
            search_results_total.inc(len(results))
            search_latency_seconds.observe(time.perf_counter() - start_time)
            return results

        try:
            response = await asyncio.to_thread(
                self._client.search,  # type: ignore
                query=query,
                search_depth="advanced",
                max_results=max_results,
                include_raw_content=False,
            )

            filtered_results: list[RawSearchResult] = []
            total_results = len(response.get("results", []))
            filtered_count = 0

            for item in response.get("results", []):
                score = item.get("score", 0)
                if score >= self.MIN_RELEVANCE_SCORE:
                    filtered_results.append(
                        RawSearchResult(
                            title=item.get("title", ""),
                            content=item.get("content", ""),
                            url=item.get("url", ""),
                            score=score,
                        )
                    )
                else:
                    filtered_count += 1

            # Record metrics
            search_requests_total.labels(status="success").inc()
            search_results_total.inc(total_results)
            search_results_filtered_total.inc(filtered_count)
            search_latency_seconds.observe(time.perf_counter() - start_time)

            return filtered_results

        except Exception as e:
            logger.error(f"Search error for query '{query}': {e}")
            search_requests_total.labels(status="failure").inc()
            search_latency_seconds.observe(time.perf_counter() - start_time)
            return []

    async def search_batch(
        self,
        queries: list[str],
        max_results_per_query: int = 5,
    ) -> dict[str, list[RawSearchResult]]:
        """
        Perform multiple searches in parallel.

        Args:
            queries: List of search query strings.
            max_results_per_query: Maximum results per query.

        Returns:
            Dictionary mapping queries to their results.
        """
        tasks = [self.search(q, max_results_per_query) for q in queries]
        results = await asyncio.gather(*tasks)
        return dict(zip(queries, results, strict=True))

    def _mock_search(self, query: str) -> list[RawSearchResult]:
        """Generate mock search results for testing."""
        return [
            RawSearchResult(
                title=f"Mock Result for: {query}",
                content=(
                    f"This is detailed mock content regarding '{query}'. "
                    "It contains relevant information that would typically "
                    "be extracted from real search results. AI systems require "
                    "strategic oversight and continuous monitoring."
                ),
                url=f"https://mock-source.com/article/{hash(query) % 10000}",
                score=0.95,
            )
        ]


@lru_cache
def get_search_service() -> SearchService:
    """Get cached search service instance."""
    settings = get_settings()
    return SearchService(api_key=settings.tavily_api_key)
