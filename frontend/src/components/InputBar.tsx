/**
 * InputBar - Bottom input area for entering research queries.
 */

import { useState, type FormEvent, type KeyboardEvent } from "react";
import { Send, X, Sparkles } from "lucide-react";
import type { ResearchStatus } from "../types";

interface InputBarProps {
  onSubmit: (query: string) => void;
  onCancel: () => void;
  status: ResearchStatus;
}

export function InputBar({ onSubmit, onCancel, status }: InputBarProps) {
  const [query, setQuery] = useState("");

  const isLoading = status === "researching" || status === "finalizing";
  const canSubmit = query.trim().length >= 10 && !isLoading;

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (canSubmit) {
      onSubmit(query.trim());
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (canSubmit) {
        onSubmit(query.trim());
      }
    }
  };

  return (
    <div className="w-full px-6 py-4 border-t border-indigo-500/20 bg-[#0d0d14]">
      <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
        <div className="relative">
          {/* Input Container */}
          <div className="relative flex items-center glass rounded-2xl overflow-hidden transition-all duration-300 focus-within:ring-2 focus-within:ring-indigo-500/50 focus-within:border-indigo-500/50">
            {/* Icon */}
            <div className="pl-4 text-indigo-400">
              <Sparkles className="w-5 h-5" />
            </div>

            {/* Textarea */}
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Enter your research question... (min 10 characters)"
              disabled={isLoading}
              rows={1}
              className="flex-1 px-4 py-4 bg-transparent text-white placeholder-gray-500 resize-none focus:outline-none disabled:opacity-50"
              style={{ minHeight: "56px", maxHeight: "120px" }}
            />

            {/* Action Button */}
            <div className="pr-3">
              {isLoading ? (
                <button
                  type="button"
                  onClick={onCancel}
                  className="p-2.5 rounded-xl bg-red-500/20 text-red-400 hover:bg-red-500/30 transition-all"
                >
                  <X className="w-5 h-5" />
                </button>
              ) : (
                <button
                  type="submit"
                  disabled={!canSubmit}
                  className={`p-2.5 rounded-xl transition-all ${
                    canSubmit
                      ? "bg-gradient-to-r from-indigo-500 to-purple-500 text-white hover:opacity-90 shadow-lg shadow-indigo-500/25"
                      : "bg-gray-700/50 text-gray-500 cursor-not-allowed"
                  }`}
                >
                  <Send className="w-5 h-5" />
                </button>
              )}
            </div>
          </div>

          {/* Helper Text */}
          <div className="flex justify-between items-center mt-2 px-2 text-xs text-gray-500">
            <span>Press Enter to submit, Shift+Enter for new line</span>
            <span
              className={
                query.length < 10 ? "text-amber-500" : "text-emerald-500"
              }
            >
              {query.length}/10 min
            </span>
          </div>
        </div>
      </form>
    </div>
  );
}
