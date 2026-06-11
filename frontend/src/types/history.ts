import type { ComparePayload } from "../services/api";
import type { AnalysisReport } from "./report";

export type StoredReport = {
  id: string;
  createdAt: string;
  leftName: string;
  rightName: string;
  language: string;
  report: AnalysisReport;
  payload: ComparePayload;
};

