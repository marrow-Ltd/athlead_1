"use client";

import { useEffect, useState } from "react";
import { getTrainingToday } from "@/lib/api/training";
import type { TrainingAssignment } from "@/lib/types/training";

export function useTodaysTraining() {
  const [assignments, setAssignments] = useState<TrainingAssignment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getTrainingToday()
      .then(setAssignments)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return { assignments, loading, error };
}
