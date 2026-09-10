import type { TrainingAssignment, TrainingPlan } from "@/lib/types/training";
import { apiFetch } from "./client";

export function listMyPlans() {
  return apiFetch<TrainingPlan[]>("/api/training/plans");
}

export function getTrainingToday() {
  return apiFetch<TrainingAssignment[]>("/api/training/today");
}

export function updateAssignment(assignmentId: string, patch: Partial<TrainingAssignment>) {
  return apiFetch<TrainingAssignment>(`/api/training/assignments/${assignmentId}`, {
    method: "PATCH",
    body: JSON.stringify(patch),
  });
}
