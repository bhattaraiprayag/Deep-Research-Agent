/**
 * Custom hook for managing SSE connections and research state.
 */

import { useState, useCallback, useRef } from "react";
import {
  EventType,
  type ResearchEvent,
  type ResearchState,
  type ReasoningEntry,
  type ResearchStatus,
} from "../types";

const API_BASE = "/api/v1";

function generateId(): string {
  return Math.random().toString(36).substring(2, 11);
}

function createReasoningEntry(
  node: string,
  type: ReasoningEntry["type"],
  message: string,
  details?: Record<string, unknown>
): ReasoningEntry {
  return {
    id: generateId(),
    timestamp: new Date(),
    node,
    type,
    message,
    details,
  };
}

export function useResearch() {
  const [state, setState] = useState<ResearchState>({
    status: "idle",
    query: "",
    reasoningLog: [],
    report: "",
    error: null,
    factsCount: 0,
    sourcesCount: 0,
  });

  const abortControllerRef = useRef<AbortController | null>(null);

  const addReasoningEntry = useCallback((entry: ReasoningEntry) => {
    setState((prev) => ({
      ...prev,
      reasoningLog: [...prev.reasoningLog, entry],
    }));
  }, []);

  const processEvent = useCallback(
    (event: ResearchEvent) => {
      const { event_type, node, message, data } = event;

      switch (event_type) {
        case EventType.STATUS_UPDATE:
          if (data.status === "starting") {
            setState((prev) => ({
              ...prev,
              status: "researching" as ResearchStatus,
            }));
          }
          addReasoningEntry(
            createReasoningEntry(
              node || "system",
              "info",
              message || "Status update"
            )
          );
          break;

        case EventType.NODE_START:
          addReasoningEntry(
            createReasoningEntry(
              node || "unknown",
              "start",
              message || `Starting ${node}...`
            )
          );
          break;

        case EventType.NODE_END:
          addReasoningEntry(
            createReasoningEntry(
              node || "unknown",
              "end",
              message || `Completed ${node}`
            )
          );
          break;

        case EventType.QUERIES_GENERATED: {
          const queries = (data.queries as string[]) || [];
          addReasoningEntry(
            createReasoningEntry(
              node || "strategist",
              "search",
              message || `Generated ${queries.length} search queries`,
              { queries }
            )
          );
          break;
        }

        case EventType.FACTS_EXTRACTED: {
          const count = (data.new_facts_count as number) || 0;
          const total = (data.total_facts as number) || 0;
          addReasoningEntry(
            createReasoningEntry(
              node || "curator",
              "fact",
              message || `Extracted ${count} new facts (${total} total)`,
              { count, total }
            )
          );
          setState((prev) => ({
            ...prev,
            factsCount: total,
          }));
          break;
        }

        case EventType.REPORT_CHUNK: {
          const content = (data.content as string) || "";
          setState((prev) => ({
            ...prev,
            status: "finalizing",
            report: content,
          }));
          addReasoningEntry(
            createReasoningEntry(
              node || "analyst",
              "info",
              message || "Report generated"
            )
          );
          break;
        }

        case EventType.REPORT_COMPLETE: {
          const report = (data.report as string) || "";
          const sourcesCount = (data.sources_count as number) || 0;
          setState((prev) => ({
            ...prev,
            report: report || prev.report,
            sourcesCount,
          }));
          break;
        }

        case EventType.COMPLETE:
          setState((prev) => ({
            ...prev,
            status: "complete",
          }));
          addReasoningEntry(
            createReasoningEntry("system", "info", "✅ Research complete!")
          );
          break;

        case EventType.ERROR:
          setState((prev) => ({
            ...prev,
            status: "error",
            error: (data.error as string) || "Unknown error",
          }));
          addReasoningEntry(
            createReasoningEntry(
              "system",
              "error",
              message || "Error occurred",
              data
            )
          );
          break;

        default:
          if (message) {
            addReasoningEntry(
              createReasoningEntry(node || "system", "info", message)
            );
          }
      }
    },
    [addReasoningEntry]
  );

  const startResearch = useCallback(
    async (query: string) => {
      // Cancel any existing request
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }

      abortControllerRef.current = new AbortController();

      setState({
        status: "researching",
        query,
        reasoningLog: [],
        report: "",
        error: null,
        factsCount: 0,
        sourcesCount: 0,
      });

      try {
        const response = await fetch(`${API_BASE}/research`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ query }),
          signal: abortControllerRef.current.signal,
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const reader = response.body?.getReader();
        if (!reader) {
          throw new Error("No response body");
        }

        const decoder = new TextDecoder();
        let buffer = "";

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          buffer += decoder.decode(value, { stream: true });

          // Process complete SSE messages
          const lines = buffer.split("\n\n");
          buffer = lines.pop() || "";

          for (const eventBlock of lines) {
            if (!eventBlock.trim()) continue;

            let eventData = "";

            for (const line of eventBlock.split("\n")) {
              if (line.startsWith("data:")) {
                eventData = line.slice(5).trim();
              }
            }

            if (eventData) {
              try {
                const parsed = JSON.parse(eventData) as ResearchEvent;
                processEvent(parsed);
              } catch (e) {
                console.error("Failed to parse event:", e);
              }
            }
          }
        }
      } catch (error) {
        if ((error as Error).name === "AbortError") {
          return;
        }
        setState((prev) => ({
          ...prev,
          status: "error",
          error: (error as Error).message,
        }));
      }
    },
    [processEvent]
  );

  const cancelResearch = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      setState((prev) => ({
        ...prev,
        status: "idle",
      }));
    }
  }, []);

  const reset = useCallback(() => {
    setState({
      status: "idle",
      query: "",
      reasoningLog: [],
      report: "",
      error: null,
      factsCount: 0,
      sourcesCount: 0,
    });
  }, []);

  return {
    state,
    startResearch,
    cancelResearch,
    reset,
  };
}
