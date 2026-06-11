import type { AnalysisReport } from "../types/report";
import { SimilarityChart } from "../components/SimilarityChart";

export function Analytics({ report }: { report: AnalysisReport | null }) {
  const fallback = {
    text: 0.61,
    token: 0.72,
    ast: 0.69,
    graph: 0.64,
    semantic: 0.81,
    stylometry: 0.57,
    ai_generated_probability: 0.42
  };
  return <SimilarityChart breakdown={report?.breakdown ?? fallback} />;
}

