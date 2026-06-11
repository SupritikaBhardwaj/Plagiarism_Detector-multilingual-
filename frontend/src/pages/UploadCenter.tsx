import { FileUp, ScanLine } from "lucide-react";
import { useState } from "react";
import axios from "axios";
import { CodeCompare } from "../components/CodeCompare";
import { compareSubmissions } from "../services/api";
import type { ComparePayload } from "../services/api";
import type { AnalysisReport } from "../types/report";

const languages = [
  { value: "python", label: "Python", extension: ".py" },
  { value: "javascript", label: "JavaScript", extension: ".js" },
  { value: "typescript", label: "TypeScript", extension: ".ts" },
  { value: "java", label: "Java", extension: ".java" },
  { value: "cpp", label: "C++", extension: ".cpp" },
  { value: "c", label: "C", extension: ".c" },
  { value: "text", label: "Document/Text", extension: ".txt" }
];

type Props = { onReport: (report: AnalysisReport, payload: ComparePayload) => void };

export function UploadCenter({ onReport }: Props) {
  const [left, setLeft] = useState("");
  const [right, setRight] = useState("");
  const [leftName, setLeftName] = useState("left.py");
  const [rightName, setRightName] = useState("right.py");
  const [language, setLanguage] = useState("python");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const canRun = left.trim().length > 0 && right.trim().length > 0 && !loading;

  async function readFile(file: File, side: "left" | "right") {
    const content = await file.text();
    if (side === "left") {
      setLeft(content);
      setLeftName(file.name);
    } else {
      setRight(content);
      setRightName(file.name);
    }
    setError("");
  }

  async function run() {
    if (!canRun) {
      return;
    }
    setLoading(true);
    setError("");
    try {
      const payload = {
        left: { name: leftName, language, content: left },
        right: { name: rightName, language, content: right },
        enable_ai: true
      };
      const report = await compareSubmissions({
        ...payload
      });
      onReport(report, payload);
    } catch (unknownError) {
      if (axios.isAxiosError(unknownError)) {
        const detail = unknownError.response?.data?.detail;
        setError(typeof detail === "string" ? detail : "Analysis failed. Please check the selected language and file contents.");
      } else {
        setError("Analysis failed. Please check the selected language and file contents.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-4">
      <div className="rounded-lg border border-dashed border-slate-300 bg-white p-5 dark:border-slate-700 dark:bg-slate-900">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <h2 className="text-xl font-semibold">Upload Center</h2>
            <p className="text-sm text-slate-500">Upload two files or paste code/documents directly, then run analysis.</p>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <select
              value={language}
              onChange={(event) => setLanguage(event.target.value)}
              className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm dark:border-slate-700 dark:bg-slate-950"
              aria-label="Language"
            >
              {languages.map((item) => (
                <option key={item.value} value={item.value}>{item.label}</option>
              ))}
            </select>
            <button onClick={run} disabled={!canRun} className="inline-flex items-center gap-2 rounded-lg bg-teal-500 px-4 py-2 font-semibold text-white shadow-panel transition hover:bg-teal-600 disabled:cursor-not-allowed disabled:opacity-60">
              <ScanLine size={18} />
              {loading ? "Scanning" : "Run Analysis"}
            </button>
          </div>
        </div>
        <div className="mt-5 grid gap-3 md:grid-cols-2">
          <label className="flex cursor-pointer items-center justify-between gap-3 rounded-lg border border-slate-200 bg-slate-50 px-4 py-3 text-sm transition hover:border-teal-400 dark:border-slate-800 dark:bg-slate-950">
            <span className="flex min-w-0 items-center gap-2">
              <FileUp size={18} className="shrink-0 text-teal-500" />
              <span className="truncate">{leftName}</span>
            </span>
            <span className="shrink-0 text-xs text-slate-500">Choose left file</span>
            <input className="hidden" type="file" accept={languages.map((item) => item.extension).join(",")} onChange={(event) => event.target.files?.[0] && readFile(event.target.files[0], "left")} />
          </label>
          <label className="flex cursor-pointer items-center justify-between gap-3 rounded-lg border border-slate-200 bg-slate-50 px-4 py-3 text-sm transition hover:border-teal-400 dark:border-slate-800 dark:bg-slate-950">
            <span className="flex min-w-0 items-center gap-2">
              <FileUp size={18} className="shrink-0 text-teal-500" />
              <span className="truncate">{rightName}</span>
            </span>
            <span className="shrink-0 text-xs text-slate-500">Choose right file</span>
            <input className="hidden" type="file" accept={languages.map((item) => item.extension).join(",")} onChange={(event) => event.target.files?.[0] && readFile(event.target.files[0], "right")} />
          </label>
        </div>
        <p className="mt-3 text-xs text-slate-500">
          Python uses native AST parsing. JavaScript, TypeScript, Java, C, C++, and text currently use normalized token and fallback AST analysis.
        </p>
        {error && (
          <div className="mt-4 rounded-lg border border-rose-300 bg-rose-50 px-4 py-3 text-sm text-rose-700 dark:border-rose-900 dark:bg-rose-950 dark:text-rose-200">
            {error}
          </div>
        )}
      </div>
      <CodeCompare left={left} right={right} onLeftChange={setLeft} onRightChange={setRight} />
    </div>
  );
}
