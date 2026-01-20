/**
 * Layout - Main application layout with split-pane workspace.
 */

import type { ReactNode } from 'react';
import { Sparkles } from 'lucide-react';
import { StatusIndicator } from './StatusIndicator';
import type { ResearchStatus } from '../types';

interface LayoutProps {
    leftPane: ReactNode;
    rightPane: ReactNode;
    bottomBar: ReactNode;
    status: ResearchStatus;
    factsCount: number;
    sourcesCount: number;
}

export function Layout({
    leftPane,
    rightPane,
    bottomBar,
    status,
    factsCount,
    sourcesCount
}: LayoutProps) {
    return (
        <div className="h-screen w-screen flex flex-col overflow-hidden bg-[#0a0a0f]">
            {/* Header */}
            <header className="flex items-center justify-between px-6 py-4 border-b border-indigo-500/20 bg-[#0d0d14]/80 backdrop-blur-xl">
                <div className="flex items-center gap-3">
                    <div className="p-2 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 shadow-lg shadow-indigo-500/20">
                        <Sparkles className="w-5 h-5 text-white" />
                    </div>
                    <div>
                        <h1 className="text-xl font-bold gradient-text">Deep Research Agent</h1>
                        <p className="text-xs text-gray-500">AI-Powered Research with Transparent Reasoning</p>
                    </div>
                </div>

                <StatusIndicator
                    status={status}
                    factsCount={factsCount}
                    sourcesCount={sourcesCount}
                />
            </header>

            {/* Main Content - Split Panes */}
            <main className="flex-1 flex overflow-hidden">
                {/* Left Pane - Reasoning */}
                <div className="w-[400px] min-w-[350px] max-w-[500px] border-r border-indigo-500/20 bg-[#0d0d14]/50">
                    {leftPane}
                </div>

                {/* Right Pane - Report */}
                <div className="flex-1 bg-[#0a0a0f]">
                    {rightPane}
                </div>
            </main>

            {/* Bottom Bar - Input */}
            {bottomBar}
        </div>
    );
}
