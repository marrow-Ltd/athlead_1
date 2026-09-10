import { apiFetch } from "./client";

export function getRecommendations(studentId: string) {
  return apiFetch<any>("/api/ai/recommendations", {
    method: "POST",
    body: JSON.stringify({ student_id: studentId }),
  });
}
