import { Trash2 } from "lucide-react";
import { percent } from "../utils/format";
import type { StoredReport } from "../types/history";

type Props = {
  items: StoredReport[];
  onOpen: (item: StoredReport) => void;
  onClear: () => void;
};

export function History({ items, onOpen, onClear }: Props) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-panel dark:border-slate-800 dark:bg-slate-900">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-xl font-semibold">Previous Reports</h2>
        <button onClick={onClear} disabled={items.length === 0} className="inline-flex items-center gap-2 rounded-lg border border-slate-300 px-3 py-2 text-sm disabled:cursor-not-allowed disabled:opacity-50 dark:border-slate-700">
          <Trash2 size={16} />
          Clear
        </button>
      </div>
      {items.length === 0 ? (
        <div className="rounded-lg border border-dashed border-slate-300 p-6 text-center text-sm text-slate-500 dark:border-slate-700">
          No reports yet. Run an analysis from Upload or Live and it will appear here.
        </div>
      ) : (
        <div className="space-y-2">
          {items.map((item) => (
            <button
              key={item.id}
              onClick={() => onOpen(item)}
              className="flex w-full flex-wrap items-center justify-between gap-3 rounded-lg border border-slate-200 p-3 text-left transition hover:border-teal-400 hover:bg-slate-50 dark:border-slate-800 dark:hover:bg-slate-800"
            >
              <div>
                <div className="font-medium">{item.leftName} vs {item.rightName}</div>
                <div className="text-sm text-slate-500">{new Date(item.createdAt).toLocaleString()} · {item.language}</div>
              </div>
              <div className="text-right">
                <div className="text-lg font-semibold">{percent(item.report.overall_similarity)}</div>
                <div className="text-xs uppercase text-slate-500">{item.report.risk_level}</div>
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
