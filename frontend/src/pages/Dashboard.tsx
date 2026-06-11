import { motion } from "framer-motion";
import { UploadCloud } from "lucide-react";
import { MetricCard } from "../components/MetricCard";
import type { AnalysisReport } from "../types/report";

export function Dashboard({ report }: { report: AnalysisReport | null }) {
  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="space-y-6">
      <section className="rounded-lg bg-slate-950 p-6 text-white dark:bg-slate-900">
        <h2 className="text-3xl font-bold">AI-powered plagiarism intelligence</h2>
        <p className="mt-2 max-w-3xl text-slate-300">Detect exact copying, renamed variables, reordered statements, graph-level algorithm reuse, semantic similarity, AI-generated code patterns, and document plagiarism.</p>
      </section>
      {report ? (
        <div className="grid gap-4 md:grid-cols-3">
          <MetricCard label="Overall Similarity" value={report.overall_similarity} tone="orange" />
          <MetricCard label="Semantic Similarity" value={report.breakdown.semantic} tone="teal" />
          <MetricCard label="Graph Similarity" value={report.breakdown.graph} tone="violet" />
        </div>
      ) : (
        <div className="rounded-lg border border-dashed border-slate-300 bg-white p-8 text-center shadow-panel dark:border-slate-800 dark:bg-slate-900">
          <UploadCloud className="mx-auto text-teal-500" size={36} />
          <h3 className="mt-4 text-xl font-semibold">No analysis has been run yet</h3>
          <p className="mx-auto mt-2 max-w-2xl text-sm text-slate-500 dark:text-slate-400">
            Upload or paste two submissions from the Upload page to generate real similarity, semantic, AST, CFG, and report metrics.
          </p>
        </div>
      )}
    </motion.div>
  );
}
