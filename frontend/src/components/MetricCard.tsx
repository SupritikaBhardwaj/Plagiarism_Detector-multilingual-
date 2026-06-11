import { percent } from "../utils/format";

type Props = {
  label: string;
  value: number;
  tone?: "teal" | "orange" | "violet";
};

const toneMap = {
  teal: "from-teal-500 to-emerald-500",
  orange: "from-orange-500 to-rose-500",
  violet: "from-violet-500 to-indigo-500"
};

export function MetricCard({ label, value, tone = "teal" }: Props) {
  return (
    <div className="rounded-lg border border-slate-200 bg-white p-4 shadow-panel dark:border-slate-800 dark:bg-slate-900">
      <div className="text-sm text-slate-500 dark:text-slate-400">{label}</div>
      <div className="mt-3 flex items-end justify-between gap-3">
        <div className="text-3xl font-semibold text-slate-950 dark:text-white">{percent(value)}</div>
        <div className="h-2 w-24 overflow-hidden rounded-full bg-slate-200 dark:bg-slate-800">
          <div className={`h-full rounded-full bg-gradient-to-r ${toneMap[tone]}`} style={{ width: percent(value) }} />
        </div>
      </div>
    </div>
  );
}

