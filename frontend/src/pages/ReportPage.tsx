import { SimilarityChart } from "../components/SimilarityChart";
import { MetricCard } from "../components/MetricCard";
import type { AnalysisReport } from "../types/report";

export function ReportPage({ report }: { report: AnalysisReport | null }) {
  if (!report) {
    return <div className="rounded-lg bg-white p-6 dark:bg-slate-900">Run an analysis to generate an explainable report.</div>;
  }
  return (
    <div className="space-y-4">
      <div className="grid gap-4 md:grid-cols-3">
        <MetricCard label="Overall" value={report.overall_similarity} tone="orange" />
        <MetricCard label="AI Probability" value={report.breakdown.ai_generated_probability} tone="violet" />
        <MetricCard label="Token Match" value={report.breakdown.token} tone="teal" />
      </div>
      <SimilarityChart breakdown={report.breakdown} />
      <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-panel dark:border-slate-800 dark:bg-slate-900">
        <h2 className="mb-3 font-semibold">Explainable Reasons</h2>
        <div className="space-y-2">
          {report.evidence.map((item) => (
            <div key={`${item.kind}-${item.message}`} className="rounded-lg bg-slate-100 p-3 dark:bg-slate-800">
              <div className="font-medium">{item.kind.toUpperCase()} - {Math.round(item.confidence * 100)}%</div>
              <div className="text-sm text-slate-600 dark:text-slate-300">{item.message}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

