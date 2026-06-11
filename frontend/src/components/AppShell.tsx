import { BarChart3, FileClock, GitGraph, Home, Lock, Moon, PanelTop, Upload, Workflow } from "lucide-react";
import type { ReactNode } from "react";

type Props = {
  active: string;
  onNavigate: (page: string) => void;
  onToggleTheme: () => void;
  children: ReactNode;
};

const items = [
  ["dashboard", Home, "Dashboard"],
  ["upload", Upload, "Upload"],
  ["live", Workflow, "Live"],
  ["ast", GitGraph, "AST"],
  ["report", PanelTop, "Report"],
  ["analytics", BarChart3, "Analytics"],
  ["admin", Lock, "Admin"],
  ["history", FileClock, "History"]
] as const;

export function AppShell({ active, onNavigate, onToggleTheme, children }: Props) {
  return (
    <div className="min-h-screen bg-slate-100 text-slate-950 dark:bg-slate-950 dark:text-slate-100">
      <aside className="fixed inset-y-0 left-0 hidden w-72 border-r border-slate-200 bg-white/90 px-4 py-5 backdrop-blur lg:block dark:border-slate-800 dark:bg-slate-950/90">
        <div className="mb-8 px-2">
          <div className="text-xl font-bold tracking-normal">PlagiaScope AI</div>
          <div className="text-sm text-slate-500">Compiler-aware similarity lab</div>
        </div>
        <nav className="space-y-1">
          {items.map(([id, Icon, label]) => (
            <button
              key={id}
              onClick={() => onNavigate(id)}
              className={`flex w-full items-center gap-3 rounded-lg px-3 py-2 text-left text-sm transition ${
                active === id ? "bg-slate-950 text-white dark:bg-white dark:text-slate-950" : "text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-900"
              }`}
              title={label}
            >
              <Icon size={18} />
              {label}
            </button>
          ))}
        </nav>
      </aside>
      <main className="lg:pl-72">
        <header className="sticky top-0 z-10 flex items-center justify-between border-b border-slate-200 bg-white/80 px-4 py-3 backdrop-blur dark:border-slate-800 dark:bg-slate-950/80">
          <div>
            <div className="text-xs uppercase text-teal-600 dark:text-teal-300">Research-grade plagiarism analysis</div>
            <h1 className="text-lg font-semibold">Similarity Operations Console</h1>
          </div>
          <button onClick={onToggleTheme} className="rounded-lg border border-slate-200 p-2 dark:border-slate-800" title="Toggle theme">
            <Moon size={18} />
          </button>
        </header>
        <div className="mx-auto max-w-7xl p-4 md:p-6">{children}</div>
      </main>
    </div>
  );
}

