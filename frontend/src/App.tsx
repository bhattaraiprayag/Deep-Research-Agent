/**
 * Deep Research Agent - Main Application Component
 */

import { Layout } from './components/Layout';
import { ReasoningPane } from './components/ReasoningPane';
import { ReportPane } from './components/ReportPane';
import { InputBar } from './components/InputBar';
import { useResearch } from './hooks/useResearch';

export default function App() {
  const { state, startResearch, cancelResearch } = useResearch();

  const isActive = state.status === 'researching' || state.status === 'finalizing';

  return (
    <Layout
      status={state.status}
      factsCount={state.factsCount}
      sourcesCount={state.sourcesCount}
      leftPane={
        <ReasoningPane
          entries={state.reasoningLog}
          isActive={isActive}
        />
      }
      rightPane={
        <ReportPane
          report={state.report}
          status={state.status}
          query={state.query}
        />
      }
      bottomBar={
        <InputBar
          onSubmit={startResearch}
          onCancel={cancelResearch}
          status={state.status}
        />
      }
    />
  );
}
