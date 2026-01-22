/**
 * Type definitions for the Deep Research Agent frontend.
 */

/** Event types from the backend SSE stream */
export const EventType = {
  NODE_START: "node_start",
  NODE_END: "node_end",
  PLANNING: "planning",
  SEARCHING: "searching",
  EXTRACTING: "extracting",
  WRITING: "writing",
  CRITIQUING: "critiquing",
  QUERIES_GENERATED: "queries_generated",
  FACTS_EXTRACTED: "facts_extracted",
  REPORT_CHUNK: "report_chunk",
  REPORT_COMPLETE: "report_complete",
  STATUS_UPDATE: "status_update",
  ERROR: "error",
  COMPLETE: "complete",
} as const;

export type EventTypeValue = (typeof EventType)[keyof typeof EventType];

/** Research event from backend */
export interface ResearchEvent {
  event_type: EventTypeValue;
  node: string | null;
  data: Record<string, unknown>;
  message: string | null;
}

/** Reasoning log entry for display */
export interface ReasoningEntry {
  id: string;
  timestamp: Date;
  node: string;
  type: "start" | "end" | "info" | "search" | "fact" | "error";
  message: string;
  details?: Record<string, unknown>;
}

/** Research status */
export type ResearchStatus =
  | "idle"
  | "researching"
  | "finalizing"
  | "complete"
  | "error";

/** Research state */
export interface ResearchState {
  status: ResearchStatus;
  query: string;
  reasoningLog: ReasoningEntry[];
  report: string;
  error: string | null;
  factsCount: number;
  sourcesCount: number;
}
