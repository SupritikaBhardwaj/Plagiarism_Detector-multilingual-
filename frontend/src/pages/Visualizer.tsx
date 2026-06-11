import { GraphViewer } from "../components/GraphViewer";
import type { AnalysisReport } from "../types/report";

export function Visualizer({ report }: { report: AnalysisReport | null }) {
  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-panel dark:border-slate-800 dark:bg-slate-900">
        <h2 className="mb-1 font-semibold">Parsed AST JSON</h2>
        <p className="mb-3 text-sm text-slate-500">This shows compiler structure for the left submission, not the original source file.</p>
        <pre className="max-h-96 overflow-auto rounded-lg bg-slate-950 p-4 text-xs text-teal-100">{JSON.stringify(report?.ast?.left ?? { status: "Run an analysis first" }, null, 2)}</pre>
      </div>
      <GraphViewer graph={report?.cfg?.left as never} />
    </div>
  );
}
