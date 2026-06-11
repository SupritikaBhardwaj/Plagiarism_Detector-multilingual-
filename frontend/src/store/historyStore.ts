import type { StoredReport } from "../types/history";

const KEY = "plagiascope.history.v1";

export function loadHistory(): StoredReport[] {
  try {
    const raw = window.localStorage.getItem(KEY);
    return raw ? JSON.parse(raw) as StoredReport[] : [];
  } catch {
    return [];
  }
}

export function saveHistory(items: StoredReport[]) {
  window.localStorage.setItem(KEY, JSON.stringify(items.slice(0, 20)));
}

