import { Activity, Play } from "lucide-react";
import { useState } from "react";
import { compareSubmissions } from "../services/api";
import type { ComparePayload } from "../services/api";
import type { AnalysisReport } from "../types/report";

type Props = {
  payload: ComparePayload | null;
  onReport: (report: AnalysisReport, payload: ComparePayload) => void;
};

const phases = ["Validating language", "Tokenizing", "Building AST/CFG/PDG", "Computing embeddings", "Fusing scores"];

export function LiveAnalysis({ payload, onReport }: Props) {
  const [progress, setProgress] = useState(0);
  const [phase, setPhase] = useState("Waiting for a submission");
  const [running, setRunning] = useState(false);
  const [error, setError] = useState("");

  async function runLive() {
    if (!payload || running) {
      return;
    }
    setRunning(true);
    setError("");
    setProgress(0);
    try {
      for (let index = 0; index < phases.length; index += 1) {
        setPhase(phases[index]);
        setProgress((index + 1) * 16);
        await new Promise((resolve) => window.setTimeout(resolve, 220));
      }
      const report = await compareSubmissions(payload);
      setPhase("Complete");
      setProgress(100);
      onReport(report, payload);
    } catch {
      setPhase("Failed");
      setError("Live scan failed. Check the selected language and backend status.");
    } finally {
      setRunning(false);
    }
  }

  return (
    <div className="space-y-4">
      <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-panel dark:border-slate-800 dark:bg-slate-900">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 className="text-xl font-semibold">Live Analysis</h2>
            <p className="text-sm text-slate-500">Runs the latest upload again and streams visible scan phases.</p>
          </div>
          <button
            onClick={runLive}
            disabled={!payload || running}
            className="inline-flex items-center gap-2 rounded-lg bg-teal-500 px-4 py-2 font-semibold text-white transition hover:bg-teal-600 disabled:cursor-not-allowed disabled:opacity-60"
          >
            <Play size={18} />
            {running ? "Running" : "Run Live Scan"}
          </button>
        </div>
        <div className="mt-5 h-3 overflow-hidden rounded-full bg-slate-200 dark:bg-slate-800">
          <div className="h-full rounded-full bg-teal-500 transition-all" style={{ width: `${progress}%` }} />
        </div>
        <div className="mt-4 flex items-center gap-2 text-sm text-slate-500">
          <Activity size={16} />
          {payload ? phase : "Upload or paste two submissions first."}
        </div>
        {payload && (
          <div className="mt-4 rounded-lg bg-slate-100 p-3 text-sm dark:bg-slate-800">
            Latest input: <span className="font-medium">{payload.left.name}</span> vs <span className="font-medium">{payload.right.name}</span> as <span className="font-medium">{payload.left.language}</span>
          </div>
        )}
        {error && <div className="mt-4 rounded-lg bg-rose-50 p-3 text-sm text-rose-700 dark:bg-rose-950 dark:text-rose-200">{error}</div>}
      </div>
    </div>
  );
}
