"use client";

import { useTodaysTraining } from "@/lib/hooks/useTrainingPlan";
import { updateAssignment } from "@/lib/api/training";
import { Card } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

export default function TrainingTodayPage() {
  const { assignments, loading } = useTodaysTraining();

  async function markDone(id: string) {
    await updateAssignment(id, { status: "completed" });
    window.location.reload();
  }

  return (
    <main className="mx-auto max-w-3xl px-6 py-10">
      <h1 className="text-2xl font-bold text-brand">Today&apos;s Practice</h1>
      {loading && <p className="mt-4 text-sm text-gray-400">Loading…</p>}
      <div className="mt-4 space-y-3">
        {assignments.map((a) => (
          <Card key={a.id} className="flex items-center justify-between">
            <div>
              <p className="font-semibold">Drill #{a.drill_id.slice(0, 8)}</p>
              <p className="text-xs text-gray-500">{a.sets ?? "-"} sets × {a.reps ?? "-"} reps</p>
            </div>
            {a.status !== "completed" ? (
              <Button className="w-32" onClick={() => markDone(a.id)}>Mark done</Button>
            ) : (
              <span className="text-xs font-semibold text-green-600">Completed</span>
            )}
          </Card>
        ))}
      </div>
    </main>
  );
}
