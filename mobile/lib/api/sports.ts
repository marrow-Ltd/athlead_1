import type { Sport, SportSearchResponse } from "@/lib/types/sport";
import { apiFetch } from "./client";

export function listSports() {
  return apiFetch<Sport[]>("/api/sports");
}

export function searchSports(query?: string) {
  const qs = query ? `?q=${encodeURIComponent(query)}` : "";
  return apiFetch<SportSearchResponse>(`/api/sports/search${qs}`);
}
