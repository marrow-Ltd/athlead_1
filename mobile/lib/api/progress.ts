import type { StudentSkillProgress } from "@/lib/types/progress";
import { apiFetch } from "./client";

export function getMyProgress() {
  return apiFetch<StudentSkillProgress[]>("/api/progress");
}
