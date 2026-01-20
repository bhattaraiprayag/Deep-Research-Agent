/**
 * StatusIndicator - Displays the current research status with visual feedback.
 */

import { Loader2, CheckCircle2, XCircle, Sparkles, Clock } from 'lucide-react';
import type { ResearchStatus } from '../types';

interface StatusIndicatorProps {
    status: ResearchStatus;
    factsCount: number;
    sourcesCount: number;
}

const statusConfig: Record<ResearchStatus, {
    icon: React.ReactNode;
    label: string;
    className: string
}> = {
    idle: {
        icon: <Clock className="w-4 h-4" />,
        label: 'Ready',
        className: 'text-gray-400',
    },
    researching: {
        icon: <Loader2 className="w-4 h-4 animate-spin" />,
        label: 'Researching...',
        className: 'text-amber-400',
    },
    finalizing: {
        icon: <Sparkles className="w-4 h-4 animate-pulse" />,
        label: 'Synthesizing Report',
        className: 'text-purple-400',
    },
    complete: {
        icon: <CheckCircle2 className="w-4 h-4" />,
        label: 'Complete',
        className: 'text-emerald-400',
    },
    error: {
        icon: <XCircle className="w-4 h-4" />,
        label: 'Error',
        className: 'text-red-400',
    },
};

export function StatusIndicator({ status, factsCount, sourcesCount }: StatusIndicatorProps) {
    const config = statusConfig[status];

    return (
        <div className="flex items-center gap-6">
            {/* Status Badge */}
            <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full glass ${config.className}`}>
                {config.icon}
                <span className="text-sm font-medium">{config.label}</span>
            </div>

            {/* Stats */}
            {(status !== 'idle' && status !== 'error') && (
                <div className="flex items-center gap-4 text-sm text-gray-400">
                    <div className="flex items-center gap-1.5">
                        <span className="w-2 h-2 rounded-full bg-indigo-500"></span>
                        <span>{factsCount} facts</span>
                    </div>
                    {sourcesCount > 0 && (
                        <div className="flex items-center gap-1.5">
                            <span className="w-2 h-2 rounded-full bg-purple-500"></span>
                            <span>{sourcesCount} sources</span>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
