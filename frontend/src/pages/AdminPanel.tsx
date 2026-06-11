import { RefreshCcw } from "lucide-react";
import { useEffect, useState } from "react";
import { getHealth } from "../services/api";

export function AdminPanel() {
  const [status, setStatus] = useState("checking");
  const [service, setService] = useState("unknown");

  async function refresh() {
    setStatus("checking");
    try {
      const health = await getHealth();
      setStatus(health.status);
      setService(health.service);
    } catch {
      setStatus("offline");
      setService("unreachable");
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  const engineItems = [
    ["API Service", service, status === "ok" ? "online" : status],
    ["Parser Mode", "Python AST + generic fallback", "active"],
    ["Model Mode", "Local deterministic embeddings", "active"],
    ["Report Storage", "Browser localStorage history", "active"],
    ["Rate Limit Middleware", "SlowAPI", "enabled"],
    ["Upload Guard", "Extension + syntax validation", "enabled"]
  ];

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3 rounded-lg border border-slate-200 bg-white p-4 shadow-panel dark:border-slate-800 dark:bg-slate-900">
        <div>
          <h2 className="text-xl font-semibold">Admin Panel</h2>
          <p className="text-sm text-slate-500">Operational status for the local analysis stack.</p>
        </div>
        <button onClick={refresh} className="inline-flex items-center gap-2 rounded-lg border border-slate-300 px-3 py-2 text-sm dark:border-slate-700">
          <RefreshCcw size={16} />
          Refresh
        </button>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        {engineItems.map(([label, value, badge]) => (
          <div key={label} className="rounded-lg border border-slate-200 bg-white p-5 shadow-panel dark:border-slate-800 dark:bg-slate-900">
            <div className="flex items-center justify-between gap-3">
              <div className="text-sm text-slate-500">{label}</div>
              <span className={`rounded-full px-2 py-1 text-xs ${badge === "online" || badge === "active" || badge === "enabled" || badge === "ok" ? "bg-teal-100 text-teal-700 dark:bg-teal-950 dark:text-teal-200" : "bg-rose-100 text-rose-700 dark:bg-rose-950 dark:text-rose-200"}`}>{badge}</span>
            </div>
            <div className="mt-2 text-lg font-semibold">{value}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
