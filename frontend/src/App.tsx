import { useState } from "react";
import type { ReactNode } from "react";
import { AppShell } from "./components/AppShell";
import { AdminPanel } from "./pages/AdminPanel";
import { Analytics } from "./pages/Analytics";
import { AuthPage } from "./pages/AuthPage";
import { Dashboard } from "./pages/Dashboard";
import { History } from "./pages/History";
import { LiveAnalysis } from "./pages/LiveAnalysis";
import { ReportPage } from "./pages/ReportPage";
import { UploadCenter } from "./pages/UploadCenter";
import { Visualizer } from "./pages/Visualizer";
import { useTheme } from "./store/useTheme";
import { loadHistory, saveHistory } from "./store/historyStore";
import type { ComparePayload } from "./services/api";
import type { StoredReport } from "./types/history";
import type { AnalysisReport } from "./types/report";

export function App() {
  const [page, setPage] = useState("dashboard");
  const [report, setReport] = useState<AnalysisReport | null>(null);
  const [lastPayload, setLastPayload] = useState<ComparePayload | null>(null);
  const [history, setHistory] = useState<StoredReport[]>(() => loadHistory());
  const { toggleTheme } = useTheme();

  function storeReport(nextReport: AnalysisReport, payload: ComparePayload) {
    const item: StoredReport = {
      id: nextReport.report_id,
      createdAt: new Date().toISOString(),
      leftName: payload.left.name,
      rightName: payload.right.name,
      language: payload.left.language,
      report: nextReport,
      payload
    };
    setReport(nextReport);
    setLastPayload(payload);
    setHistory((current) => {
      const next = [item, ...current.filter((entry) => entry.id !== item.id)];
      saveHistory(next);
      return next;
    });
  }

  const pages: Record<string, ReactNode> = {
    dashboard: <Dashboard report={report} />,
    upload: <UploadCenter onReport={(nextReport, payload) => { storeReport(nextReport, payload); setPage("report"); }} />,
    live: <LiveAnalysis payload={lastPayload} onReport={(nextReport, payload) => { storeReport(nextReport, payload); setPage("report"); }} />,
    ast: <Visualizer report={report} />,
    report: <ReportPage report={report} />,
    analytics: <Analytics report={report} />,
    admin: <AdminPanel />,
    auth: <AuthPage />,
    history: <History items={history} onOpen={(item) => { setReport(item.report); setLastPayload(item.payload); setPage("report"); }} onClear={() => { setHistory([]); saveHistory([]); }} />
  };

  return (
    <AppShell active={page} onNavigate={setPage} onToggleTheme={toggleTheme}>
      {pages[page] ?? pages.dashboard}
    </AppShell>
  );
}
