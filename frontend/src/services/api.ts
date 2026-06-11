import axios from "axios";
import type { AnalysisReport } from "../types/report";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000"
});

export type ComparePayload = {
  left: { name: string; language: string; content: string };
  right: { name: string; language: string; content: string };
  enable_ai: boolean;
};

export async function compareSubmissions(payload: ComparePayload): Promise<AnalysisReport> {
  const { data } = await api.post<AnalysisReport>("/api/analysis/compare", payload);
  return data;
}

export async function getHealth(): Promise<{ status: string; service: string }> {
  const { data } = await api.get<{ status: string; service: string }>("/health");
  return data;
}
