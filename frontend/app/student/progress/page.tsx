"use client";

import { useEffect, useState } from "react";
import { getMyProgress } from "@/lib/api/progress";
import type { StudentSkillProgress } from "@/lib/types/progress";
import { Card } from "@/components/ui/Card";

export default function ProgressDashboardPage() {
  const [progress, setProgress] = useState<StudentSkillProgress[]>([]);

  useEffect(() => {
    getMyProgress().then(setProgress);
  }, []);

  return (
    <main className="mx-auto max-w-3xl px-6 py-10">
      <h1 className="text-2xl font-bold text-brand">Progress</h1>
      <div className="mt-4 space-y-3">
        {progress.map((p) => (
          <Card key={p.id}>
            <div className="flex items-center justify-between">
              <p className="font-semibold">{p.proficiency_level ?? "Skill"}</p>
              <p className="text-sm text-gray-500">{Math.round(p.mastery_score * 100)}%</p>
            </div>
            <div className="mt-2 h-2 w-full rounded-full bg-gray-100">
              <div
                className="h-2 rounded-full bg-brand"
                style={{ width: `${Math.round(p.mastery_score * 100)}%` }}
              />
            </div>
          </Card>
        ))}
        {progress.length === 0 && <p className="text-sm text-gray-400">No progress recorded yet.</p>}
      </div>
    </main>
  );
}
