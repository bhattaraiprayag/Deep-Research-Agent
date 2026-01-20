/**
 * ReportPane - Right pane displaying the synthesized research report.
 */

import { FileText, Download, Copy, Check, Loader2 } from 'lucide-react';
import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import type { ResearchStatus } from '../types';

interface ReportPaneProps {
    report: string;
    status: ResearchStatus;
    query: string;
}

export function ReportPane({ report, status, query }: ReportPaneProps) {
    const [copied, setCopied] = useState(false);

    const handleCopy = async () => {
        if (report) {
            await navigator.clipboard.writeText(report);
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        }
    };

    const handleDownload = () => {
        if (report) {
            const blob = new Blob([report], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `research-report-${Date.now()}.md`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }
    };

    const showLoading = (status === 'researching' || status === 'finalizing') && !report;
    const hasReport = report.length > 0;

    return (
        <div className="h-full flex flex-col">
            {/* Header */}
            <div className="flex items-center justify-between px-5 py-4 border-b border-indigo-500/20">
                <div className="flex items-center gap-3">
                    <FileText className="w-5 h-5 text-purple-400" />
                    <h2 className="text-lg font-semibold gradient-text">Research Report</h2>
                </div>

                {/* Action Buttons */}
                {hasReport && (
                    <div className="flex items-center gap-2">
                        <button
                            onClick={handleCopy}
                            className="flex items-center gap-1.5 px-3 py-1.5 text-xs rounded-lg glass hover:bg-white/10 transition-all"
                        >
                            {copied ? (
                                <>
                                    <Check className="w-3.5 h-3.5 text-emerald-400" />
                                    <span className="text-emerald-400">Copied!</span>
                                </>
                            ) : (
                                <>
                                    <Copy className="w-3.5 h-3.5" />
                                    <span>Copy</span>
                                </>
                            )}
                        </button>
                        <button
                            onClick={handleDownload}
                            className="flex items-center gap-1.5 px-3 py-1.5 text-xs rounded-lg glass hover:bg-white/10 transition-all"
                        >
                            <Download className="w-3.5 h-3.5" />
                            <span>Download</span>
                        </button>
                    </div>
                )}
            </div>

            {/* Content Area */}
            <div className="flex-1 overflow-y-auto p-6">
                {status === 'idle' ? (
                    /* Empty State */
                    <div className="flex flex-col items-center justify-center h-full text-gray-500">
                        <div className="p-6 rounded-full glass mb-6">
                            <FileText className="w-16 h-16 opacity-30" />
                        </div>
                        <h3 className="text-xl font-medium mb-2 text-gray-400">No Report Yet</h3>
                        <p className="text-sm text-center max-w-md opacity-60">
                            Enter a research question below and the synthesized report will appear here.
                        </p>
                    </div>
                ) : showLoading ? (
                    /* Loading State */
                    <div className="flex flex-col items-center justify-center h-full text-gray-500">
                        <div className="relative mb-6">
                            <div className="absolute inset-0 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 animate-ping opacity-20" />
                            <div className="relative p-6 rounded-full glass">
                                <Loader2 className="w-16 h-16 animate-spin text-indigo-400" />
                            </div>
                        </div>
                        <h3 className="text-xl font-medium mb-2 gradient-text">Researching...</h3>
                        <p className="text-sm text-center max-w-md opacity-60">
                            {query}
                        </p>
                    </div>
                ) : (
                    /* Report Content */
                    <article className="prose prose-invert prose-indigo max-w-none">
                        <ReactMarkdown
                            components={{
                                h1: ({ children }) => (
                                    <h1 className="text-2xl font-bold gradient-text mb-4 pb-2 border-b border-indigo-500/30">
                                        {children}
                                    </h1>
                                ),
                                h2: ({ children }) => (
                                    <h2 className="text-xl font-semibold text-white mt-8 mb-4">
                                        {children}
                                    </h2>
                                ),
                                h3: ({ children }) => (
                                    <h3 className="text-lg font-medium text-gray-200 mt-6 mb-3">
                                        {children}
                                    </h3>
                                ),
                                p: ({ children }) => (
                                    <p className="text-gray-300 leading-relaxed mb-4">
                                        {children}
                                    </p>
                                ),
                                ul: ({ children }) => (
                                    <ul className="list-disc list-inside space-y-2 text-gray-300 mb-4">
                                        {children}
                                    </ul>
                                ),
                                ol: ({ children }) => (
                                    <ol className="list-decimal list-inside space-y-2 text-gray-300 mb-4">
                                        {children}
                                    </ol>
                                ),
                                li: ({ children }) => (
                                    <li className="text-gray-300">{children}</li>
                                ),
                                a: ({ href, children }) => (
                                    <a
                                        href={href}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="text-indigo-400 hover:text-indigo-300 underline underline-offset-2"
                                    >
                                        {children}
                                    </a>
                                ),
                                blockquote: ({ children }) => (
                                    <blockquote className="border-l-4 border-indigo-500 pl-4 italic text-gray-400 my-4">
                                        {children}
                                    </blockquote>
                                ),
                                code: ({ children }) => (
                                    <code className="bg-gray-800 px-1.5 py-0.5 rounded text-sm text-indigo-300">
                                        {children}
                                    </code>
                                ),
                                pre: ({ children }) => (
                                    <pre className="bg-gray-900 p-4 rounded-lg overflow-x-auto my-4">
                                        {children}
                                    </pre>
                                ),
                            }}
                        >
                            {report}
                        </ReactMarkdown>
                    </article>
                )}
            </div>
        </div>
    );
}
