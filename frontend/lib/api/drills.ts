import type { Drill } from "@/lib/types/drill";
import { apiFetch } from "./client";

export function listDrills(sportId?: string, skillId?: string) {
  const params = new URLSearchParams();
  if (sportId) params.set("sport_id", sportId);
  if (skillId) params.set("skill_id", skillId);
  const qs = params.toString() ? `?${params.toString()}` : "";
  return apiFetch<Drill[]>(`/api/drills${qs}`);
}

export function getDrill(drillId: string) {
  return apiFetch<Drill>(`/api/drills/${drillId}`);
}
