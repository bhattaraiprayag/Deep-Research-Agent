/**
 * ReasoningPane - Left pane showing the agent's reasoning process in real-time.
 */

import { useEffect, useRef } from "react";
import {
  Brain,
  Search,
  FileText,
  CheckCircle,
  PlayCircle,
  Lightbulb,
} from "lucide-react";
import type { ReasoningEntry } from "../types";

interface ReasoningPaneProps {
  entries: ReasoningEntry[];
  isActive: boolean;
}

const nodeIcons: Record<string, React.ReactNode> = {
  strategist: <Brain className="w-4 h-4 text-indigo-400" />,
  hunter: <Search className="w-4 h-4 text-amber-400" />,
  curator: <Lightbulb className="w-4 h-4 text-emerald-400" />,
  analyst: <FileText className="w-4 h-4 text-purple-400" />,
  critic: <CheckCircle className="w-4 h-4 text-cyan-400" />,
  system: <PlayCircle className="w-4 h-4 text-gray-400" />,
};

const typeColors: Record<string, string> = {
  start: "border-l-indigo-500",
  end: "border-l-emerald-500",
  info: "border-l-gray-500",
  search: "border-l-amber-500",
  fact: "border-l-purple-500",
  error: "border-l-red-500",
};

function formatTime(date: Date): string {
  return date.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

function renderQueries(entry: ReasoningEntry): React.ReactNode {
  const queries = entry.details?.queries;
  if (!queries || !Array.isArray(queries)) return null;

  return (
    <div className="mt-2 pl-6 space-y-1">
      {queries.map((q, i) => (
        <div
          key={i}
          className="text-xs text-amber-400/80 flex items-start gap-2"
        >
          <Search className="w-3 h-3 mt-0.5 flex-shrink-0" />
          <span>{String(q)}</span>
        </div>
      ))}
    </div>
  );
}

function EntryCard({ entry }: { entry: ReasoningEntry }) {
  return (
    <div
      className={`p-3 rounded-lg glass border-l-4 ${
        typeColors[entry.type] || "border-l-gray-500"
      } transition-all hover:bg-white/5`}
    >
      <div className="flex items-center gap-2 mb-1.5">
        {nodeIcons[entry.node] ?? nodeIcons.system}
        <span className="text-sm font-medium capitalize text-gray-300">
          {entry.node}
        </span>
        <span className="text-xs text-gray-600 ml-auto">
          {formatTime(entry.timestamp)}
        </span>
      </div>

      <p className="text-sm text-gray-400 pl-6">{entry.message}</p>

      {renderQueries(entry)}
    </div>
  );
}

export function ReasoningPane({ entries, isActive }: ReasoningPaneProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [entries]);

  return (
    <div className="h-full flex flex-col">
      <div className="flex items-center justify-between px-5 py-4 border-b border-indigo-500/20">
        <div className="flex items-center gap-3">
          <div
            className={`w-2.5 h-2.5 rounded-full ${
              isActive ? "bg-emerald-500 animate-pulse" : "bg-gray-600"
            }`}
          />
          <h2 className="text-lg font-semibold gradient-text">Reasoning</h2>
        </div>
        <span className="text-xs text-gray-500">{entries.length} steps</span>
      </div>

      <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-3">
        {entries.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-gray-500">
            <Brain className="w-12 h-12 mb-4 opacity-30" />
            <p className="text-sm">Waiting for research to begin...</p>
            <p className="text-xs mt-1 opacity-60">
              The agent's thought process will appear here
            </p>
          </div>
        ) : (
          entries.map((entry) => <EntryCard key={entry.id} entry={entry} />)
        )}

        {isActive && entries.length > 0 && (
          <div className="flex items-center gap-2 p-3 text-gray-500">
            <div className="flex gap-1">
              <span
                className="w-2 h-2 rounded-full bg-indigo-500 animate-bounce"
                style={{ animationDelay: "0ms" }}
              />
              <span
                className="w-2 h-2 rounded-full bg-indigo-500 animate-bounce"
                style={{ animationDelay: "150ms" }}
              />
              <span
                className="w-2 h-2 rounded-full bg-indigo-500 animate-bounce"
                style={{ animationDelay: "300ms" }}
              />
            </div>
            <span className="text-xs">Processing...</span>
          </div>
        )}
      </div>
    </div>
  );
}
