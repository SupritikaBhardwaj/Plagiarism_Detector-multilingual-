export type SimilarityBreakdown = {
  text: number;
  token: number;
  ast: number;
  graph: number;
  semantic: number;
  stylometry: number;
  ai_generated_probability: number;
};

export type EvidenceItem = {
  kind: string;
  message: string;
  confidence: number;
  metadata: Record<string, unknown>;
};

export type AnalysisReport = {
  report_id: string;
  overall_similarity: number;
  risk_level: string;
  breakdown: SimilarityBreakdown;
  evidence: EvidenceItem[];
  highlighted_regions: Array<Record<string, unknown>>;
  ast: Record<string, unknown>;
  cfg: Record<string, unknown>;
  pdg: Record<string, unknown>;
};

